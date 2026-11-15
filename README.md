<div align="center">

# 🌍 Earth2Mars AI

### Intelligent Earth Analog Discovery for Moon and Mars Exploration

*Discovering Earth's Next Frontier Beyond Our Planet*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-green.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red.svg)](https://streamlit.io)
[![NASA Data](https://img.shields.io/badge/NASA-Open%20Data-orange.svg)](https://data.nasa.gov)

</div>

---

## 🚀 Overview

**Earth2Mars AI** is an AI-powered planetary analog discovery platform that uses **NASA satellite data**, **geospatial analysis**, and **machine learning** to identify and rank Earth environments as analogs for future **permanent Moon bases** and **Mars exploration missions**.

No single place on Earth perfectly replicates the Moon or Mars — but by combining terrain morphology, geochemistry, climate extremes, and subsurface features, Earth2Mars AI discovers and scores locations that best approximate the conditions astronauts and engineers will face on other worlds.

---

## 🏛️ 2026 NASA Space Apps Challenge Alignment

This project is built specifically for the **[2026 NASA Space Apps Challenge: Permanent-Moon-Base-Locations-and-Mars](https://www.spaceappschallenge.org/2026/challenges/permanent-moon-base-locations-and-mars/)**.

### Space Agency Data Integration
* **NASA (USA):** Earthdata Search, Worldview (GIBS), Planetary Data System (PDS), LRO LOLA & LRO Diviner Thermal Data
* **CSA (Canada):** RADARSAT Constellation Mission (RCM), RADARSAT-1 Open Data, and Synthetic Aperture Radar (SAR) Algorithms
* **ESA (Europe):** Copernicus Data Space Ecosystem (Sentinel-1/2) & ESA Open Science Catalog
* **JAXA (Japan):** JAXA G-Portal (GSMaP Precipitation, Snow & Vegetation Indices)

---

## 🎯 Problem Statement

Space agencies (NASA, ESA, CNSA, ISRO) need terrestrial testbeds to:
- Validate **rover mobility** and **habitat construction** techniques before deploying to the Moon/Mars
- Train astronauts in **geological field operations** under analog conditions
- Test **ISRU (In-Situ Resource Utilization)** hardware for water/oxygen extraction
- Study **extremophile biology** for astrobiology mission design
- Simulate **crew psychology** under isolation and resource constraints

Currently, analog site selection relies on expert intuition and decades-old geological surveys. **Earth2Mars AI automates and scales this discovery** using satellite imagery, spectral analysis, and ML-based similarity scoring.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Earth2Mars AI Platform                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  Data Ingest  │  │  ML Engine   │  │  Viz & UI    │   │
│  │              │  │              │  │              │   │
│  │ • NASA EarthD│  │ • Feature    │  │ • Streamlit  │   │
│  │ • Landsat 8/9│  │   Extraction │  │   Dashboard  │   │
│  │ • Sentinel-2 │  │ • Similarity │  │ • 3D Globe   │   │
│  │ • MOLA/LOLA  │  │   Scoring    │  │ • Analog     │   │
│  │ • Mars Rover │  │ • CNN-based  │  │   Cards      │   │
│  │   Mineralogy │  │   Terrain    │  │ • Compare    │   │
│  │              │  │   Matching   │  │   View       │   │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘   │
│         │                 │                 │           │
│  ┌──────▼─────────────────▼─────────────────▼───────┐   │
│  │              Geospatial Data Pipeline             │   │
│  │  PostGIS • Rasterio • GeoPandas • SentinelHub    │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🌙 Moon Base Analog Categories

Earth2Mars AI identifies Earth locations matching these **lunar south pole** challenges:

### Regolith & Terrain
| Earth Analog | Location | What It Simulates |
|:---|:---|:---|
| Moses Lake Sand Dunes | Washington, USA | Loose granular soil mechanics for rover mobility |
| Mauna Kea Basalt Fields | Hawaiʻi, USA | Lunar maria — dark volcanic regolith |
| Eifel Volcanic Field | Germany | Highland regolith from maar craters |

### Impact Crater Geology
| Earth Analog | Location | What It Simulates |
|:---|:---|:---|
| Haughton Crater, Devon Island | Nunavut, Canada | 23 km impact crater in polar desert |
| Ries Crater | Bavaria, Germany | Impact melt & suevite breccia |
| Sudbury Basin | Ontario, Canada | Impact-induced hydrothermal systems |

### Cold Traps & Permanently Shadowed Regions
| Earth Analog | Location | What It Simulates |
|:---|:---|:---|
| McMurdo Dry Valleys | Antarctica | Buried ice beneath regolith in extreme cold |
| Deep Lava Tubes (Kazumura) | Hawaiʻi, USA | Perpetual darkness, frost in sunless voids |
| Svalbard Ice Caves | Norway | Sub-zero ice-stable environments |

### Lava Tube Habitats (Radiation Shielding)
| Earth Analog | Location | What It Simulates |
|:---|:---|:---|
| Lanzarote Lava Tubes | Canary Islands, Spain | Tube mapping, GPR testing, habitat shielding |
| Undara Lava Tubes | Queensland, Australia | Structural stability & microclimate isolation |
| Jeju Volcanic Tubes | South Korea | Tube morphology & collapse patterns |

---

## 🔴 Mars Analog Categories

### Arid Desert Terrain
| Earth Analog | Location | What It Simulates |
|:---|:---|:---|
| MDRS (Mars Desert Research Station) | Utah, USA | Red sandstone terrain + crew EVA simulation |
| Atacama Desert | Chile | Driest desert — UV, perchlorate soils |
| Wadi Rum | Jordan | Iron-oxide canyons like Valles Marineris |
| Dhofar Desert | Oman | Sulfate/evaporite deposits (Meridiani Planum) |

### Volcanic Basalt
| Earth Analog | Location | What It Simulates |
|:---|:---|:---|
| HI-SEAS (Mauna Loa) | Hawaiʻi, USA | Barren basalt + isolation psychology |
| Iceland Highlands (Askja) | Iceland | Active basalt fields, sinuous rilles, lava tubes |
| Craters of the Moon | Idaho, USA | Vast basaltic plains with volcanic vents |

### Polar & Cryogenic
| Earth Analog | Location | What It Simulates |
|:---|:---|:---|
| McMurdo Dry Valleys | Antarctica | Closest overall analog to Mars surface |
| Svalbard | Arctic Norway | Permafrost polygons, subsurface ice |
| Axel Heiberg Island | Nunavut, Canada | Cold saline springs (Martian RSL analog) |

### Astrobiology & Geochemistry
| Earth Analog | Location | What It Simulates |
|:---|:---|:---|
| Río Tinto | Andalusia, Spain | Acidic iron-rich water + extremophiles |
| Yellowstone Hot Springs | Wyoming, USA | Hydrothermal biosignatures |
| Pilbara Region | Western Australia | 3.5 Ga stromatolites — ancient biosignatures |
| Mono Lake | California, USA | Alkaline hypersaline paleolake analog |

### Crew Simulation Habitats
| Facility | Location | Focus |
|:---|:---|:---|
| MDRS | Utah, USA | 2-week EVA rotations, field science |
| HI-SEAS | Hawaiʻi, USA | Long-duration isolation psychology (up to 12 months) |
| CHAPEA | NASA JSC, Houston, USA | 378-day 3D-printed Mars habitat missions |
| FMARS | Devon Island, Canada | Arctic polar analog crew operations |

---

## 🔬 ML Pipeline

```
NASA Satellite Data ──► Preprocessing ──► Feature Extraction ──► Similarity Scoring ──► Ranking
     │                      │                    │                      │                  │
     ▼                      ▼                    ▼                      ▼                  ▼
  Landsat/         Atmospheric          Terrain: slope,         Cosine similarity    Top-N analog
  Sentinel-2       correction,          roughness, albedo       against Moon/Mars    sites with
  multispectral    cloud masking,       Spectral: mineral       reference vectors    confidence
  imagery          co-registration      indices (iron oxide,                         scores
                                        clay, sulfate)
                                        Thermal: diurnal
                                        temperature range
                                        Subsurface: GPR
                                        void detection
```

### Key Features Extracted
| Feature Category | Parameters | Moon/Mars Relevance |
|:---|:---|:---|
| **Terrain Morphology** | Slope, roughness, TPI, curvature, crater density | Surface traversability, landing site safety |
| **Spectral Mineralogy** | Iron oxide ratio, clay index, sulfate index, albedo | Regolith composition matching |
| **Thermal Regime** | Diurnal ΔT, min/max temperature, frost frequency | Cold-trap identification, habitat thermal design |
| **Aridity / Hydrology** | Precipitation, humidity, soil moisture, drainage density | Water ice prospecting, ISRU feasibility |
| **Subsurface Structure** | GPR reflections, gravity anomalies, cave/tube detection | Lava tube habitat discovery |

---

## 🛠️ Tech Stack

| Layer | Technologies |
|:---|:---|
| **Language** | Python 3.10+ |
| **ML / Deep Learning** | scikit-learn, PyTorch, TensorFlow |
| **Geospatial** | Rasterio, GeoPandas, GDAL, Shapely, Folium |
| **Satellite Data** | Google Earth Engine, SentinelHub, NASA EarthData |
| **Visualization** | Streamlit, Plotly, Deck.gl, PyVista |
| **Database** | PostgreSQL + PostGIS |
| **Deployment** | Docker, Streamlit Cloud |

---

## 📁 Project Structure

```
earth2mars-ai/
├── app/
│   ├── streamlit_app.py          # Main Streamlit dashboard
│   ├── pages/
│   │   ├── live_maps.py          # Interactive Earth, Moon & Mars 2D/3D maps
│   │   ├── advanced_discovery.py # AI sandbox, radiation physics & ISRU simulator
│   │   ├── moon_analogs.py       # Moon analog explorer
│   │   ├── mars_analogs.py       # Mars analog explorer
│   │   └── compare.py            # Side-by-side comparison view
│   └── components/
│       ├── analog_card.py        # Analog site info cards
│       └── similarity_chart.py   # Radar/spider charts
├── data/
│   ├── raw/                      # Raw satellite imagery
│   ├── processed/                # Preprocessed features
│   ├── analogs/                  # Known analog site database
│   └── reference/                # Moon/Mars reference vectors
├── models/
│   ├── terrain_cnn.py            # CNN for terrain classification
│   ├── spectral_matcher.py       # Spectral similarity engine
│   ├── similarity_scorer.py      # Multi-feature scoring pipeline
│   └── trained/                  # Saved model weights
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_analog_discovery.ipynb
├── pipeline/
│   ├── ingest.py                 # Satellite data download
│   ├── preprocess.py             # Atmospheric correction, tiling
│   ├── extract_features.py       # Feature extraction pipeline
│   └── score.py                  # Similarity scoring
├── tests/
│   └── ...
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
└── Dockerfile
```

---

## ⚡ Quick Start

```bash
# Clone the repository
git clone https://github.com/MalikZeeshan1122/earth2mars-ai.git
cd earth2mars-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app/streamlit_app.py
```

---

## 🗺️ Roadmap

- [x] Research and catalog 30+ known Earth analog sites
- [ ] Build satellite data ingestion pipeline (Landsat, Sentinel-2)
- [ ] Implement terrain feature extraction module
- [ ] Train CNN terrain classifier on labeled analog sites
- [ ] Build spectral mineralogy matching engine
- [ ] Develop multi-feature similarity scoring algorithm
- [ ] Create Streamlit dashboard with interactive globe
- [ ] Validate discovered analogs against NASA/ESA field campaigns
- [ ] Add ISRU feasibility scoring layer
- [ ] Publish results and open-source trained models

---

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **NASA** — Open satellite data (Landsat, MOLA, LRO)
- **ESA** — Sentinel-2 imagery and Pangaea analog training program
- **Mars Society** — MDRS and FMARS crew simulation data
- **NASA Space Apps Challenge** — Inspiration and community

---

<div align="center">

**Built for the future of space exploration 🚀**

*Earth2Mars AI — Discovering Earth's Next Frontier Beyond Our Planet*

</div>
