# Issue 1: Project scaffold

## What to build

Set up the FastAPI application skeleton with a minimal HTML upload page. The app should boot, serve the page at `/`, and be runnable locally with a single command. No profiling logic yet — just the plumbing end-to-end so all subsequent slices have a working foundation to build on.

Includes: project structure, dependency file (`requirements.txt`), FastAPI app entry point, static HTML upload form served by the app, basic `/upload` POST endpoint stub that accepts a file and returns a placeholder response.

## Acceptance criteria

- [ ] Running `uvicorn app.main:app --reload` (or equivalent) starts the server without errors
- [ ] `GET /` serves an HTML page with a file upload form
- [ ] `POST /upload` accepts a `multipart/form-data` file field and returns a 200 response (placeholder body)
- [ ] `requirements.txt` lists all dependencies (fastapi, uvicorn, pandas, plotly)
- [ ] Project structure is clean and ready for feature slices to be added

## Blocked by

None — can start immediately.
