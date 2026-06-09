# Issue 2: File upload & validation

## What to build

Wire up the upload form to POST a CSV to the server, enforce the 100MB file size limit both client-side and server-side, and display a clear error message in the browser when validation fails. On success, the server parses the CSV into a DataFrame and returns a minimal acknowledgement (row/column count) so the slice is end-to-end verifiable.

## Acceptance criteria

- [ ] User can select a `.csv` file via the upload form and submit it
- [ ] Files over 100MB are rejected server-side with a descriptive 400 error message displayed in the browser
- [ ] Client-side pre-check warns the user before upload if the file exceeds 100MB
- [ ] Non-CSV files are rejected with a clear error message
- [ ] Valid CSV files under the size limit are accepted; server responds with basic confirmation (e.g. row/column count)
- [ ] Empty or malformed CSV files return a descriptive error, not a 500

## Blocked by

- Issue 1: Project scaffold
