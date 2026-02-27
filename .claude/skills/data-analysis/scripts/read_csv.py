#!/usr/bin/env python3
"""
read_csv.py — Read and profile CSV files for Claude data analysis workflows.

Usage:
    python read_csv.py <file.csv> [options]

Options:
    --format <md|json|summary>  Output format (default: md)
    --rows <n>                  Max rows to output (default: 100; 0 = all)
    --head <n>                  Quick preview of first N rows
    --profile                   Full statistical profile
    --encoding <enc>            File encoding (default: auto-detect)
    --sep <char>                Delimiter (default: auto-detect)
    --no-data                   Profile only — do not print rows

Auto-installs: pandas, tabulate, chardet
"""

import sys
import subprocess


def _install(package: str) -> None:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])


try:
    import pandas as pd
except ImportError:
    print("Installing pandas...", file=sys.stderr)
    _install("pandas")
    import pandas as pd

try:
    from tabulate import tabulate
except ImportError:
    print("Installing tabulate...", file=sys.stderr)
    _install("tabulate")
    from tabulate import tabulate

try:
    import chardet
except ImportError:
    print("Installing chardet...", file=sys.stderr)
    _install("chardet")
    import chardet

import argparse
import json
import os
from pathlib import Path


def detect_encoding(path: Path) -> str:
    """Auto-detect file encoding."""
    raw = path.read_bytes()[:65536]  # sample first 64KB
    result = chardet.detect(raw)
    return result.get("encoding") or "utf-8"


def detect_sep(path: Path, encoding: str) -> str:
    """Auto-detect delimiter by checking first few lines."""
    with open(path, encoding=encoding, errors="replace") as f:
        sample = f.readline()
    counts = {sep: sample.count(sep) for sep in [",", "\t", ";", "|"]}
    return max(counts, key=counts.get)


def infer_types(df: pd.DataFrame) -> pd.DataFrame:
    """Attempt to parse date columns and improve type inference."""
    for col in df.columns:
        # Try datetime
        if df[col].dtype == object:
            if any(kw in col.lower() for kw in ["date", "time", "dt", "year", "month"]):
                try:
                    df[col] = pd.to_datetime(df[col], errors="coerce")
                    continue
                except Exception:
                    pass
            # Try numeric
            try:
                df[col] = pd.to_numeric(df[col].str.replace(",", "").str.replace("$", ""), errors="raise")
            except Exception:
                pass
    return df


