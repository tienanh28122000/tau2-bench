from tau2.utils.utils import DATA_DIR
from typing import Tuple
import math

URBAN_SATELLITE_DATA_DIR = DATA_DIR / "tau2" / "domains" / "urban_satellite"
URBAN_SATELLITE_DB_PATH = URBAN_SATELLITE_DATA_DIR / "db.json"
URBAN_SATELLITE_POLICY_PATH = URBAN_SATELLITE_DATA_DIR / "policy.md"
URBAN_SATELLITE_TASK_SET_PATH = URBAN_SATELLITE_DATA_DIR / "tasks.json"
URBAN_SATELLITE_IMAGE_PATH = URBAN_SATELLITE_DATA_DIR / "satellite_imgs"


def deg2num(lat_deg: float, lon_deg: float, zoom: int = 15) -> Tuple[int, int]:
    """Standard Slippy Map conversion as used in your download_pop script."""
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)
