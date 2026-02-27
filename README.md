# data-analysis-skill

> Claude Code skill for end-to-end data analysis — multi-expert workflow, HTML reports, interactive charts.

---

## What This Skill Does

Activate this skill when you want Claude to go beyond basic data summaries and deliver analysis with the depth and presentation quality of a professional analyst.

**Core capabilities:**
- **Multi-expert deep analysis** — 3–5 expert subagents analyze your data in parallel from different perspectives (financial, strategic, behavioral, etc.), then synthesize into a unified report
- **HTML reports** — publication-quality output with interactive charts (ECharts / Chart.js / D3) in 9 named styles
- **Excel & CSV ingestion** — reads files, profiles data quality, outputs markdown/JSON
- **PPTX export** — converts HTML reports to PowerPoint slides via Puppeteer
- **One step ahead** — proactively surfaces insights, risks, and next steps beyond what was asked

---

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/data-analysis-skill.git
cd data-analysis-skill
```

### 2. Install Python dependencies (for scripts)

```bash
pip install pandas openpyxl tabulate chardet
```

The scripts also auto-install missing dependencies on first run.

### 3. Install Node.js dependencies (for HTML → PPTX)

```bash
npm install puppeteer pptxgenjs
```

### 4. Register the skill with Claude Code

Copy the skill directory into your Claude config:

```bash
cp -r .claude/skills/data-analysis ~/.claude/skills/
```

Or add to your project's `.claude/skills/` directory to scope it to this project.

---

## Usage

### Triggering the skill

The skill activates when you mention any of:
`analyze data` · `make a report` · `visualize` · `Excel` · `dashboard` · `ROI` ·
`weekly report` · `monthly report` · `chart` · `insight` · `presentation` · `KPI` · `metrics`

### Basic Examples

**Analyze a CSV file:**
```
Analyze sample-data/example.csv and make an HTML report
```

**Deep analysis with a specific style:**
```
Do a deep analysis of this Excel file using the Financial Times style
```

**Quick data profile:**
```
python .claude/skills/data-analysis/scripts/read_csv.py sample-data/example.csv --profile
```

**Excel reader:**
```
python .claude/skills/data-analysis/scripts/read_excel.py your-data.xlsx --all-sheets
python .claude/skills/data-analysis/scripts/read_excel.py your-data.xlsx --sheet "Revenue" --format json
```

**Convert HTML report to PPTX:**
```
node .claude/skills/data-analysis/scripts/html2pptx.js report.html output.pptx
```

### Script Reference

| Script | Purpose | Key Options |
|--------|---------|-------------|
| `scripts/read_csv.py` | Read & profile CSV files | `--profile` `--format md\|json` `--rows N` |
| `scripts/read_excel.py` | Read Excel files | `--sheet` `--all-sheets` `--profile` |
| `scripts/html2pptx.js` | HTML → PPTX conversion | `--selector .slide` `--full-page` `--layout WIDE` |

---

## Report Styles

When no style is specified, Claude randomly selects one to keep outputs fresh.

| Style | Feel | Best for |
|-------|------|----------|
| **Financial Times** | Salmon warmth, serif authority | Financial analysis, narrative reports |
| **McKinsey** | Navy structure, Exhibit numbering | Strategy decks, frameworks |
| **The Economist** | Red-accent, editorial opinion | Industry insight, macro reports |
| **Goldman Sachs** | Dense tables, rating badges | Financial modeling, investment memos |
| **Swiss / NZZ** | Black-and-white minimalism | Data showcase, design-forward |
| **Fathom** | Navy scientific journal | Research reports, technical analysis |
| **Takram** | Japanese light typography | Product analysis, innovation reports |
| **Editorial** | Rust red + dusty rose | Annual reports, long-form storytelling |
| **Minimal** | Ultra-heavy type + whitespace | Board reports, luxury brand decks |

Full color/font specs: [`.claude/skills/data-analysis/references/report-styles.md`](.claude/skills/data-analysis/references/report-styles.md)

---

## Multi-Expert Workflow

For any complex dataset, the skill runs a four-phase analysis:

```
Phase 1: Data Understanding   → Profile data, surface initial insights
Phase 2: Expert Selection     → Select 3–5 expert roles; write to .md for review
Phase 3: Parallel Analysis    → Each expert runs as an independent subagent (Task tool)
Phase 4: Unified Synthesis    → Senior analyst integrates all findings into final report
```

Expert names never appear in the final report — findings are organized by theme and written in a single voice.

Detailed spec: [`.claude/skills/data-analysis/references/workflows.md`](.claude/skills/data-analysis/references/workflows.md)

---

## Sample Data

`sample-data/example.csv` contains 36 months (Jan 2022 – Dec 2024) of realistic SaaS business metrics:

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

Try it:
```
Analyze sample-data/example.csv — do a deep analysis and make an HTML report
```

---

## Reference Files

| File | Contents |
|------|---------|
| [`references/report-styles.md`](.claude/skills/data-analysis/references/report-styles.md) | Color palettes, typography, layout specs for all 9 styles |
| [`references/workflows.md`](.claude/skills/data-analysis/references/workflows.md) | Multi-expert workflow execution spec, subagent prompt templates |
| [`references/html-templates.md`](.claude/skills/data-analysis/references/html-templates.md) | HTML/CSS/JS component library for report building |
| [`references/domain-knowledge.md`](.claude/skills/data-analysis/references/domain-knowledge.md) | Financial metrics, SaaS KPIs, chart selection, statistical methods |

---

## Design Principles

- **Context, not control** — Reference files are inspiration, not verbatim instructions
- **Conclusion first** — Headlines state the finding, not the topic
- **Data honesty** — Y-axis always starts at 0; charts must not mislead
- **No filler** — Remove "in summary", "it should be noted", "as mentioned above"
- **Think one step ahead** — Proactively surface what the user hasn't asked for yet

---

## License

MIT — see [LICENSE](LICENSE)
