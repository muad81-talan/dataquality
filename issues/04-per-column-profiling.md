# Issue 4: Per-column profiling

## What to build

For each column in the uploaded CSV, compute and display a full profiling card: inferred data type, null count and null rate (%), unique count and cardinality ratio, min/max/mean/std (numeric columns only), top 10 most frequent values with counts, and 3–5 sample values. Each column gets its own labeled section in the report.

## Acceptance criteria

- [ ] Each column renders a named section with its inferred data type
- [ ] Null count and null rate (%) are shown for every column
- [ ] Unique count and cardinality ratio (unique / total rows) are shown for every column
- [ ] Min, max, mean, and std are shown for numeric columns; not shown for non-numeric
- [ ] Top 10 most frequent values with their counts are shown for every column
- [ ] 3–5 sample values are shown for every column
- [ ] Metrics are correct for numeric, string, boolean, and datetime-like columns
- [ ] Columns with all-null values do not cause errors

## Blocked by

- Issue 3: Dataset-level metrics
