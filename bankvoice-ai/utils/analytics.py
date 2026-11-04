"""
Banking Voice Analytics Engine and Chart Generation.
Handles persistent CSV operations, key metrics aggregation, and Plotly visualizations.
"""

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, Tuple


DATA_FILENAME = "interactions.csv"


def get_csv_path() -> str:
    """
    Resolve CSV path safely whether running from bankvoice-ai/ or repository root.
    """
    candidates = [
        os.path.join(os.path.dirname(__file__), "..", "data", DATA_FILENAME),
        os.path.join("data", DATA_FILENAME),
        os.path.join("bankvoice-ai", "data", DATA_FILENAME),
        DATA_FILENAME
    ]
    for c in candidates:
        if os.path.exists(c):
            return os.path.abspath(c)
    # Default to first candidate and create dir if needed
    target = os.path.abspath(candidates[0])
    os.makedirs(os.path.dirname(target), exist_ok=True)
    return target


def load_interactions() -> pd.DataFrame:
    """
    Load interactions dataset from CSV with schema safety.
    """
    csv_path = get_csv_path()
    
    expected_cols = [
        "interaction_id", "timestamp", "customer_name", "audio_filename",
        "transcript", "sentiment", "sentiment_score", "complaint_category",
        "urgency", "is_sample", "voice_auth_status"
    ]

    if not os.path.exists(csv_path):
        df = pd.DataFrame(columns=expected_cols)
        return df

    try:
        df = pd.read_csv(csv_path)
        # Ensure all expected columns exist
        for col in expected_cols:
            if col not in df.columns:
                df[col] = None
        # Convert types
        df["sentiment_score"] = pd.to_numeric(df["sentiment_score"], errors="coerce").fillna(0.75)
        df["is_sample"] = df["is_sample"].astype(bool)
        return df
    except Exception as e:
        print(f"Warning: Failed to parse {csv_path}: {e}")
        return pd.DataFrame(columns=expected_cols)


def save_interaction(interaction_dict: Dict[str, Any]) -> bool:
    """
    Append a new interaction record to the persistent CSV file.
    """
    csv_path = get_csv_path()
    try:
        df = load_interactions()
        new_row = pd.DataFrame([interaction_dict])
        updated_df = pd.concat([df, new_row], ignore_index=True)
        updated_df.to_csv(csv_path, index=False)
        return True
    except Exception as e:
        print(f"Error saving interaction to {csv_path}: {e}")
        return False


