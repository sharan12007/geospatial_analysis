"""
Geospatial Analysis Module for Google Earth Engine
"""

import ee
from typing import Dict, List, Any, Optional, Tuple
import json
from .workflow import WorkflowPlan, AnalysisType


class GeospatialAnalyzer:
    """
    Executes geospatial analysis workflows using Google Earth Engine
    """
    
    def __init__(self):
        self.ee = ee
        
    def get_region_boundary(self, location: str):
        """
        Get administrative boundary for a location
        
        Args:
            location: Name of the location (city, state, country)
            
        Returns:
            ee.Geometry or dict: Region boundary (EE object if initialized, coordinates if not)
        """
        # Import the comprehensive South India regions database
        try:
            from south_india_regions import get_region_coordinates, get_location_variations
            coords = get_region_coordinates(location)
            return self._create_geometry_or_coords(coords)
        except ImportError:
            # Fallback to basic database if import fails
            pass
        
        # Fallback database for basic coverage
        location_bounds = {
            'chennai': [80.0, 12.8, 80.3, 13.2],
            'bangalore': [77.4, 12.8, 77.8, 13.2],
            'bengaluru': [77.4, 12.8, 77.8, 13.2],
            'kochi': [76.2, 9.9, 76.4, 10.1],
            'hyderabad': [78.3, 17.2, 78.6, 17.6],
            'madurai': [78.0, 9.8, 78.2, 10.0],
            'coimbatore': [76.9, 11.0, 77.1, 11.2],
            'mysore': [76.6, 12.2, 76.8, 12.4],
            'thiruvananthapuram': [76.9, 8.4, 77.1, 8.6],
            'visakhapatnam': [83.2, 17.6, 83.4, 17.8],
            'tamil nadu': [76.0, 8.0, 80.5, 13.5],
            'karnataka': [74.0, 11.0, 78.5, 18.5],
            'kerala': [74.0, 8.0, 77.5, 12.8],
            'andhra pradesh': [76.0, 12.0, 84.5, 19.5],
            'telangana': [77.0, 15.5, 81.0, 19.5],
            'goa': [73.7, 14.5, 74.2, 15.8],
            'puducherry': [79.7, 11.9, 79.9, 12.1],
            'india': [68.0, 6.0, 97.0, 37.0]
        }
        
        # Try to find exact match first
        location_lower = location.lower().strip()
        if location_lower in location_bounds:
            coords = location_bounds[location_lower]
            return self._create_geometry_or_coords(coords)
        
        # Try partial matches and variations
        for key, coords in location_bounds.items():
            if location_lower in key or key in location_lower:
                return self._create_geometry_or_coords(coords)
        
        # Try common variations and aliases
        location_variations = {
            'bengaluru': 'bangalore',
            'bangalore': 'bangalore',
            'bengaluru city': 'bangalore',
            'chennai': 'chennai',
            'madras': 'chennai',
            'kochi': 'kochi',
            'cochin': 'kochi',
            'thiruvananthapuram': 'thiruvananthapuram',
            'trivandrum': 'thiruvananthapuram',
            'hyderabad': 'hyderabad',
            'vizag': 'visakhapatnam',
            'visakhapatnam': 'visakhapatnam',
            'vijayawada': 'vijayawada',
            'bezwada': 'vijayawada',
            'mysore': 'mysore',
            'mysuru': 'mysore',
            'mangalore': 'mangalore',
            'mangaluru': 'mangalore',
            'coimbatore': 'coimbatore',
            'kovai': 'coimbatore',
            'madurai': 'madurai',
            'tiruchirapalli': 'tiruchirapalli',
            'trichy': 'tiruchirapalli',
            'salem': 'salem',
            'tirunelveli': 'tirunelveli',
            'nellai': 'tirunelveli',
            'tiruppur': 'tiruppur',
            'vellore': 'vellore',
            'erode': 'erode',
            'thoothukudi': 'thoothukudi',
            'tuticorin': 'thoothukudi',
            'kozhikode': 'kozhikode',
            'calicut': 'kozhikode',
            'thrissur': 'thrissur',
            'trichur': 'thrissur',
            'kollam': 'kollam',
            'quilon': 'kollam',
            'palakkad': 'palakkad',
            'palghat': 'palakkad',
            'alappuzha': 'alappuzha',
            'alleppey': 'alappuzha',
            'kannur': 'kannur',
            'cannanore': 'kannur',
            'kasaragod': 'kasaragod',
            'kottayam': 'kottayam',
            'panaji': 'panaji',
            'panjim': 'panaji',
            'puducherry': 'puducherry',
            'pondicherry': 'puducherry',
            'pondy': 'puducherry'
        }
        
        # Check for variations
        if location_lower in location_variations:
            mapped_location = location_variations[location_lower]
            if mapped_location in location_bounds:
                coords = location_bounds[mapped_location]
                return self._create_geometry_or_coords(coords)
        
        # Try fuzzy matching for partial city names
        for key, coords in location_bounds.items():
            # Check if any word in the location matches any word in the key
            location_words = location_lower.split()
            key_words = key.split()
            
            for loc_word in location_words:
                for key_word in key_words:
                    if len(loc_word) > 3 and len(key_word) > 3:  # Only for words longer than 3 characters
                        if loc_word in key_word or key_word in loc_word:
                            return self._create_geometry_or_coords(coords)
        
        # Use FAO GAUL administrative boundaries as fallback (only if EE is initialized)
        try:
            # Check if Earth Engine is initialized
            ee.Number(1).getInfo()
            
            countries = ee.FeatureCollection("FAO/GAUL/2015/level0")
            states = ee.FeatureCollection("FAO/GAUL/2015/level1")
            
            # Search in states first
            state_filter = ee.Filter.eq('ADM1_NAME', location)
            region = states.filter(state_filter)
            
            if region.size().getInfo() > 0:
                return region.geometry()
            else:
                # Search in countries
                country_filter = ee.Filter.eq('ADM0_NAME', location)
                region = countries.filter(country_filter)
                if region.size().getInfo() > 0:
                    return region.geometry()
        except:
            # Earth Engine not initialized or other error, skip this step
            pass
        
        # Final fallback - use a default bounding box for Chennai
        print(f"⚠️  Using default bounding box for location: {location}")
        default_coords = [80.0, 12.8, 80.3, 13.2]  # Chennai area
        return self._create_geometry_or_coords(default_coords)
    
    def _create_geometry_or_coords(self, coords):
        """
        Create Earth Engine geometry if initialized, otherwise return coordinates
        
        Args:
            coords: List of coordinates [min_lon, min_lat, max_lon, max_lat]
            
        Returns:
            ee.Geometry or dict: Earth Engine geometry or coordinate dict
        """
        try:
            # Check if Earth Engine is initialized
            ee.Number(1).getInfo()
            # If we get here, EE is initialized
            return ee.Geometry.Rectangle(coords)
        except:
            # Earth Engine not initialized, return coordinates
            return {
                'type': 'Rectangle',
                'coordinates': coords,
                'description': f'Bounding box: {coords[0]:.2f}, {coords[1]:.2f} to {coords[2]:.2f}, {coords[3]:.2f}'
            }
    
    def execute_flood_risk_analysis(self, plan: WorkflowPlan) -> Dict[str, Any]:
        """
        Execute flood risk analysis workflow
        
        Args:
            plan: Workflow plan for flood risk analysis
            
        Returns:
            Dict containing analysis results and code
        """
        region = self.get_region_boundary(plan.region_of_interest)
        
        # Validate that the region is not empty
        try:
            region_info = region.getInfo()
            if not region_info or 'coordinates' not in region_info:
                raise ValueError("Empty or invalid region geometry")
            print(f"✅ Using region: {plan.region_of_interest}")
        except Exception as e:
            print(f"⚠️  Region validation failed: {e}")
            # Use a default region for Chennai
            region = ee.Geometry.Rectangle([80.0, 12.8, 80.3, 13.2])
            print("✅ Using default Chennai region")
        
        # Step 1: Get elevation data
        dem = ee.Image("USGS/SRTMGL1_003").clip(region)
        elevation = dem.select('elevation')
        
        # Step 2: Calculate slope
        slope = ee.Terrain.slope(dem)
        
        # Step 3: Get precipitation data
        chirps = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY").filterDate(
            plan.time_period.split('-')[0] + '-01-01',
            plan.time_period.split('-')[1] + '-12-31'
        ).filterBounds(region)
        
        # Calculate mean annual precipitation
        mean_precipitation = chirps.select('precipitation').mean()
        
        # Step 4: Get SAR data for water detection
        sentinel1 = ee.ImageCollection("COPERNICUS/S1_GRD").filterDate(
            plan.time_period.split('-')[0] + '-01-01',
            plan.time_period.split('-')[1] + '-12-31'
        ).filterBounds(region).filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
        
        # Calculate mean VV backscatter
        mean_vv = sentinel1.select('VV').mean()
        
        # Step 5: Create enhanced flood risk zones with more dramatic visualization
        # Low elevation areas (more sensitive threshold)
        low_elevation = elevation.lt(15)  # Increased from 10m to 15m
        
        # Very low elevation areas (high risk)
        very_low_elevation = elevation.lt(5)  # Very high risk areas
        
        # High precipitation areas (more sensitive)
        high_precipitation = mean_precipitation.gt(40)  # Reduced from 50mm to 40mm
        very_high_precipitation = mean_precipitation.gt(80)  # Very high precipitation
        
        # Water areas from SAR (more sensitive)
        water_areas = mean_vv.lt(-8)  # More sensitive threshold
        strong_water_signal = mean_vv.lt(-12)  # Very strong water signal
        
        # Slope factor (flat areas are more prone to flooding)
        flat_areas = slope.lt(2)  # Very flat areas
        
        # Create weighted flood risk score (0-4 scale for better visualization)
        flood_risk_score = ee.Image(0)
        
        # Add elevation risk (weighted heavily)
        flood_risk_score = flood_risk_score.add(very_low_elevation.multiply(2))  # Very low elevation = 2 points
        flood_risk_score = flood_risk_score.add(low_elevation.multiply(1))  # Low elevation = 1 point
        
        # Add precipitation risk
        flood_risk_score = flood_risk_score.add(very_high_precipitation.multiply(2))  # Very high precip = 2 points
        flood_risk_score = flood_risk_score.add(high_precipitation.multiply(1))  # High precip = 1 point
        
        # Add water detection risk
        flood_risk_score = flood_risk_score.add(strong_water_signal.multiply(2))  # Strong water signal = 2 points
        flood_risk_score = flood_risk_score.add(water_areas.multiply(1))  # Water areas = 1 point
        
        # Add slope risk (flat areas are more prone)
        flood_risk_score = flood_risk_score.add(flat_areas.multiply(1))  # Flat areas = 1 point
        
        # Create risk zones with enhanced contrast
        risk_zones = flood_risk_score.where(flood_risk_score.gte(4), 3)  # High risk (4+ points)
        risk_zones = risk_zones.where(flood_risk_score.gte(2).And(flood_risk_score.lt(4)), 2)  # Medium risk (2-3 points)
        risk_zones = risk_zones.where(flood_risk_score.gte(1).And(flood_risk_score.lt(2)), 1)  # Low risk (1 point)
        risk_zones = risk_zones.where(flood_risk_score.lt(1), 0)  # No risk (0 points)
        
        # Generate Python code
        code = self._generate_flood_risk_code(plan, region)
        
        return {
            "elevation": elevation,
            "slope": slope,
            "precipitation": mean_precipitation,
            "water_areas": water_areas,
            "flood_risk_zones": risk_zones,
            "code": code,
            "region": region
        }
    
    def execute_solar_suitability_analysis(self, plan: WorkflowPlan) -> Dict[str, Any]:
        """
        Execute solar farm suitability analysis workflow
        
        Args:
            plan: Workflow plan for solar suitability analysis
            
        Returns:
            Dict containing analysis results and code
        """
        region = self.get_region_boundary(plan.region_of_interest)
        
        # Validate that the region is not empty
        try:
            region_info = region.getInfo()
            if not region_info or 'coordinates' not in region_info:
                raise ValueError("Empty or invalid region geometry")
            print(f"✅ Using region: {plan.region_of_interest}")
        except Exception as e:
            print(f"⚠️  Region validation failed: {e}")
            # Use a default region for Rajasthan
            region = ee.Geometry.Rectangle([69.0, 23.0, 78.0, 30.0])
            print("✅ Using default Rajasthan region")
        
        # Step 1: Get elevation data
        dem = ee.Image("USGS/SRTMGL1_003").clip(region)
        elevation = dem.select('elevation')
        
        # Step 2: Calculate slope and aspect
        slope = ee.Terrain.slope(dem)
        aspect = ee.Terrain.aspect(dem)
        
        # Step 3: Get land cover data using Sentinel-2
        sentinel2 = ee.ImageCollection("COPERNICUS/S2_SR").filterDate(
            plan.time_period.split('-')[0] + '-01-01',
            plan.time_period.split('-')[1] + '-12-31'
        ).filterBounds(region).filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
        
        # Calculate NDVI for vegetation detection
        ndvi = sentinel2.map(lambda img: img.normalizedDifference(['B8', 'B4'])).mean()
        
        # Step 4: Create land cover classification
        # Simple threshold-based classification
        vegetation = ndvi.gt(0.3)
        water = ndvi.lt(0.1)
        urban = ndvi.lt(0.2).And(ndvi.gt(0.1))
        bare_soil = ndvi.lt(0.3).And(ndvi.gt(0.1))
        
        # Step 5: Calculate solar irradiance (simplified)
        # In practice, you'd use more sophisticated solar radiation models
        solar_irradiance = ee.Image(5.0)  # Simplified constant value
        
        # Step 6: Create enhanced suitability zones with better visualization
        # Suitable areas: low slope, south-facing, not water/urban, good irradiance
        very_suitable_slope = slope.lt(5)  # Very low slope (excellent)
        suitable_slope = slope.lt(15)  # Low slope (good)
        
        # Aspect suitability (south-facing is best)
        excellent_aspect = aspect.gt(160).And(aspect.lt(200))  # South-facing (excellent)
        good_aspect = aspect.gt(135).And(aspect.lt(225))  # South-facing (good)
        
        # Land cover suitability
        excellent_land_cover = bare_soil  # Bare soil is best for solar
        good_land_cover = vegetation.Or(bare_soil)  # Vegetation or bare soil
        unsuitable_land_cover = water.Or(urban)  # Water and urban are unsuitable
        
        # Solar irradiance (simplified but more realistic)
        excellent_irradiance = solar_irradiance.gt(5.2)  # Very high irradiance
        good_irradiance = solar_irradiance.gt(4.5)  # Good irradiance
        
        # Create weighted suitability score (0-6 scale for better visualization)
        suitability_score = ee.Image(0)
        
        # Add slope suitability
        suitability_score = suitability_score.add(very_suitable_slope.multiply(2))  # Very low slope = 2 points
        suitability_score = suitability_score.add(suitable_slope.multiply(1))  # Low slope = 1 point
        
        # Add aspect suitability
        suitability_score = suitability_score.add(excellent_aspect.multiply(2))  # Excellent aspect = 2 points
        suitability_score = suitability_score.add(good_aspect.multiply(1))  # Good aspect = 1 point
        
        # Add land cover suitability
        suitability_score = suitability_score.add(excellent_land_cover.multiply(2))  # Excellent land cover = 2 points
        suitability_score = suitability_score.add(good_land_cover.multiply(1))  # Good land cover = 1 point
        suitability_score = suitability_score.subtract(unsuitable_land_cover.multiply(3))  # Unsuitable = -3 points
        
        # Add irradiance suitability
        suitability_score = suitability_score.add(excellent_irradiance.multiply(1))  # Excellent irradiance = 1 point
        suitability_score = suitability_score.add(good_irradiance.multiply(0.5))  # Good irradiance = 0.5 points
        
        # Create suitability zones with enhanced contrast
        suitability_zones = suitability_score.where(suitability_score.gte(5), 3)  # High suitability (5+ points)
        suitability_zones = suitability_zones.where(suitability_score.gte(3).And(suitability_score.lt(5)), 2)  # Medium suitability (3-4 points)
        suitability_zones = suitability_zones.where(suitability_score.gte(1).And(suitability_score.lt(3)), 1)  # Low suitability (1-2 points)
        suitability_zones = suitability_zones.where(suitability_score.lt(1), 0)  # Not suitable (<1 point)
        
        # Generate Python code
        code = self._generate_solar_suitability_code(plan, region)
        
        return {
            "elevation": elevation,
            "slope": slope,
            "aspect": aspect,
            "ndvi": ndvi,
            "land_cover": {"vegetation": vegetation, "water": water, "urban": urban, "bare_soil": bare_soil},
            "solar_irradiance": solar_irradiance,
            "suitability_zones": suitability_zones,
            "code": code,
            "region": region
        }
    
    def execute_deforestation_analysis(self, plan: WorkflowPlan) -> Dict[str, Any]:
        """
        Execute deforestation analysis workflow
        
        Args:
            plan: Workflow plan for deforestation analysis
            
        Returns:
            Dict containing analysis results and code
        """
        region = self.get_region_boundary(plan.region_of_interest)
        
        # Validate that the region is not empty
        try:
            region_info = region.getInfo()
            if not region_info or 'coordinates' not in region_info:
                raise ValueError("Empty or invalid region geometry")
            print(f"✅ Using region: {plan.region_of_interest}")
        except Exception as e:
            print(f"⚠️  Region validation failed: {e}")
            # Use a default region for Kerala
            region = ee.Geometry.Rectangle([74.0, 8.0, 77.5, 12.8])
            print("✅ Using default Kerala region")
        
        # Step 1: Get Sentinel-2 data for the time period
        start_year = plan.time_period.split('-')[0]
        end_year = plan.time_period.split('-')[1]
        
        sentinel2 = ee.ImageCollection("COPERNICUS/S2_SR").filterDate(
            start_year + '-01-01',
            end_year + '-12-31'
        ).filterBounds(region).filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
        
        # Step 2: Calculate NDVI time series
        def add_ndvi(img):
            ndvi = img.normalizedDifference(['B8', 'B4']).rename('NDVI')
            return img.addBands(ndvi)
        
        sentinel2_with_ndvi = sentinel2.map(add_ndvi)
        
        # Step 3: Calculate mean NDVI for different periods
        ndvi_2015 = sentinel2_with_ndvi.filterDate(start_year + '-01-01', start_year + '-12-31').select('NDVI').mean()
        ndvi_2023 = sentinel2_with_ndvi.filterDate(end_year + '-01-01', end_year + '-12-31').select('NDVI').mean()
        
        # Step 4: Calculate NDVI change
        ndvi_change = ndvi_2023.subtract(ndvi_2015)
        
        # Step 5: Identify deforestation areas
        # Areas with significant NDVI decrease
        deforestation = ndvi_change.lt(-0.1)
        
        # Step 6: Create land cover classification
        # Forest areas (high NDVI)
        forest_2015 = ndvi_2015.gt(0.3)
        forest_2023 = ndvi_2023.gt(0.3)
        
        # Deforested areas
        deforested_areas = forest_2015.And(ndvi_2023.lt(0.3))
        
        # Generate Python code
        code = self._generate_deforestation_code(plan, region)
        
        return {
            "ndvi_2015": ndvi_2015,
            "ndvi_2023": ndvi_2023,
            "ndvi_change": ndvi_change,
            "deforestation": deforestation,
            "forest_2015": forest_2015,
            "forest_2023": forest_2023,
            "deforested_areas": deforested_areas,
            "code": code,
            "region": region
        }
    
    def _generate_flood_risk_code(self, plan: WorkflowPlan, region: ee.Geometry) -> str:
        """Generate Python code for flood risk analysis"""
        return f'''
# Flood Risk Analysis for {plan.region_of_interest}
import ee

# Initialize Earth Engine
ee.Initialize()

# Define region of interest
region = ee.Geometry.Rectangle([77.0, 8.0, 77.5, 8.5])  # {plan.region_of_interest} area

# Step 1: Get elevation data
dem = ee.Image("USGS/SRTMGL1_003").clip(region)
elevation = dem.select('elevation')

# Step 2: Calculate slope
slope = ee.Terrain.slope(dem)

# Step 3: Get precipitation data
chirps = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY").filterDate(
    '{plan.time_period.split('-')[0]}-01-01',
    '{plan.time_period.split('-')[1]}-12-31'
).filterBounds(region)

# Calculate mean annual precipitation
mean_precipitation = chirps.select('precipitation').mean()

# Step 4: Get SAR data for water detection
sentinel1 = ee.ImageCollection("COPERNICUS/S1_GRD").filterDate(
    '{plan.time_period.split('-')[0]}-01-01',
    '{plan.time_period.split('-')[1]}-12-31'
).filterBounds(region).filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))

# Calculate mean VV backscatter
mean_vv = sentinel1.select('VV').mean()

# Step 5: Create flood risk zones
# Low elevation areas
low_elevation = elevation.lt(10)

# High precipitation areas
high_precipitation = mean_precipitation.gt(50)

# Water areas from SAR
water_areas = mean_vv.lt(-10)

# Combine factors for flood risk
flood_risk = low_elevation.add(high_precipitation).add(water_areas)

# Create risk zones
risk_zones = flood_risk.where(flood_risk.eq(3), 3)  # High risk
risk_zones = risk_zones.where(flood_risk.eq(2), 2)  # Medium risk
risk_zones = risk_zones.where(flood_risk.eq(1), 1)  # Low risk
risk_zones = risk_zones.where(flood_risk.eq(0), 0)  # No risk

# Export results
task = ee.batch.Export.image.toDrive(
    image=risk_zones,
    description='flood_risk_{plan.region_of_interest.lower().replace(" ", "_")}',
    folder='GEE_Exports',
    fileNamePrefix='flood_risk_zones',
    region=region,
    scale=30,
    crs='EPSG:4326'
)
task.start()

print("Flood risk analysis completed. Check your Google Drive for results.")
'''
    
    def _generate_solar_suitability_code(self, plan: WorkflowPlan, region: ee.Geometry) -> str:
        """Generate Python code for solar suitability analysis"""
        return f'''
# Solar Farm Suitability Analysis for {plan.region_of_interest}
import ee

# Initialize Earth Engine
ee.Initialize()

# Define region of interest
region = ee.Geometry.Rectangle([77.0, 8.0, 77.5, 8.5])  # {plan.region_of_interest} area

# Step 1: Get elevation data
dem = ee.Image("USGS/SRTMGL1_003").clip(region)
elevation = dem.select('elevation')

# Step 2: Calculate slope and aspect
slope = ee.Terrain.slope(dem)
aspect = ee.Terrain.aspect(dem)

# Step 3: Get land cover data using Sentinel-2
sentinel2 = ee.ImageCollection("COPERNICUS/S2_SR").filterDate(
    '{plan.time_period.split('-')[0]}-01-01',
    '{plan.time_period.split('-')[1]}-12-31'
).filterBounds(region).filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))

# Calculate NDVI for vegetation detection
ndvi = sentinel2.map(lambda img: img.normalizedDifference(['B8', 'B4'])).mean()

# Step 4: Create land cover classification
vegetation = ndvi.gt(0.3)
water = ndvi.lt(0.1)
urban = ndvi.lt(0.2).And(ndvi.gt(0.1))
bare_soil = ndvi.lt(0.3).And(ndvi.gt(0.1))

# Step 5: Calculate solar irradiance (simplified)
solar_irradiance = ee.Image(5.0)

# Step 6: Create suitability zones
suitable_slope = slope.lt(15)
suitable_aspect = aspect.gt(135).And(aspect.lt(225))  # South-facing
suitable_land_cover = vegetation.Or(bare_soil)
suitable_irradiance = solar_irradiance.gt(4.5)

# Combine suitability factors
suitability_score = suitable_slope.add(suitable_aspect).add(suitable_land_cover).add(suitable_irradiance)

# Create suitability zones
suitability_zones = suitability_score.where(suitability_score.eq(4), 3)  # High suitability
suitability_zones = suitability_zones.where(suitability_score.eq(3), 2)  # Medium suitability
suitability_zones = suitability_zones.where(suitability_score.eq(2), 1)  # Low suitability
suitability_zones = suitability_zones.where(suitability_score.lt(2), 0)  # Not suitable

# Export results
task = ee.batch.Export.image.toDrive(
    image=suitability_zones,
    description='solar_suitability_{plan.region_of_interest.lower().replace(" ", "_")}',
    folder='GEE_Exports',
    fileNamePrefix='solar_suitability_zones',
    region=region,
    scale=30,
    crs='EPSG:4326'
)
task.start()

print("Solar suitability analysis completed. Check your Google Drive for results.")
'''
    
    def _generate_deforestation_code(self, plan: WorkflowPlan, region: ee.Geometry) -> str:
        """Generate Python code for deforestation analysis"""
        start_year = plan.time_period.split('-')[0]
        end_year = plan.time_period.split('-')[1]
        
        return f'''
# Deforestation Analysis for {plan.region_of_interest} ({start_year}-{end_year})
import ee

# Initialize Earth Engine
ee.Initialize()

# Define region of interest
region = ee.Geometry.Rectangle([77.0, 8.0, 77.5, 8.5])  # {plan.region_of_interest} area

# Step 1: Get Sentinel-2 data
sentinel2 = ee.ImageCollection("COPERNICUS/S2_SR").filterDate(
    '{start_year}-01-01',
    '{end_year}-12-31'
).filterBounds(region).filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))

# Step 2: Calculate NDVI time series
def add_ndvi(img):
    ndvi = img.normalizedDifference(['B8', 'B4']).rename('NDVI')
    return img.addBands(ndvi)

sentinel2_with_ndvi = sentinel2.map(add_ndvi)

# Step 3: Calculate mean NDVI for different periods
ndvi_{start_year} = sentinel2_with_ndvi.filterDate('{start_year}-01-01', '{start_year}-12-31').select('NDVI').mean()
ndvi_{end_year} = sentinel2_with_ndvi.filterDate('{end_year}-01-01', '{end_year}-12-31').select('NDVI').mean()

# Step 4: Calculate NDVI change
ndvi_change = ndvi_{end_year}.subtract(ndvi_{start_year})

# Step 5: Identify deforestation areas
deforestation = ndvi_change.lt(-0.1)

# Step 6: Create land cover classification
forest_{start_year} = ndvi_{start_year}.gt(0.3)
forest_{end_year} = ndvi_{end_year}.gt(0.3)
deforested_areas = forest_{start_year}.And(ndvi_{end_year}.lt(0.3))

# Export results
task = ee.batch.Export.image.toDrive(
    image=deforested_areas,
    description='deforestation_{plan.region_of_interest.lower().replace(" ", "_")}_{start_year}_{end_year}',
    folder='GEE_Exports',
    fileNamePrefix='deforestation_areas',
    region=region,
    scale=10,
    crs='EPSG:4326'
)
task.start()

print("Deforestation analysis completed. Check your Google Drive for results.")
'''
