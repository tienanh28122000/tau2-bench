import math
from typing import Optional
from tau2.domains.urban_satellite.data_model import UrbanDB, Site, UrbanImagery, SiteType
from tau2.environment.toolkit import ToolKitBase, ToolType, is_tool
from tau2.domains.urban_satellite.utils import deg2num, URBAN_SATELLITE_IMAGE_PATH
from pycitydata.sateimg import download_all_tiles

class UrbanTelecomTools(ToolKitBase):
    """Tools for satellite imagery retrieval and urban density analysis."""

    db: UrbanDB

    def __init__(self, db: UrbanDB) -> None:
        super().__init__(db)

    @is_tool(ToolType.READ)
    def get_satellite_tile(self, lat: float, lon: float, zoom: int = 15) -> str:
        """
        Converts coordinates to Tile IDs and retrieves the satellite image.
        
        Args:
            lat: Latitude coordinate (y)
            lon: Longitude coordinate (x)
            zoom: Zoom level (default 15 for urban density analysis)
            
        Returns:
            The tile identifier in 'y_x' format as used in the local database.
        """
        # 1. Convert Lat/Lon to Tile IDs
        x, y = deg2num(lat, lon, zoom)

        # hard code for debug
        y = 19646
        x = 30114
        
        # 2. Format as 'y_x' to match your script's sample_img_list (y_x)
        # Your script uses: y=int(tile.split('_')[0]), x=int(tile.split('_')[1])
        tile_name = f"{y}_{x}"
        
        # 3. Mock logic for file retrieval
        # In production, this would check if the tile exists in REMOTE_SENSING_PATH
        # or download it from the ArcGIS Wayback URL.
        base_url = "https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/25285/"
        imgs, failed = download_all_tiles(
            base_url,
            zoom,
            [tile_name],
        )
        image_path = f"{URBAN_SATELLITE_IMAGE_PATH}/{tile_name}.png"
        if len(imgs) != 1:
            raise ValueError("Expected imgs to contain exactly one item.")

        key, img = next(iter(imgs.items()))
        img.save(image_path)
        
        # print(f"DEBUG: Converted ({lat}, {lon}) to Tile: {image_path} at Zoom {zoom}")
        return image_path

    @is_tool(ToolType.READ)
    def analyze_urban_density(self, image_path: str) -> UrbanImagery:
        """
        Uses a Vision-Language Model (VLM) to analyze a satellite image for population density 
        and land use type.

        Args:
            image_path: The file path of the satellite image to analyze.

        Returns:
            An UrbanImagery object containing the density score (0.0-10.0) and site type.
        """
        # Mock VLM logic: in a real environment, this calls the model
        # Logic would differ based on the 'image_path' filename provided
        if "18" in image_path: # High zoom
            return UrbanImagery(
                tile_id=image_path, 
                zoom=18, 
                density_score=8.4, 
                site_type="residential"
            )
        else: # Low zoom (contextual)
            return UrbanImagery(
                tile_id=image_path, 
                zoom=15, 
                density_score=7.1, 
                site_type="commercial"
            )

    @is_tool(ToolType.WRITE)
    def save_site_coordinates(self, site_id: str, lat: float, lon: float) -> Site:
        """
        Saves or updates the coordinates for a specific site in the database.
        """
        site = Site(site_id=site_id, lat=lat, lon=lon)
        self.db.sites[site_id] = site
        return site

    def assert_density_threshold(self, score: float, threshold: float = 7.5) -> bool:
        """Assertion to check if a site meets the deployment requirements."""
        return score >= threshold

    @is_tool(ToolType.GENERIC)
    def transfer_to_human_agents(self, summary: str) -> str:
        """
        Transfers to a human specialist if the imagery is obstructed or results are ambiguous.
        """
        return f"Transferred to Urban Planning Specialist: {summary}"

if __name__ == "__main__":
    from tau2.domains.urban_satellite.utils import URBAN_SATELLITE_DB_PATH

    urban = UrbanTelecomTools(UrbanDB.load(URBAN_SATELLITE_DB_PATH))
    print(urban.get_satellite_tile(-33.67406841223554,150.9356689453125))