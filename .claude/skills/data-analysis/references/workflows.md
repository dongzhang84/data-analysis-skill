# Workflows Reference

> Detailed execution specification for the Multi-Expert Deep Analysis workflow.
> This is the operational manual for Phase 1–4 of the four-phase process.

---

## When to Use Multi-Expert Analysis

| Trigger | Action |
|---------|--------|
| User says "deep analysis", "comprehensive", "make a report" | Full 4-phase |
| Dataset has >500 rows OR >10 fields | Full 4-phase |
| Data has multiple analytical dimensions (time + financials + behavior) | Full 4-phase |
| Simple lookup, formula request, table formatting | Skip — direct execution |
| Single-metric question ("what's the total?") | Skip — direct execution |

---

## Phase 1: Data Understanding

### Step-by-step

**1. Read the data**
- Use `scripts/read_excel.py` or `scripts/read_csv.py`
- If multi-sheet Excel: list all sheets, ask user which to analyze (or analyze all)

**2. Immediately output a structured overview:**

```markdown
## Data Overview

**Dimensions:** [N rows] × [M columns]
**Time range:** [start] → [end] ([N periods])
**Grain:** [what each row represents — e.g., "one transaction per row"]

**Fields:**
| Field | Type | Non-null | Sample Values |
|-------|------|----------|---------------|
| date  | date | 100%     | 2023-01, 2023-02 |
| ...   |      |          |               |

**Basic Statistics (numeric fields):**
| Field | Mean | Median | Min | Max | Std Dev | Null% |
|-------|------|--------|-----|-----|---------|-------|

**Data Quality Issues:**
- [List any: missing values, duplicates, inconsistent formats, outliers]
- [Note if any fields have >5% missing — flag for attention]

**Initial Insights (visible immediately):**
1. [Most obvious trend or pattern — state it clearly]
2. [Second observation — anomaly, outlier, or correlation]
```

**3. Identify analytical dimensions available:**
- Time dimension? (trend analysis, seasonality, YoY comparison)
- Geographic dimension? (regional breakdown, market comparison)
- Product/category dimension? (portfolio analysis, mix shift)
- Customer dimension? (cohort, segmentation, behavior)
- Financial dimension? (P&L, margins, cash flow)

---

## Phase 2: Expert Selection

### Selection Criteria

Pick **3–5 roles** that are:
1. **Domain-matched** — each role's core expertise directly applies to the data
2. **Non-overlapping** — together they cover quantitative / qualitative / strategic / risk / behavioral
3. **Credible** — use real frameworks, institutions, or public intellectual names as anchors

### Expert Role Library

Pick from this library or create new roles as appropriate:

