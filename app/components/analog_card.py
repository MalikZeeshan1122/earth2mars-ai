"""
Earth2Mars AI - Analog Card Component
Reusable card component for displaying analog site information.
"""

import streamlit as st


def render_analog_card(
    site_name: str,
    location: str,
    category: str,
    simulates: str,
    score: float,
    users: str = "",
    lat: float = None,
    lon: float = None,
):
    """Render a styled card for an Earth analog site."""

    # Score color
    if score >= 0.90:
        score_color = "🟢"
    elif score >= 0.75:
        score_color = "🟡"
    else:
        score_color = "🔴"

    with st.container():
        st.markdown(
            f"""
            <div style="
                border: 1px solid #333;
                border-radius: 10px;
                padding: 1.2rem;
                margin-bottom: 1rem;
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            ">
                <h4 style="margin: 0;">{site_name}</h4>
                <p style="color: #aaa; margin: 0.2rem 0;">📍 {location} &nbsp; | &nbsp; 📂 {category}</p>
                <p style="margin: 0.5rem 0;">{simulates}</p>
                <p style="margin: 0.3rem 0;">
                    {score_color} <b>Similarity Score:</b> {score:.2f}
                    {"&nbsp; | &nbsp; 👥 " + users if users else ""}
                </p>
                {"<p style='color: #888; margin: 0;'>🌐 " + f"{lat:.2f}°, {lon:.2f}°" + "</p>" if lat and lon else ""}
            </div>
            """,
            unsafe_allow_html=True,
        )
