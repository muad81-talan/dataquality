import plotly.graph_objects as go


def null_rate_bar(columns: dict) -> str:
    names = list(columns.keys())
    rates = [round(m["null_rate"] * 100, 1) for m in columns.values()]
    fig = go.Figure(go.Bar(x=names, y=rates, marker_color="#ef4444"))
    fig.update_layout(
        title="Null rate per column (%)",
        xaxis_title="Column",
        yaxis_title="Null rate (%)",
        yaxis_range=[0, 100],
        margin=dict(t=40, b=40),
        height=300,
    )
    return fig.to_html(full_html=False, include_plotlyjs="cdn")


def histogram(series_values: list, col_name: str) -> str:
    fig = go.Figure(go.Histogram(x=series_values, marker_color="#6366f1"))
    fig.update_layout(
        title=f"{col_name} — distribution",
        margin=dict(t=40, b=40),
        height=250,
    )
    return fig.to_html(full_html=False, include_plotlyjs=False)


def top_values_bar(top_values: list, col_name: str) -> str:
    labels = [str(item["value"]) for item in reversed(top_values)]
    counts = [item["count"] for item in reversed(top_values)]
    fig = go.Figure(go.Bar(x=counts, y=labels, orientation="h", marker_color="#10b981"))
    fig.update_layout(
        title=f"{col_name} — top values",
        margin=dict(t=40, b=40),
        height=max(200, len(labels) * 28),
    )
    return fig.to_html(full_html=False, include_plotlyjs=False)
