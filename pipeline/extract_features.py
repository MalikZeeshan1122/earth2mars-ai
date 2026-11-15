"""
Earth2Mars AI - Feature Extraction Pipeline
Extracts terrain, spectral, thermal, and aridity features from
preprocessed satellite imagery for analog similarity scoring.
"""

import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import numpy as np
from dataclasses import asdict
from typing import Dict
from loguru import logger

from models.similarity_scorer import AnalogFeatures


def extract_terrain_features(dem: np.ndarray, pixel_size_m: float = 30.0) -> Dict[str, float]:
    """
    Extract terrain morphology features from a Digital Elevation Model.

    Args:
        dem: 2D elevation array in meters
        pixel_size_m: Ground sampling distance in meters

    Returns:
        Dictionary of terrain features
    """
    logger.info("Extracting terrain features from DEM")

    # Slope (gradient magnitude)
    gy, gx = np.gradient(dem, pixel_size_m)
    slope = np.sqrt(gx**2 + gy**2)
    mean_slope = float(np.mean(slope))

    # Surface roughness (standard deviation of elevation in local windows)
    from scipy.ndimage import uniform_filter
    local_mean = uniform_filter(dem, size=5)
    local_sq_mean = uniform_filter(dem**2, size=5)
    roughness = np.sqrt(np.maximum(local_sq_mean - local_mean**2, 0))
    mean_roughness = float(np.mean(roughness))

    # Normalize to [0, 1]
    slope_norm = min(mean_slope / 0.5, 1.0)  # 0.5 = ~27° is max expected
    roughness_norm = min(mean_roughness / 50.0, 1.0)  # 50m std is max expected

    return {
        "slope_roughness": (slope_norm + roughness_norm) / 2,
        "mean_slope_deg": float(np.degrees(np.arctan(mean_slope))),
        "mean_roughness_m": mean_roughness,
    }


def extract_spectral_features(
    bands: Dict[str, np.ndarray],
) -> Dict[str, float]:
    """
    Extract spectral mineralogy indices from multispectral bands.

    Args:
        bands: Dictionary mapping band names to 2D arrays
               Expected keys: "blue", "red", "nir", "swir1", "swir2"

    Returns:
        Dictionary of spectral features
    """
    logger.info("Extracting spectral features")

    red = bands.get("red", np.zeros((1, 1)))
    blue = bands.get("blue", np.zeros((1, 1)))
    nir = bands.get("nir", np.zeros((1, 1)))
    swir1 = bands.get("swir1", np.zeros((1, 1)))
    swir2 = bands.get("swir2", np.zeros((1, 1)))

    # Iron oxide ratio
    iron_oxide = np.where(blue > 0, red / blue, 0)

    # Clay mineral index
    clay = np.where(swir2 > 0, swir1 / swir2, 0)

    # Sulfate index
    sulfate = np.where(
        (swir1 + nir) > 0,
        (swir1 - nir) / (swir1 + nir),
        0,
    )

    # NDVI
    ndvi_arr = np.where(
        (nir + red) > 0,
        (nir - red) / (nir + red),
        0,
    )

    # Mean albedo (simple average of visible bands)
    all_bands = [b for b in bands.values()]
    mean_albedo = float(np.mean([np.mean(b) for b in all_bands]))

    return {
        "iron_oxide_index": float(np.clip(np.mean(iron_oxide) / 3.0, 0, 1)),
        "clay_index": float(np.clip(np.mean(clay) / 2.0, 0, 1)),
        "sulfate_index": float(np.clip((np.mean(sulfate) + 1) / 2, 0, 1)),
        "vegetation_index": float(np.mean(ndvi_arr)),
        "albedo": float(np.clip(mean_albedo, 0, 1)),
    }


def extract_thermal_features(
    temperature_data: Dict[str, float],
) -> Dict[str, float]:
    """
    Extract thermal regime features from climate data.

    Args:
        temperature_data: Dictionary with temperature statistics
            Expected keys: "max_temp_c", "min_temp_c", "frost_days_per_year"

    Returns:
        Dictionary of thermal features
    """
    logger.info("Extracting thermal features")

    max_t = temperature_data.get("max_temp_c", 20)
    min_t = temperature_data.get("min_temp_c", 0)
    frost_days = temperature_data.get("frost_days_per_year", 0)

    return {
        "diurnal_delta_t": max_t - min_t,
        "min_temperature": min_t,
        "frost_frequency": min(frost_days / 365.0, 1.0),
    }


def build_feature_vector(
    terrain: Dict[str, float],
    spectral: Dict[str, float],
    thermal: Dict[str, float],
    precipitation_mm: float = 0.0,
    soil_moisture: float = 0.0,
    lava_tube_prob: float = 0.0,
) -> AnalogFeatures:
    """
    Combine all extracted features into a single AnalogFeatures object
    ready for similarity scoring.
    """
    return AnalogFeatures(
        slope_roughness=terrain.get("slope_roughness", 0),
        iron_oxide_index=spectral.get("iron_oxide_index", 0),
        clay_index=spectral.get("clay_index", 0),
        sulfate_index=spectral.get("sulfate_index", 0),
        albedo=spectral.get("albedo", 0),
        vegetation_index=spectral.get("vegetation_index", 0),
        diurnal_delta_t=thermal.get("diurnal_delta_t", 0),
        min_temperature=thermal.get("min_temperature", 0),
        frost_frequency=thermal.get("frost_frequency", 0),
        annual_precipitation_mm=precipitation_mm,
        soil_moisture=soil_moisture,
        lava_tube_probability=lava_tube_prob,
    )
