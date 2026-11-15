# Earth2Mars AI - Pipeline Package

from .ingest import NASADataIngestor
from .preprocess import atmospheric_correction, cloud_mask, tile_image
from .extract_features import (
    extract_terrain_features,
    extract_spectral_features,
    extract_thermal_features,
    build_feature_vector,
)
from .score import score_candidate, rank_candidates
from .mission_dossier import generate_mission_dossier

__all__ = [
    "NASADataIngestor",
    "atmospheric_correction",
    "cloud_mask",
    "tile_image",
    "extract_terrain_features",
    "extract_spectral_features",
    "extract_thermal_features",
    "build_feature_vector",
    "score_candidate",
    "rank_candidates",
    "generate_mission_dossier",
]
