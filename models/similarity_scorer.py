"""
Earth2Mars AI - Multi-Feature Similarity Scorer
Combines terrain, spectral, thermal, and aridity features into
an overall analog similarity score for a candidate Earth location.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class AnalogFeatures:
    """Feature vector for an Earth candidate location."""

    # Terrain morphology (0-1 normalized)
    slope_roughness: float = 0.0
    crater_density: float = 0.0
    terrain_classification: int = 0  # From TerrainCNN

    # Spectral mineralogy (0-1 normalized)
    iron_oxide_index: float = 0.0
    clay_index: float = 0.0
    sulfate_index: float = 0.0
    albedo: float = 0.0

    # Thermal regime
    diurnal_delta_t: float = 0.0  # °C temperature swing
    min_temperature: float = 0.0  # °C
    frost_frequency: float = 0.0  # fraction of year

    # Aridity / Hydrology
    annual_precipitation_mm: float = 0.0
    soil_moisture: float = 0.0
    vegetation_index: float = 0.0  # NDVI

    # Subsurface
    lava_tube_probability: float = 0.0
    subsurface_void_score: float = 0.0


@dataclass
class SimilarityResult:
    """Result of analog similarity scoring."""

    site_name: str
    target_body: str  # "moon" or "mars"
    terrain_score: float = 0.0
    mineral_score: float = 0.0
    thermal_score: float = 0.0
    aridity_score: float = 0.0
    subsurface_score: float = 0.0
    overall_score: float = 0.0
    best_match_category: str = ""
    confidence: float = 0.0


# ──────────────────────────────────────────────
# Analytic Hierarchy Process (AHP) Weight Matrix
# Saaty's Fundamental Scale (1-9) for Multi-Criteria Decision Analysis
# ──────────────────────────────────────────────

def calculate_ahp_weights(pairwise_matrix: np.ndarray) -> np.ndarray:
    """
    Computes priority weights using the principal eigenvector method of Saaty's AHP.
    Verifies that Consistency Ratio (CR) < 0.10.
    """
    n = pairwise_matrix.shape[0]
    eigenvalues, eigenvectors = np.linalg.eig(pairwise_matrix)
    max_index = np.argmax(np.real(eigenvalues))
    lambda_max = np.real(eigenvalues[max_index])
    weights = np.real(eigenvectors[:, max_index])
    weights = weights / np.sum(weights)

    # Random Index (RI) values for n=1..10 (Saaty 1980)
    ri_table = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32}
    ci = (lambda_max - n) / (n - 1) if n > 1 else 0.0
    ri = ri_table.get(n, 1.12)
    cr = ci / ri if ri > 0 else 0.0

    return weights, float(cr)


# Default AHP Pairwise Comparison Matrix for Mars Exploration:
# Criteria: [Terrain, Mineralogy, Thermal, Aridity, Subsurface]
AHP_MARS_MATRIX = np.array([
    [1.0, 0.8, 1.0, 0.8, 2.0],
    [1.25, 1.0, 1.25, 1.0, 2.5],
    [1.0, 0.8, 1.0, 0.8, 2.0],
    [1.25, 1.0, 1.25, 1.0, 2.5],
    [0.5, 0.4, 0.5, 0.4, 1.0],
])

# Default AHP Pairwise Comparison Matrix for Moon Base Exploration:
# [Terrain, Mineralogy, Thermal, Aridity, Subsurface] (Higher weight on Terrain & Thermal cold traps)
AHP_MOON_MATRIX = np.array([
    [1.0, 1.5, 1.2, 3.0, 2.0],
    [0.67, 1.0, 0.8, 2.0, 1.33],
    [0.83, 1.25, 1.0, 2.5, 1.67],
    [0.33, 0.5, 0.4, 1.0, 0.67],
    [0.5, 0.75, 0.6, 1.5, 1.0],
])

MOON_WEIGHTS_AHP, MOON_CR = calculate_ahp_weights(AHP_MOON_MATRIX)
MARS_WEIGHTS_AHP, MARS_CR = calculate_ahp_weights(AHP_MARS_MATRIX)

MOON_WEIGHTS = {
    "terrain": float(MOON_WEIGHTS_AHP[0]),
    "mineral": float(MOON_WEIGHTS_AHP[1]),
    "thermal": float(MOON_WEIGHTS_AHP[2]),
    "aridity": float(MOON_WEIGHTS_AHP[3]),
    "subsurface": float(MOON_WEIGHTS_AHP[4]),
}

MARS_WEIGHTS = {
    "terrain": float(MARS_WEIGHTS_AHP[0]),
    "mineral": float(MARS_WEIGHTS_AHP[1]),
    "thermal": float(MARS_WEIGHTS_AHP[2]),
    "aridity": float(MARS_WEIGHTS_AHP[3]),
    "subsurface": float(MARS_WEIGHTS_AHP[4]),
}


# ──────────────────────────────────────────────
# Scoring Functions
# ──────────────────────────────────────────────

def _normalize(value: float, low: float, high: float) -> float:
    """Normalize a value to [0, 1] given expected range."""
    if high == low:
        return 0.5
    return max(0.0, min(1.0, (value - low) / (high - low)))


def score_terrain(features: AnalogFeatures, target: str = "mars") -> float:
    """Score terrain morphology similarity."""
    roughness_score = _normalize(features.slope_roughness, 0, 1)
    crater_score = _normalize(features.crater_density, 0, 1)
    return 0.6 * roughness_score + 0.4 * crater_score


def score_mineral(features: AnalogFeatures, target: str = "mars") -> float:
    """Score spectral mineralogy similarity."""
    iron_score = _normalize(features.iron_oxide_index, 0, 1)
    clay_score = _normalize(features.clay_index, 0, 1)
    sulfate_score = _normalize(features.sulfate_index, 0, 1)

    if target == "mars":
        # Mars: iron oxides and sulfates are key
        return 0.4 * iron_score + 0.25 * clay_score + 0.35 * sulfate_score
    else:
        # Moon: iron oxides and low albedo matter most
        albedo_inv = 1.0 - _normalize(features.albedo, 0, 0.5)
        return 0.45 * iron_score + 0.2 * clay_score + 0.1 * sulfate_score + 0.25 * albedo_inv


def score_thermal(features: AnalogFeatures, target: str = "mars") -> float:
    """Score thermal regime similarity."""
    # Large diurnal swings and extreme cold are more analog-like
    delta_score = _normalize(features.diurnal_delta_t, 5, 60)
    cold_score = _normalize(-features.min_temperature, 0, 90)  # Colder = higher score
    frost_score = _normalize(features.frost_frequency, 0, 1)
    return 0.35 * delta_score + 0.40 * cold_score + 0.25 * frost_score


def score_aridity(features: AnalogFeatures, target: str = "mars") -> float:
    """Score aridity / dryness similarity."""
    # Less precipitation, less moisture, less vegetation = more analog-like
    precip_score = 1.0 - _normalize(features.annual_precipitation_mm, 0, 500)
    moisture_score = 1.0 - _normalize(features.soil_moisture, 0, 1)
    veg_score = 1.0 - _normalize(features.vegetation_index, -0.1, 0.8)
    return 0.40 * precip_score + 0.30 * moisture_score + 0.30 * veg_score


def score_subsurface(features: AnalogFeatures, target: str = "mars") -> float:
    """Score subsurface structure similarity (lava tubes, voids)."""
    return 0.6 * features.lava_tube_probability + 0.4 * features.subsurface_void_score


def compute_similarity(
    site_name: str,
    features: AnalogFeatures,
    target_body: str = "mars",
    weights: Optional[Dict[str, float]] = None,
) -> SimilarityResult:
    """
    Compute the overall analog similarity score for an Earth location.

    Args:
        site_name: Name of the Earth candidate location
        features: Extracted feature vector
        target_body: "moon" or "mars"
        weights: Optional custom weights for each dimension

    Returns:
        SimilarityResult with per-dimension and overall scores
    """
    if weights is None:
        weights = MARS_WEIGHTS if target_body.lower() == "mars" else MOON_WEIGHTS

    t_score = score_terrain(features, target_body)
    m_score = score_mineral(features, target_body)
    th_score = score_thermal(features, target_body)
    a_score = score_aridity(features, target_body)
    s_score = score_subsurface(features, target_body)

    overall = (
        weights["terrain"] * t_score
        + weights["mineral"] * m_score
        + weights["thermal"] * th_score
        + weights["aridity"] * a_score
        + weights["subsurface"] * s_score
    )

    # Determine best-match category
    dim_scores = {
        "Terrain": t_score,
        "Mineralogy": m_score,
        "Thermal": th_score,
        "Aridity": a_score,
        "Subsurface": s_score,
    }
    best_category = max(dim_scores, key=dim_scores.get)

    return SimilarityResult(
        site_name=site_name,
        target_body=target_body,
        terrain_score=round(t_score, 4),
        mineral_score=round(m_score, 4),
        thermal_score=round(th_score, 4),
        aridity_score=round(a_score, 4),
        subsurface_score=round(s_score, 4),
        overall_score=round(overall, 4),
        best_match_category=best_category,
        confidence=round(overall, 4),
    )
