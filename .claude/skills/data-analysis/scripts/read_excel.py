#!/usr/bin/env python3
"""
read_excel.py — Read Excel files for Claude data analysis workflows.

Usage:
    python read_excel.py <file.xlsx> [options]

Options:
    --sheet <name|index>   Sheet to read (default: first sheet)
    --all-sheets           List all sheets and their dimensions
    --format <md|csv|json> Output format (default: md)
    --rows <n>             Max rows to output (default: 100; 0 = all)
    --profile              Include statistical profile of numeric columns
    --head <n>             Show only first n rows (quick preview)

Auto-installs: openpyxl, pandas, tabulate
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
    import openpyxl  # noqa: F401 — required for pandas Excel engine
except ImportError:
    print("Installing openpyxl...", file=sys.stderr)
    _install("openpyxl")

try:
    from tabulate import tabulate
except ImportError:
    print("Installing tabulate...", file=sys.stderr)
    _install("tabulate")
    from tabulate import tabulate

import argparse
import json
import os
from pathlib import Path


def profile_dataframe(df: pd.DataFrame) -> str:
    """Generate a statistical profile of numeric columns."""
    lines = []
    lines.append("\n## Statistical Profile\n")

    # Dimensions
    lines.append(f"**Dimensions:** {df.shape[0]:,} rows × {df.shape[1]} columns\n")

    # Column overview
    col_info = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null = df[col].notna().sum()
        null_pct = (df[col].isna().sum() / len(df) * 100)
        sample = str(df[col].dropna().iloc[0]) if non_null > 0 else "—"
        if len(sample) > 30:
            sample = sample[:27] + "..."
        col_info.append([col, dtype, f"{non_null:,}", f"{null_pct:.1f}%", sample])

    lines.append("### Column Overview\n")
    lines.append(tabulate(
        col_info,
        headers=["Column", "Type", "Non-null", "Null %", "Sample"],
        tablefmt="pipe"
    ))
    lines.append("")

    # Numeric stats
    num_cols = df.select_dtypes(include="number").columns.tolist()
    if num_cols:
        lines.append("\n### Numeric Statistics\n")
        stats = df[num_cols].describe().T
        stats.index.name = "Column"
        stats = stats.round(2)
        lines.append(tabulate(stats, headers="keys", tablefmt="pipe", floatfmt=".2f"))
        lines.append("")

    # Date column detection
    date_cols = [c for c in df.columns if "date" in c.lower() or "time" in c.lower()
                 or df[c].dtype == "datetime64[ns]"]
    if date_cols:
        lines.append("\n### Date Ranges\n")
        for col in date_cols:
            try:
                parsed = pd.to_datetime(df[col], errors="coerce")
                valid = parsed.dropna()
                if len(valid) > 0:
                    lines.append(f"- **{col}:** {valid.min().date()} → {valid.max().date()} "
                                 f"({len(valid):,} valid dates)")
            except Exception:
                pass
        lines.append("")

    # Missing value summary
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if not missing.empty:
        lines.append("\n### Missing Values\n")
        for col, count in missing.items():
            pct = count / len(df) * 100
            lines.append(f"- **{col}:** {count:,} missing ({pct:.1f}%)")
        lines.append("")

    return "\n".join(lines)


def read_excel(
    path: str,
    sheet: str | int | None = None,
    all_sheets: bool = False,
    fmt: str = "md",
    max_rows: int = 100,
    profile: bool = False,
    head: int | None = None,
) -> None:
    path = Path(path)
    if not path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    xl = pd.ExcelFile(path)
    sheet_names = xl.sheet_names

    # List all sheets
    if all_sheets:
        print(f"## Sheets in {path.name}\n")
        for i, name in enumerate(sheet_names):
            df = pd.read_excel(path, sheet_name=name, header=0)
            print(f"- **Sheet {i}:** `{name}` — {df.shape[0]:,} rows × {df.shape[1]} columns")
        return

    # Select sheet
    if sheet is None:
        sheet = sheet_names[0]
    elif sheet.isdigit():
        sheet = int(sheet)

    df = pd.read_excel(path, sheet_name=sheet, header=0)

    # Header info
    sheet_label = sheet if isinstance(sheet, str) else sheet_names[sheet]
    print(f"# {path.name} — Sheet: {sheet_label}\n")
    print(f"**{df.shape[0]:,} rows × {df.shape[1]} columns**\n")

    # Profile first if requested
    if profile:
        print(profile_dataframe(df))

    # Slice rows for output
    if head is not None:
        df_out = df.head(head)
    elif max_rows == 0:
        df_out = df
    else:
        df_out = df.head(max_rows)

    truncated = len(df_out) < len(df)

    if fmt == "md":
        print(f"\n## Data ({len(df_out):,} of {len(df):,} rows)\n")
        print(tabulate(df_out, headers="keys", tablefmt="pipe",
                       showindex=False, floatfmt=".2f"))
        if truncated:
            print(f"\n*… {len(df) - len(df_out):,} more rows not shown. "
                  f"Use --rows 0 to output all.*")

    elif fmt == "csv":
        print(df_out.to_csv(index=False))
        if truncated:
            print(f"# … {len(df) - len(df_out):,} more rows", file=sys.stderr)

    elif fmt == "json":
        records = json.loads(df_out.to_json(orient="records", date_format="iso"))
        print(json.dumps({
            "file": str(path),
            "sheet": sheet_label,
            "total_rows": len(df),
            "output_rows": len(df_out),
            "columns": df.columns.tolist(),
            "data": records
        }, indent=2, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser(description="Read Excel files for Claude analysis")
    parser.add_argument("file", help="Path to .xlsx or .xls file")
    parser.add_argument("--sheet", default=None, help="Sheet name or index (default: first)")
    parser.add_argument("--all-sheets", action="store_true", help="List all sheets")
    parser.add_argument("--format", choices=["md", "csv", "json"], default="md")
    parser.add_argument("--rows", type=int, default=100, help="Max rows to output (0 = all)")
    parser.add_argument("--profile", action="store_true", help="Show statistical profile")
    parser.add_argument("--head", type=int, default=None, help="Show only first N rows")
    args = parser.parse_args()

    read_excel(
        path=args.file,
        sheet=args.sheet,
        all_sheets=args.all_sheets,
        fmt=args.format,
        max_rows=args.rows,
        profile=args.profile,
        head=args.head,
    )


if __name__ == "__main__":
    main()
