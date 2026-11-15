# 🏆 Earth2Mars AI — Official NASA Space Apps Challenge Submission

<div align="center">

# 🌍 Earth2Mars AI
### Intelligent Earth Analog Discovery for Moon and Mars Exploration
*Discovering Earth's Next Frontier Beyond Our Planet*

**Challenge Track:** Planetary Exploration / Moon to Mars Architecture  
**Target Missions:** NASA Artemis Program (Lunar South Pole Base Camp) & NASA Moon to Mars Strategy (Mars 2030+)

</div>

---

## 🚀 1. High-Impact Elevator Pitch (30 Seconds)
Before humanity journeys **384,400 km to the Moon** or **225 million km to Mars**, every life-support system, autonomous rover, and spacesuit joint must be battle-tested on Earth. Yet today, planetary analog selection relies on 50-year-old qualitative surveys. 

**Earth2Mars AI** is the world's first open-source, AI-powered planetary analog discovery engine. By synthesizing **NASA satellite imagery (HLS, Landsat 8/9, Sentinel-2)**, **Planetary Data System topography (LRO LOLA, MGS MOLA)**, and **CRISM spectral mineralogy**, our multi-modal neural network and Analytic Hierarchy Process (AHP) objectively identify, rank, and map Earth's closest twins for lunar south pole cold traps, lava tube radiation shelters, and Martian river deltas.

---

## 🎯 2. The Problem & Why It Matters
Establishing a permanent presence on the Moon and Mars presents unprecedented operational hazards:
* **The Lunar South Pole** features extreme low-angle lighting, permanently shadowed regions (PSRs) colder than Pluto (<40 K), abrasive electrostatically charged regolith, and vacuum thermal swings.
* **Mars** subjects hardware to corrosive iron-oxide dust, perchlorate oxidizers, hypobaric CO₂ atmospheres, and high-energy cosmic rays.
* **The Cost of Failure:** Sending unvalidated rovers or drilling rigs to space costs upwards of **$100,000 per kilogram**.

Space agencies (NASA, ESA, JAXA, ISRO) desperately need high-fidelity terrestrial testbeds to train astronaut crews, calibrate autonomous visual odometry, and optimize In-Situ Resource Utilization (ISRU) water ice extractors.

---

## 💡 3. The Earth2Mars AI Solution
Earth2Mars AI bridges NASA Earth Science and Deep Space Exploration through five synchronized systems:

1. **Multi-Modal AI Similarity Engine:**
   * **Spectral Angle Mapper (SAM) & Spectral Information Divergence (SID):** NASA JPL/USGS standards calculating multi-band spectral divergence between Earth terrain and extraterrestrial mineralogy.
   * **Saaty's Analytic Hierarchy Process (AHP):** Mathematically rigorous weighting of terrain roughness, spectral mineralogy, thermal cryo-dynamics, and aridity with validated consistency ratios ($CR < 0.05$).
   * **Convolutional Neural Network (TerrainCNN):** 8-class patch classifier trained on planetary surface morphology.

2. **Interactive Live Planetary Cartography:**
   * Seamless 2D and 3D WebGL globes for **Earth** (19+ catalogued testbeds), **the Moon** (Shackleton Rim, Malapert Mountain, Marius Hills lava tubes), and **Mars** (Jezero Crater, Arcadia Planitia, Gale Crater, Olympus Mons).
   * Direct embedded integration with **NASA Moon Trek** and **NASA Mars Trek**.

3. **Subterranean Radiation Shielding Simulator:**
   * Models galactic cosmic ray (GCR) and solar particle event (SPE) biological equivalent doses (mSv) through basalt regolith roofs, benchmarking safety against the **NASA 600 mSv career limit**.

4. **Cryogenic ISRU Water & Propellant Extractor:**
   * Simulates thermal sublimation power requirements (kWh/kg) and daily yield for breathable $O_2$ and liquid $H_2$ rocket propellant from polar ice deposits.

5. **AstroScout AI Copilot & Mission Dossier Generator:**
   * Natural language planetary science assistant + 1-click generator of NASA ESDMD-standard Expedition Briefs for field deployment.

---

