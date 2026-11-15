"""
Earth2Mars AI - Advanced Planetary Discovery & Simulation Suite
Cutting-edge AI discovery sandbox, radiation shielding modeler,
ISRU resource yield simulator, and orbital trajectory calculator.
"""

import sys
import os

# Ensure repository root is on sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from models.similarity_scorer import (
    AnalogFeatures,
    compute_similarity,
    MOON_WEIGHTS,
    MARS_WEIGHTS,
)
from models.spectral_matcher import match_best_reference

st.set_page_config(
    page_title="Advanced AI Discovery | Earth2Mars AI",
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ Advanced Planetary Discovery & Simulation Suite")
st.markdown(
    "Next-generation AI modeling tools for **planetary analog discovery**, **radiation shielding physics**, "
    "**ISRU resource extraction economics**, and **geospatial feature matching**."
)

tab_sandbox, tab_rad, tab_isru, tab_arcs = st.tabs([
    "🧠 AI Analog Discovery Sandbox",
    "🛡️ Radiation Shielding & Lava Tube Physics",
    "💧 ISRU Water Ice & Oxygen Yield Simulator",
    "🌐 Multi-Planetary Teleportation Arcs",
])

# ====================================================================
# TAB 1: AI ANALOG DISCOVERY SANDBOX
# ====================================================================
with tab_sandbox:
    st.subheader("🧠 Live AI Analog Discovery Sandbox")
    st.markdown(
        "Simulate an unmapped terrestrial region or enter custom environmental parameters to predict "
        "its planetary analog classification and similarity scores in real-time using our multi-modal AI engine."
    )

    col_presets, col_target = st.columns([2, 1])
    with col_presets:
        preset_choice = st.selectbox(
            "Load Candidate Earth Hotspot Preset or Custom",
            [
                "Custom Coordinates / Manual Input",
                "Altiplano High Plateau (Bolivia / Chile) - Extreme UV & High Altitude",
                "Afar Depression / Dallol (Ethiopia) - Hydrothermal Acidic Brines",
                "Salar de Uyuni (Bolivia) - Evaporite Salt Flat / Martian Paleolake",
                "Richat Structure (Mauritania) - Circular Dome / Impact Morphology",
                "Dry Valleys Subglacial Lake (Antarctica) - Cryptic Subsurface Biosignatures",
            ],
        )
    with col_target:
        eval_target = st.radio("Evaluate Against Target Body", ["Mars", "Moon"], horizontal=True)

    # Populate defaults based on preset
    presets_data = {
        "Altiplano High Plateau (Bolivia / Chile) - Extreme UV & High Altitude": {
            "slope": 0.65, "crater": 0.20, "iron": 0.70, "clay": 0.40, "sulfate": 0.50,
            "albedo": 0.28, "delta_t": 35.0, "min_t": -20.0, "frost": 0.60,
            "precip": 120.0, "moisture": 0.15, "ndvi": 0.05, "tube": 0.30,
        },
        "Afar Depression / Dallol (Ethiopia) - Hydrothermal Acidic Brines": {
            "slope": 0.40, "crater": 0.10, "iron": 0.90, "clay": 0.30, "sulfate": 0.95,
            "albedo": 0.35, "delta_t": 25.0, "min_t": 22.0, "frost": 0.0,
            "precip": 80.0, "moisture": 0.08, "ndvi": -0.05, "tube": 0.10,
        },
        "Salar de Uyuni (Bolivia) - Evaporite Salt Flat / Martian Paleolake": {
            "slope": 0.05, "crater": 0.05, "iron": 0.30, "clay": 0.55, "sulfate": 0.85,
            "albedo": 0.75, "delta_t": 30.0, "min_t": -15.0, "frost": 0.45,
            "precip": 150.0, "moisture": 0.10, "ndvi": -0.08, "tube": 0.05,
        },
        "Richat Structure (Mauritania) - Circular Dome / Impact Morphology": {
            "slope": 0.80, "crater": 0.85, "iron": 0.75, "clay": 0.25, "sulfate": 0.20,
            "albedo": 0.32, "delta_t": 30.0, "min_t": 10.0, "frost": 0.0,
            "precip": 50.0, "moisture": 0.03, "ndvi": -0.05, "tube": 0.20,
        },
        "Dry Valleys Subglacial Lake (Antarctica) - Cryptic Subsurface Biosignatures": {
            "slope": 0.75, "crater": 0.40, "iron": 0.55, "clay": 0.20, "sulfate": 0.40,
            "albedo": 0.18, "delta_t": 48.0, "min_t": -58.0, "frost": 0.95,
            "precip": 15.0, "moisture": 0.01, "ndvi": -0.10, "tube": 0.65,
        },
    }

    default_vals = presets_data.get(preset_choice, {
        "slope": 0.60, "crater": 0.30, "iron": 0.65, "clay": 0.30, "sulfate": 0.40,
        "albedo": 0.22, "delta_t": 30.0, "min_t": -10.0, "frost": 0.40,
        "precip": 100.0, "moisture": 0.10, "ndvi": 0.02, "tube": 0.20,
    })

    st.markdown("#### 🎛️ Multi-Modal Environmental Feature Inputs")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("**🏔️ Terrain & Morphology**")
        in_slope = st.slider("Slope Roughness", 0.0, 1.0, float(default_vals["slope"]), 0.05)
        in_crater = st.slider("Crater / Depression Density", 0.0, 1.0, float(default_vals["crater"]), 0.05)
        in_tube = st.slider("Lava Tube Probability", 0.0, 1.0, float(default_vals["tube"]), 0.05)

    with col2:
        st.markdown("**🧪 Spectral Mineralogy**")
        in_iron = st.slider("Iron Oxide Index (Red/Blue)", 0.0, 1.0, float(default_vals["iron"]), 0.05)
        in_clay = st.slider("Clay / Phyllosilicate Index", 0.0, 1.0, float(default_vals["clay"]), 0.05)
        in_sulfate = st.slider("Sulfate Mineral Index", 0.0, 1.0, float(default_vals["sulfate"]), 0.05)
        in_albedo = st.slider("Surface Albedo", 0.0, 1.0, float(default_vals["albedo"]), 0.05)

    with col3:
        st.markdown("**🌡️ Thermal Regime**")
        in_delta_t = st.slider("Diurnal ΔT (°C)", 5.0, 60.0, float(default_vals["delta_t"]), 1.0)
        in_min_t = st.slider("Annual Minimum Temp (°C)", -90.0, 35.0, float(default_vals["min_t"]), 1.0)
        in_frost = st.slider("Frost Frequency Fraction", 0.0, 1.0, float(default_vals["frost"]), 0.05)

    with col4:
        st.markdown("**🏜️ Aridity & Hydrology**")
        in_precip = st.slider("Annual Precipitation (mm)", 0.0, 600.0, float(default_vals["precip"]), 10.0)
        in_moisture = st.slider("Soil Moisture Content", 0.0, 1.0, float(default_vals["moisture"]), 0.02)
        in_ndvi = st.slider("Vegetation Index (NDVI)", -0.15, 0.80, float(default_vals["ndvi"]), 0.02)

    # Compute live inference
    custom_features = AnalogFeatures(
        slope_roughness=in_slope,
        crater_density=in_crater,
        iron_oxide_index=in_iron,
        clay_index=in_clay,
        sulfate_index=in_sulfate,
        albedo=in_albedo,
        diurnal_delta_t=in_delta_t,
        min_temperature=in_min_t,
        frost_frequency=in_frost,
        annual_precipitation_mm=in_precip,
        soil_moisture=in_moisture,
        vegetation_index=in_ndvi,
        lava_tube_probability=in_tube,
        subsurface_void_score=in_tube * 0.9,
    )

    sim_res = compute_similarity(
        site_name=preset_choice if preset_choice != "Custom Coordinates / Manual Input" else "Candidate Region",
        features=custom_features,
        target_body=eval_target.lower(),
    )

    spec_dict = {
        "iron_oxide": in_iron,
        "clay": in_clay,
        "sulfate": in_sulfate,
        "ndvi": in_ndvi,
        "albedo": in_albedo,
    }
    best_spec_name, best_spec_score = match_best_reference(spec_dict, eval_target.lower())

    st.divider()
    st.markdown("### 📊 AI Inference Results")

    res_col1, res_col2, res_col3, res_col4 = st.columns(4)
    res_col1.metric("Overall Similarity", f"{sim_res.overall_score * 100:.1f}%", help="Weighted multi-factor score")
    res_col2.metric("Dominant Feature", sim_res.best_match_category, help="Highest contributing dimension")
    res_col3.metric("Spectral Match", best_spec_name.replace("_", " ").title(), f"{best_spec_score * 100:.1f}%")
    res_col4.metric(
        "Candidate Quality",
        "🌟 Prime Benchmark" if sim_res.overall_score > 0.85 else ("✅ Good Analog" if sim_res.overall_score > 0.70 else "⚠️ Marginal Analog")
    )

    # Radar breakdown chart
    radar_cats = ["Terrain", "Mineralogy", "Thermal", "Aridity", "Subsurface"]
    radar_vals = [
        sim_res.terrain_score, sim_res.mineral_score, sim_res.thermal_score,
        sim_res.aridity_score, sim_res.subsurface_score
    ]
    radar_vals.append(radar_vals[0])
    radar_cats.append(radar_cats[0])

    fig_res_radar = go.Figure(data=go.Scatterpolar(
        r=radar_vals,
        theta=radar_cats,
        fill="toself",
        line=dict(color="#06b6d4" if eval_target == "Moon" else "#f97316", width=2),
        name=sim_res.site_name,
    ))
    fig_res_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1], gridcolor="#334155")),
        height=380,
        margin=dict(l=60, r=60, t=30, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_res_radar, width="stretch")

