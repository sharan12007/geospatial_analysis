# 🌍 GeoGPT - AI-Powered Geospatial Analysis Assistant

**GeoGPT** is an advanced AI-powered assistant that transforms natural language queries into comprehensive geospatial analysis using Google Earth Engine. It combines cutting-edge AI technologies with professional geospatial tools to make complex Earth observation analysis accessible to everyone.

## ✨ Key Features

### 🎯 **Natural Language Processing**
- Ask questions in plain English: *"Find flood-prone areas in Chennai"*
- Intelligent query interpretation and workflow planning
- Support for complex multi-criteria analysis

### 🔬 **Advanced Analysis Capabilities**
- **Flood Risk Assessment**: Elevation, precipitation, and SAR-based flood zone mapping
- **Solar Site Suitability**: Slope, aspect, land cover, and solar irradiance analysis
- **Deforestation Monitoring**: NDVI time series and change detection
- **Urban Growth Analysis**: Land use change and development patterns
- **Agricultural Suitability**: Soil, climate, and terrain assessment

### 🗺️ **Interactive Visualization**
- Multi-layer interactive maps with Folium
- Real-time layer toggling and customization
- Professional cartographic styling
- Export capabilities for maps and data

### 🤖 **AI-Powered Insights**
- **Tavily Integration**: Real-time news and data search
- **Groq LLM**: Enhanced analysis summaries using GPT-OSS-20B
- **Chain-of-Thought Analysis**: Transparent workflow visualization
- **Automated Code Generation**: Ready-to-run Google Earth Engine Python code

### 🎨 **Professional Web Interface**
- Modern Streamlit-based UI with responsive design
- Intuitive workflow planning and execution
- Real-time progress tracking
- Download options for all outputs

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Earth Engine account
- Tavily API key (optional, for enhanced features)
- Groq API key (optional, for AI summaries)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ShadesOfCyberak/Geospatial_Analyzer.git
   cd Geospatial_Analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Earth Engine authentication**
   ```bash
   earthengine authenticate
   ```

4. **Configure API keys (Optional)**
   Create `.streamlit/secrets.toml`:
   ```toml
   TAVILY_API_KEY = "your_tavily_api_key_here"
   GROQ_API_KEY = "your_groq_api_key_here"
   ```

### Launch the Application

**Option 1: Enhanced Web Interface (Recommended)**
```bash
python run_app.py
```

**Option 2: Command Line Interface**
```bash
python geogpt_main.py "Find flood-prone areas in Chennai" "Chennai" "2020-2023"
```

The web interface will open at `http://localhost:8501`

## 📋 Supported Analysis Types

### 🌊 Flood Risk Analysis
**Query Examples:**
- "Find flood-prone areas in Chennai"
- "Identify flood zones in Mumbai"
- "Assess flood risk for Kochi"

**Datasets Used:**
- SRTM DEM (elevation data)
- CHIRPS Precipitation (rainfall patterns)
- Sentinel-1 SAR (water detection)
- Flow accumulation models

**Output:**
- Flood risk zones (High/Medium/Low/No Risk)
- Interactive risk maps
- Detailed analysis summary
- Executable GEE Python code

### ☀️ Solar Farm Suitability Analysis
**Query Examples:**
- "Suggest suitable sites for solar farms in Rajasthan"
- "Find optimal solar locations in Gujarat"
- "Identify solar potential in Karnataka"

**Datasets Used:**
- SRTM DEM (slope and aspect)
- Sentinel-2 MSI (land cover)
- Solar irradiance models
- Administrative boundaries

**Output:**
- Suitability zones (High/Medium/Low/Not Suitable)
- Solar potential maps
- Site-specific recommendations
- Technical feasibility reports

### 🌳 Deforestation Monitoring
**Query Examples:**
- "Identify deforestation regions in Kerala since 2015"
- "Monitor forest loss in Karnataka"
- "Analyze deforestation patterns in Tamil Nadu"

**Datasets Used:**
- Sentinel-2 MSI (vegetation monitoring)
- NDVI time series analysis
- Land cover classification
- Change detection algorithms

**Output:**
- Deforestation hotspots
- Forest cover change maps
- Quantified loss statistics
- Conservation recommendations

## 🛠️ Project Structure

