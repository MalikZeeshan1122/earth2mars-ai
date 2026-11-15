"""
Earth2Mars AI - Scoring Pipeline
End-to-end pipeline for scoring candidate Earth locations
against Moon and Mars reference profiles.
"""

import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from typing import Dict, List
from dataclasses import asdict
from loguru import logger

from models.similarity_scorer import (
    AnalogFeatures,
    SimilarityResult,
    compute_similarity,
)
from models.spectral_matcher import match_best_reference


def score_candidate(
    site_name: str,
    features: AnalogFeatures,
    target_body: str = "mars",
) -> SimilarityResult:
    """
    Score a single candidate site against Moon or Mars reference profiles.

    Args:
        site_name: Name of the Earth candidate
        features: Extracted feature vector
        target_body: "moon" or "mars"

    Returns:
        SimilarityResult with overall and per-dimension scores
    """
    logger.info(f"Scoring {site_name} against {target_body}")

    result = compute_similarity(site_name, features, target_body)

    # Also find best spectral match
    spectral_features = {
        "iron_oxide": features.iron_oxide_index,
        "clay": features.clay_index,
        "sulfate": features.sulfate_index,
        "ndvi": features.vegetation_index,
        "albedo": features.albedo,
    }
    best_ref, spectral_score = match_best_reference(spectral_features, target_body)
    logger.info(
        f"  Best spectral match: {best_ref} (score={spectral_score:.3f})"
    )
    logger.info(
        f"  Overall score: {result.overall_score:.3f} "
        f"(T={result.terrain_score:.2f} M={result.mineral_score:.2f} "
        f"Th={result.thermal_score:.2f} A={result.aridity_score:.2f} "
        f"S={result.subsurface_score:.2f})"
    )

    return result


def rank_candidates(
    candidates: List[Dict],
    target_body: str = "mars",
    top_n: int = 10,
) -> List[SimilarityResult]:
    """
    Score and rank multiple candidate Earth locations.

    Args:
        candidates: List of dicts with "name" and "features" (AnalogFeatures)
        target_body: "moon" or "mars"
        top_n: Number of top results to return

    Returns:
        Sorted list of SimilarityResult objects (highest score first)
    """
    logger.info(f"Ranking {len(candidates)} candidates against {target_body}")

    results = []
    for candidate in candidates:
        result = score_candidate(
            site_name=candidate["name"],
            features=candidate["features"],
            target_body=target_body,
        )
        results.append(result)

    # Sort by overall score (descending)
    results.sort(key=lambda r: r.overall_score, reverse=True)

    logger.info(f"Top {min(top_n, len(results))} candidates:")
    for i, r in enumerate(results[:top_n]):
        logger.info(f"  {i + 1}. {r.site_name}: {r.overall_score:.3f}")

    return results[:top_n]
