"""
Earth2Mars AI - Preprocessing Pipeline
Atmospheric correction, cloud masking, co-registration, and tiling
of satellite imagery for feature extraction.
"""

import numpy as np
from typing import Tuple
from loguru import logger


def atmospheric_correction(
    raw_radiance: np.ndarray,
    solar_zenith_angle: float,
    earth_sun_distance: float = 1.0,
) -> np.ndarray:
    """
    Convert top-of-atmosphere radiance to surface reflectance
    using a simplified dark-object subtraction method.

    Args:
        raw_radiance: Raw radiance array (bands, height, width)
        solar_zenith_angle: Solar zenith angle in degrees
        earth_sun_distance: Earth-Sun distance in AU

    Returns:
        Surface reflectance array
    """
    logger.info("Applying atmospheric correction (dark-object subtraction)")

    cos_sza = np.cos(np.radians(solar_zenith_angle))

    corrected = np.zeros_like(raw_radiance, dtype=np.float32)

    for band_idx in range(raw_radiance.shape[0]):
        band = raw_radiance[band_idx].astype(np.float32)
        # Dark-object subtraction
        dark_value = np.percentile(band[band > 0], 1)
        corrected_band = (band - dark_value) / (cos_sza * earth_sun_distance**2)
        corrected[band_idx] = np.clip(corrected_band, 0, 1)

    return corrected


def cloud_mask(
    blue_band: np.ndarray,
    nir_band: np.ndarray,
    thermal_band: np.ndarray = None,
    blue_threshold: float = 0.25,
    nir_threshold: float = 0.3,
) -> np.ndarray:
    """
    Generate a binary cloud mask.

    Args:
        blue_band: Blue band reflectance
        nir_band: NIR band reflectance
        thermal_band: Optional thermal band (clouds are cold)
        blue_threshold: Threshold for blue reflectance
        nir_threshold: Threshold for NIR reflectance

    Returns:
        Boolean mask (True = cloud, False = clear)
    """
    logger.info("Generating cloud mask")

    mask = (blue_band > blue_threshold) & (nir_band > nir_threshold)

    if thermal_band is not None:
        cold_threshold = np.percentile(thermal_band, 20)
        mask = mask & (thermal_band < cold_threshold)

    cloud_pct = 100.0 * np.sum(mask) / mask.size
    logger.info(f"Cloud cover: {cloud_pct:.1f}%")

    return mask


def tile_image(
    image: np.ndarray,
    tile_size: int = 64,
    overlap: int = 0,
) -> Tuple[np.ndarray, list]:
    """
    Split a large satellite image into fixed-size tiles for CNN input.

    Args:
        image: Input array (bands, height, width)
        tile_size: Tile dimension in pixels
        overlap: Overlap between adjacent tiles in pixels

    Returns:
        Tuple of (tiles array, list of (row, col) positions)
    """
    _, h, w = image.shape
    stride = tile_size - overlap

    tiles = []
    positions = []

    for row in range(0, h - tile_size + 1, stride):
        for col in range(0, w - tile_size + 1, stride):
            tile = image[:, row : row + tile_size, col : col + tile_size]
            tiles.append(tile)
            positions.append((row, col))

    logger.info(f"Generated {len(tiles)} tiles of size {tile_size}x{tile_size}")

    return np.array(tiles), positions
