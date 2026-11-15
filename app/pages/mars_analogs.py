"""
Earth2Mars AI - Mars Analog Explorer Page
Detailed view of Earth locations analogous to Mars exploration sites.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Mars Analogs | Earth2Mars AI", page_icon="🔴", layout="wide")

st.title("🔴 Mars Analog Explorer")
st.markdown("Explore Earth locations that simulate **Martian conditions** for exploration, astrobiology, and crew training.")

# ──────────────────────────────────────────────
# Analog Site Data
# ──────────────────────────────────────────────
MARS_ANALOGS = [
    {
        "site": "Atacama Desert",
        "lat": -24.5, "lon": -69.25,
        "country": "Chile",
        "category": "Arid Desert Terrain",
        "simulates": "Driest non-polar desert — Mars-like UV, perchlorate soils, extreme aridity for life-detection testing",
        "users": "NASA, ESA, SETI Institute",
        "terrain_score": 0.90,
        "mineral_score": 0.93,
        "thermal_score": 0.82,
        "aridity_score": 0.98,
        "overall": 0.95,
    },
    {
        "site": "McMurdo Dry Valleys",
        "lat": -77.5, "lon": 162.0,
        "country": "Antarctica",
        "category": "Polar / Cryogenic",
        "simulates": "Closest overall analog to Mars — hyperarid, freezing, permafrost, endolithic microbial life",
        "users": "NASA, NSF, ESA",
        "terrain_score": 0.88,
        "mineral_score": 0.82,
        "thermal_score": 0.97,
        "aridity_score": 0.96,
        "overall": 0.96,
    },
    {
        "site": "Río Tinto",
        "lat": 37.69, "lon": -6.56,
        "country": "Spain",
        "category": "Astrobiology",
        "simulates": "Acidic (pH 2) iron-rich river with iron-oxide/sulfate mineralogy matching Meridiani Planum",
        "users": "NASA, CAB-INTA-CSIC",
        "terrain_score": 0.72,
        "mineral_score": 0.96,
        "thermal_score": 0.55,
        "aridity_score": 0.60,
        "overall": 0.93,
    },
    {
        "site": "Iceland Highlands (Askja)",
        "lat": 65.05, "lon": -16.75,
        "country": "Iceland",
        "category": "Volcanic Basalt",
        "simulates": "Active volcanic basalt fields, sinuous rilles, lava tubes — analog for Tharsis volcanism",
        "users": "ESA, NASA BASALT project",
        "terrain_score": 0.94,
        "mineral_score": 0.90,
        "thermal_score": 0.78,
        "aridity_score": 0.65,
        "overall": 0.92,
    },
    {
        "site": "MDRS (Mars Desert Research Station)",
        "lat": 38.41, "lon": -110.79,
        "country": "USA",
        "category": "Arid Desert Terrain",
        "simulates": "Iron-rich red sandstone terrain with full crew simulation habitat and EVA protocols",
        "users": "Mars Society",
        "terrain_score": 0.88,
        "mineral_score": 0.85,
        "thermal_score": 0.72,
        "aridity_score": 0.90,
        "overall": 0.89,
    },
    {
        "site": "Wadi Rum",
        "lat": 29.57, "lon": 35.42,
        "country": "Jordan",
        "category": "Arid Desert Terrain",
        "simulates": "Iron-oxide red sandstone canyons resembling Valles Marineris outflow channels",
        "users": "Austrian Space Forum (AMADEE)",
        "terrain_score": 0.91,
        "mineral_score": 0.84,
        "thermal_score": 0.70,
        "aridity_score": 0.88,
        "overall": 0.86,
    },
    {
        "site": "HI-SEAS (Mauna Loa)",
        "lat": 19.47, "lon": -155.58,
        "country": "USA",
        "category": "Volcanic Basalt",
        "simulates": "Barren basaltic lava flows, no vegetation — long-duration crew isolation psychology",
        "users": "University of Hawaiʻi, NASA",
        "terrain_score": 0.90,
        "mineral_score": 0.87,
        "thermal_score": 0.62,
        "aridity_score": 0.73,
        "overall": 0.88,
    },
    {
        "site": "Svalbard",
        "lat": 78.23, "lon": 15.63,
        "country": "Norway",
        "category": "Polar / Cryogenic",
        "simulates": "Permafrost polygonal ground matching Mars polygon terrain, subsurface ice",
        "users": "ESA, AMASE project",
        "terrain_score": 0.80,
        "mineral_score": 0.75,
        "thermal_score": 0.93,
        "aridity_score": 0.85,
        "overall": 0.87,
    },
    {
        "site": "Pilbara Region",
        "lat": -21.17, "lon": 119.0,
        "country": "Australia",
        "category": "Astrobiology",
        "simulates": "3.5 Ga stromatolites — oldest life evidence; analog for recognizing Martian biosignatures",
        "users": "Australian Centre for Astrobiology",
        "terrain_score": 0.78,
        "mineral_score": 0.88,
        "thermal_score": 0.60,
        "aridity_score": 0.82,
        "overall": 0.84,
    },
]

df = pd.DataFrame(MARS_ANALOGS)

# ──────────────────────────────────────────────
# Globe Map
# ──────────────────────────────────────────────
st.subheader("🗺️ Global Distribution")

fig_map = px.scatter_geo(
    df,
    lat="lat",
    lon="lon",
    hover_name="site",
    color="category",
    size="overall",
    size_max=20,
    projection="natural earth",
    title="Mars Analog Sites on Earth",
    color_discrete_sequence=px.colors.qualitative.Bold,
)
fig_map.update_layout(height=500, margin=dict(l=0, r=0, t=40, b=0))
st.plotly_chart(fig_map, use_container_width=True)

# ──────────────────────────────────────────────
# Ranking Bar Chart
# ──────────────────────────────────────────────
st.subheader("📊 Similarity Rankings")

df_sorted = df.sort_values("overall", ascending=True)
fig_bar = px.bar(
    df_sorted,
    x="overall",
    y="site",
    orientation="h",
    color="category",
    title="Mars Analog Similarity Scores",
    labels={"overall": "Overall Similarity Score", "site": ""},
    color_discrete_sequence=px.colors.qualitative.Bold,
)
fig_bar.update_layout(height=450, showlegend=True)
st.plotly_chart(fig_bar, use_container_width=True)

# ──────────────────────────────────────────────
# Detailed Cards
# ──────────────────────────────────────────────
st.subheader("📋 Analog Site Details")

for _, row in df.iterrows():
    with st.expander(f"**{row['site']}** — {row['category']} (Score: {row['overall']:.2f})"):
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"**Country:** {row['country']}")
            st.markdown(f"**Coordinates:** {row['lat']:.2f}°, {row['lon']:.2f}°")
            st.markdown(f"**What it simulates:** {row['simulates']}")
            st.markdown(f"**Used by:** {row['users']}")

        with col2:
            categories_radar = ["Terrain", "Mineral", "Thermal", "Aridity"]
            values = [row["terrain_score"], row["mineral_score"], row["thermal_score"], row["aridity_score"]]
            values.append(values[0])
            categories_radar.append(categories_radar[0])

            fig_radar = go.Figure(
                data=go.Scatterpolar(r=values, theta=categories_radar, fill="toself", name=row["site"]),
            )
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                showlegend=False,
                height=250,
                margin=dict(l=40, r=40, t=20, b=20),
            )
            st.plotly_chart(fig_radar, use_container_width=True)
