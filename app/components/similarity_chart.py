"""
Earth2Mars AI - Similarity Chart Component
Reusable radar/spider chart for visualizing multi-dimensional similarity scores.
"""

import plotly.graph_objects as go


def create_similarity_radar(
    site_name: str,
    terrain: float,
    mineral: float,
    thermal: float,
    aridity: float,
    color: str = "#636EFA",
    height: int = 300,
) -> go.Figure:
    """Create a radar chart showing similarity scores across feature dimensions."""

    categories = ["Terrain", "Mineralogy", "Thermal", "Aridity"]
    values = [terrain, mineral, thermal, aridity]
    values.append(values[0])  # Close the polygon
    categories.append(categories[0])

    fig = go.Figure(
        data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            name=site_name,
            line=dict(color=color),
            fillcolor=color.replace(")", ", 0.3)").replace("rgb", "rgba")
            if "rgb" in color
            else None,
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], tickvals=[0.25, 0.5, 0.75, 1.0]),
        ),
        showlegend=True,
        height=height,
        margin=dict(l=60, r=60, t=30, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def create_comparison_radar(
    site_a_name: str,
    site_a_scores: dict,
    site_b_name: str,
    site_b_scores: dict,
    height: int = 400,
) -> go.Figure:
    """Create an overlay radar chart comparing two analog sites."""

    categories = ["Terrain", "Mineralogy", "Thermal", "Aridity"]
    values_a = [site_a_scores.get(c.lower(), 0) for c in categories]
    values_b = [site_b_scores.get(c.lower(), 0) for c in categories]

    # Close polygons
    values_a.append(values_a[0])
    values_b.append(values_b[0])
    categories_closed = categories + [categories[0]]

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=values_a,
            theta=categories_closed,
            fill="toself",
            name=site_a_name,
            line=dict(color="#636EFA"),
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=values_b,
            theta=categories_closed,
            fill="toself",
            name=site_b_name,
            line=dict(color="#EF553B"),
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1]),
        ),
        height=height,
        margin=dict(l=80, r=80, t=40, b=40),
    )

    return fig
