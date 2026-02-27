# HTML Templates Reference

> Reusable HTML/CSS/JS components for building analysis reports.
> These are **building blocks and reference patterns** — not verbatim templates.
> Adapt structure, colors, and content to the chosen report style.

---

## Layout Shell

Every report starts with this structural skeleton. Replace `[STYLE-VARIABLES]` with the chosen style's values.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Report Title]</title>
  <!-- ECharts for complex charts -->
  <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
  <!-- Optional: Chart.js for simpler charts -->
  <!-- <script src="https://cdn.jsdelivr.net/npm/chart.js"></script> -->
  <style>
    /* ── Reset ─────────────────────────────── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    /* ── Layout Contract (required for ALL styles) ── */
    html {
      background: [body-bg];          /* must match body — no side strips */
    }
    body {
      max-width: 1200px;
      margin: 0 auto;
      padding: 40px 48px;
      background: [body-bg];
      color: [text-color];
      font-family: [font-stack];
      font-size: 16px;
      line-height: 1.6;
    }

    /* ── Typography ─────────────────────────── */
    h1 { font-size: 2.25rem; font-weight: 700; line-height: 1.2; margin-bottom: 0.5rem; }
    h2 { font-size: 1.5rem; font-weight: 600; margin: 2.5rem 0 1rem; }
    h3 { font-size: 1.15rem; font-weight: 600; margin: 1.5rem 0 0.75rem; }
    p  { margin-bottom: 1rem; }

    /* ── Section Divider ────────────────────── */
    .section { margin: 3rem 0; }
    .divider  { border: none; border-top: 1px solid [border-color]; margin: 2rem 0; }

    /* ── Chart Container ────────────────────── */
    .chart-wrap {
      width: 100%;
      margin: 1.5rem 0;
    }
    .chart-wrap canvas,
    .chart-wrap div[id] {
      width: 100% !important;
      height: 360px;
    }
    .chart-title {
      font-size: 0.95rem;
      font-weight: 600;
      color: [subhead-color];
      margin-bottom: 0.5rem;
    }
    .chart-source {
      font-size: 0.75rem;
      color: [muted-color];
      margin-top: 0.4rem;
    }
  </style>
</head>
<body>
  <!-- Report Header -->
  <header class="report-header">
    <p class="report-meta">[Date] · [Prepared by / Source]</p>
    <h1>[Report Title — conclusion format]</h1>
    <p class="report-subtitle">[One-sentence framing of the key finding]</p>
  </header>

  <hr class="divider">

  <!-- Executive Summary -->
  <!-- [insert exec-summary component] -->

  <!-- Sections -->
  <!-- [insert section components] -->

  <!-- Footer -->
  <footer style="margin-top: 4rem; padding-top: 1.5rem; border-top: 1px solid [border-color];
                 font-size: 0.75rem; color: [muted-color];">
    <p>Source: [data source] · Analysis generated [date] · All figures in [currency/unit] unless noted</p>
  </footer>
</body>
</html>
```

---

## Executive Summary Box

```html
<section class="exec-summary" style="
  background: [highlight-bg];
  border-left: 4px solid [accent-color];
  padding: 1.5rem 2rem;
  margin: 2rem 0;
  border-radius: 0 4px 4px 0;
">
  <h2 style="margin-top: 0; font-size: 1.1rem; color: [accent-color]; text-transform: uppercase;
             letter-spacing: 0.05em; font-weight: 700;">Executive Summary</h2>
  <ul style="padding-left: 1.25rem; margin: 0.5rem 0;">
    <li style="margin-bottom: 0.6rem;">[Conclusion 1 — most important finding]</li>
    <li style="margin-bottom: 0.6rem;">[Conclusion 2]</li>
    <li style="margin-bottom: 0.6rem;">[Conclusion 3]</li>
    <li style="margin-bottom: 0.6rem;">[Key risk or watch item]</li>
    <li style="margin-bottom: 0.6rem;">[Top recommendation]</li>
  </ul>
</section>
```

---

## KPI Metric Cards

Use for at-a-glance key numbers at the top of a report.

```html
<div class="kpi-grid" style="
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
">
  <!-- Single KPI Card -->
  <div class="kpi-card" style="
    background: #fff;
    border: 1px solid [border-color];
    border-radius: 6px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  ">
    <div class="kpi-label" style="font-size: 0.75rem; text-transform: uppercase;
                                   letter-spacing: 0.08em; color: [muted-color]; margin-bottom: 0.4rem;">
      [Metric Name]
    </div>
    <div class="kpi-value" style="font-size: 2.25rem; font-weight: 700; color: [text-color]; line-height: 1;">
      [Value]
    </div>
    <div class="kpi-delta" style="margin-top: 0.4rem; font-size: 0.85rem;">
      <!-- Positive delta -->
      <span style="color: #2E7D32;">▲ +12.4% vs prior period</span>
      <!-- Negative delta: color: #C62828; ▼ -->
    </div>
    <div class="kpi-context" style="font-size: 0.75rem; color: [muted-color]; margin-top: 0.3rem;">
      [Brief context — e.g., "Best quarter since Q2 2022"]
    </div>
  </div>

  <!-- Repeat for each KPI -->
