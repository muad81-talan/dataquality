# Issue 6: Visualizations

## What to build

Add three Plotly-powered interactive charts embedded inline in the report: a bar chart of null rates across all columns, a histogram of value distributions for each numeric column, and a horizontal bar chart of top value frequencies for each categorical (non-numeric) column. Charts are rendered as inline HTML divs — no PNG export, no external requests.

## Acceptance criteria

- [ ] A null rate bar chart (one bar per column, x = column name, y = null rate %) appears in the summary section
- [ ] A histogram appears in each numeric column's section showing value distribution
- [ ] A top-values frequency bar chart appears in each categorical column's section
- [ ] All charts are interactive (hover tooltips) via Plotly's inline JS
- [ ] Charts render correctly for columns with all-null values, one unique value, or high cardinality
- [ ] No external network requests are made to render charts (fully self-contained HTML)

## Blocked by

- Issue 4: Per-column profiling
