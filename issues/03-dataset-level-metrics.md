# Issue 3: Dataset-level metrics

## What to build

Compute and display dataset-level summary statistics at the top of the report page. After a successful upload, the browser renders a summary section showing row count, column count, duplicate row count, and file size. This establishes the report page structure that per-column slices will extend.

## Acceptance criteria

- [ ] Report page shows: total row count, total column count, duplicate row count, file size (human-readable, e.g. "2.4 MB")
- [ ] Summary section is rendered at the top of the report, above any column detail
- [ ] Duplicate row count is accurate (exact duplicate rows across all columns)
- [ ] Metrics are correct for CSVs with headers, varied column counts, and zero duplicates

## Blocked by

- Issue 2: File upload & validation
