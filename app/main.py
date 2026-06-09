import io
import pandas as pd
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from app.profiler import profile
from app.flags import detect
from app import report as report_renderer

app = FastAPI()

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>CSV Data Quality</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: system-ui, sans-serif; background: #f8fafc; display: flex;
       justify-content: center; align-items: center; min-height: 100vh; }
.card { background: white; border-radius: 12px; padding: 2.5rem;
        box-shadow: 0 4px 16px rgba(0,0,0,.08); width: 100%; max-width: 480px; }
h1 { font-size: 1.4rem; font-weight: 700; margin-bottom: 0.5rem; }
p { color: #64748b; font-size: 0.9rem; margin-bottom: 1.5rem; }
input[type=file] { display: block; width: 100%; padding: 0.6rem;
                   border: 2px dashed #cbd5e1; border-radius: 8px;
                   margin-bottom: 1rem; font-size: 0.9rem; cursor: pointer; }
button { background: #6366f1; color: white; border: none; border-radius: 8px;
         padding: 0.65rem 1.5rem; font-size: 0.95rem; font-weight: 600;
         cursor: pointer; width: 100%; }
button:hover { background: #4f46e5; }
.hint { font-size: 0.75rem; color: #94a3b8; margin-top: 0.75rem; text-align: center; }
#error { color: #ef4444; font-size: 0.85rem; margin-top: 0.75rem; display: none; }
</style></head>
<body>
<div class="card">
  <h1>CSV Data Quality</h1>
  <p>Upload a CSV file to get an instant data quality report.</p>
  <form action="/upload" method="post" enctype="multipart/form-data"
        onsubmit="return validate()">
    <input type="file" name="file" accept=".csv" id="file-input">
    <button type="submit">Analyze</button>
    <div id="error"></div>
    <div class="hint">Maximum file size: 100 MB</div>
  </form>
</div>
<script>
function validate() {
  const f = document.getElementById('file-input').files[0];
  const err = document.getElementById('error');
  if (!f) { err.textContent = 'Please select a file.'; err.style.display = 'block'; return false; }
  if (!f.name.endsWith('.csv')) { err.textContent = 'Only .csv files are supported.'; err.style.display = 'block'; return false; }
  if (f.size > 100 * 1024 * 1024) { err.textContent = 'File exceeds the 100 MB limit.'; err.style.display = 'block'; return false; }
  return true;
}
</script>
</body></html>"""


@app.get("/", response_class=HTMLResponse)
def index():
    return INDEX_HTML


@app.post("/upload", response_class=HTMLResponse)
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        return HTMLResponse(content="File exceeds 100MB limit.", status_code=400)
    if not file.filename.endswith(".csv"):
        return HTMLResponse(content="Only CSV files are supported.", status_code=400)
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as exc:
        return HTMLResponse(content=f"Could not parse CSV: {exc}", status_code=400)
    result = profile(df, file_size_bytes=len(contents))
    for col_name, metrics in result["columns"].items():
        metrics["flags"] = detect(metrics, row_count=result["dataset"]["row_count"])
    html = report_renderer.render(result, df)
    return HTMLResponse(content=html, status_code=200)
