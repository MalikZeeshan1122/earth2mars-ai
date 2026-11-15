"""
Earth2Mars AI - Spectral Matcher
Computes spectral similarity between Earth satellite imagery and
Moon/Mars reference mineralogy signatures.
"""

import numpy as np
from typing import Dict, List, Tuple


# ──────────────────────────────────────────────
# Spectral Indices for Analog Matching
# ──────────────────────────────────────────────

def iron_oxide_ratio(red: np.ndarray, blue: np.ndarray) -> np.ndarray:
    """
    Iron oxide index: Red / Blue ratio.
    High values → iron-rich surfaces (Mars-like, Río Tinto analog).
    """
    return np.divide(red, blue, out=np.zeros_like(red, dtype=float), where=(blue > 0))


def clay_mineral_index(swir1: np.ndarray, swir2: np.ndarray) -> np.ndarray:
    """
    Clay mineral index: SWIR1 / SWIR2 ratio.
    Detects phyllosilicates relevant to Mars sedimentary deposits.
    """
    return np.divide(swir1, swir2, out=np.zeros_like(swir1, dtype=float), where=(swir2 > 0))


def sulfate_index(swir1: np.ndarray, nir: np.ndarray) -> np.ndarray:
    """
    Sulfate absorption index.
    Detects sulfate minerals (gypsum, jarosite) found on Mars.
    """
    denom = swir1 + nir
    return np.divide(swir1 - nir, denom, out=np.zeros_like(denom, dtype=float), where=(denom > 0))


def ndvi(nir: np.ndarray, red: np.ndarray) -> np.ndarray:
    """
    Normalized Difference Vegetation Index.
    Low/negative NDVI → barren terrain (more Mars/Moon-like).
    """
    denom = nir + red
    return np.divide(nir - red, denom, out=np.zeros_like(denom, dtype=float), where=(denom > 0))


def albedo(bands: List[np.ndarray], weights: List[float] = None) -> np.ndarray:
    """
    Broadband albedo estimate from multi-band reflectance.
    Low albedo → dark basaltic surfaces (lunar maria analog).
    """
    if weights is None:
        weights = [1.0 / len(bands)] * len(bands)
    return sum(w * b for w, b in zip(weights, bands))


# ──────────────────────────────────────────────
# Reference Vectors
# ──────────────────────────────────────────────

# Normalized reference spectral signatures for Moon and Mars surfaces
MOON_REFERENCE = {
    "lunar_maria": {
        "iron_oxide": 0.72,
        "clay": 0.15,
        "sulfate": 0.08,
        "ndvi": -0.05,
        "albedo": 0.12,
    },
    "lunar_highland": {
        "iron_oxide": 0.35,
        "clay": 0.22,
        "sulfate": 0.10,
        "ndvi": -0.03,
        "albedo": 0.25,
    },
    "south_pole_psr": {
        "iron_oxide": 0.40,
        "clay": 0.18,
        "sulfate": 0.12,
        "ndvi": -0.08,
        "albedo": 0.08,
    },
}

MARS_REFERENCE = {
    "meridiani_planum": {
        "iron_oxide": 0.85,
        "clay": 0.30,
        "sulfate": 0.65,
        "ndvi": -0.10,
        "albedo": 0.18,
    },
    "tharsis_basalt": {
        "iron_oxide": 0.68,
        "clay": 0.12,
        "sulfate": 0.15,
        "ndvi": -0.08,
        "albedo": 0.14,
    },
    "polar_ice_cap": {
        "iron_oxide": 0.20,
        "clay": 0.10,
        "sulfate": 0.08,
        "ndvi": -0.12,
        "albedo": 0.65,
    },
    "gusev_crater": {
        "iron_oxide": 0.75,
        "clay": 0.45,
        "sulfate": 0.35,
        "ndvi": -0.09,
        "albedo": 0.20,
    },
}


# ──────────────────────────────────────────────
# Similarity Computation
# ──────────────────────────────────────────────

def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """Compute cosine similarity between two feature vectors."""
    dot = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot / (norm_a * norm_b))