#### Finance & Valuation
- **DCF / Fundamental Analyst** (Damodaran-style) — earnings quality, intrinsic value, capital allocation
- **Credit / Risk Analyst** (Moody's-style) — liquidity, leverage, default risk, covenant headroom
- **Portfolio Manager** (Bridgewater-style) — macro backdrop, correlation, position sizing, risk-adjusted return
- **CFO Lens** — working capital, cash conversion cycle, EBITDA bridge, CapEx decisions

#### Growth & Marketing
- **Growth Strategist** (Andreessen Horowitz-style) — CAC, LTV, payback period, channel efficiency
- **Brand / Customer Analyst** — NPS, retention, cohort behavior, willingness to pay
- **Pricing Economist** — price elasticity, unit economics, discounting patterns

#### Operations & Supply Chain
- **Operations Efficiency Analyst** — throughput, utilization, bottleneck analysis, cycle time
- **Supply Chain Analyst** — inventory turns, lead time, supplier concentration, resilience
- **Process Improvement** (Toyota-style) — waste identification, lean metrics, defect rates

#### Strategy & Competitive
- **Strategy Consultant** (McKinsey-style) — market share, competitive position, strategic options
- **Competitive Intelligence Analyst** — relative performance, industry benchmarks, disruption signals
- **M&A / Corporate Development** — accretion/dilution, synergy potential, valuation multiples

#### Behavioral & Qualitative
- **Behavioral Economist** (Kahneman-style) — cognitive patterns in data, anchoring effects, loss aversion signals
- **Customer Insights Analyst** — usage patterns, churn signals, engagement depth
- **Sociologist / Ethnographer** — qualitative context, cultural factors, non-obvious explanations

#### Data Science
- **Statistician** — significance tests, confidence intervals, regression analysis, spurious correlations
- **Time Series Analyst** — trend decomposition, seasonality, forecasting, anomaly detection
- **Machine Learning Engineer** — feature importance, clustering, predictive modeling

---

### Phase 2 Output Format

Write role selections to a `.md` file before proceeding:

```markdown
# Expert Panel: [Dataset Name] Analysis

## Selected Roles

### Expert 1: [Role Title]
**Framework:** [Named methodology or institution]
**Analytical Focus:** [2–3 sentences on what this expert will examine]
**Key Questions This Role Answers:**
- [Question 1]
- [Question 2]
- [Question 3]

### Expert 2: [Role Title]
...

---
*User: Review the panel above. Reply "proceed" to begin parallel analysis, or suggest changes.*
```

Wait for user confirmation before proceeding to Phase 3.

---

## Phase 3: Parallel Deep Analysis

### Subagent Invocation Pattern

Launch all experts simultaneously using `Task` tool with `run_in_background=true`.

**Prompt template for each subagent:**

```
You are [Role Title], analyzing data on behalf of a senior management team.

## Your Role
[2–3 paragraph role definition — who you are, your analytical framework, your mental models]

## Data
File path: [absolute path]
Data summary: [paste Phase 1 overview here]

## Your Analysis Tasks
1. [Specific question 1 — tied to this role's expertise]
2. [Specific question 2]
3. [Specific question 3]
4. [Specific question 4]
5. Surface any anomalies, risks, or opportunities visible from your vantage point

## Output Format
Return a JSON object with this structure:
{
  "role": "[your role title]",
  "headline": "[single most important finding — conclusion format, not description]",
  "findings": [
    {
      "theme": "[theme name]",
      "conclusion": "[conclusion sentence]",
      "evidence": "[specific numbers, percentages, comparisons]",
      "chart_recommendation": "[chart type + data to visualize]"
    }
  ],
  "risks": ["[risk 1]", "[risk 2]"],
  "recommendations": ["[action 1]", "[action 2]", "[action 3]"],
  "charts": [
    {
      "title": "[chart title]",
      "type": "[bar | line | scatter | table | waterfall]",
      "data_fields": ["[field1]", "[field2]"],
      "insight": "[what this chart proves]"
    }
  ]
}
```

### Collecting Results

After all subagents complete:
1. Parse each JSON response
2. Deduplicate overlapping findings
3. Note contradictions between experts (these are often the most interesting insights)
4. Rank findings by business impact
5. Proceed to Phase 4

---

## Phase 4: Unified Synthesis

### Core Rules

- **Expert names never appear in the final report** — write as a single "senior analyst" voice
- **Organize by theme**, not by expert: themes like "Fundamentals", "Risk", "Growth Trajectory", "Efficiency"
- **Headline = conclusion**: "Free Cash Flow Turns Negative for First Time in Six Quarters" not "Cash Flow Analysis"
- **Cross-reference**: when two experts see the same pattern from different angles, the combined view is stronger
- **Contradictions = depth**: if one expert sees growth momentum and another sees margin deterioration, present both — that's the real story

### Synthesis Structure

```
Executive Summary (3–5 bullet points — conclusion format only)

Section 1: [Theme — named for the insight, not the domain]
  → Lead with the headline conclusion
  → Supporting data: specific numbers, year-over-year comparisons
  → Chart: the one chart that best proves this point
  → Subtext: nuance, caveats, or context

Section 2: [Theme]
  ...

Section N: Risk & Opportunity Landscape
  → Risks ranked by likelihood × impact
  → Opportunities the data suggests

Recommendations (3–5 items, ordered by priority and executability)

Next Steps (think one step ahead — what the user should investigate next)
```

### Headline Writing Rules

| Don't | Do |
|-------|-----|
| "Revenue Analysis" | "Revenue Growth Stalls in Core Segment While New Products Accelerate" |
| "Customer Churn Data" | "Monthly Churn Doubled Since Q2 — Concentrated in Enterprise Tier" |
| "Cost Review" | "COGS as % of Revenue Hit 5-Year High — Margin Recovery Requires Volume or Price Action" |

### Chart Selection per Theme

| Theme | Best Chart |
|-------|-----------|
| Trend over time | Line chart (with annotation at inflection points) |
| Composition change | Stacked bar or 100% stacked bar |
| Relative performance | Bar chart, sorted descending |
| Correlation | Scatter plot |
| Decomposition / attribution | Waterfall / bridge chart |
| Distribution | Histogram or box plot |
| Comparison (few items) | Grouped bar chart |
| High-level KPIs | Metric cards with delta indicators |

---

## Scale Guide

| Complexity | Description | Expert Count | Duration |
|------------|-------------|-------------|----------|
| Simple | Single table, <10 fields, one clear question | Skip multi-expert | —  |
| Medium | Multi-dimension, time series, financials | 3 experts | Phase 3 parallel |
| Complex | Multi-table, multi-domain, strategic question | 5 experts | Phase 3 parallel |
| Mega | Multiple datasets, competitive landscape, M&A | 5+ experts | Phase 3 parallel + sub-phases |

---

## Common Expert Combinations by Data Type

| Data Type | Recommended Expert Panel |
|-----------|-------------------------|
| SaaS metrics (MRR, churn, CAC) | Growth Strategist + Customer Insights + CFO Lens |
| Public company financials | DCF Analyst + Credit Analyst + Strategy Consultant |
| E-commerce / retail sales | Growth Strategist + Operations Efficiency + Behavioral Economist |
| Supply chain / operations | Supply Chain + Operations Efficiency + CFO Lens |
| HR / workforce data | Behavioral Economist + CFO Lens + Strategy Consultant |
| Product usage data | Customer Insights + Behavioral Economist + Growth Strategist |
| Market / industry data | Strategy Consultant + Competitive Intelligence + Time Series Analyst |
