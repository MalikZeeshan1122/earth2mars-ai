"""
Earth2Mars AI - AstroScout AI Assistant
Conversational planetary science reasoning engine for analog selection and mission planning.
"""

import streamlit as st
import json
import os

st.set_page_config(
    page_title="AstroScout AI Copilot | Earth2Mars AI",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AstroScout AI — Planetary Analog Intelligence Copilot")
st.markdown(
    "Ask natural-language questions about **Earth analogs**, **Artemis Lunar Base Camp locations**, "
    "**Mars landing sites**, and **optimal testing grounds for rover and ISRU hardware**."
)

# Load analog database
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "analogs", "known_analogs.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    analogs = json.load(f)

# Knowledge retrieval engine
def query_astroscout(user_prompt: str) -> str:
    prompt_lower = user_prompt.lower()

    # Rule & keyword matching on knowledge base
    if "viper" in prompt_lower or "rover mobility" in prompt_lower or "wheel" in prompt_lower:
        return (
            "🚜 **VIPER & Heavy Rover Mobility Recommendation:**\n\n"
            "The premier Earth testbed for rover mobility in loose, fine-grained regolith is **Moses Lake Sand Dunes (Washington State, USA)**. "
            "NASA used Moses Lake specifically for VIPER wheel-traction testing because the dune mechanics closely mimic the shear strength and cohesion "
            "of polar lunar regolith. For rocky, boulder-strewn traverse validation, pair this with **Haughton Crater on Devon Island**."
        )
    elif "cold trap" in prompt_lower or "shackleton" in prompt_lower or "psr" in prompt_lower or "water ice" in prompt_lower:
        return (
            "🧊 **Permanently Shadowed Region (PSR) & Cold-Trap Analogs:**\n\n"
            "For testing volatile ice prospecting at **Shackleton Crater** (temperatures < 40 K): \n"
            "1. **McMurdo Dry Valleys (Antarctica):** The closest terrestrial environment to lunar PSRs and Martian polar caps. Ancient permafrost ice is insulated beneath thin dry regolith layers.\n"
            "2. **Svalbard Ice Caves (Norway):** Year-round sub-zero ice-stable dark environments ideal for testing automated cryo-core drills."
        )
    elif "lava tube" in prompt_lower or "cave" in prompt_lower or "radiation" in prompt_lower or "subsurface" in prompt_lower:
        return (
            "🛡️ **Subterranean Lava Tube & Radiation Shielding Analogs:**\n\n"
            "To model human habitats sheltered beneath planetary basalt (such as **Marius Hills Hole on the Moon** or **Arsia Mons pits on Mars**):\n"
            "1. **Lanzarote Lava Tubes (Canary Islands, Spain):** The primary ESA Pangaea-X testbed for autonomous LiDAR mapping, GPR void detection, and subterranean habitat sealing.\n"
            "2. **Undara Lava Tubes (Queensland, Australia):** Exceptional structural stability for microclimate monitoring."
        )
    elif "jezero" in prompt_lower or "perseverance" in prompt_lower or "delta" in prompt_lower or "ancient life" in prompt_lower or "biosignature" in prompt_lower:
        return (
            "🔬 **Jezero Crater & Biosignature Analogs:**\n\n"
            "For Jezero Crater's ancient lake and river delta:\n"
            "1. **Pilbara Region (Western Australia):** Houses 3.5-billion-year-old stromatolites — the oldest fossil evidence of life on Earth. The exact mineralogical benchmark for Mars 2020 sample return.\n"
            "2. **Río Tinto (Andalusia, Spain):** Extreme acidic, iron-rich water generating jarosite and hematite deposits identical to Meridiani Planum."
        )
    elif "crew" in prompt_lower or "psychology" in prompt_lower or "isolation" in prompt_lower or "analog astronaut" in prompt_lower:
        return (
            "🧑‍🚀 **Long-Duration Crew Isolation & Human Factors:**\n\n"
            "1. **HI-SEAS (Mauna Loa, Hawaiʻi):** High-altitude volcanic isolation dedicated to NASA human behavior, food systems, and team cohesion (up to 12-month missions).\n"
            "2. **MDRS (Utah, USA):** Strict operational EVA protocols, spacesuit simulation, and pressurized habitat maintenance.\n"
            "3. **CHAPEA (NASA Johnson Space Center):** 3D-printed Mars habitat for 378-day crew health simulations."
        )
    elif "moon" in prompt_lower:
        return (
            "🌙 **Top Lunar South Pole Analog Recommendations:**\n\n"
            "• **Haughton Crater (Devon Island):** 23 km polar impact crater mirroring south pole impact morphology.\n"
            "• **Mauna Kea (Hawaiʻi):** Basaltic volcanic regolith analogous to lunar maria and dark highlands.\n"
            "• **McMurdo Dry Valleys (Antarctica):** Volatile ice cold trap preservation."
        )
    elif "mars" in prompt_lower:
        return (
            "🔴 **Top Martian Analog Recommendations:**\n\n"
            "• **Atacama Desert (Chile):** Hyper-arid, perchlorate-rich soil with Mars-grade UV surface flux.\n"
            "• **Iceland Highlands (Askja):** Active volcanic basalt, sinuous channels, and lava tubes mirroring Tharsis.\n"
            "• **Svalbard (Arctic Norway):** Polygonal patterned ground and ground-ice structures matching Arcadia Planitia."
        )
    else:
        # Default intelligent response matching highest similarity sites
        top_sites = sorted(analogs, key=lambda x: x["overall_score"], reverse=True)[:3]
        site_bullets = "\n".join([f"• **{s['site']}** ({s['country']}) — Score: {s['overall_score']*100:.1f}% ({s['simulates']})" for s in top_sites])
        return (
            f"🪐 **AstroScout AI Analysis:**\n\n"
            f"Based on your query, Earth2Mars AI recommends reviewing our highest-ranked planetary testbeds:\n\n"
            f"{site_bullets}\n\n"
            f"You can explore detailed feature breakdowns in the **Live Maps** or run custom parameters in the **AI Discovery Sandbox**."
        )

# Chat UI
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Greetings Explorer! I am **AstroScout AI**. Ask me anything about planetary analogs, Artemis Moon Base locations, Mars rover test sites, or expedition planning."}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask AstroScout AI (e.g. 'Where can I test lunar rover wheels?' or 'Best analog for Jezero Crater?')")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response = query_astroscout(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

st.divider()
st.markdown("💡 *Try asking:* `Where can I test lunar rover wheels?` | `What Earth site analogs Shackleton Crater cold traps?` | `Best place to test subterranean lava tube habitats?`")
