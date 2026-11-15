"""
Earth2Mars AI - Streamlit Dashboard
Main entry point for the interactive Earth analog discovery platform.
"""

import sys
import os

# Ensure repository root is on sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
import pandas as pd
import plotly.express as px
import json

# ──────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Earth2Mars AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Earth2Mars AI — Intelligent Earth Analog Discovery for Moon and Mars Exploration",
    },
)

# ──────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/globe-earth.png", width=80)
    st.title("Earth2Mars AI")
    st.caption("Discovering Earth's Next Frontier Beyond Our Planet")
    st.divider()

    target = st.radio(
        "🎯 Select Target Body",
        ["All Planetary Targets", "🌙 Moon (South Pole)", "🔴 Mars"],
        index=0,
    )

    st.divider()
    analog_category = st.selectbox(
        "📂 Analog Category",
        [
            "All Categories",
            "Regolith & Terrain",
            "Impact Craters",
            "Cold Traps / PSRs",
            "Lava Tube Habitats",
            "Arid Desert Terrain",
            "Volcanic Basalt",
            "Polar / Cryogenic",
            "Astrobiology",
            "Crew Simulation",
        ],
    )

    st.divider()
    st.markdown("**🔬 Similarity Threshold**")
    threshold = st.slider("Minimum score", 0.5, 1.0, 0.75, 0.02)

    st.divider()
    st.markdown("### 🪐 Quick Navigation")
    st.page_link("pages/live_maps.py", label="🪐 Live Earth, Moon & Mars Maps", icon="🗺️")
    st.page_link("pages/astroscout_ai.py", label="🤖 AstroScout AI Copilot", icon="💬")
    st.page_link("pages/advanced_discovery.py", label="⚡ Advanced AI Discovery & Physics", icon="🔬")
    st.page_link("pages/expedition_planner.py", label="📋 Mission Dossier Generator", icon="📄")
    st.page_link("pages/moon_analogs.py", label="🌙 Moon Base Analogs", icon="🌌")
    st.page_link("pages/mars_analogs.py", label="🔴 Mars Analogs", icon="🚀")
    st.page_link("pages/compare.py", label="⚖️ Head-to-Head Comparison", icon="📊")

# ──────────────────────────────────────────────
# Main Header
# ──────────────────────────────────────────────
st.title("🌍 Earth2Mars AI")
st.subheader("Intelligent Earth Analog Discovery for Moon & Mars Exploration")
st.markdown(
    """
    **Earth2Mars AI** uses NASA satellite data, geospatial analysis, and machine learning
    to identify and rank Earth locations that analog conditions for permanent **Moon bases**
    (South Pole, permanently shadowed craters, lava tubes) and **Mars human settlement**.
    """
)

# ──────────────────────────────────────────────
# Metrics Row
# ──────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("🌍 Catalogued Analogs", "19 Sites", help="Verified natural & simulated testbeds")
col2.metric("🌙 Moon Base Targets", "7 Locations", help="Shackleton, Malapert, Marius Hills, etc.")
col3.metric("🔴 Mars Mission Targets", "8 Locations", help="Jezero, Arcadia, Gale, Valles Marineris")
col4.metric("🛰️ Data Feeds", "6 Sources", help="Landsat, Sentinel-2, MOLA, LOLA, NASA Trek")

st.divider()

# ──────────────────────────────────────────────
# Load Verified Database
# ──────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "analogs", "known_analogs.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    analog_records = json.load(f)

df = pd.DataFrame(analog_records)

# Filter by target
if "Moon" in target:
    df = df[df["target_bodies"].apply(lambda tb: "moon" in tb)]
elif "Mars" in target:
    df = df[df["target_bodies"].apply(lambda tb: "mars" in tb)]

# Filter by category
if analog_category != "All Categories":
    df = df[df["categories"].apply(lambda cats: analog_category in cats)]

# Filter by threshold
df = df[df["overall_score"] >= threshold]

# ──────────────────────────────────────────────
# Live Interactive Map Section
# ──────────────────────────────────────────────
st.markdown(f"### 🗺️ Live Earth Analog Map ({len(df)} matching sites)")

if not df.empty:
    fig_map = px.scatter_geo(
        df,
        lat="lat",
        lon="lon",
        hover_name="site",
        hover_data={
            "country": True,
            "overall_score": ":.2f",
            "lat": ":.2f",
            "lon": ":.2f",
        },
        color="overall_score",
        size="overall_score",
        size_max=16,
        color_continuous_scale="Turbo",
        projection="natural earth",
        title="Live Terrestrial Analog Distribution",
    )
    fig_map.update_layout(
        height=480,
        margin=dict(l=0, r=0, t=30, b=0),
        geo=dict(
            showland=True,
            landcolor="#1e293b",
            showocean=True,
            oceancolor="#0f172a",
            showcoastlines=True,
            coastlinecolor="#0ea5e9",
            showcountries=True,
            countrycolor="#475569",
            bgcolor="rgba(0,0,0,0)",
        ),
        coloraxis_colorbar=dict(title="Similarity"),
    )
    st.plotly_chart(fig_map, width="stretch")
else:
    st.warning("No analog sites match your selected filters. Try lowering the similarity threshold.")

st.divider()

# ──────────────────────────────────────────────
# Analog Data Table
# ──────────────────────────────────────────────
st.markdown(f"### 📍 Analog Site Details ({len(df)} sites)")

if not df.empty:
    df_display = df[[
        "site", "country", "categories", "target_bodies", "overall_score",
        "terrain_score", "mineral_score", "thermal_score", "aridity_score", "simulates"
    ]].copy()
    df_display["categories"] = df_display["categories"].apply(lambda x: ", ".join(x))
    df_display["target_bodies"] = df_display["target_bodies"].apply(lambda x: ", ".join(x).title())

    st.dataframe(
        df_display.rename(columns={
            "site": "Site Name",
            "country": "Country",
            "categories": "Categories",
            "target_bodies": "Target",
            "overall_score": "Score",
            "terrain_score": "Terrain",
            "mineral_score": "Mineral",
            "thermal_score": "Thermal",
            "aridity_score": "Aridity",
            "simulates": "What It Simulates",
        }).style.background_gradient(subset=["Score"], cmap="RdYlGn", vmin=0.75, vmax=1.0),
        width="stretch",
        hide_index=True,
    )

st.divider()

# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.markdown(
    """
    <div style="text-align: center; color: gray; padding: 2rem 0;">
        <b>Earth2Mars AI</b> — Discovering Earth's Next Frontier Beyond Our Planet<br>
        Built for the future of space exploration 🚀
    </div>
    """,
    unsafe_allow_html=True,
)