</div>
```

---

## ECharts: Line Chart (Time Series)

```html
<div class="chart-wrap">
  <div class="chart-title">[Chart Title — conclusion format]</div>
  <div id="chart-line-1" style="height: 360px;"></div>
  <div class="chart-source">Source: [data source]</div>
</div>

<script>
const lineChart = echarts.init(document.getElementById('chart-line-1'));
lineChart.setOption({
  color: ['[series-1-color]', '[series-2-color]'],
  grid: { top: 30, right: 20, bottom: 50, left: 60 },
  tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } },
  legend: { bottom: 0, icon: 'circle', itemWidth: 8 },
  xAxis: {
    type: 'category',
    data: [/* dates or categories */],
    axisLine: { lineStyle: { color: '[border-color]' } },
    axisTick: { show: false },
    axisLabel: { color: '[muted-color]', fontSize: 11 }
  },
  yAxis: {
    type: 'value',
    min: 0,                              /* always start at 0 for bar charts */
    axisLabel: {
      color: '[muted-color]', fontSize: 11,
      formatter: (v) => `$${(v/1000).toFixed(0)}K`  /* adapt formatter */
    },
    splitLine: { lineStyle: { color: '[border-color]', type: 'dashed' } },
    axisLine: { show: false },
    axisTick: { show: false }
  },
  series: [
    {
      name: '[Series 1 Name]',
      type: 'line',
      data: [/* values */],
      smooth: 0.3,
      lineStyle: { width: 2 },
      symbol: 'circle', symbolSize: 5,
      /* Optional area fill: */
      areaStyle: { opacity: 0.08 }
    },
    {
      name: '[Series 2 Name]',
      type: 'line',
      data: [/* values */],
      smooth: 0.3,
      lineStyle: { width: 2, type: 'dashed' }
    }
  ]
});
window.addEventListener('resize', () => lineChart.resize());
</script>
```

---

## ECharts: Bar Chart (Sorted Ranking)

```html
<div class="chart-wrap">
  <div class="chart-title">[Chart Title]</div>
  <div id="chart-bar-1" style="height: 360px;"></div>
  <div class="chart-source">Source: [data source]</div>
</div>

<script>
// Data sorted descending — rankings descend
const categories = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E'];
const values     = [1250000, 980000, 740000, 620000, 390000];

const barChart = echarts.init(document.getElementById('chart-bar-1'));
barChart.setOption({
  color: ['[primary-color]'],
  grid: { top: 20, right: 20, bottom: 50, left: 70 },
  tooltip: {
    trigger: 'axis',
    formatter: (p) => `${p[0].name}: ${(p[0].value/1e6).toFixed(2)}M`
  },
  xAxis: {
    type: 'value',
    min: 0,
    axisLabel: { formatter: (v) => `$${(v/1000).toFixed(0)}K`, fontSize: 11, color: '[muted-color]' },
    splitLine: { lineStyle: { color: '[border-color]', type: 'dashed' } },
    axisLine: { show: false }
  },
  yAxis: {
    type: 'category',
    data: categories,
    axisLabel: { fontSize: 11, color: '[text-color]' },
    axisLine: { show: false },
    axisTick: { show: false }
  },
  series: [{
    type: 'bar',
    data: values,
    barMaxWidth: 48,
    /* Protect near-zero bars */
    itemStyle: {
      borderRadius: [0, 3, 3, 0],
      color: (params) => params.value < 50000 ? '[muted-color]' : '[primary-color]'
    },
    label: {
      show: true, position: 'right',
      formatter: (p) => `$${(p.value/1000).toFixed(0)}K`,
      fontSize: 11, color: '[text-color]'
    }
  }]
});
window.addEventListener('resize', () => barChart.resize());
</script>
```

---

## ECharts: Waterfall / Bridge Chart

```html
<div class="chart-wrap">
  <div class="chart-title">[Start] → [End]: What Changed and Why</div>
  <div id="chart-waterfall" style="height: 360px;"></div>
</div>

<script>
// Waterfall pattern: use stacked bar with transparent bottom segment
const labels  = ['Start', 'Volume', 'Price', 'Mix', 'FX', 'End'];
const base    = [0, 1000, 0, 0, 0, 0];          // transparent offset
const pos     = [1000, 200, 0, 150, 0, 1420];   // positive changes + start + end
const neg     = [0, 0, -80, 0, -50, 0];          // negative changes