# ====================================================================
# TAB 2: RADIATION SHIELDING & LAVA TUBE PHYSICS
# ====================================================================
with tab_rad:
    st.subheader("🛡️ Subterranean Habitat & Radiation Shielding Physics")
    st.markdown(
        "Compare galactic cosmic ray (GCR) and solar particle event (SPE) biological equivalent dose rates "
        "on the surface vs. inside protective basaltic lava tubes across Earth, Moon, and Mars."
    )

    col_overburden, col_time = st.columns([1, 1])
    with col_overburden:
        regolith_thickness_m = st.slider("Basalt / Regolith Shield Thickness (meters)", 0.0, 10.0, 3.0, 0.5)
    with col_time:
        mission_duration_days = st.slider("Crew Surface Exposure Duration (days)", 30, 1000, 365, 30)

    # Physics modeling:
    # Earth surface: ~3 mSv/year (protected by 1000 g/cm² atmosphere + magnetic field)
    # Moon surface: ~380 mSv/year unshielded (zero atmosphere, zero magnetic dipole)
    # Mars surface: ~240-270 mSv/year unshielded (~20 g/cm² thin CO₂ atmosphere)
    # Basalt density ~ 2.8 g/cm³, half-value layer for GCR ~ 0.5 - 0.7 m
    attenuation = np.exp(-0.693 * (regolith_thickness_m / 0.65))

    moon_surface_rate = 380.0 # mSv/yr
    mars_surface_rate = 250.0 # mSv/yr
    earth_surface_rate = 3.0   # mSv/yr

    moon_shielded_rate = max(15.0, moon_surface_rate * attenuation)
    mars_shielded_rate = max(12.0, mars_surface_rate * attenuation)

    # Mission total dose (mSv)
    duration_yr = mission_duration_days / 365.25
    dose_earth = earth_surface_rate * duration_yr
    dose_moon_surf = moon_surface_rate * duration_yr
    dose_moon_tube = moon_shielded_rate * duration_yr
    dose_mars_surf = mars_surface_rate * duration_yr
    dose_mars_tube = mars_shielded_rate * duration_yr

    # NASA Career Limit reference: ~600 mSv (varies by age/sex, standard career risk ceiling)
    col_d1, col_d2, col_d3 = st.columns(3)
    col_d1.metric("Moon Surface Dose", f"{dose_moon_surf:.0f} mSv", f"{dose_moon_surf / 600 * 100:.1f}% NASA Career Limit", delta_color="inverse")
    col_d2.metric("Moon Lava Tube Dose", f"{dose_moon_tube:.0f} mSv", f"Saved {dose_moon_surf - dose_moon_tube:.0f} mSv", delta_color="normal")
    col_d3.metric("Protection Factor", f"{moon_surface_rate / moon_shielded_rate:.1f}x", "Regolith Attenuation")

    # Bar chart comparison
    df_rad = pd.DataFrame({
        "Environment": [
            "Earth Surface (Baseline)",
            "Moon Surface (Unshielded)",
            f"Moon Lava Tube ({regolith_thickness_m}m Roof)",
            "Mars Surface (Unshielded)",
            f"Mars Lava Tube ({regolith_thickness_m}m Roof)",
            "NASA Career Safety Limit",
        ],
        "Dose_mSv": [dose_earth, dose_moon_surf, dose_moon_tube, dose_mars_surf, dose_mars_tube, 600.0],
        "Category": ["Earth", "Moon Surface", "Moon Subterranean", "Mars Surface", "Mars Subterranean", "Safety Benchmark"],
    })

    fig_rad = px.bar(
        df_rad,
        x="Environment",
        y="Dose_mSv",
        color="Category",
        text_auto=".0f",
        title=f"Cumulative Ionizing Radiation Exposure ({mission_duration_days} Days Mission)",
        labels={"Dose_mSv": "Cumulative Dose (mSv)", "Environment": ""},
        color_discrete_map={
            "Earth": "#10b981",
            "Moon Surface": "#ef4444",
            "Moon Subterranean": "#3b82f6",
            "Mars Surface": "#f97316",
            "Mars Subterranean": "#8b5cf6",
            "Safety Benchmark": "#eab308",
        },
    )
    fig_rad.add_hline(y=600, line_dash="dash", line_color="gold", annotation_text="NASA 600 mSv Career Ceiling")
    fig_rad.update_layout(height=450, showlegend=False)
    st.plotly_chart(fig_rad, width="stretch")

    st.info(
        "💡 **Key Scientific Insight:** Terrestrial lava tubes in **Lanzarote (Spain)** and **Undara (Australia)** "
        "provide critical structural analogs for robotic inspection and LiDAR mapping of overhead basalt thickness "
        "to guarantee astronauts receive less than 5% of their career radiation threshold."
    )

