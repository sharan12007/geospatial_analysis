"""
GeoGPT - Main Interface for Geospatial Analysis
This is the main entry point for GeoGPT functionality
"""

from geogpt import GEEAuthenticator, WorkflowPlanner, GeospatialAnalyzer, MapVisualizer
from typing import Dict, Any
import json


class GeoGPT:
    """
    Main GeoGPT class that orchestrates geospatial analysis workflows
    """
    
    def __init__(self, client_id: str = None):
        """
        Initialize GeoGPT with OAuth2 client ID
        
        Args:
            client_id: OAuth2 Client ID for Google Earth Engine authentication
        """
        self.client_id = client_id
        self.authenticator = GEEAuthenticator(client_id) if client_id else None
        self.planner = WorkflowPlanner()
        self.analyzer = GeospatialAnalyzer()
        self.visualizer = MapVisualizer()
        
    def analyze(self, query: str, location: str, time_period: str = "2020-2023") -> Dict[str, Any]:
        """
        Perform geospatial analysis based on user query
        
        Args:
            query: User's geospatial analysis query
            location: Location of interest
            time_period: Time period for analysis
            
        Returns:
            Dict containing workflow plan, results, code, and visualization
        """
        print(f"🌍 GeoGPT Analysis: {query}")
        print(f"📍 Location: {location}")
        print(f"📅 Time Period: {time_period}")
        print("-" * 60)
        
        # Step 1: Plan the workflow
        print("📋 Planning workflow...")
        workflow_plan = self.planner.plan_analysis(query, location, time_period)
        
        print("Workflow Plan:")
        for i, step in enumerate(workflow_plan.steps, 1):
            print(f"  {i}. {step.description}")
            print(f"     Method: {step.method}")
            if step.datasets:
                print(f"     Datasets: {[d.name for d in step.datasets]}")
            print()
        
        # Step 2: Execute the analysis
        print("🔬 Executing analysis...")
        if workflow_plan.analysis_type.value == "flood_risk":
            results = self.analyzer.execute_flood_risk_analysis(workflow_plan)
        elif workflow_plan.analysis_type.value == "solar_suitability":
            results = self.analyzer.execute_solar_suitability_analysis(workflow_plan)
        elif workflow_plan.analysis_type.value == "deforestation":
            results = self.analyzer.execute_deforestation_analysis(workflow_plan)
        else:
            raise ValueError(f"Unsupported analysis type: {workflow_plan.analysis_type}")
        
        # Step 3: Create visualization
        print("🗺️ Creating map visualization...")
        if workflow_plan.analysis_type.value == "flood_risk":
            map_html = self.visualizer.create_flood_risk_map(results, results['region'])
        elif workflow_plan.analysis_type.value == "solar_suitability":
            map_html = self.visualizer.create_solar_suitability_map(results, results['region'])
        elif workflow_plan.analysis_type.value == "deforestation":
            map_html = self.visualizer.create_deforestation_map(results, results['region'])
        
        # Step 4: Generate summary
        print("📊 Generating summary...")
        summary = self._generate_summary(workflow_plan, results)
        
        return {
            "workflow_plan": workflow_plan,
            "results": results,
            "map_html": map_html,
            "summary": summary,
            "analysis_type": workflow_plan.analysis_type.value
        }
    
    def _generate_summary(self, workflow_plan, results) -> str:
        """Generate analysis summary based on workflow plan and results"""
        
        analysis_type = workflow_plan.analysis_type.value
        
        if analysis_type == "flood_risk":
            return self._generate_flood_risk_summary(workflow_plan, results)
        elif analysis_type == "solar_suitability":
            return self._generate_solar_suitability_summary(workflow_plan, results)
        elif analysis_type == "deforestation":
            return self._generate_deforestation_summary(workflow_plan, results)
        else:
            return "Summary not available for this analysis type."
    
    def _generate_flood_risk_summary(self, workflow_plan, results) -> str:
        """Generate flood risk analysis summary"""
        return f"""
🌊 FLOOD RISK ANALYSIS SUMMARY
{'=' * 50}

📍 Location: {workflow_plan.region_of_interest}
📅 Analysis Period: {workflow_plan.time_period}

🔍 ANALYSIS METHODOLOGY:
{workflow_plan.visualization_instructions}

📊 KEY FINDINGS:
• Elevation Analysis: Identified low-lying areas below 10m elevation
• Precipitation Analysis: Analyzed rainfall patterns using CHIRPS data
• SAR Analysis: Used Sentinel-1 data to detect water bodies
• Risk Zoning: Combined factors to create flood risk zones

🎯 RISK ZONES:
• High Risk (Red): Areas with low elevation + high precipitation + water detection
• Medium Risk (Orange): Areas with 2 out of 3 risk factors
• Low Risk (Yellow): Areas with 1 risk factor
• No Risk (Green): Areas with no significant risk factors

📈 RECOMMENDATIONS:
1. Focus flood preparedness efforts on high-risk zones
2. Implement early warning systems in medium-risk areas
3. Consider land use planning restrictions in high-risk zones
4. Monitor precipitation patterns during monsoon seasons

🔧 TECHNICAL DETAILS:
• Datasets Used: SRTM DEM, CHIRPS Precipitation, Sentinel-1 SAR
• Spatial Resolution: 30m (DEM), 5km (Precipitation), 10m (SAR)
• Analysis Method: Multi-criteria risk assessment
• Output Format: GeoTIFF and interactive web map

⚠️  DISCLAIMER:
This analysis is for research and planning purposes. For official flood risk assessment, 
consult with local authorities and use additional local data sources.
"""
    
    def _generate_solar_suitability_summary(self, workflow_plan, results) -> str:
        """Generate solar suitability analysis summary"""
        return f"""
☀️ SOLAR FARM SUITABILITY ANALYSIS SUMMARY
{'=' * 50}

📍 Location: {workflow_plan.region_of_interest}
📅 Analysis Period: {workflow_plan.time_period}

🔍 ANALYSIS METHODOLOGY:
{workflow_plan.visualization_instructions}

📊 KEY FINDINGS:
• Slope Analysis: Identified areas with slopes < 15° for optimal panel installation
• Aspect Analysis: Prioritized south-facing slopes (135°-225°) for maximum sun exposure
• Land Cover Analysis: Excluded water bodies, urban areas, and dense forests
• Solar Irradiance: Assessed solar energy potential across the region

🎯 SUITABILITY ZONES:
• High Suitability (Green): Optimal conditions for solar farm development
• Medium Suitability (Yellow): Good conditions with minor constraints
• Low Suitability (Orange): Challenging conditions requiring careful planning
• Not Suitable (Red): Areas with significant constraints

📈 RECOMMENDATIONS:
1. Prioritize high-suitability zones for large-scale solar projects
2. Consider medium-suitability areas for smaller installations
3. Avoid areas with steep slopes or poor solar exposure
4. Ensure proper environmental impact assessment for all sites

🔧 TECHNICAL DETAILS:
• Datasets Used: SRTM DEM, Sentinel-2 MSI, Solar Irradiance Models
• Spatial Resolution: 30m (DEM), 10-20m (Sentinel-2)
• Analysis Method: Multi-criteria suitability assessment
• Output Format: GeoTIFF and interactive web map

⚠️  DISCLAIMER:
This analysis is for preliminary site assessment. For actual project development,
conduct detailed feasibility studies including environmental impact assessment,
grid connectivity analysis, and local regulatory compliance.
"""
    
    def _generate_deforestation_summary(self, workflow_plan, results) -> str:
        """Generate deforestation analysis summary"""
        return f"""
🌳 DEFORESTATION ANALYSIS SUMMARY
{'=' * 50}

📍 Location: {workflow_plan.region_of_interest}
📅 Analysis Period: {workflow_plan.time_period}

🔍 ANALYSIS METHODOLOGY:
{workflow_plan.visualization_instructions}

📊 KEY FINDINGS:
• NDVI Time Series: Analyzed vegetation health changes over time
• Change Detection: Identified areas with significant NDVI decrease
• Land Cover Classification: Mapped forest, agriculture, urban, and other land types
• Deforestation Quantification: Calculated area and extent of forest loss

🎯 DEFORESTATION PATTERNS:
• Deforestation Areas (Red): Areas where forest cover was lost
• Forest Cover 2015 (Dark Green): Initial forest extent
• Forest Cover 2023 (Light Green): Current forest extent
• NDVI Change: Vegetation health changes (red = loss, green = gain)

📈 RECOMMENDATIONS:
1. Focus conservation efforts on remaining forest areas
2. Investigate causes of deforestation in identified hotspots
3. Implement reforestation programs in suitable areas
4. Strengthen forest protection and monitoring systems

🔧 TECHNICAL DETAILS:
• Datasets Used: Sentinel-2 MSI, NDVI Time Series
• Spatial Resolution: 10-20m
• Analysis Method: Change detection using NDVI thresholds
• Output Format: GeoTIFF and interactive web map

⚠️  DISCLAIMER:
This analysis is for research and monitoring purposes. For official forest cover
assessment, consult with forest departments and use additional ground truth data.
"""
    
    def save_results(self, analysis_results: Dict[str, Any], output_dir: str = ".") -> None:
        """
        Save analysis results to files
        
        Args:
            analysis_results: Results from analyze() method
            output_dir: Directory to save files
        """
        import os
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Save map HTML
        map_filename = f"{analysis_results['analysis_type']}_map.html"
        map_path = os.path.join(output_dir, map_filename)
        with open(map_path, 'w') as f:
            f.write(analysis_results['map_html'])
        
        # Save generated code
        code_filename = f"{analysis_results['analysis_type']}_code.py"
        code_path = os.path.join(output_dir, code_filename)
        with open(code_path, 'w') as f:
            f.write(analysis_results['results']['code'])
        
        # Save summary
        summary_filename = f"{analysis_results['analysis_type']}_summary.txt"
        summary_path = os.path.join(output_dir, summary_filename)
        with open(summary_path, 'w') as f:
            f.write(analysis_results['summary'])
        
        print(f"✅ Results saved to {output_dir}/")
        print(f"📁 Files generated:")
        print(f"  - {map_filename} (Interactive map)")
        print(f"  - {code_filename} (Executable GEE code)")
        print(f"  - {summary_filename} (Analysis summary)")


def main():
    """
    Main function for command-line usage
    """
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python geogpt_main.py <query> <location> [time_period]")
        print("Example: python geogpt_main.py 'Find flood-prone areas in Chennai' 'Chennai' '2020-2023'")
        return
    
    query = sys.argv[1]
    location = sys.argv[2]
    time_period = sys.argv[3] if len(sys.argv) > 3 else "2020-2023"
    
    # Initialize GeoGPT
    geogpt = GeoGPT("108832868460957844084")
    
    # Perform analysis
    results = geogpt.analyze(query, location, time_period)
    
    # Save results
    geogpt.save_results(results)
    
    # Print summary
    print("\n" + results['summary'])


if __name__ == "__main__":
    main()
