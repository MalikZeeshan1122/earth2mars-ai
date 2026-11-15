"""
Earth2Mars AI - Unit Tests for Similarity Scorer & AHP Weights
"""

import pytest
import numpy as np
from models.similarity_scorer import (
    AnalogFeatures,
    SimilarityResult,
    compute_similarity,
    score_terrain,
    score_mineral,
    score_thermal,
    score_aridity,
    calculate_ahp_weights,
    AHP_MARS_MATRIX,
    AHP_MOON_MATRIX,
)
from pipeline.mission_dossier import generate_mission_dossier


class TestAnalogFeatures:
    """Test AnalogFeatures dataclass."""

    def test_default_values(self):
        features = AnalogFeatures()
        assert features.slope_roughness == 0.0
        assert features.iron_oxide_index == 0.0
        assert features.min_temperature == 0.0

    def test_custom_values(self):
        features = AnalogFeatures(
            slope_roughness=0.85,
            iron_oxide_index=0.92,
            min_temperature=-40.0,
        )
        assert features.slope_roughness == 0.85
        assert features.iron_oxide_index == 0.92
        assert features.min_temperature == -40.0


class TestAHP:
    """Test Saaty's Analytic Hierarchy Process calculation and consistency."""

    def test_ahp_mars_matrix_consistency(self):
        weights, cr = calculate_ahp_weights(AHP_MARS_MATRIX)
        assert len(weights) == 5
        assert np.sum(weights) == pytest.approx(1.0, abs=1e-5)
        # Consistency Ratio must be < 0.10 for scientific validity
        assert cr < 0.10

    def test_ahp_moon_matrix_consistency(self):
        weights, cr = calculate_ahp_weights(AHP_MOON_MATRIX)
        assert len(weights) == 5
        assert np.sum(weights) == pytest.approx(1.0, abs=1e-5)
        assert cr < 0.10


class TestScoring:
    """Test individual scoring functions."""

    def test_terrain_score_range(self):
        features = AnalogFeatures(slope_roughness=0.5, crater_density=0.3)
        score = score_terrain(features)
        assert 0.0 <= score <= 1.0

    def test_mineral_score_range(self):
        features = AnalogFeatures(iron_oxide_index=0.8, clay_index=0.3, sulfate_index=0.5)
        score = score_mineral(features, "mars")
        assert 0.0 <= score <= 1.0

    def test_thermal_score_extreme_cold(self):
        cold_features = AnalogFeatures(diurnal_delta_t=50, min_temperature=-60, frost_frequency=0.9)
        warm_features = AnalogFeatures(diurnal_delta_t=10, min_temperature=15, frost_frequency=0.0)

        cold_score = score_thermal(cold_features)
        warm_score = score_thermal(warm_features)

        assert cold_score > warm_score

    def test_aridity_score_dry_vs_wet(self):
        dry_features = AnalogFeatures(annual_precipitation_mm=5, soil_moisture=0.02, vegetation_index=-0.05)
        wet_features = AnalogFeatures(annual_precipitation_mm=400, soil_moisture=0.8, vegetation_index=0.7)

        dry_score = score_aridity(dry_features)
        wet_score = score_aridity(wet_features)

        assert dry_score > wet_score


class TestComputeSimilarity:
    """Test end-to-end similarity computation."""

    def test_returns_result(self):
        features = AnalogFeatures(
            slope_roughness=0.8,
            iron_oxide_index=0.9,
            clay_index=0.3,
            sulfate_index=0.6,
            diurnal_delta_t=45,
            min_temperature=-50,
            frost_frequency=0.8,
            annual_precipitation_mm=10,
            soil_moisture=0.05,
            vegetation_index=-0.08,
        )
        result = compute_similarity("Test Site", features, "mars")

        assert isinstance(result, SimilarityResult)
        assert result.site_name == "Test Site"
        assert result.target_body == "mars"
        assert 0.0 <= result.overall_score <= 1.0


class TestMissionDossier:
    """Test Mission Dossier generation."""

    def test_generate_dossier_contains_key_elements(self):
        site_data = {
            "site": "McMurdo Dry Valleys",
            "country": "Antarctica",
            "lat": -77.5,
            "lon": 162.0,
            "target_bodies": ["moon", "mars"],
            "categories": ["Cold Traps / PSRs"],
            "overall_score": 0.96,
            "simulates": "Cryogenic polar volatile ice preservation",
        }
        dossier = generate_mission_dossier(site_data, "Test Crew")
        assert "McMurdo Dry Valleys" in dossier
        assert "Antarctica" in dossier
        assert "96.0%" in dossier
        assert "Test Crew" in dossier