## 🛰️ 4. NASA & Space Agency Datasets Used
| Dataset / Tool | Space Agency | Application in Earth2Mars AI |
|:---|:---|:---|
| **NASA CMR (Common Metadata Repository)** | NASA EarthData | Real-time querying of Harmonized Landsat Sentinel-2 (HLS) granules |
| **NASA GIBS (Global Imagery Browse Services)** | NASA EOSDIS | True-color and thermal satellite imagery tile layers |
| **LRO LOLA (Lunar Orbiter Laser Altimeter)** | NASA Goddard / PDS | Digital elevation models and surface roughness of lunar polar craters |
| **MGS MOLA (Mars Orbiter Laser Altimeter)** | NASA JPL / PDS | Global Martian topographic grids and elevation baselines |
| **CRISM Spectral Library** | NASA / JHUAPL | Reference absorption spectra for Martian sulfates, hematite, and clays |
| **LRO Diviner Lunar Radiometer** | NASA / UCLA | Surface kinetic temperature and cold-trap volatile stability bounds |
| **NASA Moon Trek & Mars Trek** | NASA Solar System Treks | High-resolution interactive 3D orbital GIS embedded in-app |

---

## 🏗️ 5. Technical Architecture
```
┌────────────────────────────────────────────────────────────────────────┐
│                        Earth2Mars AI Architecture                      │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  [NASA EarthData / HLS]      [LRO LOLA / MOLA PDS]    [CRISM Library]  │
│             │                          │                     │         │
│             ▼                          ▼                     ▼         │
│      [Data Ingestion]           [USGS WMS Layers]     [Ref Signatures] │
│             │                          │                     │         │
│             └──────────────────┬───────┴─────────────────────┘         │
│                                ▼                                       │
│                    [Feature Extraction Pipeline]                       │
│              • Terrain Roughness & Slope Gradient                      │
│              • SAM Spectral Angle & SID Divergence                     │
│              • Diurnal Thermal Range & Frost Frequency                 │
│              • Aridity, Soil Moisture & Inverted NDVI                  │
│                                │                                       │
│                                ▼                                       │
│                    [AHP Multi-Criteria Engine]                         │
│                    (Saaty Consistency Ratio < 0.05)                    │
│                                │                                       │
│                                ▼                                       │
│           [Streamlit Interactive Operations Dashboard]                 │
│      • Live 3D Planetary Spheres (Earth • Moon • Mars)                │
│      • AstroScout AI Planetary Copilot                                 │
│      • Radiation Shielding & Lava Tube Physics Engine                  │
│      • Cryogenic ISRU Volatile Yield Simulator                         │
│      • NASA ESDMD Field Campaign Dossier Generator                     │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🔬 6. Verified Top Analog Discoveries
* **Shackleton Crater Cold Trap (Moon) ➔ McMurdo Dry Valleys (Antarctica):** Fidelity Score **96%**. Hyper-arid cryogenic permafrost preserving ancient buried volatile ice.
* **Marius Hills & Mare Tranquillitatis Lava Tubes (Moon) ➔ Lanzarote & Undara:** Fidelity Score **90%**. Intact basaltic conduits offering natural radiation shielding.
* **Meridiani Planum Acid Sulfates (Mars) ➔ Río Tinto (Spain):** Fidelity Score **93%**. Iron-oxidizing extremophile biomes generating hematite concretions.
* **Jezero Crater Lacustrine Delta (Mars) ➔ Pilbara Region (Australia):** Fidelity Score **84%**. 3.5 Ga fossilized stromatolites directly guiding the search for Martian biosignatures.

---

## 📈 7. Scalability & Future Roadmap
* **Phase 1 (Achieved):** 19 verified global sites catalogued, SAM/SID spectral engine, Streamlit HUD, mission dossier exporter, 19 automated tests (100% pass rate).
* **Phase 2 (Next 6 Months):** Integrate real-time automated Copernicus Sentinel-2 STAC downloads and Google Earth Engine server-side tile processing.
* **Phase 3 (Artemis III / Mars 2028+):** Partner with space agencies to establish field deployment telemetry relays, syncing rover test streams directly into the Earth2Mars AI dashboard.

---

## 👥 8. Author & Acknowledgments
* **Lead Developer & Planetary AI Architect:** Muhammad Zeeshan
* **Open Source License:** MIT License
* **Repository:** [https://github.com/MalikZeeshan1122/earth2mars-ai](https://github.com/MalikZeeshan1122/earth2mars-ai)

*Developed for the NASA Space Apps Challenge.*
