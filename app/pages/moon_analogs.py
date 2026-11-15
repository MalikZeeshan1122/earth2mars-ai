"""
Earth2Mars AI - Moon Analog Explorer Page
Detailed view of Earth locations analogous to permanent Moon base sites.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Moon Analogs | Earth2Mars AI", page_icon="🌙", layout="wide")

st.title("🌙 Moon Base Analog Explorer")
st.markdown("Explore Earth locations that simulate conditions at the **lunar south pole** for permanent base construction.")

# ──────────────────────────────────────────────
# Analog Site Data
# ──────────────────────────────────────────────
MOON_ANALOGS = [
    {
        "site": "Haughton Crater, Devon Island",
        "lat": 75.38, "lon": -89.67,
        "country": "Canada",
        "category": "Impact Craters",
        "simulates": "23 km impact crater in polar desert — impact-shattered rock analogous to south-pole crater geology",
        "users": "NASA HMP, Mars Society (FMARS)",
        "terrain_score": 0.92,
        "mineral_score": 0.78,
        "thermal_score": 0.95,
        "aridity_score": 0.88,
        "overall": 0.94,
    },
    {
        "site": "McMurdo Dry Valleys",
        "lat": -77.5, "lon": 162.0,
        "country": "Antarctica",
        "category": "Cold Traps / PSRs",
        "simulates": "Hyper-arid, freezing desert; buried ice deposits under regolith mirror volatile trapping in PSRs",
        "users": "NASA, NSF",
        "terrain_score": 0.85,
        "mineral_score": 0.80,
        "thermal_score": 0.97,
        "aridity_score": 0.96,
        "overall": 0.93,
    },
    {
        "site": "Lanzarote Lava Tubes",
        "lat": 29.05, "lon": -13.63,
        "country": "Spain",
        "category": "Lava Tube Habitats",
        "simulates": "Intact volcanic tube systems for GPR testing, autonomous mapping, and habitat shielding",
        "users": "ESA Pangaea-X",
        "terrain_score": 0.88,
        "mineral_score": 0.91,
        "thermal_score": 0.65,
        "aridity_score": 0.72,
        "overall": 0.90,
    },
    {
        "site": "Moses Lake Sand Dunes",
        "lat": 47.13, "lon": -119.28,
        "country": "USA",
        "category": "Regolith & Terrain",
        "simulates": "Loose granular soil mechanics mimicking lunar plains for rover mobility testing",
        "users": "NASA (VIPER rover)",
        "terrain_score": 0.94,
        "mineral_score": 0.70,
        "thermal_score": 0.55,
        "aridity_score": 0.75,
        "overall": 0.87,
    },
    {
        "site": "Mauna Kea Basalt Fields",
        "lat": 19.82, "lon": -155.47,
        "country": "USA",
        "category": "Regolith & Terrain",
        "simulates": "Lunar maria — dark basaltic lava flows, cinder cones, volcanic regolith textures",
        "users": "NASA, University of Hawaiʻi",
        "terrain_score": 0.93,
        "mineral_score": 0.89,
        "thermal_score": 0.60,
        "aridity_score": 0.68,
        "overall": 0.91,
    },
    {
        "site": "Svalbard Ice Caves",
        "lat": 78.23, "lon": 15.63,
        "country": "Norway",
        "category": "Cold Traps / PSRs",
        "simulates": "Sub-zero ice-stable environments in permanent darkness for ice prospecting",
        "users": "ESA, SINTEF",
        "terrain_score": 0.72,
        "mineral_score": 0.68,
        "thermal_score": 0.94,
        "aridity_score": 0.82,
        "overall": 0.85,
    },
]

df = pd.DataFrame(MOON_ANALOGS)

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
    projection="orthographic",
    title="Moon Analog Sites on Earth",
    color_discrete_sequence=px.colors.qualitative.Set2,
)
fig_map.update_layout(height=500, margin=dict(l=0, r=0, t=40, b=0))
st.plotly_chart(fig_map, use_container_width=True)

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
            # Radar chart for this site
            categories_radar = ["Terrain", "Mineral", "Thermal", "Aridity"]
            values = [row["terrain_score"], row["mineral_score"], row["thermal_score"], row["aridity_score"]]
            values.append(values[0])  # close the polygon
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
