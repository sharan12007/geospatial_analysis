"""
Workflow Planning Module for Geospatial Analysis
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class AnalysisType(Enum):
    """Types of geospatial analysis supported"""
    FLOOD_RISK = "flood_risk"
    SOLAR_SUITABILITY = "solar_suitability"
    DEFORESTATION = "deforestation"
    URBAN_GROWTH = "urban_growth"
    AGRICULTURAL_SUITABILITY = "agricultural_suitability"
    WILDFIRE_RISK = "wildfire_risk"
    LAND_USE_CHANGE = "land_use_change"


@dataclass
class Dataset:
    """Represents a GEE dataset"""
    name: str
    collection_id: str
    description: str
    bands: List[str]
    temporal_resolution: str
    spatial_resolution: str


@dataclass
class AnalysisStep:
    """Represents a step in the analysis workflow"""
    step_number: int
    description: str
    method: str
    datasets: List[Dataset]
    parameters: Dict[str, Any]


@dataclass
class WorkflowPlan:
    """Complete workflow plan for geospatial analysis"""
    analysis_type: AnalysisType
    region_of_interest: str
    time_period: str
    steps: List[AnalysisStep]
    output_layers: List[str]
    visualization_instructions: str


class WorkflowPlanner:
    """
    Plans geospatial analysis workflows based on user queries
    """
    
    def __init__(self):
        self.datasets = self._initialize_datasets()
    
    def _initialize_datasets(self) -> Dict[str, Dataset]:
        """Initialize available GEE datasets"""
        return {
            "srtm": Dataset(
                name="SRTM Digital Elevation Model",
                collection_id="USGS/SRTMGL1_003",
                description="30m resolution DEM",
                bands=["elevation"],
                temporal_resolution="static",
                spatial_resolution="30m"
            ),
            "sentinel2": Dataset(
                name="Sentinel-2 MSI",
                collection_id="COPERNICUS/S2_SR",
                description="Multispectral imagery for vegetation analysis",
                bands=["B2", "B3", "B4", "B8", "B11", "B12"],
                temporal_resolution="5 days",
                spatial_resolution="10-20m"
            ),
            "sentinel1": Dataset(
                name="Sentinel-1 SAR",
                collection_id="COPERNICUS/S1_GRD",
                description="SAR imagery for flood detection",
                bands=["VV", "VH"],
                temporal_resolution="6 days",
                spatial_resolution="10m"
            ),
            "chirps": Dataset(
                name="CHIRPS Precipitation",
                collection_id="UCSB-CHG/CHIRPS/DAILY",
                description="Daily precipitation estimates",
                bands=["precipitation"],
                temporal_resolution="daily",
                spatial_resolution="5km"
            ),
            "modis_ndvi": Dataset(
                name="MODIS NDVI",
                collection_id="MODIS/006/MOD13Q1",
                description="Vegetation indices",
                bands=["NDVI", "EVI"],
                temporal_resolution="16 days",
                spatial_resolution="250m"
            ),
            "landsat8": Dataset(
                name="Landsat 8 Surface Reflectance",
                collection_id="LANDSAT/LC08/C02/T1_L2",
                description="Multispectral imagery",
                bands=["SR_B2", "SR_B3", "SR_B4", "SR_B5", "SR_B6", "SR_B7"],
                temporal_resolution="16 days",
                spatial_resolution="30m"
            ),
            "worldpop": Dataset(
                name="WorldPop Population",
                collection_id="WorldPop/POP/2020",
                description="Population density estimates",
                bands=["population"],
                temporal_resolution="annual",
                spatial_resolution="100m"
            )
        }
    
    def plan_flood_risk_analysis(self, location: str, time_period: str = "2020-2023") -> WorkflowPlan:
        """Plan flood risk analysis workflow"""
        steps = [
            AnalysisStep(
                step_number=1,
                description=f"Define region of interest for {location}",
                method="Administrative boundary extraction",
                datasets=[],
                parameters={"location": location}
            ),
            AnalysisStep(
                step_number=2,
                description="Extract elevation data and compute slope",
                method="DEM analysis and slope calculation",
                datasets=[self.datasets["srtm"]],
                parameters={"elevation_threshold": 10, "slope_threshold": 5}
            ),
            AnalysisStep(
                step_number=3,
                description="Analyze precipitation patterns",
                method="Rainfall intensity and frequency analysis",
                datasets=[self.datasets["chirps"]],
                parameters={"precipitation_threshold": 50, "time_period": time_period}
            ),
            AnalysisStep(
                step_number=4,
                description="Identify flood-prone areas using SAR imagery",
                method="Water body detection using Sentinel-1",
                datasets=[self.datasets["sentinel1"]],
                parameters={"vv_threshold": -10, "vh_threshold": -15}
            ),
            AnalysisStep(
                step_number=5,
                description="Combine factors to create flood risk map",
                method="Multi-criteria analysis",
                datasets=[],
                parameters={"weights": {"elevation": 0.4, "precipitation": 0.3, "sar_water": 0.3}}
            )
        ]
        
        return WorkflowPlan(
            analysis_type=AnalysisType.FLOOD_RISK,
            region_of_interest=location,
            time_period=time_period,
            steps=steps,
            output_layers=["elevation", "slope", "precipitation", "flood_risk_zones"],
            visualization_instructions="Display flood risk zones with color coding: red (high risk), yellow (medium risk), green (low risk). Overlay on satellite imagery base map."
        )
    
    def plan_solar_suitability_analysis(self, location: str, time_period: str = "2020-2023") -> WorkflowPlan:
        """Plan solar farm suitability analysis workflow"""
        steps = [
            AnalysisStep(
                step_number=1,
                description=f"Define region of interest for {location}",
                method="Administrative boundary extraction",
                datasets=[],
                parameters={"location": location}
            ),
            AnalysisStep(
                step_number=2,
                description="Analyze slope and aspect for solar panel orientation",
                method="DEM-based slope and aspect analysis",
                datasets=[self.datasets["srtm"]],
                parameters={"max_slope": 15, "preferred_aspect": "south"}
            ),
            AnalysisStep(
                step_number=3,
                description="Assess land cover and land use",
                method="Land cover classification using Sentinel-2",
                datasets=[self.datasets["sentinel2"]],
                parameters={"exclude_classes": ["water", "urban", "forest"]}
            ),
            AnalysisStep(
                step_number=4,
                description="Calculate solar irradiance potential",
                method="Solar radiation modeling",
                datasets=[self.datasets["srtm"]],
                parameters={"min_irradiance": 4.5}
            ),
            AnalysisStep(
                step_number=5,
                description="Exclude protected areas and infrastructure",
                method="Constraint mapping",
                datasets=[],
                parameters={"buffer_distance": 1000}
            ),
            AnalysisStep(
                step_number=6,
                description="Generate solar suitability map",
                method="Multi-criteria suitability analysis",
                datasets=[],
                parameters={"weights": {"slope": 0.3, "land_cover": 0.3, "irradiance": 0.4}}
            )
        ]
        
        return WorkflowPlan(
            analysis_type=AnalysisType.SOLAR_SUITABILITY,
            region_of_interest=location,
            time_period=time_period,
            steps=steps,
            output_layers=["slope", "aspect", "land_cover", "solar_irradiance", "suitability_zones"],
            visualization_instructions="Display suitability zones with color coding: green (high suitability), yellow (medium suitability), red (low suitability). Overlay on satellite imagery with slope and aspect information."
        )
    
    def plan_deforestation_analysis(self, location: str, time_period: str = "2015-2023") -> WorkflowPlan:
        """Plan deforestation analysis workflow"""
        steps = [
            AnalysisStep(
                step_number=1,
                description=f"Define region of interest for {location}",
                method="Administrative boundary extraction",
                datasets=[],
                parameters={"location": location}
            ),
            AnalysisStep(
                step_number=2,
                description="Calculate NDVI time series",
                method="Vegetation index analysis using Sentinel-2",
                datasets=[self.datasets["sentinel2"]],
                parameters={"time_period": time_period, "cloud_threshold": 20}
            ),
            AnalysisStep(
                step_number=3,
                description="Detect forest cover changes",
                method="Change detection using NDVI thresholds",
                datasets=[self.datasets["sentinel2"]],
                parameters={"ndvi_threshold": 0.3, "change_threshold": 0.1}
            ),
            AnalysisStep(
                step_number=4,
                description="Classify land cover types",
                method="Supervised classification",
                datasets=[self.datasets["sentinel2"]],
                parameters={"classes": ["forest", "agriculture", "urban", "water", "bare_soil"]}
            ),
            AnalysisStep(
                step_number=5,
                description="Quantify deforestation areas",
                method="Spatial analysis and statistics",
                datasets=[],
                parameters={"min_patch_size": 0.1}
            )
        ]
        
        return WorkflowPlan(
            analysis_type=AnalysisType.DEFORESTATION,
            region_of_interest=location,
            time_period=time_period,
            steps=steps,
            output_layers=["ndvi_time_series", "forest_cover", "deforestation_areas", "land_cover_change"],
            visualization_instructions="Display deforestation areas in red, forest areas in green, and other land cover types with appropriate colors. Show time series of NDVI changes."
        )
    
    def plan_analysis(self, query: str, location: str, time_period: str = "2020-2023") -> WorkflowPlan:
        """
        Plan analysis workflow based on user query
        
        Args:
            query: User's geospatial analysis query
            location: Location of interest
            time_period: Time period for analysis
            
        Returns:
            WorkflowPlan: Complete workflow plan
        """
        query_lower = query.lower()
        
        if any(keyword in query_lower for keyword in ["flood", "flooding", "flood-prone", "water", "inundation"]):
            return self.plan_flood_risk_analysis(location, time_period)
        elif any(keyword in query_lower for keyword in ["solar", "renewable", "energy", "farm", "suitability"]):
            return self.plan_solar_suitability_analysis(location, time_period)
        elif any(keyword in query_lower for keyword in ["deforestation", "forest", "vegetation", "tree", "deforestation"]):
            return self.plan_deforestation_analysis(location, time_period)
        else:
            # Default to flood risk analysis
            return self.plan_flood_risk_analysis(location, time_period)
