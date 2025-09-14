#!/usr/bin/env python3
"""
Enhanced GeoGPT Streamlit Application
Matching the wireframe design with Tavily search and Groq LLM integration
"""

import streamlit as st
import sys
import os
import json
import requests
from datetime import datetime
import tempfile

# Add the current directory to Python path
sys.path.insert(0, '.')

from geogpt.auth import GEEAuthenticator
from geogpt.workflow import WorkflowPlanner
from geogpt.analyzer import GeospatialAnalyzer
from geogpt.visualizer import MapVisualizer

# Configure Streamlit page
st.set_page_config(
    page_title="GeoGPT - Geospatial Analysis Assistant",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for wireframe-style design
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        color: #1f77b4;
    }
    
    .query-input-container {
        background-color: #f8f9fa;
        padding: 0.01rem;
        border-radius: 10px;
        height: 0.5px;
        margin-bottom: 2rem;
        border: 2px solid #e9ecef;
    }
    
    .chain-of-thought {
        background-color: #fff3cd;
        padding: 0.075rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin-bottom: 1rem;
    }
    
    .results-section {
        background-color: #d1ecf1;
        padding: 0.075rem;
        border-radius: 8px;
        border-left: 4px solid #17a2b8;
        margin-top: 1rem;
    }
    
    .insights-section {
        background-color: #f8d7da;
        padding: 0.075rem;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        margin-bottom: 1rem;
    }
    
    .workflow-section {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
    }
    
    .map-container {
        border: 2px solid #dee2e6;
        border-radius: 8px;
        padding: 0.075rem;
        background-color: #ffffff;
    }
    
    .layer-controls {
        background-color: #f8f9fa;
        padding: 0.075rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
    }
    
    .stButton > button {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background-color: #0056b3;
    }
    
    /* Hide sidebar completely */
    .css-1d391kg {
        display: none;
    }
    
    .css-1v0mbdj {
        display: none;
    }
    
    /* Ensure main content takes full width */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
</style>
""", unsafe_allow_html=True)

class TavilySearch:
    """Tavily search integration for geospatial and natural disaster news"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.tavily.com/search"
    
    def search_geospatial_news(self, query: str, location: str, analysis_type: str, max_results: int = 5) -> list:
        """Search for geospatial and natural disaster news specific to the region and analysis type"""
        try:
            # Define geospatial keywords based on analysis type
            geospatial_keywords = {
                'flood_risk': [
                    'flood', 'flooding', 'flood risk', 'flood zones', 'water levels',
                    'rainfall', 'precipitation', 'storm', 'cyclone', 'monsoon',
                    'drainage', 'water management', 'flood control', 'disaster management',
                    'extreme weather', 'climate change', 'sea level rise'
                ],
                'solar_suitability': [
                    'solar energy', 'renewable energy', 'solar power', 'solar panels',
                    'clean energy', 'solar projects', 'energy policy', 'solar farms',
                    'renewable resources', 'sustainable energy', 'green energy',
                    'solar installation', 'photovoltaic', 'solar capacity'
                ],
                'deforestation': [
                    'deforestation', 'forest loss', 'tree cutting', 'forest conservation',
                    'environmental impact', 'biodiversity', 'forest fires', 'wildlife',
                    'carbon emissions', 'climate change', 'environmental protection',
                    'forest restoration', 'afforestation', 'green cover', 'ecosystem'
                ]
            }
            
            # Get relevant keywords for the analysis type
            keywords = geospatial_keywords.get(analysis_type, [
                'geospatial', 'satellite', 'remote sensing', 'GIS', 'mapping',
                'environmental', 'natural disaster', 'climate', 'weather'
            ])
            
            # Create targeted search query
            keyword_string = ' OR '.join(keywords[:5])  # Use top 5 keywords
            search_query = f"({keyword_string}) AND {location} recent news 2025 and 2024"
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "query": search_query,
                "max_results": max_results * 2,  # Get more results to filter
                "include_domains": [
                    "bbc.com", "reuters.com", "weather.com", "floodlist.com",
                    "timesofindia.indiatimes.com", "thehindu.com", "indianexpress.com",
                    "downtoearth.org.in", "mongabay.com", "news.mongabay.com",
                    "climate.gov", "noaa.gov", "nasa.gov", "esa.int"
                ],
                "search_depth": "advanced"
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            raw_results = data.get('results', [])
            
            # Filter results for geospatial relevance
            filtered_results = self._filter_geospatial_results(
                raw_results, 
                keywords, 
                location
            )
            
            return filtered_results[:max_results]  # Return top results
            
        except Exception as e:
            st.error(f"Tavily geospatial search error: {str(e)}")
            return []
    
    def _filter_geospatial_results(self, results: list, keywords: list, location: str) -> list:
        """Filter search results for geospatial relevance"""
        filtered = []
        
        for result in results:
            title = result.get('title', '').lower()
            content = result.get('content', '').lower()
            url = result.get('url', '').lower()
            
            # Check if result contains geospatial keywords
            text_to_check = f"{title} {content} {url}"
            
            # Must contain location and at least one geospatial keyword
            if location.lower() in text_to_check:
                keyword_matches = sum(1 for keyword in keywords if keyword.lower() in text_to_check)
                if keyword_matches > 0:
                    # Add relevance score and keywords found
                    result['relevance_score'] = keyword_matches
                    result['geospatial_keywords_found'] = [
                        kw for kw in keywords if kw.lower() in text_to_check
                    ]
                    result['location_mentioned'] = location
                    filtered.append(result)
        
        # Sort by relevance score
        filtered.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        return filtered