# ====================================================================
# TAB 3: ISRU WATER ICE & OXYGEN YIELD SIMULATOR
# ====================================================================
with tab_isru:
    st.subheader("💧 In-Situ Resource Utilization (ISRU) Production Engine")
    st.markdown(
        "Calculate water ice extraction efficiency, thermal sublimation energy, and propellant/oxygen output "
        "at Lunar South Pole Permanently Shadowed Regions vs. Martian Mid-Latitude Glacial Sheets."
    )

    col_isru1, col_isru2, col_isru3 = st.columns(3)
    with col_isru1:
        isru_target = st.selectbox("Target Body & Deposit", ["Moon (Shackleton Cold Trap)", "Mars (Arcadia Glacial Ice)"])
        ice_concentration = st.slider("Regolith Ice Weight Fraction (wt %)", 1.0, 40.0, 8.0 if "Moon" in isru_target else 25.0, 1.0)
    with col_isru2:
        mining_rate_kg_hr = st.slider("Raw Excavation Rate (kg regolith / hr)", 50, 2000, 250, 50)
        thermal_reactor_eff = st.slider("Sublimation Thermal Efficiency (%)", 40, 95, 75, 5)
    with col_isru3:
        solar_power_available_kw = st.slider("Available Dedicated Surface Power (kW)", 5.0, 150.0, 30.0, 5.0)

    # Physics calculations:
    # Specific heat of water ice + latent heat of sublimation = ~2.83 MJ / kg H₂O (at cryogenic temps)
    # 2.83 MJ = 0.786 kWh per kg of pure water
    # Water yield per day (kg):
    raw_daily_kg = mining_rate_kg_hr * 24.0
    water_extracted_kg = raw_daily_kg * (ice_concentration / 100.0) * (thermal_reactor_eff / 100.0)

    # Electrolysis: 2 H2O -> 2 H2 + O2
    # 1 kg H2O produces 0.888 kg O2 and 0.112 kg H2
    # Energy to electrolyze: ~4.5 kWh / kg H2O
    o2_produced_kg = water_extracted_kg * 0.888
    h2_produced_kg = water_extracted_kg * 0.112

    thermal_power_required_kw = (water_extracted_kg / 24.0) * 0.786 / (thermal_reactor_eff / 100.0)
    electrolysis_power_kw = (water_extracted_kg / 24.0) * 4.5

    total_power_needed_kw = thermal_power_required_kw + electrolysis_power_kw

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Purified Water Yield", f"{water_extracted_kg:.1f} L / day", f"{water_extracted_kg * 365 / 1000:.1f} metric tons / yr")
    c2.metric("Oxygen (O₂) Generated", f"{o2_produced_kg:.1f} kg / day", f"Sustains {o2_produced_kg / 0.84:.0f} astronauts" if o2_produced_kg > 0 else "0")
    c3.metric("Liquid H₂ Propellant", f"{h2_produced_kg:.1f} kg / day", "Rocket Fuel")
    c4.metric(
        "Power Feasibility",
        f"{solar_power_available_kw:.1f} kW / {total_power_needed_kw:.1f} kW",
        "Power Sufficient ✅" if solar_power_available_kw >= total_power_needed_kw else "Deficit ⚠️",
        delta_color="normal" if solar_power_available_kw >= total_power_needed_kw else "inverse"
    )

    # Sensitivity chart: Daily water yield across varying ice wt %
    wt_range = np.linspace(1, 35, 30)
    yields = [raw_daily_kg * (w / 100.0) * (thermal_reactor_eff / 100.0) for w in wt_range]
    df_isru_curve = pd.DataFrame({"Ice_wt_pct": wt_range, "Water_Yield_L_day": yields})

    fig_isru = px.line(
        df_isru_curve,
        x="Ice_wt_pct",
        y="Water_Yield_L_day",
        title="Extraction Sensitivity: Daily Water Yield vs. Regolith Ice Content",
        labels={"Ice_wt_pct": "Regolith Ice Content (wt %)", "Water_Yield_L_day": "Water Output (Liters / Day)"},
        markers=True,
    )
    fig_isru.add_vline(x=ice_concentration, line_dash="dash", line_color="cyan", annotation_text=f"Selected: {ice_concentration}% wt")
    fig_isru.update_traces(line_color="#06b6d4")
    fig_isru.update_layout(height=400)
    st.plotly_chart(fig_isru, width="stretch")