def profile(df: pd.DataFrame, path: Path) -> str:
    """Full statistical profile of the dataframe."""
    lines = []

    lines.append(f"# CSV Profile: {path.name}\n")
    lines.append(f"**Dimensions:** {df.shape[0]:,} rows × {df.shape[1]} columns")
    lines.append(f"**File size:** {path.stat().st_size / 1024:.1f} KB\n")

    # Column summary
    col_rows = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        n_valid = df[col].notna().sum()
        null_pct = df[col].isna().sum() / len(df) * 100
        n_unique = df[col].nunique()

        if df[col].dtype in ["float64", "int64"]:
            summary = (f"min={df[col].min():.2g}, "
                       f"mean={df[col].mean():.2g}, "
                       f"max={df[col].max():.2g}")
        elif str(df[col].dtype).startswith("datetime"):
            summary = f"{df[col].min().date()} → {df[col].max().date()}"
        else:
            top = df[col].value_counts().index[:3].tolist()
            summary = ", ".join(str(v) for v in top)
            if len(summary) > 50:
                summary = summary[:47] + "..."

        col_rows.append([col, dtype, f"{n_valid:,}", f"{null_pct:.1f}%",
                          f"{n_unique:,}", summary])

    lines.append("## Column Overview\n")
    lines.append(tabulate(
        col_rows,
        headers=["Column", "Type", "Non-null", "Null %", "Unique", "Summary"],
        tablefmt="pipe"
    ))
    lines.append("")

    # Numeric stats
    num_df = df.select_dtypes(include="number")
    if not num_df.empty:
        lines.append("\n## Numeric Statistics\n")
        desc = num_df.describe().T.round(3)
        lines.append(tabulate(desc, headers="keys", tablefmt="pipe", floatfmt=".3f"))
        lines.append("")

    # Date ranges
    dt_cols = df.select_dtypes(include=["datetime64[ns]"]).columns
    if len(dt_cols) > 0:
        lines.append("\n## Date Ranges\n")
        for col in dt_cols:
            valid = df[col].dropna()
            lines.append(f"- **{col}:** {valid.min().date()} → {valid.max().date()} "
                         f"({len(valid):,} valid)")
        lines.append("")

    # Categorical overview
    cat_cols = df.select_dtypes(include="object").columns
    if len(cat_cols) > 0:
        lines.append("\n## Top Values (Categorical)\n")
        for col in cat_cols[:6]:  # limit to first 6 categorical cols
            vc = df[col].value_counts().head(5)
            lines.append(f"**{col}** ({df[col].nunique()} unique):")
            for val, cnt in vc.items():
                pct = cnt / len(df) * 100
                lines.append(f"  - `{val}`: {cnt:,} ({pct:.1f}%)")
        lines.append("")

    # Missing value heatmap (text-based)
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    if not missing.empty:
        lines.append("\n## Missing Values\n")
        for col, cnt in missing.items():
            pct = cnt / len(df) * 100
            bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            lines.append(f"  {col:30s} {bar} {pct:.1f}% ({cnt:,})")
        lines.append("")

    # Data quality flags
    flags = []
    dupe_count = df.duplicated().sum()
    if dupe_count > 0:
        flags.append(f"⚠️  **{dupe_count:,} duplicate rows** detected")
    if missing.sum() > 0:
        flags.append(f"⚠️  **{missing.sum():,} total missing values** across {len(missing)} columns")
    # Check for constant columns
    const_cols = [c for c in df.columns if df[c].nunique() <= 1]
    if const_cols:
        flags.append(f"⚠️  **Constant columns** (zero variance): {', '.join(const_cols)}")

    if flags:
        lines.append("\n## Data Quality Flags\n")
        lines.extend(flags)
        lines.append("")
    else:
        lines.append("\n## Data Quality\n")
        lines.append("✅ No obvious quality issues detected.\n")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Read and profile CSV files for Claude analysis")
    parser.add_argument("file", help="Path to CSV file")
    parser.add_argument("--format", choices=["md", "json", "summary"], default="md")
    parser.add_argument("--rows", type=int, default=100, help="Max rows to output (0 = all)")
    parser.add_argument("--head", type=int, default=None, help="Show only first N rows")
    parser.add_argument("--profile", action="store_true", help="Full statistical profile")
    parser.add_argument("--encoding", default=None, help="File encoding (default: auto)")
    parser.add_argument("--sep", default=None, help="Delimiter (default: auto)")
    parser.add_argument("--no-data", action="store_true", help="Profile only, skip data output")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    # Auto-detect encoding and separator
    encoding = args.encoding or detect_encoding(path)
    sep = args.sep or detect_sep(path, encoding)

    # Read
    df = pd.read_csv(path, sep=sep, encoding=encoding, low_memory=False)
    df = infer_types(df)

    # Profile mode
    if args.profile or args.format == "summary":
        print(profile(df, path))
        if args.no_data or args.format == "summary":
            return

    # Data output
    if args.no_data:
        return

    n_out = args.head if args.head is not None else (len(df) if args.rows == 0 else args.rows)
    df_out = df.head(n_out)
    truncated = len(df_out) < len(df)

    if args.format == "md":
        if not (args.profile or args.format == "summary"):
            print(f"# {path.name}\n")
            print(f"**{df.shape[0]:,} rows × {df.shape[1]} columns** | "
                  f"encoding: {encoding} | sep: `{sep}`\n")
        print(f"\n## Data ({len(df_out):,} of {len(df):,} rows)\n")
        print(tabulate(df_out, headers="keys", tablefmt="pipe",
                       showindex=False, floatfmt=".4f"))
        if truncated:
            print(f"\n*… {len(df) - len(df_out):,} more rows. Use --rows 0 to output all.*")

    elif args.format == "json":
        records = json.loads(df_out.to_json(orient="records", date_format="iso"))
        print(json.dumps({
            "file": str(path),
            "encoding": encoding,
            "separator": sep,
            "total_rows": len(df),
            "output_rows": len(df_out),
            "columns": df.columns.tolist(),
            "dtypes": {c: str(t) for c, t in df.dtypes.items()},
            "data": records
        }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
