"""
Earth2Mars AI - Comprehensive Unit Tests for Spectral Matcher
Includes tests for Spectral Angle Mapper (SAM) and Spectral Information Divergence (SID).
"""

import pytest
import numpy as np
from models.spectral_matcher import (
    iron_oxide_ratio,
    clay_mineral_index,
    sulfate_index,
    ndvi,
    cosine_similarity,
    spectral_angle_mapper,
    spectral_information_divergence,
    spectral_similarity,
    match_best_reference,
)


class TestSpectralIndices:
    """Test spectral index calculations."""

    def test_iron_oxide_ratio(self):
        red = np.array([0.3, 0.5, 0.8])
        blue = np.array([0.1, 0.2, 0.4])
        result = iron_oxide_ratio(red, blue)
        np.testing.assert_allclose(result, [3.0, 2.5, 2.0])

    def test_iron_oxide_zero_division(self):
        red = np.array([0.5])
        blue = np.array([0.0])
        result = iron_oxide_ratio(red, blue)
        assert result[0] == 0

    def test_ndvi_vegetation(self):
        nir = np.array([0.8])
        red = np.array([0.2])
        result = ndvi(nir, red)
        assert result[0] == pytest.approx(0.6, abs=0.01)

    def test_ndvi_bare_soil(self):
        nir = np.array([0.15])
        red = np.array([0.25])
        result = ndvi(nir, red)
        assert result[0] < 0  # Negative NDVI = barren (good for analog)


class TestSAMandSID:
    """Test NASA-standard SAM and SID algorithms."""

    def test_sam_identical_vectors(self):
        vec = np.array([0.5, 0.3, 0.2, 0.1])
        score = spectral_angle_mapper(vec, vec)
        assert score == pytest.approx(1.0, abs=1e-5)

    def test_sam_orthogonal_vectors(self):
        a = np.array([1.0, 0.0])
        b = np.array([0.0, 1.0])
        score = spectral_angle_mapper(a, b)
        assert score == pytest.approx(0.0, abs=1e-5)

    def test_sid_identical_vectors(self):
        vec = np.array([0.4, 0.3, 0.2, 0.1])
        score = spectral_information_divergence(vec, vec)
        assert score == pytest.approx(1.0, abs=1e-4)

    def test_spectral_similarity_modes(self):
        earth = {"iron_oxide": 0.8, "clay": 0.3, "sulfate": 0.5}
        ref = {"iron_oxide": 0.85, "clay": 0.30, "sulfate": 0.65}
        sam = spectral_similarity(earth, ref, method="sam")
        sid = spectral_similarity(earth, ref, method="sid")
        hybrid = spectral_similarity(earth, ref, method="hybrid")
        assert 0.0 <= sam <= 1.0
        assert 0.0 <= sid <= 1.0
        assert 0.0 <= hybrid <= 1.0


class TestMatchBestReference:
    """Test reference matching against Martian and Lunar libraries."""

    def test_mars_match(self):
        earth = {"iron_oxide": 0.83, "clay": 0.28, "sulfate": 0.60, "ndvi": -0.09, "albedo": 0.17}
        name, score = match_best_reference(earth, "mars")
        assert name == "meridiani_planum"
        assert score > 0.85

    def test_moon_match(self):
        earth = {"iron_oxide": 0.70, "clay": 0.14, "sulfate": 0.07, "ndvi": -0.04, "albedo": 0.11}
        name, score = match_best_reference(earth, "moon")
        assert name == "lunar_maria"
        assert score > 0.85