class GroqLLM:
    """Groq LLM integration for enhanced analysis summaries"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
    
    def generate_summary(self, query: str, analysis_results: dict, recent_data: list = None) -> str:
        """Generate enhanced analysis summary using Groq LLM"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Prepare context
            context = f"""
            Query: {query}
            Analysis Type: {analysis_results.get('analysis_type', 'Unknown')}
            Location: {analysis_results.get('location', 'Unknown')}
            Time Period: {analysis_results.get('time_period', 'Unknown')}
            """
            
            if recent_data:
                context += "\nRecent Data:\n"
                for item in recent_data[:2]:  # Use top 2 results
                    context += f"- {item.get('title', 'No title')}: {item.get('content', 'No content')[:200]}...\n"
            
            prompt = f"""
            You are a geospatial analysis expert. Based on the following query and analysis results, provide a comprehensive, direct answer to the user's question.
            
            Context: {context}
            
            Please provide:
            1. A direct answer to the user's question
            2. Specific locations or areas identified
            3. Key findings and insights
            4. Any relevant recent developments from the data provided
            
            Format your response as a clear, informative summary that directly answers the user's question.
            """
            
            # Try different model names in order of preference
            models_to_try = [
                "openai/gpt-oss-20b"
            ]
            
            for model_name in models_to_try:
                try:
                    payload = {
                        "model": model_name,
                        "messages": [
                            {"role": "system", "content": "You are a helpful geospatial analysis assistant."},
                            {"role": "user", "content": prompt}
                        ],
                        "max_tokens": 500,
                        "temperature": 0.7,
                        "stream": False
                    }
                    
                    response = requests.post(self.base_url, headers=headers, json=payload)
                    response.raise_for_status()
                    
                    data = response.json()
                    return data['choices'][0]['message']['content']
                    
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 400:
                        # Try next model
                        continue
                    else:
                        raise e
                except Exception as e:
                    # Try next model
                    continue
            
            # If all models fail, return a generic error
            return "Unable to generate enhanced summary due to API configuration issues."
            
        except Exception as e:
            st.error(f"Groq LLM error: {str(e)}")
            return "Unable to generate enhanced summary due to API error."
    
    def test_connection(self) -> bool:
        """Test Groq API connection"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 10
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload)
            return response.status_code == 200
            
        except:
            return False

def initialize_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'workflow_plan' not in st.session_state:
        st.session_state.workflow_plan = None
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'map_html' not in st.session_state:
        st.session_state.map_html = None
    if 'chain_of_thought' not in st.session_state:
        st.session_state.chain_of_thought = []
    if 'recent_data' not in st.session_state:
        st.session_state.recent_data = []
    if 'enhanced_summary' not in st.session_state:
        st.session_state.enhanced_summary = ""
    if 'analysis_in_progress' not in st.session_state:
        st.session_state.analysis_in_progress = False
    if 'analysis_completed' not in st.session_state:
        st.session_state.analysis_completed = False

def display_header():
    """Display the main header"""
    st.markdown('<h1 class="main-header">🌍 Geospatial Analysis Assistant</h1>', unsafe_allow_html=True)

def display_query_input():
    """Display the query input section matching the wireframe"""
    st.markdown('<div class="query-input-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([4, 1, 1])
    
    with col1:
        query = st.text_input(
            "Query Input",
            placeholder="Ask a query like 'SHOW FLOOD PRONE ZONES IN CHENNAI'",
            label_visibility="collapsed",
            key="main_query"
        )
    
    with col2:
        st.markdown("🎤")  # Microphone icon placeholder
    
    with col3:
        col3a, col3b = st.columns(2)
        with col3a:
            analyse_clicked = st.button("Analyse", type="primary", key="analyse_btn")
        with col3b:
            refresh_clicked = st.button("🔄", help="Refresh UI", key="refresh_btn")
    
    # Show status if analysis is in progress or completed
    if st.session_state.get('analysis_in_progress', False):
        st.info("🔄 Analysis in progress...")
    elif st.session_state.get('analysis_completed', False):
        st.success("✅ Analysis completed!")
    
    # Handle refresh button
    if refresh_clicked:
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return query, analyse_clicked

def display_chain_of_thought():
    """Display chain-of-thought section"""
    if st.session_state.chain_of_thought:
        st.markdown('<div class="chain-of-thought">', unsafe_allow_html=True)
        st.markdown("**Chain-of-Thought:**")
        for step in st.session_state.chain_of_thought:
            st.markdown(f"→ {step}")
        st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state.get('analysis_in_progress', False):
        st.markdown('<div class="chain-of-thought">', unsafe_allow_html=True)
        st.markdown("**Chain-of-Thought:**")
        st.info("🔄 Analyzing query and planning workflow...")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="chain-of-thought">', unsafe_allow_html=True)
        st.markdown("**Chain-of-Thought:**")
        st.info("Analysis steps will appear here after processing.")
        st.markdown('</div>', unsafe_allow_html=True)

def display_layer_controls():
    """Display layer toggle controls"""
    st.markdown('<div class="layer-controls">', unsafe_allow_html=True)
    st.markdown("**Layer Controls:**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        risk_zones = st.checkbox("Risk zones", value=True, key="risk_zones")
    
    with col2:
        dem_data = st.checkbox("DEM data", value=True, key="dem_data")
    
    with col3:
        satellite_map = st.checkbox("Satellite map", value=True, key="satellite_map")
    
    with col4:
        precipitation = st.checkbox("Precipitation", value=False, key="precipitation")
    
    # Additional layer controls in a second row
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        ndvi_layer = st.checkbox("NDVI", value=False, key="ndvi_layer")
    
    with col6:
        water_bodies = st.checkbox("Water bodies", value=False, key="water_bodies")
    
    with col7:
        urban_areas = st.checkbox("Urban areas", value=False, key="urban_areas")
    
    with col8:
        forest_cover = st.checkbox("Forest cover", value=False, key="forest_cover")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return {
        'risk_zones': risk_zones,
        'dem_data': dem_data,
        'satellite_map': satellite_map,
        'precipitation': precipitation,
        'ndvi_layer': ndvi_layer,
        'water_bodies': water_bodies,
        'urban_areas': urban_areas,
        'forest_cover': forest_cover
    }

def display_map_visualization():
    """Display the map visualization"""
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    st.markdown("**Map**")
    
    if st.session_state.map_html:
        # Create a temporary HTML file and display it
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(st.session_state.map_html)
            temp_file = f.name
        
        try:
            with open(temp_file, 'r', encoding='utf-8') as f:
                map_content = f.read()
            
            st.components.v1.html(map_content, height=500)
            
            # Clean up
            os.unlink(temp_file)
            
        except Exception as e:
            st.error(f"Error displaying map: {str(e)}")
    else:
        st.info("Map output area with marked locations")
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_results():
    """Display the results section with enhanced summary"""
    if st.session_state.enhanced_summary:
        st.markdown('<div class="results-section">', unsafe_allow_html=True)
        st.markdown("**Results:**")
        st.markdown(st.session_state.enhanced_summary)
        st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state.get('analysis_in_progress', False):
        st.markdown('<div class="results-section">', unsafe_allow_html=True)
        st.markdown("**Results:**")
        st.info("🔄 Generating analysis results...")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="results-section">', unsafe_allow_html=True)
        st.markdown("**Results:**")
        st.info("Enter a query and click 'Analyse' to see results here.")
        st.markdown('</div>', unsafe_allow_html=True)

def display_live_insights():
    """Display geospatial news and insights section"""
    if st.session_state.recent_data:
        st.markdown('<div class="insights-section">', unsafe_allow_html=True)
        st.markdown("**🌍 Geospatial News & Insights:**")
        
        for i, item in enumerate(st.session_state.recent_data[:3]):
            # Display relevance score and keywords
            relevance_score = item.get('relevance_score', 0)
            keywords_found = item.get('geospatial_keywords_found', [])
            location_mentioned = item.get('location_mentioned', '')
            
            st.markdown(f"**{i+1}. {item.get('title', 'No title')}**")
            
            # Show relevance indicators
            if relevance_score > 0:
                st.markdown(f"  📍 Location: {location_mentioned}")
                if keywords_found:
                    st.markdown(f"  🔑 Keywords: {', '.join(keywords_found[:3])}")
            
            # Show content preview
            content = item.get('content', 'No content')
            if len(content) > 200:
                content = content[:200] + "..."
            st.markdown(f"  📄 {content}")
            
            # Show URL
            if item.get('url'):
                st.markdown(f"  🔗 [Read full article]({item['url']})")
            
            st.markdown("---")
        
        # Show search summary
        total_results = len(st.session_state.recent_data)
        if total_results > 0:
            st.markdown(f"*Found {total_results} relevant geospatial news articles*")
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="insights-section">', unsafe_allow_html=True)
        st.markdown("**🌍 Geospatial News & Insights:**")
        st.markdown("No recent geospatial news found for this region and analysis type.")
        st.markdown('</div>', unsafe_allow_html=True)

def display_workflow_panel():
    """Display workflow panel and download options"""
    if st.session_state.workflow_plan:
        st.markdown('<div class="workflow-section">', unsafe_allow_html=True)
        st.markdown("**Workflow Panel & Download Options:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Generated Workflow:**")
            if st.button("View JSON"):
                workflow_json = {
                    "analysis_type": st.session_state.workflow_plan.analysis_type.value,
                    "region": st.session_state.workflow_plan.region_of_interest,
                    "time_period": st.session_state.workflow_plan.time_period,
                    "steps": [{"description": step.description, "method": step.method} for step in st.session_state.workflow_plan.steps]
                }
                st.json(workflow_json)
        
        with col2:
            st.markdown("**Download:**")
            if st.session_state.analysis_results:
                # Create download buttons
                if st.button("📄 GIS Output Files"):
                    st.download_button(
                        label="Download result.txt",
                        data=str(st.session_state.analysis_results),
                        file_name="result.txt",
                        mime="text/plain"
                    )
                
                if st.button("🗺️ Map Files"):
                    st.download_button(
                        label="Download result_map.html",
                        data=st.session_state.map_html or "No map data",
                        file_name="result_map.html",
                        mime="text/html"
                    )
        
        st.markdown('</div>', unsafe_allow_html=True)

def extract_location_from_query(query: str) -> str:
    """Extract location from the query using comprehensive South India database"""
    query_lower = query.lower()
    
    # Import comprehensive South India regions database
    try:
        from south_india_regions import get_south_india_regions, get_location_variations
        
        # Get all regions and variations
        regions = get_south_india_regions()
        variations = get_location_variations()
        
        # Try exact match first
        if query_lower in regions:
            return query_lower.title()
        
        # Try variations
        if query_lower in variations:
            mapped_location = variations[query_lower]
            if mapped_location in regions:
                return mapped_location.title()
        
        # Try partial matching
        for region_name in regions.keys():
            if region_name in query_lower or query_lower in region_name:
                return region_name.title()
        
        # Try word-by-word matching
        query_words = query_lower.split()
        for word in query_words:
            if word in regions:
                return word.title()
            if word in variations:
                mapped = variations[word]
                if mapped in regions:
                    return mapped.title()
        
    except ImportError:
        # Fallback to basic matching if import fails
        pass
    
    # Fallback locations
    fallback_locations = {
        'chennai': 'Chennai',
        'bangalore': 'Bangalore',
        'bengaluru': 'Bangalore',
        'kochi': 'Kochi',
        'hyderabad': 'Hyderabad',
        'madurai': 'Madurai',
        'coimbatore': 'Coimbatore',
        'mysore': 'Mysore',
        'thiruvananthapuram': 'Thiruvananthapuram',
        'visakhapatnam': 'Visakhapatnam',
        'tamil nadu': 'Tamil Nadu',
        'karnataka': 'Karnataka',
        'kerala': 'Kerala',
        'andhra pradesh': 'Andhra Pradesh',
        'telangana': 'Telangana',
        'goa': 'Goa',
        'puducherry': 'Puducherry'
    }
    
    # Find location in query
    for keyword, location in fallback_locations.items():
        if keyword in query_lower:
            return location
    
    # Default to Chennai if no location found
    return "Chennai"

def process_query(query: str):
    """Process the user query and generate analysis"""
    if not query.strip():
        return
    
    # Extract location from query
    location = extract_location_from_query(query)
    
    # Initialize services using secrets
    tavily_api_key = st.secrets.get("TAVILY_API_KEY", "")
    groq_api_key = st.secrets.get("GROQ_API_KEY", "")
    
    tavily_search = TavilySearch(tavily_api_key) if tavily_api_key else None
    groq_llm = GroqLLM(groq_api_key) if groq_api_key else None
    
    # Test Groq connection
    if groq_llm and not groq_llm.test_connection():
        st.warning("⚠️ Groq API connection failed. Using fallback summary.")
        groq_llm = None
    
    # Set analysis status
    st.session_state.analysis_in_progress = True
    st.session_state.analysis_completed = False
    
    # Show processing status in the main area
    with st.spinner("Processing query..."):
        try:
            # Step 1: Plan workflow
            planner = WorkflowPlanner()
            workflow_plan = planner.plan_analysis(query, location, "2020-2023")
            st.session_state.workflow_plan = workflow_plan
            
            # Generate chain-of-thought
            st.session_state.chain_of_thought = [
                f"Extracted region: {location}",
                f"Selected tools: {', '.join([step.method for step in workflow_plan.steps[:2]])}",
                f"Applied thresholding > Stream buffer zone"
            ]
            
            # Step 2: Execute analysis
            analyzer = GeospatialAnalyzer()
            if workflow_plan.analysis_type.value == "flood_risk":
                results = analyzer.execute_flood_risk_analysis(workflow_plan)
            elif workflow_plan.analysis_type.value == "solar_suitability":
                results = analyzer.execute_solar_suitability_analysis(workflow_plan)
            elif workflow_plan.analysis_type.value == "deforestation":
                results = analyzer.execute_deforestation_analysis(workflow_plan)
            else:
                st.error("Unsupported analysis type")
                return
            
            st.session_state.analysis_results = results
            
            # Step 3: Create visualization
            visualizer = MapVisualizer()
            # Get layer controls from session state
            layer_controls = st.session_state.get('layer_controls', {})
            
            if workflow_plan.analysis_type.value == "flood_risk":
                map_html = visualizer.create_flood_risk_map(results, results['region'], layer_controls)
            elif workflow_plan.analysis_type.value == "solar_suitability":
                map_html = visualizer.create_solar_suitability_map(results, results['region'], layer_controls)
            elif workflow_plan.analysis_type.value == "deforestation":
                map_html = visualizer.create_deforestation_map(results, results['region'], layer_controls)
            
            st.session_state.map_html = map_html
            
            # Step 4: Search for geospatial news
            if tavily_search:
                recent_data = tavily_search.search_geospatial_news(
                    query, 
                    location, 
                    workflow_plan.analysis_type.value,
                    max_results=5
                )
                st.session_state.recent_data = recent_data
            
            # Step 5: Generate enhanced summary
            if groq_llm:
                enhanced_summary = groq_llm.generate_summary(
                    query, 
                    results, 
                    st.session_state.recent_data
                )
                st.session_state.enhanced_summary = enhanced_summary
            else:
                # Fallback summary based on analysis type and location
                if workflow_plan.analysis_type.value == "flood_risk":
                    st.session_state.enhanced_summary = f"""