def spectral_angle_mapper(vec_earth: np.ndarray, vec_ref: np.ndarray) -> float:
    """
    Spectral Angle Mapper (SAM) — NASA JPL & USGS planetary standard.
    Treats spectra as vectors in an n-dimensional space and calculates
    the spectral angle (in radians) between them:
        alpha = arccos( (A . B) / (||A|| * ||B||) )
    Smaller angle = higher similarity.
    Returns: normalized similarity score in [0, 1] where 1.0 is a perfect match.
    """
    dot = np.dot(vec_earth, vec_ref)
    norm_e = np.linalg.norm(vec_earth)
    norm_r = np.linalg.norm(vec_ref)
    if norm_e == 0 or norm_r == 0:
        return 0.0
    cos_theta = np.clip(dot / (norm_e * norm_r), -1.0, 1.0)
    angle_rad = np.arccos(cos_theta)
    # Map [0, pi/2] radians to [1.0, 0.0] similarity
    return float(max(0.0, 1.0 - (angle_rad / (np.pi / 2.0))))


def spectral_information_divergence(vec_earth: np.ndarray, vec_ref: np.ndarray) -> float:
    """
    Spectral Information Divergence (SID) — Information-theoretic measure
    based on Kullback-Leibler divergence between normalized probability distributions
    of two spectra. Widely used for discriminating subtle mineral absorption bands.
    Returns: similarity score in [0, 1].
    """
    p = vec_earth / (np.sum(vec_earth) + 1e-12)
    q = vec_ref / (np.sum(vec_ref) + 1e-12)
    # Symmetrical KL divergence
    kl_pq = np.sum(np.where((p > 0) & (q > 0), p * np.log((p + 1e-12) / (q + 1e-12)), 0.0))
    kl_qp = np.sum(np.where((q > 0) & (p > 0), q * np.log((q + 1e-12) / (p + 1e-12)), 0.0))
    sid = float(kl_pq + kl_qp)
    # Exponential decay mapping divergence to [0, 1]
    return float(np.exp(-2.0 * sid))


def spectral_similarity(
    earth_features: Dict[str, float],
    reference: Dict[str, float],
    method: str = "sam",
) -> float:
    """
    Compute spectral similarity between an Earth site's spectral features
    and a Moon/Mars reference signature using NASA-grade metrics.

    Methods:
        - "sam": Spectral Angle Mapper (default, angle in radians)
        - "sid": Spectral Information Divergence (information theory)
        - "hybrid": Joint SAM + SID weighted combination
        - "cosine": Standard cosine similarity

    Returns: similarity score in [0, 1]
    """
    keys = sorted(set(earth_features.keys()) & set(reference.keys()))
    if not keys:
        return 0.0

    vec_earth = np.array([earth_features[k] for k in keys], dtype=float)
    vec_ref = np.array([reference[k] for k in keys], dtype=float)

    if method == "sam":
        return spectral_angle_mapper(vec_earth, vec_ref)
    elif method == "sid":
        return spectral_information_divergence(vec_earth, vec_ref)
    elif method == "hybrid":
        sam_score = spectral_angle_mapper(vec_earth, vec_ref)
        sid_score = spectral_information_divergence(vec_earth, vec_ref)
        return float(0.6 * sam_score + 0.4 * sid_score)
    else:
        cos_sim = cosine_similarity(vec_earth, vec_ref)
        return float((cos_sim + 1.0) / 2.0)


def match_best_reference(
    earth_features: Dict[str, float],
    target_body: str = "mars",
) -> Tuple[str, float]:
    """
    Find the best-matching reference surface type for an Earth location.

    Returns: (reference_name, similarity_score)
    """
    references = MARS_REFERENCE if target_body.lower() == "mars" else MOON_REFERENCE

    best_name = ""
    best_score = -1.0

    for name, ref_vector in references.items():
        score = spectral_similarity(earth_features, ref_vector)
        if score > best_score:
            best_score = score
            best_name = name

    return best_name, best_score