def get_dashboard_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Compute executive banking KPI metrics.
    """
    if df.empty:
        return {
            "total_interactions": 0,
            "positive_count": 0,
            "negative_count": 0,
            "positive_pct": 0.0,
            "negative_pct": 0.0,
            "top_complaint": "None",
            "top_complaint_count": 0,
            "critical_fraud_count": 0,
            "live_records": 0,
            "sample_records": 0,
            "avg_sentiment_score": 0.0
        }

    total = len(df)
    positive_count = int((df["sentiment"] == "Positive").sum())
    negative_count = int((df["sentiment"] == "Negative").sum())
    positive_pct = round((positive_count / total) * 100, 1) if total > 0 else 0.0
    negative_pct = round((negative_count / total) * 100, 1) if total > 0 else 0.0

    # Top complaint
    complaint_counts = df["complaint_category"].value_counts()
    top_complaint = complaint_counts.index[0] if not complaint_counts.empty else "N/A"
    top_complaint_count = int(complaint_counts.iloc[0]) if not complaint_counts.empty else 0

    critical_fraud = int(((df["complaint_category"] == "Fraud Complaints") | (df["urgency"] == "Critical")).sum())
    sample_records = int((df["is_sample"] == True).sum())
    live_records = total - sample_records
    avg_score = round(df["sentiment_score"].mean() * 100, 1)

    return {
        "total_interactions": total,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "positive_pct": positive_pct,
        "negative_pct": negative_pct,
        "top_complaint": top_complaint,
        "top_complaint_count": top_complaint_count,
        "critical_fraud_count": critical_fraud,
        "live_records": live_records,
        "sample_records": sample_records,
        "avg_sentiment_score": avg_score
    }


def create_sentiment_donut_chart(df: pd.DataFrame) -> go.Figure:
    """
    Institutional high-contrast sentiment breakdown donut chart.
    """
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No interaction records available", showarrow=False, font=dict(color="#94A3B8"))
        return fig

    counts = df["sentiment"].value_counts().reset_index()
    counts.columns = ["Sentiment", "Count"]

    color_map = {
        "Positive": "#10B981",  # Institutional Emerald
        "Negative": "#EF4444"   # Institutional Crimson Red
    }
    colors = [color_map.get(s, "#64748B") for s in counts["Sentiment"]]

    fig = go.Figure(data=[
        go.Pie(
            labels=counts["Sentiment"],
            values=counts["Count"],
            hole=0.62,
            marker=dict(colors=colors, line=dict(color="#0F172A", width=2)),
            textinfo="label+percent",
            textposition="outside",
            textfont=dict(family="Segoe UI, -apple-system, sans-serif", size=13, color="#F8FAFC"),
            hoverinfo="label+value+percent",
            hovertemplate="<b>%{label} Interaction</b><br>Volume: %{value}<br>Share: %{percent}<extra></extra>"
        )
    ])

    fig.update_layout(
        title=dict(
            text="<b>Sentiment Distribution</b>",
            font=dict(family="Segoe UI, -apple-system, sans-serif", size=16, color="#F1F5F9"),
            x=0.05
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(color="#CBD5E1", size=12)
        ),
        margin=dict(l=20, r=20, t=50, b=30),
        height=320
    )
    return fig


def create_complaint_bar_chart(df: pd.DataFrame) -> go.Figure:
    """
    Horizontal complaint distribution bar chart sorted by frequency.
    """
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No interaction records available", showarrow=False, font=dict(color="#94A3B8"))
        return fig

    counts = df["complaint_category"].value_counts().reset_index()
    counts.columns = ["Category", "Interactions"]
    counts = counts.sort_values(by="Interactions", ascending=True)

    # Accent color gradient highlighting Fraud & High-risk categories
    bar_colors = []
    for cat in counts["Category"]:
        if cat == "Fraud Complaints":
            bar_colors.append("#DC2626")  # Severe Red
        elif cat in ["Transaction Issues", "Card Issues"]:
            bar_colors.append("#2563EB")  # Institutional Navy Blue
        elif cat == "Loan Issues":
            bar_colors.append("#0284C7")  # Slate Blue
        else:
            bar_colors.append("#64748B")  # Neutral Slate

    fig = go.Figure(data=[
        go.Bar(
            x=counts["Interactions"],
            y=counts["Category"],
            orientation="h",
            marker=dict(
                color=bar_colors,
                line=dict(color="#1E293B", width=1),
                opacity=0.92
            ),
            text=counts["Interactions"],
            textposition="auto",
            textfont=dict(color="#FFFFFF", size=12, family="Segoe UI, sans-serif"),
            hovertemplate="<b>%{y}</b><br>Interactions: %{x}<extra></extra>"
        )
    ])

    fig.update_layout(
        title=dict(
            text="<b>Complaint Category Breakdown</b>",
            font=dict(family="Segoe UI, -apple-system, sans-serif", size=16, color="#F1F5F9"),
            x=0.05
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            title="",
            showgrid=True,
            gridcolor="#1E293B",
            tickfont=dict(color="#94A3B8"),
            zeroline=False
        ),
        yaxis=dict(
            title="",
            tickfont=dict(color="#E2E8F0", size=12),
            showgrid=False
        ),
        margin=dict(l=10, r=20, t=50, b=20),
        height=320
    )
    return fig


def create_category_sentiment_stacked(df: pd.DataFrame) -> go.Figure:
    """
    Stacked breakdown comparing Positive vs Negative interactions per category.
    """
    if df.empty:
        return go.Figure()

    ct = pd.crosstab(df["complaint_category"], df["sentiment"]).reset_index()
    if "Positive" not in ct.columns:
        ct["Positive"] = 0
    if "Negative" not in ct.columns:
        ct["Negative"] = 0

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Positive",
        x=ct["complaint_category"],
        y=ct["Positive"],
        marker_color="#10B981"
    ))
    fig.add_trace(go.Bar(
        name="Negative",
        x=ct["complaint_category"],
        y=ct["Negative"],
        marker_color="#EF4444"
    ))

    fig.update_layout(
        barmode="stack",
        title=dict(
            text="<b>Sentiment by Banking Domain</b>",
            font=dict(family="Segoe UI, sans-serif", size=15, color="#F1F5F9"),
            x=0.05
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickangle=-15, tickfont=dict(color="#CBD5E1", size=11), gridcolor="#1E293B"),
        yaxis=dict(title="Cases", gridcolor="#1E293B", tickfont=dict(color="#94A3B8")),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#CBD5E1")
        ),
        margin=dict(l=20, r=20, t=60, b=40),
        height=300
    )
    return fig

