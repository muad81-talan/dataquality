# PRD: CSV Data Quality Web App

## Problem Statement

Data engineers working with CSV datasets have no quick way to assess the quality of a file before using it in a pipeline or analysis. Manually inspecting CSVs in a spreadsheet or writing one-off profiling scripts is slow, inconsistent, and produces no shareable output. They need a fast, self-serve tool that gives a comprehensive, factual quality report from a raw CSV upload.

## Solution

A local, stateless web application where a data engineer uploads a CSV file (up to 100MB) and immediately receives a rendered data quality report in the browser. The report covers dataset-level statistics, per-column profiling metrics, data quality flags, and visualizations — all factual, no AI-generated commentary.

## User Stories

1. As a data engineer, I want to upload a CSV file via a browser UI, so that I can start profiling without writing any code.
2. As a data engineer, I want to see the total row count and column count of my dataset, so that I can verify the file loaded correctly.
3. As a data engineer, I want to see the file size displayed in the report, so that I know what volume of data was analyzed.
4. As a data engineer, I want to see the number of duplicate rows in my dataset, so that I can identify data integrity issues early.
5. As a data engineer, I want to see the inferred data type for each column, so that I can detect type mismatches without opening the file.
6. As a data engineer, I want to see the null rate (%) for each column, so that I can identify columns with missing data.
7. As a data engineer, I want to see the unique value count and cardinality for each column, so that I can distinguish ID columns from categorical ones.
8. As a data engineer, I want to see min, max, mean, and standard deviation for numeric columns, so that I can spot distribution anomalies.
9. As a data engineer, I want to see the top N most frequent values for each column, so that I can understand the shape of categorical data.
10. As a data engineer, I want to see sample values for each column, so that I can visually inspect raw content without opening the file.
11. As a data engineer, I want columns with a null rate above 50% to be flagged, so that I can quickly identify columns that may be unusable.
12. As a data engineer, I want constant columns (only one distinct value) to be flagged, so that I can remove them from my pipeline.
13. As a data engineer, I want suspected ID columns (cardinality ≈ row count) to be flagged, so that I can confirm or exclude them from aggregations.
14. As a data engineer, I want columns where a numeric type is stored as string to be flagged, so that I can fix upstream schema issues.
15. As a data engineer, I want a bar chart of null rates per column, so that I can spot missing-data patterns at a glance.
16. As a data engineer, I want histograms for numeric columns, so that I can see value distributions without writing plotting code.
17. As a data engineer, I want a top-values chart for categorical columns, so that I can see frequency distributions visually.
18. As a data engineer, I want the report rendered directly in the browser after upload, so that I get immediate feedback without any extra steps.
19. As a data engineer, I want the app to reject files over 100MB with a clear error message, so that I know why the upload failed.
20. As a data engineer, I want the app to handle the upload and processing without requiring login or credentials, so that I can use it instantly without setup friction.
21. As a data engineer, I want the app to process each upload fresh with no stored state, so that previous uploads do not affect current results.
22. As a data engineer, I want the report to display a summary section at the top with dataset-level metrics, so that I get a high-level overview before drilling into columns.
23. As a data engineer, I want each column's profiling section to be clearly labeled with the column name and type, so that I can navigate the report easily.
24. As a data engineer, I want quality flags to be visually distinct (e.g. highlighted or badged), so that issues stand out without reading every metric.

## Implementation Decisions

- **Backend**: FastAPI — handles file upload via `multipart/form-data`, runs pandas profiling, returns rendered HTML or JSON to the frontend.
- **Profiling engine**: pandas — computes all per-column and dataset-level metrics directly; no third-party profiling library dependency.
- **Charting**: Plotly — generates interactive charts (bar, histogram, frequency) embedded as HTML `<div>` components in the report page.
- **Frontend**: Plain HTML + vanilla JS — single-page app with an upload form; on submission, posts the file and replaces the page content with the returned report HTML. No build toolchain.
- **File size enforcement**: 100MB hard limit enforced server-side in FastAPI; client also shows a pre-upload size check for fast feedback.
- **Statefulness**: Fully stateless — no database, no file storage, no session. Each request is self-contained.
- **Authentication**: None — designed for local or trusted internal network use.
- **Metrics computed per column**:
  - Data type (inferred)
  - Null count and null rate (%)
  - Unique count and cardinality ratio
  - Min, max, mean, std (numeric columns only)
  - Top 10 most frequent values with counts
  - 3–5 sample values
- **Dataset-level metrics**: row count, column count, duplicate row count, file size
- **Quality flags** (computed server-side, rendered as badges):
  - High null rate: null rate > 50%
  - Constant column: unique count == 1
  - Suspected ID column: unique count / row count > 0.95
  - Numeric-as-string: column dtype is object but >90% of non-null values parse as numeric

## Testing Decisions

- **What makes a good test**: Tests should assert on the profiling output (metrics dict / report content) given a known CSV input — not on internal pandas calls or helper function internals. Use small, hand-crafted CSV fixtures that exercise specific edge cases.
- **Modules to test**:
  - Profiling logic: given a CSV (as bytes or DataFrame), returns the correct metrics for each column and dataset level.
  - Quality flag logic: given known column characteristics (all nulls, one unique value, high cardinality, numeric strings), the correct flags are raised.
  - File size validation: files over 100MB are rejected; files at or under the limit are accepted.
  - FastAPI endpoint: upload a valid CSV, assert a 200 response with report content; upload an oversized file, assert a 4xx response.
- **Testing approach**: pytest for backend unit and integration tests; FastAPI `TestClient` for endpoint tests. No frontend testing in scope for v1.

## Out of Scope

- AI-generated narrative insights or LLM commentary
- Downloadable report (PDF or HTML export)
- Session history or persistent report storage
- Authentication or user accounts
- Support for file formats other than CSV (Excel, Parquet, JSON)
- Streaming or sampling for files over the size limit
- Scheduled or batch profiling
- Custom user-defined quality rules
- Deployment configuration (Docker, cloud hosting)

## Further Notes

- The app is intentionally minimal and local-first. Deployment hardening (auth, rate limiting, HTTPS) is deferred.
- Plotly charts should be rendered as inline HTML (not PNG) to keep the report interactive in the browser.
- The 100MB limit is a practical constraint for synchronous processing; async/chunked processing is a future concern.
- Column type inference should use pandas' default dtype detection, with a post-processing pass to detect numeric-as-string columns.
