"""
Map Visualization Module for Google Earth Engine Results
"""

import ee
import folium
from typing import Dict, List, Any, Optional, Tuple
import json


class MapVisualizer:
    """
    Creates interactive maps for geospatial analysis results
    """
    
    def __init__(self):
        self.ee = ee
        
    def create_flood_risk_map(self, results: Dict[str, Any], region: ee.Geometry, layer_controls: Dict[str, bool] = None) -> str:
        """
        Create interactive map for flood risk analysis results
        
        Args:
            results: Analysis results from flood risk analysis
            region: Region of interest
            
        Returns:
            str: HTML map content
        """
        # Get region center for map
        try:
            region_center = region.centroid().getInfo()['coordinates']
            center_lat, center_lon = region_center[1], region_center[0]
        except:
            # Fallback to Chennai coordinates
            center_lat, center_lon = 13.0827, 80.2707
        
        # Create base map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=10,
            tiles='OpenStreetMap'
        )
        
        # Add satellite imagery
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Satellite Imagery',
            overlay=False,
            control=True
        ).add_to(m)
        
        # Define flood risk visualization parameters with enhanced visibility
        flood_risk_vis = {
            'min': 0,
            'max': 3,
            'palette': ['#00ff00', '#ffff00', '#ff8000', '#ff0000'],  # Bright, distinct colors
            'opacity': 0.8
        }
        
        # Add flood risk zones
        flood_risk_url = self._get_tile_url(results['flood_risk_zones'], flood_risk_vis, region)
        
        folium.raster_layers.TileLayer(
            tiles=flood_risk_url,
            attr='Flood Risk Zones',
            name='Flood Risk Zones',
            overlay=True,
            control=True,
            opacity=0.8
        ).add_to(m)
        
        # Add elevation layer
        elevation_vis = {
            'min': 0,
            'max': 100,
            'palette': ['blue', 'green', 'yellow', 'red'],
            'opacity': 0.5
        }
        
        elevation_url = self._get_tile_url(results['elevation'], elevation_vis, region)
        
        folium.raster_layers.TileLayer(
            tiles=elevation_url,
            attr='Elevation',
            name='Elevation',
            overlay=True,
            control=True,
            opacity=0.5
        ).add_to(m)
        
        # Add precipitation layer if enabled
        if layer_controls is None or layer_controls.get('precipitation', False):
            precipitation_vis = {
                'min': 0,
                'max': 200,
                'palette': ['white', 'lightblue', 'blue', 'darkblue'],
                'opacity': 0.6
            }
            
            precipitation_url = self._get_tile_url(results['precipitation'], precipitation_vis, region)
            
            folium.raster_layers.TileLayer(
                tiles=precipitation_url,
                attr='Precipitation (mm)',
                name='Precipitation',
                overlay=True,
                control=True,
                opacity=0.6
            ).add_to(m)
        
        # Add dynamic legend
        self._add_dynamic_legend(m, "flood_risk")
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        return m._repr_html_()
    
    def create_solar_suitability_map(self, results: Dict[str, Any], region: ee.Geometry, layer_controls: Dict[str, bool] = None) -> str:
        """
        Create interactive map for solar suitability analysis results
        
        Args:
            results: Analysis results from solar suitability analysis
            region: Region of interest
            
        Returns:
            str: HTML map content
        """
        # Get region center for map
        try:
            region_center = region.centroid().getInfo()['coordinates']
            center_lat, center_lon = region_center[1], region_center[0]
        except:
            # Fallback to Rajasthan coordinates
            center_lat, center_lon = 26.2389, 73.0243
        
        # Create base map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=10,
            tiles='OpenStreetMap'
        )
        
        # Add satellite imagery
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Satellite Imagery',
            overlay=False,
            control=True
        ).add_to(m)
        
        # Define solar suitability visualization parameters with enhanced visibility
        suitability_vis = {
            'min': 0,
            'max': 3,
            'palette': ['#ff0000', '#ff8000', '#ffff00', '#00ff00'],  # Bright, distinct colors
            'opacity': 0.8
        }
        
        # Add suitability zones
        suitability_url = self._get_tile_url(results['suitability_zones'], suitability_vis, region)
        
        folium.raster_layers.TileLayer(
            tiles=suitability_url,
            attr='Solar Suitability Zones',
            name='Solar Suitability Zones',
            overlay=True,
            control=True,
            opacity=0.8
        ).add_to(m)
        
        # Add slope layer
        slope_vis = {
            'min': 0,
            'max': 30,
            'palette': ['green', 'yellow', 'orange', 'red'],
            'opacity': 0.5
        }
        
        slope_url = self._get_tile_url(results['slope'], slope_vis, region)
        
        folium.raster_layers.TileLayer(
            tiles=slope_url,
            attr='Slope',
            name='Slope',
            overlay=True,
            control=True,
            opacity=0.5
        ).add_to(m)
        
        # Add NDVI layer
        ndvi_vis = {
            'min': -1,
            'max': 1,
            'palette': ['red', 'yellow', 'green'],
            'opacity': 0.6
        }
        
        ndvi_url = self._get_tile_url(results['ndvi'], ndvi_vis, region)
        
        folium.raster_layers.TileLayer(
            tiles=ndvi_url,
            attr='NDVI',
            name='NDVI',
            overlay=True,
            control=True,
            opacity=0.6
        ).add_to(m)
        
        # Add dynamic legend
        self._add_dynamic_legend(m, "solar_suitability")
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        return m._repr_html_()
    
    def create_deforestation_map(self, results: Dict[str, Any], region: ee.Geometry, layer_controls: Dict[str, bool] = None) -> str:
        """
        Create interactive map for deforestation analysis results
        
        Args:
            results: Analysis results from deforestation analysis
            region: Region of interest
            
        Returns:
            str: HTML map content
        """
        # Get region center for map
        try:
            region_center = region.centroid().getInfo()['coordinates']
            center_lat, center_lon = region_center[1], region_center[0]
        except:
            # Fallback to Kerala coordinates
            center_lat, center_lon = 10.8505, 76.2711
        
        # Create base map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=10,
            tiles='OpenStreetMap'
        )
        
        # Add satellite imagery
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Satellite Imagery',
            overlay=False,
            control=True
        ).add_to(m)
        
        # Add deforestation areas with enhanced visibility
        deforestation_vis = {
            'min': 0,
            'max': 1,
            'palette': ['#000000', '#ff0000'],  # Black for no deforestation, bright red for deforestation
            'opacity': 0.9
        }
        
        deforestation_url = self._get_tile_url(results['deforested_areas'], deforestation_vis, region)
        
        folium.raster_layers.TileLayer(
            tiles=deforestation_url,
            attr='Deforestation Areas',
            name='Deforestation Areas',
            overlay=True,
            control=True,
            opacity=0.9
        ).add_to(m)
        
        # Add NDVI change layer
        ndvi_change_vis = {
            'min': -0.5,
            'max': 0.5,
            'palette': ['red', 'white', 'green'],
            'opacity': 0.6
        }
        
        ndvi_change_url = self._get_tile_url(results['ndvi_change'], ndvi_change_vis, region)
        
        folium.raster_layers.TileLayer(
            tiles=ndvi_change_url,
            attr='NDVI Change',
            name='NDVI Change',
            overlay=True,
            control=True,
            opacity=0.6
        ).add_to(m)
        
        # Add forest cover 2015
        forest_2015_vis = {
            'min': 0,
            'max': 1,
            'palette': ['#000000', '#006400'],  # Black for no forest, dark green for forest
            'opacity': 0.5
        }
        
        forest_2015_url = self._get_tile_url(results['forest_2015'], forest_2015_vis, region)
        
        folium.raster_layers.TileLayer(
            tiles=forest_2015_url,
            attr='Forest Cover 2015',
            name='Forest Cover 2015',
            overlay=True,
            control=True,
            opacity=0.5
        ).add_to(m)
        
        # Add forest cover 2023
        forest_2023_vis = {
            'min': 0,
            'max': 1,
            'palette': ['#000000', '#00ff00'],  # Black for no forest, bright green for forest
            'opacity': 0.5
        }
        
        forest_2023_url = self._get_tile_url(results['forest_2023'], forest_2023_vis, region)
        
        folium.raster_layers.TileLayer(
            tiles=forest_2023_url,
            attr='Forest Cover 2023',
            name='Forest Cover 2023',
            overlay=True,
            control=True,
            opacity=0.5
        ).add_to(m)
        
        # Add dynamic legend
        self._add_dynamic_legend(m, "deforestation")
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        return m._repr_html_()
    
    def _get_tile_url(self, image: ee.Image, vis_params: Dict[str, Any], region: ee.Geometry) -> str:
        """
        Get tile URL for Earth Engine image
        
        Args:
            image: Earth Engine image
            vis_params: Visualization parameters
            region: Region of interest
            
        Returns:
            str: Tile URL
        """
        # Get the map ID
        map_id = image.getMapId(vis_params)
        
        # Return the tile URL
        return map_id['tile_fetcher'].url_format
    
    def _add_dynamic_legend(self, map_obj, analysis_type: str):
        """Add dynamic legend based on analysis type with toggle functionality"""
        legend_configs = {
            "flood_risk": {
                "title": "Flood Risk Zones",
                "items": [
                    ("#00ff00", "No Risk (0)"),
                    ("#ffff00", "Low Risk (1)"),
                    ("#ff8000", "Medium Risk (2)"),
                    ("#ff0000", "High Risk (3)")
                ]
            },
            "solar_suitability": {
                "title": "Solar Suitability",
                "items": [
                    ("#ff0000", "Not Suitable (0)"),
                    ("#ff8000", "Low Suitability (1)"),
                    ("#ffff00", "Medium Suitability (2)"),
                    ("#00ff00", "High Suitability (3)")
                ]
            },
            "deforestation": {
                "title": "Deforestation Analysis",
                "items": [
                    ("#ff0000", "Deforestation Areas"),
                    ("#006400", "Forest 2015"),
                    ("#00ff00", "Forest 2023"),
                    ("#ffffff", "NDVI Change")
                ]
            }
        }
        
        config = legend_configs.get(analysis_type, legend_configs["flood_risk"])
        
        # Create legend HTML with toggle functionality
        legend_html = f'''
        <div id="legend-container-{analysis_type}" style="position: fixed; 
                    bottom: 20px; left: 20px; z-index: 9999; 
                    font-family: Arial, sans-serif;">
            
            <!-- Toggle Button -->
            <div id="legend-toggle-{analysis_type}" style="
                background: #007bff;
                color: white;
                padding: 8px 15px;
                border-radius: 5px 5px 0 0;
                cursor: pointer;
                font-size: 13px;
                font-weight: bold;
                text-align: center;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                user-select: none;
                min-width: 120px;
            " onclick="toggleLegend_{analysis_type}()">
                📊 Legend ▼
            </div>
            
            <!-- Legend Content -->
            <div id="legend-content-{analysis_type}" style="
                background-color: rgba(255, 255, 255, 0.95); 
                border: 2px solid #333; 
                border-top: none;
                border-radius: 0 0 8px 8px; 
                font-size: 14px; 
                padding: 15px; 
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
                min-width: 200px;
                display: none;
            ">
                <p style="margin: 0 0 10px 0; font-weight: bold; font-size: 16px; color: #333;">{config['title']}</p>
        '''
        
        for color, label in config['items']:
            if color == "#ffffff":
                # Special styling for white items with border
                legend_html += f'<p style="margin: 5px 0; display: flex; align-items: center;"><span style="display: inline-block; width: 20px; height: 20px; background-color: {color}; border: 2px solid #000; margin-right: 8px;"></span> {label}</p>'
            else:
                legend_html += f'<p style="margin: 5px 0; display: flex; align-items: center;"><span style="display: inline-block; width: 20px; height: 20px; background-color: {color}; margin-right: 8px; border: 1px solid #333;"></span> {label}</p>'
        
        legend_html += '''
            </div>
        </div>
        '''
        
        # Add JavaScript for toggle functionality and legend management
        legend_html += f'''
        <script>
        // Toggle legend function for {analysis_type}
        function toggleLegend_{analysis_type}() {{
            const content = document.getElementById('legend-content-{analysis_type}');
            const toggle = document.getElementById('legend-toggle-{analysis_type}');
            
            if (content.style.display === 'none' || content.style.display === '') {{
                content.style.display = 'block';
                toggle.innerHTML = '📊 Legend ▲';
                toggle.style.borderRadius = '5px 5px 0 0';
            }} else {{
                content.style.display = 'none';
                toggle.innerHTML = '📊 Legend ▼';
                toggle.style.borderRadius = '5px';
            }}
        }}
        
        // Remove any existing legends when switching analyses
        function updateLegend_{analysis_type}() {{
            const existingLegends = document.querySelectorAll('[id^="legend-container-"]');
            existingLegends.forEach(legend => {{
                if (legend.id !== 'legend-container-{analysis_type}') {{
                    legend.remove();
                }}
            }});
        }}
        
        // Initialize legend as collapsed and clean up others
        document.addEventListener('DOMContentLoaded', function() {{
            updateLegend_{analysis_type}();
            const toggle = document.getElementById('legend-toggle-{analysis_type}');
            if (toggle) {{
                toggle.innerHTML = '📊 Legend ▼';
                toggle.style.borderRadius = '5px';
            }}
        }});
        </script>
        '''
        
        map_obj.get_root().html.add_child(folium.Element(legend_html))
    
    def generate_visualization_code(self, analysis_type: str, results: Dict[str, Any]) -> str:
        """
        Generate Python code for map visualization
        
        Args:
            analysis_type: Type of analysis
            results: Analysis results
            
        Returns:
            str: Python code for visualization
        """
        if analysis_type == "flood_risk":
            return self._generate_flood_risk_visualization_code()
        elif analysis_type == "solar_suitability":
            return self._generate_solar_suitability_visualization_code()
        elif analysis_type == "deforestation":
            return self._generate_deforestation_visualization_code()
        else:
            return "# Visualization code not available for this analysis type"
    
    def _generate_flood_risk_visualization_code(self) -> str:
        """Generate visualization code for flood risk analysis"""
        return '''
# Flood Risk Map Visualization
import folium
import ee

# Initialize Earth Engine
ee.Initialize()

# Create base map
m = folium.Map(
    location=[8.0, 77.0],  # Chennai coordinates
    zoom_start=10,
    tiles='OpenStreetMap'
)

# Add satellite imagery
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Satellite Imagery',
    overlay=False,
    control=True
).add_to(m)

# Add flood risk zones
flood_risk_vis = {
    'min': 0,
    'max': 3,
    'palette': ['green', 'yellow', 'orange', 'red'],
    'opacity': 0.7
}

# Get tile URL for flood risk zones
flood_risk_url = flood_risk_zones.getMapId(flood_risk_vis)['tile_fetcher'].url_format

folium.raster_layers.TileLayer(
    tiles=flood_risk_url,
    attr='Flood Risk Zones',
    name='Flood Risk Zones',
    overlay=True,
    control=True,
    opacity=0.7
).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Save map
m.save('flood_risk_map.html')
print("Flood risk map saved as 'flood_risk_map.html'")
'''
    
    def _generate_solar_suitability_visualization_code(self) -> str:
        """Generate visualization code for solar suitability analysis"""
        return '''
# Solar Suitability Map Visualization
import folium
import ee

# Initialize Earth Engine
ee.Initialize()

# Create base map
m = folium.Map(
    location=[8.0, 77.0],  # Chennai coordinates
    zoom_start=10,
    tiles='OpenStreetMap'
)

# Add satellite imagery
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Satellite Imagery',
    overlay=False,
    control=True
).add_to(m)

# Add solar suitability zones
suitability_vis = {
    'min': 0,
    'max': 3,
    'palette': ['red', 'orange', 'yellow', 'green'],
    'opacity': 0.7
}

# Get tile URL for suitability zones
suitability_url = suitability_zones.getMapId(suitability_vis)['tile_fetcher'].url_format

folium.raster_layers.TileLayer(
    tiles=suitability_url,
    attr='Solar Suitability Zones',
    name='Solar Suitability Zones',
    overlay=True,
    control=True,
    opacity=0.7
).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Save map
m.save('solar_suitability_map.html')
print("Solar suitability map saved as 'solar_suitability_map.html'")
'''
    
    def _generate_deforestation_visualization_code(self) -> str:
        """Generate visualization code for deforestation analysis"""
        return '''
# Deforestation Map Visualization
import folium
import ee

# Initialize Earth Engine
ee.Initialize()

# Create base map
m = folium.Map(
    location=[8.0, 77.0],  # Chennai coordinates
    zoom_start=10,
    tiles='OpenStreetMap'
)

# Add satellite imagery
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Satellite Imagery',
    overlay=False,
    control=True
).add_to(m)

# Add deforestation areas
deforestation_vis = {
    'min': 0,
    'max': 1,
    'palette': ['#000000', '#ff0000'],
    'opacity': 0.8
}

# Get tile URL for deforestation areas
deforestation_url = deforested_areas.getMapId(deforestation_vis)['tile_fetcher'].url_format

folium.raster_layers.TileLayer(
    tiles=deforestation_url,
    attr='Deforestation Areas',
    name='Deforestation Areas',
    overlay=True,
    control=True,
    opacity=0.8
).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Save map
m.save('deforestation_map.html')
print("Deforestation map saved as 'deforestation_map.html'")
'''
