"""
Earth2Mars AI - Side-by-Side Comparison Page
Compare Earth analog sites head-to-head across all feature dimensions.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Compare | Earth2Mars AI", page_icon="⚖️", layout="wide")

st.title("⚖️ Analog Site Comparison")
st.markdown("Compare two Earth analog sites **side-by-side** across terrain, mineralogy, thermal, and aridity dimensions.")

# ──────────────────────────────────────────────
# Combined Analog Database
# ──────────────────────────────────────────────
ALL_ANALOGS = {
    "Haughton Crater, Devon Island": {"terrain": 0.92, "mineral": 0.78, "thermal": 0.95, "aridity": 0.88, "body": "Moon", "category": "Impact Craters"},
    "McMurdo Dry Valleys": {"terrain": 0.88, "mineral": 0.82, "thermal": 0.97, "aridity": 0.96, "body": "Moon & Mars", "category": "Cold Traps / Polar"},
    "Lanzarote Lava Tubes": {"terrain": 0.88, "mineral": 0.91, "thermal": 0.65, "aridity": 0.72, "body": "Moon", "category": "Lava Tube Habitats"},
    "Moses Lake Sand Dunes": {"terrain": 0.94, "mineral": 0.70, "thermal": 0.55, "aridity": 0.75, "body": "Moon", "category": "Regolith & Terrain"},
    "Mauna Kea Basalt Fields": {"terrain": 0.93, "mineral": 0.89, "thermal": 0.60, "aridity": 0.68, "body": "Moon", "category": "Regolith & Terrain"},
    "Atacama Desert": {"terrain": 0.90, "mineral": 0.93, "thermal": 0.82, "aridity": 0.98, "body": "Mars", "category": "Arid Desert"},
    "Río Tinto": {"terrain": 0.72, "mineral": 0.96, "thermal": 0.55, "aridity": 0.60, "body": "Mars", "category": "Astrobiology"},
    "Iceland Highlands (Askja)": {"terrain": 0.94, "mineral": 0.90, "thermal": 0.78, "aridity": 0.65, "body": "Mars", "category": "Volcanic Basalt"},
    "MDRS (Utah)": {"terrain": 0.88, "mineral": 0.85, "thermal": 0.72, "aridity": 0.90, "body": "Mars", "category": "Arid Desert"},
    "HI-SEAS (Mauna Loa)": {"terrain": 0.90, "mineral": 0.87, "thermal": 0.62, "aridity": 0.73, "body": "Mars", "category": "Volcanic Basalt"},
    "Svalbard": {"terrain": 0.80, "mineral": 0.75, "thermal": 0.93, "aridity": 0.85, "body": "Moon & Mars", "category": "Polar / Cryogenic"},
    "Wadi Rum": {"terrain": 0.91, "mineral": 0.84, "thermal": 0.70, "aridity": 0.88, "body": "Mars", "category": "Arid Desert"},
}

site_names = list(ALL_ANALOGS.keys())

# ──────────────────────────────────────────────
# Selection
# ──────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    site_a = st.selectbox("🅰️ Site A", site_names, index=0)
with col2:
    site_b = st.selectbox("🅱️ Site B", site_names, index=5)

if site_a == site_b:
    st.warning("Please select two different sites to compare.")
    st.stop()

data_a = ALL_ANALOGS[site_a]
data_b = ALL_ANALOGS[site_b]

# ──────────────────────────────────────────────
# Info Cards
# ──────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### 🅰️ {site_a}")
    st.markdown(f"**Target Body:** {data_a['body']}")
    st.markdown(f"**Category:** {data_a['category']}")

with col2:
    st.markdown(f"### 🅱️ {site_b}")
    st.markdown(f"**Target Body:** {data_b['body']}")
    st.markdown(f"**Category:** {data_b['category']}")

st.divider()

# ──────────────────────────────────────────────
# Overlay Radar Chart
# ──────────────────────────────────────────────
st.subheader("🕸️ Feature Comparison")

categories = ["Terrain", "Mineral", "Thermal", "Aridity"]

values_a = [data_a["terrain"], data_a["mineral"], data_a["thermal"], data_a["aridity"]]
values_b = [data_b["terrain"], data_b["mineral"], data_b["thermal"], data_b["aridity"]]
values_a.append(values_a[0])
values_b.append(values_b[0])
categories_closed = categories + [categories[0]]

fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=values_a, theta=categories_closed, fill="toself",
    name=site_a, line=dict(color="#636EFA"),
))
fig.add_trace(go.Scatterpolar(
    r=values_b, theta=categories_closed, fill="toself",
    name=site_b, line=dict(color="#EF553B"),
))
fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
    height=450,
    margin=dict(l=80, r=80, t=40, b=40),
)
st.plotly_chart(fig, use_container_width=True)

# ──────────────────────────────────────────────
# Score Table
# ──────────────────────────────────────────────
st.subheader("📊 Score Breakdown")

comparison_df = pd.DataFrame({
    "Feature": categories,
    site_a: values_a[:4],
    site_b: values_b[:4],
    "Δ (A − B)": [a - b for a, b in zip(values_a[:4], values_b[:4])],
})

st.dataframe(
    comparison_df.style.background_gradient(subset=[site_a, site_b], cmap="RdYlGn", vmin=0.5, vmax=1.0),
    use_container_width=True,
    hide_index=True,
)
