from app import charts

FLAG_LABELS = {
    "high_null_rate": ("High null rate", "#ef4444"),
    "constant_column": ("Constant column", "#f97316"),
    "suspected_id": ("Suspected ID", "#8b5cf6"),
    "numeric_as_string": ("Numeric as string", "#0ea5e9"),
}

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: system-ui, sans-serif; background: #f8fafc; color: #1e293b; padding: 2rem; }
h1 { font-size: 1.5rem; font-weight: 700; margin-bottom: 1.5rem; }
h2 { font-size: 1.1rem; font-weight: 600; margin-bottom: 0.75rem; }
h3 { font-size: 0.95rem; font-weight: 600; color: #475569; margin-bottom: 0.5rem; }
.summary { background: white; border-radius: 8px; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem;
           box-shadow: 0 1px 3px rgba(0,0,0,.08); }
.summary-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1rem; }
.stat { text-align: center; }
.stat-value { font-size: 1.6rem; font-weight: 700; color: #6366f1; }
.stat-label { font-size: 0.75rem; color: #64748b; margin-top: 2px; }
.columns { display: flex; flex-direction: column; gap: 1rem; }
.col-card { background: white; border-radius: 8px; padding: 1.25rem 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,.08); }
.col-header { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem; }
.col-name { font-size: 1rem; font-weight: 700; }
.dtype-badge { font-size: 0.7rem; background: #e2e8f0; color: #475569;
               padding: 2px 8px; border-radius: 99px; font-weight: 600; }
.flags { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 4px; }
.flag { font-size: 0.7rem; padding: 2px 8px; border-radius: 99px; color: white; font-weight: 600; }
.metrics-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 0.5rem;
                margin-bottom: 1rem; }
.metric { background: #f8fafc; border-radius: 6px; padding: 0.5rem 0.75rem; }
.metric-label { font-size: 0.7rem; color: #94a3b8; text-transform: uppercase; letter-spacing: .04em; }
.metric-value { font-size: 0.95rem; font-weight: 600; margin-top: 2px; }
.top-values { margin-top: 0.5rem; }
.top-values table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
.top-values td { padding: 3px 8px; border-bottom: 1px solid #f1f5f9; }
.top-values td:last-child { text-align: right; color: #64748b; }
.samples { font-size: 0.8rem; color: #64748b; margin-top: 0.5rem; }
.back { display: inline-block; margin-bottom: 1.5rem; font-size: 0.85rem; color: #6366f1; text-decoration: none; }
.back:hover { text-decoration: underline; }
"""


def _fmt(value) -> str:
    if isinstance(value, float):
        return f"{value:,.4g}"
    return str(value)


def _col_card(name: str, metrics: dict, flags: list, df_col) -> str:
    flag_html = "".join(
        f'<span class="flag" style="background:{FLAG_LABELS[f][1]}">{FLAG_LABELS[f][0]}</span>'
        for f in flags
        if f in FLAG_LABELS
    )
    metric_items = [
        ("Null count", metrics["null_count"]),
        ("Null rate", f"{metrics['null_rate']*100:.1f}%"),
        ("Unique values", metrics["unique_count"]),
        ("Cardinality", f"{metrics['cardinality_ratio']*100:.1f}%"),
    ]
    if "min" in metrics:
        metric_items += [
            ("Min", _fmt(metrics["min"])),
            ("Max", _fmt(metrics["max"])),
            ("Mean", _fmt(metrics["mean"])),
            ("Std dev", _fmt(metrics["std"])),
        ]
    metrics_html = "".join(
        f'<div class="metric"><div class="metric-label">{lbl}</div>'
        f'<div class="metric-value">{val}</div></div>'
        for lbl, val in metric_items
    )
    top_rows = "".join(
        f"<tr><td>{item['value']}</td><td>{item['count']}</td></tr>"
        for item in metrics["top_values"]
    )
    samples_txt = ", ".join(str(v) for v in metrics["sample_values"])

    if metrics["dtype"] == "numeric" and df_col is not None:
        chart_html = charts.histogram(df_col.dropna().tolist(), name)
    else:
        chart_html = charts.top_values_bar(metrics["top_values"], name) if metrics["top_values"] else ""

    return f"""
    <div class="col-card">
      <div class="col-header">
        <span class="col-name">{name}</span>
        <span class="dtype-badge">{metrics['dtype']}</span>
        <div class="flags">{flag_html}</div>
      </div>
      <div class="metrics-grid">{metrics_html}</div>
      <div class="top-values">
        <h3>Top values</h3>
        <table><tbody>{top_rows}</tbody></table>
      </div>
      <div class="samples"><strong>Samples:</strong> {samples_txt}</div>
      {chart_html}
    </div>
    """


def render(report: dict, df) -> str:
    ds = report["dataset"]
    null_chart = charts.null_rate_bar(report["columns"])
    col_cards = "".join(
        _col_card(name, metrics, metrics.get("flags", []), df[name] if df is not None else None)
        for name, metrics in report["columns"].items()
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Data Quality Report</title>
<style>{CSS}</style></head>
<body>
<a class="back" href="/">← Analyze another file</a>
<h1>Data Quality Report</h1>
<div class="summary">
  <h2>Dataset overview</h2>
  <div class="summary-grid">
    <div class="stat"><div class="stat-value">{ds['row_count']:,}</div><div class="stat-label">Rows</div></div>
    <div class="stat"><div class="stat-value">{ds['col_count']}</div><div class="stat-label">Columns</div></div>
    <div class="stat"><div class="stat-value">{ds['duplicate_rows']:,}</div><div class="stat-label">Duplicate rows</div></div>
    <div class="stat"><div class="stat-value">{ds['file_size_bytes']/1024/1024:.2f} MB</div><div class="stat-label">File size</div></div>
  </div>
  {null_chart}
</div>
<div class="columns">{col_cards}</div>
</body></html>"""