const wfChart = echarts.init(document.getElementById('chart-waterfall'));
wfChart.setOption({
  color: ['transparent', '[positive-color]', '[negative-color]', '[primary-color]'],
  tooltip: { trigger: 'axis' },
  xAxis: { type: 'category', data: labels },
  yAxis: { type: 'value', min: 0 },
  series: [
    { name: 'Base', type: 'bar', stack: 'wf', data: base, itemStyle: { opacity: 0 } },
    { name: 'Increase', type: 'bar', stack: 'wf', data: pos },
    { name: 'Decrease', type: 'bar', stack: 'wf', data: neg }
  ]
});
</script>
```

---

## Data Table (Striped, Ranked)

```html
<div style="overflow-x: auto; margin: 1.5rem 0;">
  <table style="
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
  ">
    <thead>
      <tr style="background: [header-bg]; color: [header-text];">
        <th style="padding: 10px 14px; text-align: left; font-weight: 600; font-size: 0.78rem;
                   text-transform: uppercase; letter-spacing: 0.06em;">#</th>
        <th style="padding: 10px 14px; text-align: left; ...">Category</th>
        <th style="padding: 10px 14px; text-align: right; ...">Revenue</th>
        <th style="padding: 10px 14px; text-align: right; ...">Growth</th>
        <th style="padding: 10px 14px; text-align: right; ...">Margin</th>
      </tr>
    </thead>
    <tbody>
      <!-- Row: alternating background for readability -->
      <tr style="background: #fff;">
        <td style="padding: 10px 14px; color: [muted-color];">1</td>
        <td style="padding: 10px 14px; font-weight: 500;">[Category A]</td>
        <td style="padding: 10px 14px; text-align: right; font-variant-numeric: tabular-nums;">$1.25M</td>
        <td style="padding: 10px 14px; text-align: right; color: [positive-color];">▲ +18.2%</td>
        <td style="padding: 10px 14px; text-align: right;">72.4%</td>
      </tr>
      <tr style="background: [alt-row-bg];">
        <!-- Repeat... -->
      </tr>
    </tbody>
    <tfoot>
      <tr style="background: [header-bg]; color: [header-text]; font-weight: 600;">
        <td colspan="2" style="padding: 10px 14px;">Total</td>
        <td style="padding: 10px 14px; text-align: right;">$4.98M</td>
        <td style="padding: 10px 14px; text-align: right; color: [positive-color];">▲ +14.7%</td>
        <td style="padding: 10px 14px; text-align: right;">68.9%</td>
      </tr>
    </tfoot>
  </table>
</div>
```

---

## Annotation Pattern (Chart Callout)

For highlighting a specific data point on a chart (ECharts `markPoint` or inline HTML):

```javascript
// Inside ECharts series options:
markPoint: {
  data: [
    {
      name: 'Key event',
      coord: ['2023-09', 890000],
      value: '↑ Product launch',
      itemStyle: { color: '[accent-color]' },
      label: { fontSize: 11, position: 'top', color: '[accent-color]' }
    }
  ]
},
markLine: {
  data: [{ type: 'average', name: 'Avg' }],
  lineStyle: { type: 'dashed', color: '[muted-color]' },
  label: { formatter: 'Avg: {c}' }
}
```

---

## Inline Insight Box (Pull Quote / Callout)

```html
<div style="
  margin: 1.5rem 0;
  padding: 1rem 1.5rem;
  border-left: 3px solid [accent-color];
  background: [highlight-bg];
  font-style: italic;
  font-size: 1.05rem;
  color: [text-color];
">
  "[Key insight stated as a complete sentence — the most important thing on this page.]"
</div>
```

---

## Responsive Two-Column Layout

```html
<div style="
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin: 1.5rem 0;
">
  <div><!-- Left column: text, table, or small chart --></div>
  <div><!-- Right column --></div>
</div>

<!-- Single-column fallback for narrow displays -->
<style>
  @media (max-width: 768px) {
    /* Override grid to single column */
  }
</style>
```

---

## CDN Library Reference

```html
<!-- ECharts (preferred for complex charts) -->
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>

<!-- Chart.js (simpler API for basic charts) -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<!-- D3.js (maximum control, for custom visuals) -->
<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>

<!-- Google Fonts (serif options) -->
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;600;700&family=Source+Serif+Pro:wght@400;600&display=swap" rel="stylesheet">

<!-- Google Fonts (sans options) -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&family=Noto+Sans+JP:wght@400;700&display=swap" rel="stylesheet">
```

---

## Common CSS Utilities

```css
/* Typography utilities */
.text-muted    { color: [muted-color]; }
.text-positive { color: [positive-color]; }
.text-negative { color: [negative-color]; }
.text-small    { font-size: 0.8rem; }
.text-mono     { font-family: "IBM Plex Mono", "Courier New", monospace; }
.text-right    { text-align: right; }

/* Number formatting */
.tabular-nums  { font-variant-numeric: tabular-nums; }

/* Delta indicators */
.delta-up   { color: [positive-color]; }
.delta-down { color: [negative-color]; }

/* Spacing */
.mt-4 { margin-top: 4rem; }
.mb-2 { margin-bottom: 2rem; }
.section-gap { margin: 3rem 0; }

/* Print optimization */
@media print {
  body { max-width: 100%; padding: 20px; }
  .chart-wrap div { height: 280px !important; }
  .no-print { display: none; }
}
```
