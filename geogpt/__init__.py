"""
GeoGPT - AI Assistant for Google Earth Engine Geospatial Analysis

This package provides tools for:
- OAuth2 authentication with Google Earth Engine
- Geospatial workflow planning and execution
- Map visualization and result interpretation
- Common analysis patterns (flood risk, site suitability, deforestation, etc.)
"""

__version__ = "1.0.0"
__author__ = "GeoGPT"

from .auth import GEEAuthenticator
from .workflow import WorkflowPlanner
from .analyzer import GeospatialAnalyzer
from .visualizer import MapVisualizer

__all__ = [
    "GEEAuthenticator",
    "WorkflowPlanner", 
    "GeospatialAnalyzer",
    "MapVisualizer"
]
