"""
Earth2Mars AI - Live Planetary Maps
Interactive live 2D and 3D maps of Earth, Moon, and Mars with analog site connections.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import json
import os

st.set_page_config(
    page_title="Live Maps: Earth, Moon & Mars | Earth2Mars AI",
    page_icon="🪐",
    layout="wide",
)

st.title("🪐 Live Planetary Maps: Earth • Moon • Mars")
st.markdown(
    "Explore high-resolution, interactive live maps of **Earth** (analog testbeds), "
    "**the Moon** (Artemis base candidates & lava tubes), and **Mars** (human settlement sites & rover destinations)."
)

# Load known Earth analog dataset
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "analogs", "known_analogs.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    earth_analogs = json.load(f)

df_earth = pd.DataFrame(earth_analogs)
# Flatten categories/targets for filtering
df_earth["target_str"] = df_earth["target_bodies"].apply(lambda x: ", ".join(x).title())
df_earth["category_str"] = df_earth["categories"].apply(lambda x: ", ".join(x))

# ──────────────────────────────────────────────
# Moon Feature Catalog
# ──────────────────────────────────────────────
MOON_FEATURES = [
    {
        "name": "Shackleton Crater Rim",
        "lat": -89.9,
        "lon": 0.0,
        "type": "Artemis Base Camp Prime Site",
        "significance": "Peaks of Eternal Light (~86-92% continuous sunlight); direct access to interior cold traps.",
        "earth_analog": "McMurdo Dry Valleys & Devon Island",
        "elevation_km": 1.2,
        "water_ice": "Confirmed in interior shadow",
    },
    {
        "name": "Malapert Mountain (Massif)",
        "lat": -84.9,
        "lon": 12.9,
        "type": "Communication Relay & Solar Hub",
        "significance": "5 km high plateau with continuous line-of-sight to Earth; excellent radar and solar power vantage.",
        "earth_analog": "Mauna Kea Basalt Summit",
        "elevation_km": 5.0,
        "water_ice": "Adjacent cold traps",
    },
    {
        "name": "Connecting Ridge",
        "lat": -89.4,
        "lon": 138.0,
        "type": "Surface Traverse Corridor",
        "significance": "Narrow sunlit bridge between Shackleton and de Gerlache craters for rover expeditions.",
        "earth_analog": "Moses Lake Dunes & Iceland",
        "elevation_km": 0.5,
        "water_ice": "Flanked by permanent shadows",
    },
    {
        "name": "Haworth Crater Interior",
        "lat": -87.4,
        "lon": -5.1,
        "type": "Permanently Shadowed Region (PSR)",
        "significance": "Deep volatile cold trap with surface temperatures < 40 K (-233 °C); high water-equivalent hydrogen.",
        "earth_analog": "Svalbard Ice Caves & Deep Caves",
        "elevation_km": -3.8,
        "water_ice": "Abundant surface frost",
    },
    {
        "name": "Marius Hills Lava Tube",
        "lat": 14.2,
        "lon": -56.7,
        "type": "Subsurface Habitation Site",
        "significance": "Deep volcanic skylight (pit crater) opening into an intact lava tube offering natural radiation shielding.",
        "earth_analog": "Lanzarote Lava Tubes (Spain)",
        "elevation_km": -0.1,
        "water_ice": "Thermal stability (~ -20 °C)",
    },
    {
        "name": "Mare Tranquillitatis Pit",
        "lat": 8.3,
        "lon": 33.2,
        "type": "Subsurface Cave Entrance",
        "significance": "100m deep pit confirmed by radar data to lead to an underground cave conduit; ideal permanent habitat.",
        "earth_analog": "Undara Lava Tubes (Australia)",
        "elevation_km": -0.1,
        "water_ice": "Shielded habitat environment",
    },
    {
        "name": "Apollo 11 Landing Site (Statio Tranquillitatis)",
        "lat": 0.67,
        "lon": 23.47,
        "type": "Historical Exploration Site",
        "significance": "First crewed lunar landing in basaltic mare regolith; primary reference for lunar soil mechanics.",
        "earth_analog": "Hawaiʻi Basalt Fields",
        "elevation_km": -0.5,
        "water_ice": "None (Equatorial)",
    },
]

df_moon = pd.DataFrame(MOON_FEATURES)

# ──────────────────────────────────────────────
# Mars Feature Catalog
# ──────────────────────────────────────────────
MARS_FEATURES = [
    {
        "name": "Jezero Crater Delta",
        "lat": 18.38,
        "lon": 77.58,
        "type": "River Delta & Paleolake",
        "mission": "Perseverance Rover & Ingenuity Helicopter",
        "significance": "Ancient lacustrine clay and carbonate deposits with high biosignature preservation potential.",
        "earth_analog": "Pilbara Stromatolites & Lake Salda",
        "elevation_km": -2.5,
    },
    {
        "name": "Gale Crater (Mount Sharp)",
        "lat": -5.4,
        "lon": 137.8,
        "type": "Layered Sedimentary Mountain",
        "mission": "Curiosity Rover",
        "significance": "5 km central mound showing transition from ancient wet conditions to hyper-arid modern Mars.",
        "earth_analog": "Atacama Desert & Death Valley",
        "elevation_km": -4.5,
    },
    {
        "name": "Meridiani Planum",
        "lat": 0.2,
        "lon": -2.5,
        "type": "Hematite & Sulfate Plains",
        "mission": "Opportunity Rover",
        "significance": "Acid-sulfate sedimentary rocks and iron-oxide hematite concretions ('blueberries').",
        "earth_analog": "Río Tinto (Spain)",
        "elevation_km": -1.4,
    },
    {
        "name": "Arcadia Planitia",
        "lat": 39.2,
        "lon": -170.3,
        "type": "Candidate Human Settlement Base",
        "mission": "SpaceX Starship Landing Candidate",
        "significance": "Smooth, low-elevation volcanic plain with massive subsurface water ice sheets just 1-2m below soil.",
        "earth_analog": "Svalbard & High Arctic Permafrost",
        "elevation_km": -4.0,
    },
    {
        "name": "Valles Marineris (Coprates Chasma)",
        "lat": -14.0,
        "lon": -59.2,
        "type": "Grand Canyon of Mars",
        "mission": "Orbital Remote Sensing",
        "significance": "4,000 km tectonic chasm up to 7 km deep exposing billions of years of layered Martian crust.",
        "earth_analog": "Wadi Rum (Jordan)",
        "elevation_km": -7.0,
    },
    {
        "name": "Olympus Mons Caldera",
        "lat": 18.65,
        "lon": -133.8,
        "type": "Shield Volcano & Massive Lava Tubes",
        "mission": "Global Survey",
        "significance": "Tallest volcano in the Solar System (21.9 km high) with enormous collapsed lava tubes and skylights.",
        "earth_analog": "Hawaiʻi Mauna Loa & Iceland Askja",
        "elevation_km": 21.9,
    },
    {
        "name": "Utopia Planitia",
        "lat": 46.7,
        "lon": 117.5,
        "type": "Permafrost & Subsurface Ice Reservoir",
        "mission": "Zhurong Rover & Viking 2",
        "significance": "Underground ice reservoir estimated to hold as much water as Lake Superior; polygon-patterned terrain.",
        "earth_analog": "Devon Island & Axel Heiberg Island",
        "elevation_km": -3.8,
    },
    {
        "name": "Elysium Planitia",
        "lat": 4.5,
        "lon": 135.9,
        "type": "Young Volcanic Plains",
        "mission": "InSight Lander",
        "significance": "Geologically young basalt flows; monitored for marsquakes and internal planetary heat flow.",
        "earth_analog": "Craters of the Moon (Idaho, USA)",
        "elevation_km": -2.6,
    },
]

df_mars = pd.DataFrame(MARS_FEATURES)

# ──────────────────────────────────────────────
# Interactive Tabs for Earth, Moon, Mars
# ──────────────────────────────────────────────
tab_earth, tab_moon, tab_mars = st.tabs([
    "🌍 Earth: Planetary Analog Map",
    "🌙 Moon: Permanent Base & Cold-Trap Map",
    "🔴 Mars: Settlement & Exploration Map",
])

# ==============================================================
# TAB 1: EARTH LIVE MAP
# ==============================================================
with tab_earth:
    st.subheader("🌍 Earth Analog Testbeds for Moon & Mars")
    st.markdown(
        "Interactive global map of verified terrestrial locations that simulate lunar and Martian environments. "
        "Filter by target planetary body or analog classification."
    )

    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1, 1, 1])
    with col_ctrl1:
        target_filter = st.selectbox(
            "Filter by Planetary Target",
            ["All Targets", "Moon", "Mars"],
            key="earth_target_filter",
        )
    proj_map = {
        "Natural Earth": "natural earth",
        "3D Globe (Orthographic)": "orthographic",
        "Equirectangular": "equirectangular",
        "Mercator": "mercator",
        "Robinson": "robinson",
    }
    with col_ctrl2:
        projection_label = st.selectbox(
            "Map Projection",
            list(proj_map.keys()),
            index=0,
            key="earth_proj",
        )
        selected_proj = proj_map[projection_label]
    with col_ctrl3:
        min_score = st.slider("Minimum Similarity Score", 0.70, 1.0, 0.75, 0.01, key="earth_min_score")

    # Filter data
    df_filtered_earth = df_earth[df_earth["overall_score"] >= min_score].copy()
    if target_filter == "Moon":
        df_filtered_earth = df_filtered_earth[df_filtered_earth["target_bodies"].apply(lambda t: "moon" in t)]
    elif target_filter == "Mars":
        df_filtered_earth = df_filtered_earth[df_filtered_earth["target_bodies"].apply(lambda t: "mars" in t)]

    # Plotly interactive map
    fig_earth = px.scatter_geo(
        df_filtered_earth,
        lat="lat",
        lon="lon",
        hover_name="site",
        hover_data={
            "country": True,
            "overall_score": ":.2f",
            "target_str": True,
            "category_str": True,
            "lat": ":.2f",
            "lon": ":.2f",
        },
        color="overall_score",
        size="overall_score",
        size_max=18,
        color_continuous_scale="Viridis",
        projection=selected_proj,
        title=f"Earth Analog Sites ({len(df_filtered_earth)} active sites plotted)",
    )

    fig_earth.update_layout(
        height=620,
        margin=dict(l=0, r=0, t=30, b=0),
        geo=dict(
            showland=True,
            landcolor="#1c2331",
            showocean=True,
            oceancolor="#0b111e",
            showlakes=True,
            lakecolor="#0f172a",
            showrivers=False,
            showcoastlines=True,
            coastlinecolor="#38bdf8",
            showcountries=True,
            countrycolor="#475569",
            bgcolor="rgba(0,0,0,0)",
        ),
        coloraxis_colorbar=dict(title="Similarity Score"),
    )
    st.plotly_chart(fig_earth, width="stretch")

    # Expandable table of filtered sites
    with st.expander("📋 View Earth Analog Details & Coordinates", expanded=False):
        st.dataframe(
            df_filtered_earth[[
                "site", "country", "lat", "lon", "target_str", "category_str",
                "overall_score", "terrain_score", "mineral_score", "thermal_score", "aridity_score"
            ]].rename(columns={
                "target_str": "Target Body",
                "category_str": "Categories",
                "overall_score": "Overall",
                "terrain_score": "Terrain",
                "mineral_score": "Mineral",
                "thermal_score": "Thermal",
                "aridity_score": "Aridity",
            }),
            width="stretch",
            hide_index=True,
        )

# ==============================================================
# TAB 2: MOON LIVE MAP
# ==============================================================
with tab_moon:
    st.subheader("🌙 Lunar South Pole & Permanent Base Map")
    st.markdown(
        "Mapped locations of critical candidate sites for permanent lunar settlement — "
        "including **Artemis Base Camp** candidates at the South Pole, **Peaks of Eternal Light**, "
        "**Permanently Shadowed Cold Traps (PSRs)**, and **intact lava tube shelters**."
    )

    col_m1, col_m2 = st.columns([1, 1])
    with col_m1:
        moon_view_mode = st.radio(
            "Display Mode",
            ["Interactive Lunar Coordinate Chart", "3D Lunar Polar Sphere"],
            horizontal=True,
            key="moon_view_mode",
        )

    if moon_view_mode == "Interactive Lunar Coordinate Chart":
        # 2D Lunar map
        fig_moon = px.scatter(
            df_moon,
            x="lon",
            y="lat",
            text="name",
            color="type",
            size=[14] * len(df_moon),
            hover_name="name",
            hover_data={
                "type": True,
                "elevation_km": ":.1f km",
                "earth_analog": True,
                "water_ice": True,
                "lat": ":.2f°",
                "lon": ":.2f°",
            },
            title="Lunar Base Candidates & Lava Tube Openings",
            labels={"lon": "Lunar Longitude (°)", "lat": "Lunar Latitude (°)"},
            color_discrete_sequence=px.colors.qualitative.Prism,
        )
        fig_moon.update_traces(textposition="top center", marker=dict(line=dict(width=1, color="white")))
        fig_moon.update_layout(
            height=550,
            xaxis=dict(range=[-180, 180], zeroline=True, gridcolor="#334155", title="Longitude (°E / °W)"),
            yaxis=dict(range=[-90, 90], zeroline=True, gridcolor="#334155", title="Latitude (°N / °S)"),
            plot_bgcolor="#090d16",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_moon, width="stretch")

    else:
        # 3D Orthographic projection of Lunar South Pole
        # Convert lat/lon to 3D Cartesian coordinates on unit sphere
        lat_rad = np.radians(df_moon["lat"])
        lon_rad = np.radians(df_moon["lon"])
        r = 1.0 + (df_moon["elevation_km"] * 0.02)
        x_pts = r * np.cos(lat_rad) * np.cos(lon_rad)
        y_pts = r * np.cos(lat_rad) * np.sin(lon_rad)
        z_pts = r * np.sin(lat_rad)

        # Create sphere wireframe
        phi = np.linspace(0, 2 * np.pi, 50)
        theta = np.linspace(0, np.pi, 50)
        xs = np.outer(np.cos(phi), np.sin(theta))
        ys = np.outer(np.sin(phi), np.sin(theta))
        zs = np.outer(np.ones(50), np.cos(theta))

        fig_moon_3d = go.Figure()
        # Moon sphere surface (grey regolith palette)
        fig_moon_3d.add_trace(go.Surface(
            x=xs, y=ys, z=zs,
            colorscale=[[0, "#1f2937"], [0.5, "#4b5563"], [1, "#9ca3af"]],
            showscale=False,
            opacity=0.85,
            hoverinfo="none",
        ))

        # Add site markers
        fig_moon_3d.add_trace(go.Scatter3d(
            x=x_pts,
            y=y_pts,
            z=z_pts,
            mode="markers+text",
            text=df_moon["name"],
            textposition="top center",
            textfont=dict(color="cyan", size=10),
            marker=dict(size=8, color="#f59e0b", symbol="diamond", line=dict(color="white", width=1)),
            hoverinfo="text",
            hovertext=[
                f"<b>{row['name']}</b><br>Type: {row['type']}<br>Coords: {row['lat']:.1f}°, {row['lon']:.1f}°<br>Earth Analog: {row['earth_analog']}"
                for _, row in df_moon.iterrows()
            ],
            name="Lunar Sites",
        ))

        fig_moon_3d.update_layout(
            title="3D Lunar Globe with Settlement Sites",
            scene=dict(
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=""),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=""),
                zaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=""),
                bgcolor="#030712",
                camera=dict(eye=dict(x=0, y=0, z=-2.2)), # Pointing toward South Pole
            ),
            margin=dict(l=0, r=0, t=30, b=0),
            height=600,
        )
        st.plotly_chart(fig_moon_3d, width="stretch")

    # NASA Trek Explorer integration
    with st.expander("🛰️ Open NASA Moon Trek High-Resolution Live Viewer", expanded=False):
        st.info("NASA Moon Trek provides real-time orbital imagery, 3D digital elevation models, and layer overlays from LRO & Chandrayaan.")
        st.components.v1.iframe("https://trek.nasa.gov/moon/", height=650, scrolling=True)

# ==============================================================
# TAB 3: MARS LIVE MAP
# ==============================================================
with tab_mars:
    st.subheader("🔴 Martian Settlement & Exploration Map")
    st.markdown(
        "Interactive planetary map of Mars detailing key destinations: "
        "**Jezero Crater**, **Gale Crater**, **Meridiani Planum**, and proposed human base regions like **Arcadia Planitia**."
    )

    col_mars1, col_mars2 = st.columns([1, 1])
    with col_mars1:
        mars_view_mode = st.radio(
            "Display Projection",
            ["Martian Topographic Scatter Map (MOLA Grid)", "3D Mars Globe"],
            horizontal=True,
            key="mars_view_mode",
        )

    if mars_view_mode == "Martian Topographic Scatter Map (MOLA Grid)":
        fig_mars = px.scatter(
            df_mars,
            x="lon",
            y="lat",
            text="name",
            color="type",
            size=[14] * len(df_mars),
            hover_name="name",
            hover_data={
                "type": True,
                "mission": True,
                "elevation_km": ":.1f km",
                "earth_analog": True,
                "lat": ":.2f°",
                "lon": ":.2f°",
            },
            title="Mars Exploration & Human Settlement Targets",
            labels={"lon": "Martian Longitude (°E / °W)", "lat": "Martian Latitude (°N / °S)"},
            color_discrete_sequence=px.colors.qualitative.Dark24,
        )
        fig_mars.update_traces(textposition="top center", marker=dict(line=dict(width=1, color="white")))
        fig_mars.update_layout(
            height=550,
            xaxis=dict(range=[-180, 180], zeroline=True, gridcolor="#451a03", title="Longitude (°E / °W)"),
            yaxis=dict(range=[-90, 90], zeroline=True, gridcolor="#451a03", title="Latitude (°N / °S)"),
            plot_bgcolor="#1c0a00", # Martian rust background
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_mars, width="stretch")

    else:
        # 3D Mars globe in Plotly
        lat_rad = np.radians(df_mars["lat"])
        lon_rad = np.radians(df_mars["lon"])
        r = 1.0 + (df_mars["elevation_km"] * 0.01)
        x_pts = r * np.cos(lat_rad) * np.cos(lon_rad)
        y_pts = r * np.cos(lat_rad) * np.sin(lon_rad)
        z_pts = r * np.sin(lat_rad)

        phi = np.linspace(0, 2 * np.pi, 50)
        theta = np.linspace(0, np.pi, 50)
        xs = np.outer(np.cos(phi), np.sin(theta))
        ys = np.outer(np.sin(phi), np.sin(theta))
        zs = np.outer(np.ones(50), np.cos(theta))

        fig_mars_3d = go.Figure()
        # Mars rust/iron oxide colored surface
        fig_mars_3d.add_trace(go.Surface(
            x=xs, y=ys, z=zs,
            colorscale=[[0, "#451a03"], [0.3, "#78350f"], [0.7, "#9a3412"], [1, "#ea580c"]],
            showscale=False,
            opacity=0.9,
            hoverinfo="none",
        ))

        # Add site markers
        fig_mars_3d.add_trace(go.Scatter3d(
            x=x_pts,
            y=y_pts,
            z=z_pts,
            mode="markers+text",
            text=df_mars["name"],
            textposition="top center",
            textfont=dict(color="#fed7aa", size=10),
            marker=dict(size=8, color="#38bdf8", symbol="diamond", line=dict(color="white", width=1)),
            hoverinfo="text",
            hovertext=[
                f"<b>{row['name']}</b><br>Type: {row['type']}<br>Mission: {row['mission']}<br>Earth Analog: {row['earth_analog']}"
                for _, row in df_mars.iterrows()
            ],
            name="Martian Sites",
        ))

        fig_mars_3d.update_layout(
            title="3D Martian Globe with Exploration Destinations",
            scene=dict(
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=""),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=""),
                zaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=""),
                bgcolor="#030712",
                camera=dict(eye=dict(x=1.8, y=1.2, z=0.8)),
            ),
            margin=dict(l=0, r=0, t=30, b=0),
            height=600,
        )
        st.plotly_chart(fig_mars_3d, width="stretch")

    # NASA Mars Trek Explorer integration
    with st.expander("🛰️ Open NASA Mars Trek High-Resolution Live Viewer", expanded=False):
        st.info("NASA Mars Trek provides interactive orbital navigation, MOLA elevation models, and Viking/HiRISE imagery layers.")
        st.components.v1.iframe("https://trek.nasa.gov/mars/", height=650, scrolling=True)

# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.divider()
st.markdown(
    """
    <div style="text-align: center; color: gray; padding: 1rem 0;">
        <b>Earth2Mars AI</b> — Interactive Planetary Cartography & Analog Modeling<br>
        Powered by NASA Trek, MOLA, LOLA & EarthData
    </div>
    """,
    unsafe_allow_html=True,
)