# ====================================================================
# TAB 4: MULTI-PLANETARY TELEPORTATION ARCS
# ====================================================================
with tab_arcs:
    st.subheader("🌐 Planetary Teleportation Arcs (Earth ↔ Moon ↔ Mars)")
    st.markdown(
        "Interactive 3D network visualizing the direct **geological correlation vectors** "
        "linking Earth analog testbeds with their target planetary destinations."
    )

    ARC_PAIRS = [
        {"earth": "McMurdo Dry Valleys, Antarctica", "earth_lat": -77.5, "earth_lon": 162.0, "planet": "Moon - Shackleton Crater", "target_lat": -89.9, "target_lon": 0.0, "type": "Volatile Ice Cold Trap"},
        {"earth": "Lanzarote Lava Tubes, Spain", "earth_lat": 29.0, "earth_lon": -13.6, "planet": "Moon - Marius Hills Pit", "target_lat": 14.2, "target_lon": -56.7, "type": "Subsurface Lava Tube"},
        {"earth": "Mauna Kea, Hawaiʻi", "earth_lat": 19.8, "earth_lon": -155.5, "planet": "Moon - Malapert Massif", "target_lat": -84.9, "target_lon": 12.9, "type": "Basaltic Highland"},
        {"earth": "Río Tinto, Spain", "earth_lat": 37.7, "earth_lon": -6.6, "planet": "Mars - Meridiani Planum", "target_lat": 0.2, "target_lon": -2.5, "type": "Acid Sulfate Hematite"},
        {"earth": "Devon Island, Canada", "earth_lat": 75.4, "earth_lon": -89.7, "planet": "Mars - Jezero Delta", "target_lat": 18.4, "target_lon": 77.6, "type": "Impact & Cold Cryosphere"},
        {"earth": "Atacama Desert, Chile", "earth_lat": -24.5, "earth_lon": -69.3, "planet": "Mars - Gale Crater", "target_lat": -5.4, "target_lon": 137.8, "type": "Hyperarid Salts & Clay"},
        {"earth": "Svalbard, Norway", "earth_lat": 78.2, "earth_lon": 15.6, "planet": "Mars - Arcadia Planitia", "target_lat": 39.2, "target_lon": -170.3, "type": "Polygonal Permafrost Ice"},
    ]

    df_arcs = pd.DataFrame(ARC_PAIRS)

    # 3D Network diagram using Plotly
    fig_arc = go.Figure()

    # Plot Earth analog nodes
    fig_arc.add_trace(go.Scatter3d(
        x=df_arcs["earth_lon"],
        y=df_arcs["earth_lat"],
        z=[0] * len(df_arcs),
        mode="markers+text",
        text=df_arcs["earth"].apply(lambda s: s.split(",")[0]),
        textposition="top center",
        marker=dict(size=8, color="#10b981", symbol="circle"),
        name="Earth Analog Sites",
        hovertext=df_arcs["earth"],
    ))

    # Plot Extraterrestrial nodes (offset on z-axis for multi-world visualization)
    fig_arc.add_trace(go.Scatter3d(
        x=df_arcs["target_lon"],
        y=df_arcs["target_lat"],
        z=[100] * len(df_arcs),
        mode="markers+text",
        text=df_arcs["planet"],
        textposition="bottom center",
        marker=dict(size=9, color="#f97316", symbol="diamond"),
        name="Moon & Mars Targets (Layer 2)",
        hovertext=df_arcs["planet"],
    ))

    # Connect lines between Earth and Planetary twins
    for _, row in df_arcs.iterrows():
        fig_arc.add_trace(go.Scatter3d(
            x=[row["earth_lon"], row["target_lon"]],
            y=[row["earth_lat"], row["target_lat"]],
            z=[0, 100],
            mode="lines",
            line=dict(color="#38bdf8", width=3, dash="dot"),
            hoverinfo="text",
            hovertext=f"Correlation: {row['type']}<br>{row['earth']} ➔ {row['planet']}",
            showlegend=False,
        ))

    fig_arc.update_layout(
        title="3D Teleportation Arcs: Earth Testbed ↔ Moon/Mars Destination Vector",
        scene=dict(
            xaxis=dict(title="Longitude (°)", gridcolor="#1e293b", backgroundcolor="#0b1120"),
            yaxis=dict(title="Latitude (°)", gridcolor="#1e293b", backgroundcolor="#0b1120"),
            zaxis=dict(title="Planetary Layer (0=Earth, 100=Moon/Mars)", gridcolor="#1e293b", backgroundcolor="#0b1120"),
            bgcolor="#030712",
        ),
        height=620,
        margin=dict(l=0, r=0, t=30, b=0),
    )
    st.plotly_chart(fig_arc, width="stretch")

    st.dataframe(
        df_arcs[["earth", "planet", "type", "earth_lat", "earth_lon", "target_lat", "target_lon"]].rename(columns={
            "earth": "Earth Analog Base",
            "planet": "Planetary Counterpart",
            "type": "Geological Match Type",
            "earth_lat": "Earth Lat",
            "earth_lon": "Earth Lon",
            "target_lat": "Target Lat",
            "target_lon": "Target Lon",
        }),
        width="stretch",
        hide_index=True,
    )
