# data-analysis-skill

A [Claude Code](https://claude.ai/claude-code) skill that turns raw data into publication-quality analysis — interactive HTML reports, multi-expert parallel reasoning, and one-click PowerPoint export.

---

## What it produces

Drop a CSV or Excel file and ask Claude to analyze it. You get:

- **A narrative HTML report** with interactive charts, insight callouts, risk cards, and executive summary — styled like a professional analyst's deliverable, not a template
- **A PowerPoint deck** if you need to present it — each report section becomes a 16:9 slide with SVG charts
- **A structured data profile** in markdown or JSON for further processing

The sample output in this repo ([`sample-output/report.html`](sample-output/report.html)) is a real analysis of 36 months of SaaS business metrics, generated from [`sample-data/example.csv`](sample-data/example.csv).

---

## How it works

### Multi-expert parallel analysis

For complex datasets, the skill doesn't run a single pass. It selects 3–5 domain experts relevant to your data, runs them as independent Claude subagents in parallel, then synthesizes their findings into a single unified report. No expert names appear in the output — everything is written in one voice, organized by theme.

```
Phase 1  Data Understanding    Profile data, surface immediate anomalies
Phase 2  Expert Selection      Select 3–5 roles; write to .md for your review
Phase 3  Parallel Analysis     Each expert runs as an independent subagent
Phase 4  Unified Report        Senior analyst synthesizes into final HTML output
```

For simple tasks — a quick table, a formula, a lookup — the multi-expert workflow is skipped and Claude responds directly.

### Nine report styles

Each style is a complete design system: color palette, typography, layout rhythm, chart style. When you don't specify one, the skill picks randomly to keep outputs fresh.

| Style | Feel | Best for |
|-------|------|----------|
| **Financial Times** | Salmon warmth, serif authority | Financial analysis, narrative reports |
| **McKinsey** | Navy structure, Exhibit numbering | Strategy decks, framework analysis |
| **The Economist** | Red-accent, editorial headline with opinion | Industry insight, macro reports |
| **Goldman Sachs** | Dense tables, rating badges | Investment memos, valuation models |
| **Swiss / NZZ** | Black-and-white minimalism | Data showcase, design-forward reports |
| **Fathom** | Navy scientific journal | Research reports, technical analysis |
| **Takram** | Japanese light typography, soft shadows | Product analysis, innovation reports |
| **Editorial** | Rust red + dusty rose palette | Annual reports, long-form storytelling |
| **Minimal** | Ultra-heavy type + 70% whitespace | Board reports, luxury brand decks |

---

## Requirements

- [Claude Code](https://claude.ai/claude-code) — the Claude CLI
- **Python 3.8+** with `pandas`, `openpyxl`, `tabulate`, `chardet`
- **Node.js 18+** with `puppeteer` and `pptxgenjs` (for PPTX export)

---

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/data-analysis-skill.git
cd data-analysis-skill
```

### 2. Install Python dependencies

```bash
pip install pandas openpyxl tabulate chardet
```

The Python scripts also auto-install any missing packages on first run.

### 3. Install Node.js dependencies

```bash
npm install
```

This installs `puppeteer` and `pptxgenjs` for the HTML-to-PPTX converter.

### 4. Register the skill with Claude Code

**Project-scoped** (only available in this project):

```bash
# The skill is already in .claude/skills/ — Claude Code picks it up automatically
```

**User-scoped** (available in all your projects):

```bash
cp -r .claude/skills/data-analysis ~/.claude/skills/
```

---

## Usage

### Triggering the skill

The skill activates automatically when you mention any of:

`analyze data` · `make a report` · `visualize` · `Excel` · `dashboard` · `ROI` · `weekly report` · `monthly report` · `data processing` · `chart` · `insight` · `presentation` · `table` · `formula` · `KPI` · `metrics`

### Try it with the sample data

```
Analyze sample-data/example.csv and make a deep analysis HTML report
```

```
Do a deep analysis of this data using the McKinsey style
```

```
Make a report and then convert it to a PowerPoint presentation
```

### Analyze your own data

```
Analyze my-data.xlsx — focus on revenue trends and customer churn
```

```
Read quarterly-results.csv and make a Goldman Sachs style investor report
```

### PPTX export

Convert any HTML report to a PowerPoint deck:

```
node .claude/skills/data-analysis/scripts/html2pptx.js sample-output/report.html output.pptx
```

Or ask Claude to do it end-to-end:

```
Make an HTML report from this data, then export it as a PowerPoint presentation
```

The converter captures each `.slide` div as a 1280×720 screenshot and assembles them into a 16:9 PPTX file.

---

## Script reference

All scripts are in `.claude/skills/data-analysis/scripts/`.

### `read_csv.py`

Reads and profiles CSV files. Outputs markdown tables, JSON, or a statistical summary.

```bash
python .claude/skills/data-analysis/scripts/read_csv.py data.csv
python .claude/skills/data-analysis/scripts/read_csv.py data.csv --profile
python .claude/skills/data-analysis/scripts/read_csv.py data.csv --format json --rows 50
```

### `read_excel.py`

Reads Excel workbooks. Handles multi-sheet files and mixed data types.

```bash
python .claude/skills/data-analysis/scripts/read_excel.py data.xlsx
python .claude/skills/data-analysis/scripts/read_excel.py data.xlsx --sheet "Revenue"
python .claude/skills/data-analysis/scripts/read_excel.py data.xlsx --all-sheets --profile
```

### `html2pptx.js`

Converts an HTML slide file to PPTX using Puppeteer. Captures each `.slide` div as a full-bleed image.

```bash
node .claude/skills/data-analysis/scripts/html2pptx.js report.html output.pptx
node .claude/skills/data-analysis/scripts/html2pptx.js slides.html deck.pptx --delay 1000
node .claude/skills/data-analysis/scripts/html2pptx.js page.html one-slide.pptx --full-page
```

| Option | Default | Description |
|--------|---------|-------------|
| `--selector <css>` | `.slide` | CSS selector for slide elements |
| `--width <px>` | `1280` | Capture width |
| `--height <px>` | `720` | Capture height |
| `--delay <ms>` | `500` | Wait after load (for animations) |
| `--full-page` | off | Capture entire page as one slide |
| `--quality <1–100>` | `95` | PNG quality |

---

## Sample data

`sample-data/example.csv` contains 36 months (Jan 2022 – Dec 2024) of realistic SaaS business metrics — a complete dataset for testing the skill's analysis depth.

<details>
<summary>26 columns: click to expand</summary>

| Column | Description |
|--------|-------------|
| `date` | Month (YYYY-MM) |
| `mrr` | Monthly Recurring Revenue |
| `arr` | Annualized Recurring Revenue |
| `new_customers` | New logos added |
| `churned_customers` | Churned logos |
| `active_customers` | Total active customer count |
| `churn_rate_pct` | Monthly logo churn % |
| `nrr_pct` | Net Revenue Retention % |
| `revenue` | Total revenue (MRR + professional services) |
| `cogs` | Cost of Goods Sold |
| `gross_profit` | Revenue − COGS |
| `gross_margin_pct` | Gross margin % |
| `sales_marketing` | S&M spend |
| `research_development` | R&D spend |
| `general_admin` | G&A spend |
| `total_opex` | Total operating expenses |
| `ebitda` | EBITDA |
| `ebitda_margin_pct` | EBITDA margin % |
| `headcount` | Employee count |
| `revenue_per_employee` | Annualized revenue per employee |
| `cac` | Customer Acquisition Cost |
| `ltv` | Customer Lifetime Value |
| `ltv_cac_ratio` | LTV / CAC ratio |
| `avg_contract_value` | Average Annual Contract Value |
| `expansion_mrr` | MRR from upsells/expansions |
| `contraction_mrr` | MRR lost from downgrades |

</details>

---

## Project structure

```
data-analysis-skill/
├── .claude/
│   └── skills/
│       └── data-analysis/
│           ├── SKILL.md                  # Skill definition loaded by Claude Code
│           ├── scripts/
│           │   ├── read_csv.py           # CSV ingestion + profiling
│           │   ├── read_excel.py         # Excel ingestion + profiling
│           │   └── html2pptx.js          # HTML → PPTX converter
│           └── references/
│               ├── report-styles.md      # Color palettes, typography, layout specs
│               ├── workflows.md          # Multi-expert workflow execution spec
│               ├── html-templates.md     # HTML/CSS/JS component library
│               └── domain-knowledge.md   # SaaS KPIs, financial metrics, chart guide
├── sample-data/
│   └── example.csv                       # 36-month SaaS dataset for testing
├── sample-output/
│   ├── report.html                       # Full HTML analysis report (Takram style)
│   ├── slides.html                       # Slide-formatted version (12 slides, SVG charts)
│   └── report.pptx                       # PPTX export from slides.html
└── package.json
```

---

## Design principles

These guide every report the skill generates:

- **Conclusion first** — headlines state the finding, not the topic. "ARR re-accelerated to 30.9%" not "ARR Analysis"
- **Data-backed** — every claim is supported by a specific number
- **No filler** — "in summary", "it should be noted", and "as mentioned above" are always removed
- **Charts don't mislead** — Y-axis always starts at 0; minimum bar height protects near-zero values
- **Think one step ahead** — proactively surface what the user hasn't asked for yet: risks, next analyses, anomalies

---

## Contributing

Contributions are welcome. A few good places to start:

- **New report style** — add a design system to `references/report-styles.md` and a sample output
- **New script** — data connectors (SQL, Google Sheets, JSON), additional export formats
- **Reference knowledge** — industry-specific domain knowledge in `references/domain-knowledge.md`
- **Bug fixes** — especially in the PPTX converter and Excel reader edge cases

Please open an issue before starting significant work so we can align on direction.

---

## License

MIT — see [LICENSE](LICENSE)
