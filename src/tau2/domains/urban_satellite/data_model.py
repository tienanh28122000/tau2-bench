from typing import Annotated, Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from tau2.domains.urban_satellite.utils import URBAN_SATELLITE_DB_PATH  # Updated path
from tau2.environment.db import DB

# Site types for urban classification
SiteType = Literal["residential", "commercial", "industrial", "mixed"]

class Site(BaseModel):
    site_id: str = Field(description="Unique identifier for the site (e.g., 'Alpha')")
    lat: float = Field(description="Latitude of the site")
    lon: float = Field(description="Longitude of the site")
    description: Optional[str] = Field(None, description="General description of the location")

class UrbanImagery(BaseModel):
    tile_id: str = Field(description="The x_y tile identifier derived from coordinates")
    zoom: int = Field(description="The zoom level of the image")
    density_score: float = Field(description="Population density score from 0.0 to 10.0")
    site_type: SiteType = Field(description="Predominant land use type detected")

class UrbanDB(DB):
    """Database containing infrastructure sites and analysis history."""
    sites: Dict[str, Site] = Field(default_factory=dict, description="Dictionary of known sites")
    analysis_cache: Dict[str, UrbanImagery] = Field(default_factory=dict, description="Cached imagery analysis results")

def get_db():
    return UrbanDB.load(URBAN_DB_PATH)
