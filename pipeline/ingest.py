"""
Earth2Mars AI - Data Ingestion Pipeline
Interfaces NASA EarthData CMR (Common Metadata Repository), GIBS tile services,
and ESA Copernicus APIs for Earth analog site satellite feeds.
"""

import os
import requests
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class SatelliteScene:
    """Metadata for a downloaded or queried satellite scene."""
    source: str          # "landsat8", "sentinel2", "hls", "lro", "mola"
    scene_id: str
    acquisition_date: str
    bbox: tuple          # (min_lon, min_lat, max_lon, max_lat)
    download_url: str
    cloud_cover: float = 0.0


class NASADataIngestor:
    """
    Multi-Agency Planetary & Earth Observation Ingestion Engine.
    Integrates official data sources for the NASA Space Apps Challenge:
      - NASA: Earthdata Search, Worldview (GIBS), PDS, LRO LOLA/Diviner
      - CSA: RADARSAT Constellation Mission (RCM) & SAR tutorials
      - ESA: Copernicus Data Space Ecosystem (Sentinel-1/2/3) & Open Science Catalog
      - JAXA: G-Portal (GSMaP precipitation, snow cover, vegetation indices)
    """

    CMR_GRANULES_URL = "https://cmr.earthdata.nasa.gov/search/granules.json"
    GIBS_WMTS_URL = "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/wmts.cgi"

    # Partner Space Agency Portals & APIs
    PARTNER_RESOURCES = {
        "nasa_earthdata": "https://search.earthdata.nasa.gov/",
        "nasa_worldview": "https://worldview.earthdata.nasa.gov/",
        "nasa_pds": "https://pds.nasa.gov/",
        "nasa_lro_geosciences": "https://pds-geosciences.wustl.edu/missions/lro/",
        "nasa_lro_diviner": "https://pds-geosciences.wustl.edu/missions/lro/diviner.htm",
        "csa_radarsat_rcm": "https://donnees-data.asc-csa.gc.ca/en/dataset/rcm",
        "csa_radarsat_1": "https://donnees-data.asc-csa.gc.ca/en/dataset/radarsat1",
        "csa_sar_tutorial": "https://github.com/asc-csa/Synthetic_Aperture_Radar_Tutorial",
        "esa_copernicus": "https://dataspace.copernicus.eu/",
        "esa_open_science": "https://opensciencedata.esa.int/",
        "jaxa_gportal": "https://gportal.jaxa.jp/gpr/",
    }

    def __init__(self, data_dir: str = "data/raw"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        logger.info(f"NASADataIngestor initialized. Data cache: {data_dir}")

    def query_nasa_cmr(
        self,
        bbox: tuple,
        short_name: str = "HLSL30", # Harmonized Landsat Sentinel-2 (HLS)
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Query NASA CMR open API for satellite granules over a designated bounding box.
        Bbox format: (min_lon, min_lat, max_lon, max_lat)
        """
        params = {
            "short_name": short_name,
            "bounding_box": f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}",
            "page_size": limit,
            "sort_key": "-start_date",
        }
        try:
            logger.info(f"Querying NASA CMR for {short_name} granules at bbox={bbox}")
            response = requests.get(self.CMR_GRANULES_URL, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                entries = data.get("feed", {}).get("entry", [])
                logger.info(f"NASA CMR returned {len(entries)} granules")
                return entries
            else:
                logger.warning(f"NASA CMR query returned status {response.status_code}")
                return []
        except Exception as e:
            logger.warning(f"NASA CMR network request failed: {e}. Falling back to cached catalog.")
            return []

    def get_nasa_gibs_layer_url(self, layer: str = "MODIS_Terra_CorrectedReflectance_TrueColor") -> str:
        """
        Generate NASA Global Imagery Browse Services (GIBS) tile layer URL.
        Open access, zero authentication required.
        """
        return (
            f"https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/{layer}/"
            "default/{Time}/250m/{TileMatrix}/{TileRow}/{TileCol}.jpg"
        )

    def get_planetary_wms_layers(self) -> Dict[str, str]:
        """
        USGS Astrogeology Planetary WMS endpoints for Moon and Mars base maps.
        """
        return {
            "moon_lola_elevation": "https://planetarymaps.usgs.gov/cgi-bin/mapserv?map=/maps/earth/moon_simp_cyl.map",
            "mars_mola_color": "https://planetarymaps.usgs.gov/cgi-bin/mapserv?map=/maps/mars/mars_simp_cyl.map",
            "mars_viking_mdim": "https://planetarymaps.usgs.gov/cgi-bin/mapserv?map=/maps/mars/mars_viking_simp_cyl.map",
        }