Based on flood risk analysis for {location}, the following areas have been identified as high-risk zones:

• Low-lying areas near water bodies
• Regions with poor drainage systems
• Areas with high precipitation patterns
• Locations with historical flood records

These areas show elevated risk factors based on elevation, precipitation patterns, and historical data.
                    """
                elif workflow_plan.analysis_type.value == "solar_suitability":
                    st.session_state.enhanced_summary = f"""
Based on solar suitability analysis for {location}, the following areas are optimal for solar farm development:

• Flat terrain with minimal slope
• Areas with high solar irradiance
• Locations away from urban centers
• Regions with good grid connectivity

These areas show excellent potential for solar energy generation based on terrain, climate, and infrastructure factors.
                    """
                elif workflow_plan.analysis_type.value == "deforestation":
                    st.session_state.enhanced_summary = f"""
Based on deforestation analysis for {location}, the following patterns have been identified:

• Areas with significant forest cover loss
• Regions showing NDVI decline
• Locations with land use change
• Areas requiring conservation attention

These findings are based on satellite imagery analysis and vegetation health monitoring.
                    """
                else:
                    st.session_state.enhanced_summary = f"""
Analysis completed for {location}. Results show various geospatial patterns and characteristics 
based on the selected analysis type and available data sources.
                    """
            
            st.success("✅ Analysis completed successfully!")
            
            # Set completion status
            st.session_state.analysis_in_progress = False
            st.session_state.analysis_completed = True
            
        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")
            import traceback
            st.error(traceback.format_exc())
            
            # Set error status
            st.session_state.analysis_in_progress = False
            st.session_state.analysis_completed = False

def initialize_authentication():
    """Initialize Google Earth Engine authentication"""
    if not st.session_state.authenticated:
        try:
            # Use credentials from secrets
            client_id = st.secrets.get("GEE_CLIENT_ID", "108832868460957844084")
            service_account_email = st.secrets.get("GEE_SERVICE_ACCOUNT", "gee-service@charged-gravity-471921-k5.iam.gserviceaccount.com")
            
            authenticator = GEEAuthenticator(client_id, service_account_email)
            if authenticator.authenticate():
                st.session_state.authenticated = True
                return True
        except Exception as e:
            st.error(f"Authentication error: {str(e)}")
            return False
    return st.session_state.authenticated

def main():
    """Main application function"""
    initialize_session_state()
    
    # Initialize authentication
    initialize_authentication()
    
    # Display header
    display_header()
    
    # Display query input
    query, analyse_clicked = display_query_input()
    
    # Process query if analyse button is clicked - BEFORE showing layout
    if analyse_clicked and query:
        if not st.session_state.authenticated:
            st.error("❌ Please authenticate with Google Earth Engine first. Run 'earthengine authenticate' in terminal.")
        else:
            process_query(query)
            # Force a rerun to update the UI
            st.rerun()
    
    # Create main layout matching the wireframe - ALWAYS show layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        # Left column - Chain of thought and layer controls
        display_chain_of_thought()
        layer_controls = display_layer_controls()
        # Store layer controls in session state
        st.session_state.layer_controls = layer_controls
    
    with col2:
        # Center column - Map visualization
        display_map_visualization()
        
        # Results section below the map
        display_results()
    
    with col3:
        # Right column - Live insights and workflow panel
        display_live_insights()
        display_workflow_panel()

if __name__ == "__main__":
    main()
