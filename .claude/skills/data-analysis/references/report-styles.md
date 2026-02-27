# Report Styles Reference

> This file provides color values, typography, and layout parameters for each named style.
> Use it as **inspiration and context** — understand the spirit, then implement with judgment.
> Do not copy verbatim. Adapt to the data and audience.

---

## Engineering Baseline (All Styles)

These constraints apply to every style without exception:

```css
html { background: [match body background — no side strip]; }
body {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 48px;
  font-size: 16px;          /* min 10pt for projection */
  line-height: 1.6;
}
```

- Bar chart Y-axis always starts at 0
- Near-zero bars: `min-height: 3px` to remain visible
- Annotate only critical data points — not every one
- Color meaning: red = problem / decline, green = healthy / growth, grey = reference / neutral

---

## Classic Styles

---

### Financial Times

**One-line feel:** Salmon warmth, serif authority, traditional finance journalism

**Best for:** Financial analysis, narrative reports, earnings summaries

#### Colors
```
Background:     #FFF1E5   (FT salmon — distinctive, warm)
Body text:      #33302E   (warm near-black)
Headline:       #1A1A1A
Accent / links: #A6190D   (FT red — use sparingly)
Subheading:     #66605A
Border / rule:  #D7B89C   (warm tan)
Chart primary:  #0D7680   (FT teal)
Chart series 2: #F2A900   (FT gold)
Chart series 3: #A6190D
Chart series 4: #96652A
Positive:       #0D7680
Negative:       #A6190D
Neutral/ref:    #B3AAA2
```

#### Typography
```
Headline font:  Georgia, "Times New Roman", serif — bold, 28–36px
Subhead:        "Metric", Arial, sans-serif — medium, 14–18px (small caps optional)
Body:           Georgia, serif — regular, 16px
Data labels:    Arial, sans-serif — regular, 12px
Byline/meta:    Arial, sans-serif — 12px, color #66605A
```