```
Site_Suitability_Analyzer_01/
├── .streamlit/
│   ├── secrets.toml                 # API credentials
├── geogpt/                          # Core package
│   ├── __init__.py                  # Package initialization
│   ├── auth.py                      # Google Earth Engine authentication
│   ├── workflow.py                  # Workflow planning and management
│   ├── analyzer.py                  # Geospatial analysis execution
│   └── visualizer.py                # Map visualization and styling
├── geogpt_main.py                   # Main CLI interface
├── run_app.py                       # Enhanced app launcher
├── streamlit_app_enhanced.py        # Enhanced web interface
├── south_india_regions.py           # Region Boundary Definition
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## 🔧 Configuration

### Google Earth Engine Setup

1. **Create a Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select existing one

2. **Enable Earth Engine API**
   - Navigate to APIs & Services > Library
   - Search for "Earth Engine API" and enable it

3. **Set up Authentication**
   ```python
   from geogpt import GEEAuthenticator
   
   authenticator = GEEAuthenticator(
       client_id="your_oauth2_client_id",
       service_account_email="your_service_account@project.iam.gserviceaccount.com"
   )
   authenticator.authenticate()
   ```

### API Keys Configuration

**Tavily API (Optional)**
1. Sign up at [tavily.com](https://tavily.com)
2. Get your API key from the dashboard
3. Add to `.streamlit/secrets.toml`:
   ```toml
   TAVILY_API_KEY = "your_tavily_api_key"
   ```

**Groq API (Optional)**
1. Sign up at [groq.com](https://groq.com)
2. Get your API key from the console
3. Add to `.streamlit/secrets.toml`:
   ```toml
   GROQ_API_KEY = "your_groq_api_key"
   ```

## 📊 Usage Examples

### Advanced Workflow Planning

```python
from geogpt import WorkflowPlanner, GeospatialAnalyzer

# Create custom workflow
planner = WorkflowPlanner()
workflow_plan = planner.plan_flood_risk_analysis("Mumbai", "2020-2023")

# Execute analysis
analyzer = GeospatialAnalyzer()
results = analyzer.execute_flood_risk_analysis(workflow_plan)
```

### Batch Processing

```python
locations = ["Chennai", "Mumbai", "Delhi", "Kolkata"]
queries = ["Find flood-prone areas in {location}" for location in locations]

for query, location in zip(queries, locations):
    results = geogpt.analyze(query, location)
    geogpt.save_results(results, f"output/{location}")
```

## 🗺️ Visualization Features

### Interactive Maps
- **Base Layers**: OpenStreetMap, Satellite imagery, Terrain
- **Analysis Layers**: Risk zones, suitability areas, change detection
- **Layer Controls**: Toggle visibility, opacity adjustment
- **Legends**: Color-coded explanations and scale bars

### Export Options
- **Interactive Maps**: HTML files with full functionality
- **Static Images**: PNG/JPEG exports for reports
- **Data Files**: GeoTIFF, GeoJSON, CSV formats
- **Code Files**: Executable Python scripts

## 📁 Output Files

Each analysis generates comprehensive outputs:

1. **Interactive Map** (`*_map.html`)
   - Web-based visualization with layer controls
   - Zoom, pan, and measurement tools
   - Export and sharing capabilities

2. **Executable Code** (`*_code.py`)
   - Ready-to-run Google Earth Engine Python code
   - Well-documented with comments
   - Modular and customizable

3. **Analysis Summary** (`*_summary.txt`)
   - Detailed results and findings
   - Methodology explanation
   - Recommendations and next steps

## 🔍 Advanced Features

### Chain-of-Thought Analysis
GeoGPT provides transparent analysis workflows:

1. **Query Interpretation**: Natural language processing
2. **Region Extraction**: Geographic boundary identification
3. **Dataset Selection**: Appropriate satellite data selection
4. **Analysis Execution**: Multi-criteria assessment
5. **Visualization**: Interactive map generation
6. **Summary Generation**: AI-powered insights

### Real-time Data Integration
- **Tavily Search**: Latest news and environmental data
- **Weather Integration**: Current conditions and forecasts
- **Policy Updates**: Recent regulatory changes
- **Environmental Alerts**: Real-time monitoring data

### AI-Powered Insights
- **Groq LLM**: Enhanced analysis summaries
- **Pattern Recognition**: Automated anomaly detection
- **Trend Analysis**: Historical pattern identification
- **Recommendation Engine**: Actionable insights

## ⚠️ Important Considerations

### Data Accuracy
- Results are for **research and planning purposes**
- Consult local authorities for official assessments
- Ground truth validation recommended for critical decisions

### Rate Limits
- Google Earth Engine has API rate limits
- Large analyses may require optimization
- Consider data export quotas

### Regional Availability
- Some datasets may not be available for all regions
- Time period limitations may apply
- Cloud cover can affect optical imagery

## 📈 Performance Optimization

### Query Optimization
- Use specific location names
- Define relevant time periods
- Avoid overly broad geographic areas

### Analysis Efficiency
- Disable unnecessary layers
- Use appropriate spatial resolution
- Consider data export limitations

### Memory Management
- Process large areas in chunks
- Use appropriate data formats
- Monitor system resources

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest

# Format code
black geogpt/

# Lint code
flake8 geogpt/
```

## 🙏 Acknowledgments

- **Google Earth Engine**: For providing powerful geospatial data processing capabilities
- **Tavily**: For real-time data search and integration
- **Groq**: For AI-powered analysis and insights
- **Streamlit**: For the intuitive web application framework
- **Folium**: For interactive map visualization
- **OpenStreetMap**: For base map data
- **Sentinel Missions**: For high-quality satellite imagery


**🌍 GeoGPT** - Making geospatial analysis accessible through AI! 

*Transform your natural language queries into powerful Earth observation insights.*