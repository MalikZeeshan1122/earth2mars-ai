"""
Earth2Mars AI - Expedition Planner & Mission Dossier Generator
Plan astronaut training field campaigns, hardware deployments, and export executive dossiers.
"""

import sys
import os

# Ensure repository root is on sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
import json
from pipeline.mission_dossier import generate_mission_dossier

st.set_page_config(
    page_title="Expedition Planner | Earth2Mars AI",
    page_icon="📋",
    layout="wide",
)

st.title("📋 Planetary Expedition Planner & Mission Dossier Generator")
st.markdown(
    "Generate executive **NASA Exploration Systems Development Mission Directorate (ESDMD)**-style field briefs. "
    "Select an analog testbed, configure crew parameters, and export mission deployment dossiers."
)

# Load catalog
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "analogs", "known_analogs.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    analogs = json.load(f)

site_dict = {item["site"]: item for item in analogs}
site_names = list(site_dict.keys())

col_sel, col_crew = st.columns([2, 1])
with col_sel:
    selected_site_name = st.selectbox("Select Target Analog Testbed", site_names, index=0)
with col_crew:
    crew_name = st.text_input("Expedition Crew Unit / Mission Tag", "Artemis Analog Crew Alpha")

site_info = site_dict[selected_site_name]

# Quick Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("Site Location", f"{site_info['country']}")
m2.metric("Coordinates", f"{site_info['lat']:.2f}°, {site_info['lon']:.2f}°")
m3.metric("Fidelity Score", f"{site_info['overall_score'] * 100:.1f}%")
m4.metric("Target Destination", ", ".join(site_info["target_bodies"]).title())

st.divider()

# Generate Dossier
dossier_text = generate_mission_dossier(site_info, crew_name)

col_view, col_dl = st.columns([3, 1])
with col_view:
    st.markdown("### 📄 Generated Expedition Dossier Preview")
with col_dl:
    st.download_button(
        label="📥 Download Official Dossier (.md)",
        data=dossier_text,
        file_name=f"NASA_Expedition_Dossier_{selected_site_name.replace(' ', '_').replace(',', '')}.md",
        mime="text/markdown",
    )

st.markdown(
    f"""
    <div style="background-color: #0d1527; border: 1px solid #1e293b; border-radius: 8px; padding: 1.5rem; font-family: monospace;">
        {dossier_text.replace(chr(10), '<br>')}
    </div>
    """,
    unsafe_allow_html=True,
)