#### Layout Signature
- Thin horizontal rule (1px, #D7B89C) under headline — no thick bars
- Section dividers: thin rule, not heavy headers
- Charts: minimal gridlines (light grey, dashed), no chart border
- Source line in bottom-left: "Source: [data]" in 11px sans-serif
- "Exhibit" labels not used — FT uses inline chart references
- Numbers right-aligned in tables
- Subtle drop shadow on chart container: `box-shadow: 0 1px 3px rgba(0,0,0,0.08)`

#### Feel Notes
Warm, authoritative, like a Saturday FT longread. Never feel corporate or cold.
Headlines state the conclusion: "Margins Erode for Third Consecutive Quarter"

---

### McKinsey Consulting

**One-line feel:** Navy structure, Exhibit numbering, consulting rigor

**Best for:** Strategy analysis, framework presentations, board decks

#### Colors
```
Background:     #FFFFFF
Body text:      #1A1A2E   (deep navy)
Headline:       #002F6C   (McKinsey navy)
Accent:         #002F6C   (primary) or #D22B27 (red — for callouts only)
Subheading:     #1A1A2E
Border:         #C8C9C7
Chart primary:  #002F6C   (navy)
Chart series 2: #4472C4   (blue)
Chart series 3: #70AD47   (green)
Chart series 4: #FFC000   (amber)
Chart series 5: #D22B27   (red — risk/problem)
Positive:       #70AD47
Negative:       #D22B27
Neutral:        #C8C9C7
```

#### Typography
```
Headline:       "Franklin Gothic Medium", Arial Black, sans-serif — 24–32px
Subhead:        "Franklin Gothic Book", Arial, sans-serif — 16–18px, uppercase tracking
Body:           Arial, Helvetica, sans-serif — 14–16px
Exhibit label:  Arial, 11px, uppercase, #002F6C
Data labels:    Arial, 11–12px
```

#### Layout Signature
- Every chart labeled **"Exhibit [N]"** in upper-left corner (uppercase, small)
- Chart titles are conclusion-format headlines
- Key insight box: navy left border (4px), light blue background (#EEF2FA), italic text
- Waterfall/bridge charts heavily used — show change decomposition
- Tables: header row navy background with white text; alternating #F5F7FA rows
- Bullet indentation: three levels max, first level is strategic, third is evidence
- Footer: "McKinsey & Company" equivalent — replace with client/project name

#### Feel Notes
Structured, confident, analytical. Every element earns its place.
Never decorative. If a chart doesn't answer "So what?", remove it.

---

### The Economist

**One-line feel:** Red-accent magazine density, editorial headline with opinion

**Best for:** Industry insight, macro analysis, opinionated market reports

#### Colors
```
Background:     #FFFFFF   (white) or #F9F9F7 (very light grey)
Body text:      #1A1A1A
Headline:       #1A1A1A   (black — no color for main headlines)
Accent:         #E3120B   (Economist red — signature, use for rules and callouts)
Subheading:     #1A1A1A
Horizontal rule:#E3120B   (the signature red line above chart titles)
Chart primary:  #E3120B   (single red for main series)
Chart series 2: #9E9E9E   (grey for comparison/reference)
Chart series 3: #424242   (dark grey)
Positive:       #2E7D32   (muted green)
Negative:       #E3120B
Neutral:        #9E9E9E
```

#### Typography
```
Headline:       "Officina Serif", "Georgia", serif — bold, 24–34px
Subhead:        "Officina Serif", Georgia, serif — italic, 16–18px
Body:           Georgia, serif — 15–16px, tight leading (1.5)
Chart title:    Arial, sans-serif — 13px, preceded by red rule
Data labels:    Arial, 11px
Caption:        Arial, italic, 11px, grey
```

#### Layout Signature
- Red horizontal rule (2px) sits directly above every chart title
- Chart titles are short, punchy, opinionated: "The gap is widening"
- Charts: single-color bars (red) with grey reference lines — no gradients
- In-line data annotations for the most important data points only
- Column layout: narrow left annotation + wide right chart (two-column)
- Subhead called "Buttonwood" / "Briefing" — replace with section labels
- "Source:" label always present, bottom-left, 10px

#### Feel Notes
Dense, opinionated, treats reader as intelligent. Headlines have a point of view.
Do not hedge: "could" and "may" are rare. State the finding.

---

### Goldman Sachs

**One-line feel:** High-density investment tables, Rating badge formality

**Best for:** Financial modeling, valuation reports, investment memos

#### Colors
```
Background:     #FFFFFF
Body text:      #000000
Headline:       #000000
Section header: #003366   (GS navy) background with white text
Accent:         #003366
Rating badge:   Buy = #1B5E20 bg / white text; Neutral = #E65100 bg / white; Sell = #B71C1C bg / white
Border:         #CCCCCC
Table alt row:  #F5F5F5
Chart primary:  #003366
Chart series 2: #0066CC
Chart series 3: #CC3300
Chart series 4: #009900
Positive:       #1B5E20
Negative:       #B71C1C
```

#### Typography
```
Headline:       "Helvetica Neue", Arial, sans-serif — bold, 20–28px
Section header: "Helvetica Neue", bold, 13px — white on navy background
Body:           "Helvetica Neue", Arial — 12–14px, tight line-height (1.4)
Table headers:  bold, 11px
Table data:     regular, 11–12px, numbers right-aligned
Footnote:       9–10px, light grey, asterisk-referenced
```

#### Layout Signature
- Dense information; multiple tables per page
- Rating badge in upper-right corner of report header (BUY / NEUTRAL / SELL)
- Price target: large number, prominent, near rating badge
- Section dividers: full-width navy bar (#003366) with white text
- Tables dominant — charts secondary, always labeled "Figure N"
- Target price table: ticker | rating | price target | upside | date
- Footnotes with asterisks at page bottom — regulatory disclosures
- Horizontal rules: 0.5pt, #CCCCCC

#### Feel Notes
Maximum information density. Assumes sophisticated reader.
Aesthetics serve legibility, not beauty. Tables are truth.

---

### Swiss / NZZ

**One-line feel:** Black-and-white minimalism, extreme type contrast

**Best for:** Data showcase, design-forward reports, when data IS the design

#### Colors
```
Background:     #FFFFFF   (pure white — or #FAFAFA very light)
Body text:      #000000
Headline:       #000000
Accent:         #000000   (black is the accent — use scale and weight)
Highlight color:#E63329   (NZZ red — single, rare use only)
Chart primary:  #000000
Chart series 2: #666666
Chart series 3: #BBBBBB
Chart series 4: #E63329   (one red series for emphasis only)
Positive:       #1A7A1A   (muted green)
Negative:       #E63329
Grid / rules:   #EEEEEE   (very light grey)
```

#### Typography
```
Headline:       "Aktiv Grotesk", "Helvetica Neue", sans-serif — Extra Bold/Black, 32–52px
Subhead:        "Aktiv Grotesk", sans-serif — Light, 16–20px — contrast with heavy headline
Body:           "Aktiv Grotesk", Arial, sans-serif — Regular, 14–16px
Data labels:    Mono (IBM Plex Mono, Courier) — 11–12px — tabular alignment
Number display: Extra Bold, 48–72px — one big number per card
Caption:        Light, 11px, #666666
```

#### Layout Signature
- 70% whitespace — information breathes, never crowds
- Typography does all the work: weight and scale create hierarchy, not color
- Headline is massive (52px+), subhead is wispy light — maximum contrast
- Charts: black bars on white, gridlines barely visible (#EEEEEE)
- No decorative elements — no gradients, no shadows, no rounded corners
- Single red element per page maximum
- Numbers presented in monospace for alignment

#### Feel Notes
Quiet confidence. The restraint IS the design statement.
If a design element doesn't carry information, it doesn't exist.

---

## Design-Forward Styles

---

### Fathom

**One-line feel:** Navy scientific journal, Figure numbering + footnote system

**Best for:** Research reports, technical analysis, policy briefs

#### Colors
```
Background:     #FFFFFF   (or #F8F9FB very light blue-grey)
Body text:      #1B2A4A   (dark navy — not black)
Headline:       #1B2A4A
Accent:         #2364AA   (Fathom blue)
Secondary:      #47A8BD   (teal — for charts/callouts)
Highlight bg:   #EEF4FB   (light blue — callout boxes)
Chart primary:  #2364AA
Chart series 2: #47A8BD
Chart series 3: #F2A65A   (amber)
Chart series 4: #E84855   (red)
Chart series 5: #3BB273   (green)
Positive:       #3BB273
Negative:       #E84855
Grid:           #E1E8F0
```

#### Typography
```
Headline:       "Source Serif Pro", Georgia, serif — 600 weight, 24–32px
Subhead:        "Source Sans Pro", Arial, sans-serif — semibold, 14–16px, navy
Body:           "Source Serif Pro", Georgia, serif — 400, 15–16px, 1.7 line-height
Figure label:   "Source Sans Pro", sans-serif — 11px, uppercase, #2364AA, tracked
Footnote:       "Source Sans Pro", 10px, #666 — superscript references
Caption:        Italic serif, 12px, #666
```

#### Layout Signature
- Every chart labeled **"Figure N"** in navy, uppercase, before title
- Chart title on its own line below figure label
- Footnote/source system at bottom: ¹ ² ³ superscript references in body text
- Callout box: #EEF4FB background, 3px left border in #2364AA, no drop shadow
- Two-column layout for body text; charts full-width or half-width
- Abstract / executive summary in italic with top border
- DOI-style reference block at end for data sources

#### Feel Notes
Rigorous, credible, peer-reviewable. Numbers are precise to 2 decimal places.
Tables have full borders and header shading. Looks like Nature or The Lancet.

---

### Takram

**One-line feel:** Japanese light typography, soft shadows, gentle tech feel

**Best for:** Product analysis, innovation reports, design-tech intersection

#### Colors
```
Background:     #FAFAF8   (warm off-white)
Body text:      #2C2C2C
Headline:       #1A1A1A
Accent:         #3D5AFE   (vibrant blue — Japanese design brand)
Secondary:      #00BCD4   (cyan — for highlights)
Soft highlight: #F0F4FF   (very light blue)
Card bg:        #FFFFFF with shadow
Chart primary:  #3D5AFE
Chart series 2: #00BCD4
Chart series 3: #FF6B6B   (soft coral)
Chart series 4: #4CAF50   (medium green)
Chart series 5: #FF9800   (amber)
Positive:       #43A047
Negative:       #EF5350
Neutral:        #9E9E9E
Shadow:         rgba(0,0,0,0.06)
```

#### Typography
```
Headline:       "Noto Sans JP", Inter, sans-serif — 600–700, 26–36px
Subhead:        "Noto Sans JP", Inter, sans-serif — 400, 16–18px, wider tracking
Body:           Inter, "Noto Sans", sans-serif — 400, 15px, 1.75 line-height
Data labels:    Inter, 11–12px
Number:         Inter, 500–600, 24–36px (accent color)
Caption:        Inter, 11px, #9E9E9E
```

#### Layout Signature
- Card-based layout: each insight in its own white card, 8px rounded corners
- Soft shadow: `box-shadow: 0 2px 12px rgba(0,0,0,0.06)` — gentle depth
- Icons: Feather or Material icons, 20px, in accent color
- KPI cards: large number (36px, accent color) + delta indicator + label
- Charts: smooth curves (not sharp angular lines), filled area with 15% opacity
- Generous padding inside cards: 24–32px
- Section transitions: thin horizontal line, 1px, #EBEBEB

#### Feel Notes
Thoughtful, human, considered. Designed for smart people who also care about beauty.
Feels like a well-designed app interface, not a PowerPoint slide.

---

### Editorial

**One-line feel:** Rust red + dusty rose unexpected palette, narrative editing

**Best for:** Annual reports, deep research, long-form data storytelling

#### Colors
```
Background:     #FAF7F2   (warm cream)
Body text:      #2D2926
Headline:       #1A0F0A
Accent:         #C14B2A   (rust red — editorial, warm)
Secondary:      #D4856A   (dusty rose — softer accent)
Tertiary:       #8B7355   (warm tan — supporting)
Highlight bg:   #F5EDE3   (light cream — callouts)
Chart primary:  #C14B2A
Chart series 2: #D4856A
Chart series 3: #8B7355
Chart series 4: #4A7C59   (muted sage green — contrast)
Chart series 5: #2D5F8A   (muted blue — data reference)
Positive:       #4A7C59
Negative:       #C14B2A
Neutral:        #8B7355
```

#### Typography
```
Headline:       "EB Garamond", Garamond, "Times New Roman", serif — bold, 32–48px
Subhead:        "EB Garamond", serif — italic, 18–22px
Body:           "EB Garamond", Georgia, serif — 400, 16–17px, 1.8 line-height
Pull quote:     Garamond, italic, 22–26px, rust red, centered — with em-dash attribution
Data labels:    "DM Sans", Arial, sans-serif — 11px
Caption:        Garamond, italic, 12px, #8B7355
Byline:         DM Sans, 12px, tracked, uppercase, #8B7355
```

#### Layout Signature
- Wide left margin used for pull quotes or annotation notes
- Section opener: large decorative initial capital (drop cap)
- Pull quote: cream background (#F5EDE3), rust border left 3px, italic Garamond
- Charts have cream backgrounds (not white) — consistent with page warmth
- Chapter/section dividers: centered ornament glyph (◆ or —) in rust red
- Author byline and date in small-caps at top
- Photo/chart captions with italic text and indented left border

#### Feel Notes
Warm, literary, narrative-forward. The writing matters as much as the charts.
Feels like a beautiful annual report or a design magazine feature story.
Never feels like a spreadsheet export — every element has editorial intention.

---

### Minimal

**One-line feel:** Ultra-heavy weight + 70% whitespace, luxury data presentation

**Best for:** Board reports, brand decks, when the data speaks loudest

#### Colors
```
Background:     #FFFFFF   (pure white — sacred)
Body text:      #111111   (near-black)
Headline:       #000000
Accent:         #000000   (weight is the accent)
One color only: Choose ONE from: #D4001A (red) / #0A0A5C (navy) / #1A6B3C (green)
                → used for a single highlight element per page
Chart primary:  #111111   (black)
Chart series 2: #888888   (medium grey)
Chart series 3: #CCCCCC   (light grey)
Chart series 4: [accent color]
Positive:       [accent color if green] or #1A6B3C
Negative:       #D4001A
Neutral:        #888888
```

#### Typography
```
Headline:       Any premium sans — "Neue Haas Grotesk", "GT America", "Söhne", Arial Black
                — Black/ExtraBold weight — 48–72px — sparse line count (2–4 words max)
Subhead:        Same family — Light/Thin weight — 16–20px — contrast is the point
Body:           Same family — Regular — 14–15px — very sparse
Number:         Black weight — 60–96px — presented alone, as the statement
Label:          Light weight — 10–12px — uppercase, tracked
```

#### Layout Signature
- One idea per section — never two competing focal points
- The "number as hero": one large metric, 96px, centered or anchored top-left
- Context in tiny type below: "Q3 2024 vs Q3 2023" at 10px
- Charts occupy the full width when present — no inline charts
- Maximum one chart per page/section
- No lines, no borders, no backgrounds — elements float in white space
- Tables: header bold, rows separated by 12px gap (not borders), right-aligned numbers

#### Feel Notes
Silence is the loudest statement. If in doubt, remove it.
Feels like a luxury brand brief, a Apple earnings slide, a museum label.
The data is so confident it doesn't need decoration.

---

## Chart Color Sequences (Quick Reference)

Use these palettes in order for multi-series charts:

| Style | Series 1 | Series 2 | Series 3 | Series 4 |
|-------|----------|----------|----------|----------|
| Financial Times | #0D7680 | #F2A900 | #A6190D | #96652A |
| McKinsey | #002F6C | #4472C4 | #70AD47 | #FFC000 |
| The Economist | #E3120B | #9E9E9E | #424242 | — |
| Goldman Sachs | #003366 | #0066CC | #CC3300 | #009900 |
| Swiss/NZZ | #000000 | #666666 | #BBBBBB | #E63329 |
| Fathom | #2364AA | #47A8BD | #F2A65A | #E84855 |
| Takram | #3D5AFE | #00BCD4 | #FF6B6B | #4CAF50 |
| Editorial | #C14B2A | #D4856A | #8B7355 | #4A7C59 |
| Minimal | #111111 | #888888 | #CCCCCC | [accent] |
