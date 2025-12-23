# PolicySim-AI User Manual

## Comprehensive Guide for Transportation Policy Analysis

**Version 1.0.0**

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Getting Started](#2-getting-started)
3. [Interface Overview](#3-interface-overview)
4. [Single Policy Analysis](#4-single-policy-analysis)
5. [Scenario Comparison](#5-scenario-comparison)
6. [Natural Language Queries](#6-natural-language-queries)
7. [Understanding Results](#7-understanding-results)
8. [Publication Figures](#8-publication-figures)
9. [Regional Contexts](#9-regional-contexts)
10. [Methodology Reference](#10-methodology-reference)
11. [Troubleshooting](#11-troubleshooting)
12. [Appendix](#12-appendix)

---

## 1. Introduction

### 1.1 What is PolicySim-AI?

PolicySim-AI is an **agentic AI-powered tool** designed to help transportation researchers, urban planners, and policy analysts evaluate the potential impacts of various transportation policies. Unlike traditional simulation tools, PolicySim-AI combines:

- **Transparent mathematical models** for quantitative analysis
- **AI-powered explanations** for intuitive understanding
- **Interactive visualizations** for data exploration
- **Natural language interface** for ease of use

### 1.2 Key Capabilities

| Capability | Description |
|------------|-------------|
| **Policy Simulation** | Evaluate impacts of congestion pricing, transit subsidies, fuel taxes, EV incentives, and parking policies |
| **Multi-Criteria Assessment** | Analyze emissions, costs, equity, efficiency, and mode share simultaneously |
| **Scenario Comparison** | Compare multiple policy combinations side-by-side |
| **AI Explanations** | Receive plain-language interpretations of complex results |
| **Publication Export** | Generate journal-ready figures and tables |

### 1.3 What PolicySim-AI is NOT

- ❌ A traffic prediction model
- ❌ A replacement for human judgment
- ❌ A black-box AI system
- ❌ A tool that makes policy decisions

---

## 2. Getting Started

### 2.1 System Requirements

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux
- **Python**: Version 3.9 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Browser**: Chrome, Firefox, Safari, or Edge (latest versions)
- **Internet**: Required for AI explanations (Groq API)

### 2.2 Installation

#### Step 1: Download the Project
```bash
git clone https://github.com/yourusername/PolicySim-AI.git
cd PolicySim-AI
```

#### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

#### Step 3: Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

#### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 5: Configure API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Create a free account
3. Generate an API key
4. Create a `.env` file in the project folder:
```
GROQ_API_KEY=your_api_key_here
```

### 2.3 Launching the Application
```bash
streamlit run app.py
```

Your default browser will open to `http://localhost:8501`

---

## 3. Interface Overview

### 3.1 Main Layout
```
┌─────────────────────────────────────────────────────────────┐
│                        HEADER                                │
│                    PolicySim-AI v1.0.0                       │
├──────────────┬──────────────────────────────────────────────┤
│              │                                              │
│   SIDEBAR    │              MAIN CONTENT                    │
│              │                                              │
│  - Context   │   Analysis results, charts, and             │
│  - Navigation│   explanations appear here                   │
│  - About     │                                              │
│              │                                              │
└──────────────┴──────────────────────────────────────────────┘
```

### 3.2 Navigation Menu

| Page | Icon | Purpose |
|------|------|---------|
| Home | 🏠 | Overview and quick start guide |
| Single Policy | 🔬 | Analyze one policy in detail |
| Compare Scenarios | 📊 | Compare multiple policy combinations |
| Natural Language | 💬 | Ask questions in plain English |
| Methodology | 📖 | View model documentation |

### 3.3 Regional Context Selector

Located in the sidebar, this allows you to select parameters for different regions:

- **Default (Generic)**: Universal parameters suitable for any urban area
- **Malaysia (Klang Valley)**: Parameters calibrated for Malaysian context
- **Thailand (Bangkok)**: Parameters calibrated for Thai context
- **Custom**: Define your own parameters

---

## 4. Single Policy Analysis

### 4.1 Overview

Single Policy Analysis allows you to evaluate the impact of one transportation policy compared to a baseline (no policy) scenario.

### 4.2 Step-by-Step Guide

#### Step 1: Select Policy Type

Choose from five available policies:

| Policy | Best For |
|--------|----------|
| 🚗 Congestion Pricing | Reducing car traffic in urban cores |
| 🚌 Public Transit Subsidy | Increasing transit ridership |
| ⛽ Fuel Tax | Reducing overall fuel consumption |
| 🔋 EV Incentive | Accelerating electric vehicle adoption |
| 🅿️ Parking Management | Managing parking demand |

#### Step 2: Set Parameters

Each policy has adjustable parameters:

**Congestion Pricing:**
- Congestion Charge ($1-20): Fee charged per entry
- Peak Multiplier (1.0-3.0): Additional charge during rush hours

**Public Transit Subsidy:**
- Subsidy Percentage (0-100%): Portion of fare covered by government

**Fuel Tax:**
- Tax Percentage (0-100%): Additional tax on fuel price

**EV Incentive:**
- Purchase Subsidy ($0-15,000): Direct subsidy for EV purchase

**Parking Management:**
- Hourly Rate ($0.50-10): Parking fee per hour

#### Step 3: Run Analysis

Click the "🚀 Run Analysis" button. The system will:

1. Run baseline simulation (no policy)
2. Run policy simulation (with your parameters)
3. Calculate changes across all metrics
4. Generate AI explanation
5. Create visualizations

#### Step 4: Review Results

Results include:
- **Key Metrics**: Score, emissions, cost, equity
- **AI Analysis**: Plain-language explanation
- **Visualizations**: Interactive charts
- **Methodology**: Transparent calculation details

### 4.3 Example Analysis

**Scenario**: 30% Public Transit Subsidy

**Input:**
- Policy: Public Transit Subsidy
- Subsidy Percentage: 30%

**Expected Output:**
- Emissions Reduction: ~3-5%
- Mode Shift to Transit: ~10-15%
- Government Cost: Calculated based on ridership
- Equity Impact: Generally positive for low-income groups

---

## 5. Scenario Comparison

### 5.1 Overview

Scenario Comparison allows you to evaluate multiple policy combinations simultaneously to identify the best approach for your objectives.

### 5.2 Pre-Built Scenarios

| Scenario | Policies Included | Focus |
|----------|-------------------|-------|
| **Baseline** | None | Current conditions |
| **Green Transport** | High congestion pricing + High transit subsidy + Fuel tax | Maximum emission reduction |
| **Balanced Approach** | Moderate congestion pricing + Moderate transit subsidy + Parking management | Multi-objective balance |
| **Equity Focus** | High transit subsidy targeting low-income groups | Affordability and access |

### 5.3 Step-by-Step Guide

1. **Select Scenarios**: Check the boxes for scenarios to compare (minimum 2)
2. **Run Comparison**: Click "🔄 Compare Scenarios"
3. **Review Best Performers**: See which scenario wins on each metric
4. **Read AI Analysis**: Understand trade-offs between scenarios
5. **Examine Charts**: Compare visually across all dimensions

### 5.4 Interpreting Comparison Results

The comparison identifies the **best performer** for each metric:

- **Best Overall**: Highest weighted score across all metrics
- **Best Emissions**: Lowest CO₂ emissions
- **Best Cost**: Lowest user cost per trip
- **Best Equity**: Most equitable distribution of benefits
- **Best Efficiency**: Shortest average travel time

---

## 6. Natural Language Queries

### 6.1 Overview

The Natural Language interface allows you to ask questions about transportation policies in plain English. The AI agent interprets your question and runs appropriate analyses.

### 6.2 Example Queries

| Query Type | Example |
|------------|---------|
| **Single Policy** | "What if we implement a $10 congestion charge?" |
| **Impact Question** | "How would a 50% transit subsidy affect emissions?" |
| **Comparison** | "Compare high parking fees with transit subsidies" |
| **What-If** | "What's the impact of doubling the fuel tax?" |

### 6.3 Tips for Effective Queries

✅ **Do:**
- Be specific about policy parameters
- Include numbers when possible
- Ask about specific metrics (emissions, cost, equity)

❌ **Avoid:**
- Vague questions like "What's the best policy?"
- Questions outside transportation scope
- Multiple unrelated questions in one query

### 6.4 How It Works
```
Your Question
     ↓
┌─────────────────────┐
│  Policy Analyzer    │ ← Interprets your question
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  Model Selector     │ ← Chooses relevant models
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  Simulator          │ ← Runs calculations
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  Explainer (LLM)    │ ← Generates explanation
└──────────┬──────────┘
           ↓
    Your Answer
```

---

## 7. Understanding Results

### 7.1 Key Metrics Explained

#### Overall Score (0-100)
A weighted composite score combining all metrics:
- 25% Emissions performance
- 25% Cost efficiency
- 25% Equity
- 25% System efficiency

**Interpretation:**
- 70+: Excellent policy performance
- 60-70: Good, with some trade-offs
- 50-60: Moderate, significant trade-offs
- <50: Poor, needs reconsideration

#### CO₂ Emissions (kg/day)
Total daily transportation emissions calculated as:
```
CO₂ = Σ(trips × distance × emission_factor)
```

**Emission Factors:**
| Mode | kg CO₂/km |
|------|-----------|
| Private Car | 0.21 |
| Motorcycle | 0.10 |
| Public Transit | 0.05 |
| Walking/Cycling | 0.00 |

#### User Cost ($/trip)
Average cost per trip including:
- Fuel costs
- Fares
- Time costs (valued at 50% of hourly wage)

#### Equity Score (0-1)
Measures fairness of cost distribution:
- 1.0 = Perfectly equal burden across income groups
- 0.0 = Extremely unequal burden
- Calculated as: 1 - Gini coefficient

#### Mode Share (%)
Distribution of trips across transportation modes:
- Private Car
- Motorcycle
- Public Transit
- Walking/Cycling

### 7.2 Understanding Mode Shift

Mode shift is calculated using **price elasticity of demand**:
```
% Change in Demand = Elasticity × % Change in Price
```

**Elasticities Used:**
| Mode | Elasticity | Interpretation |
|------|------------|----------------|
| Private Car | -0.3 | Inelastic (less responsive) |
| Motorcycle | -0.4 | Moderate |
| Public Transit | -0.4 | Moderate |
| Walking/Cycling | -0.1 | Very inelastic |

### 7.3 Reading Visualizations

#### Radar Chart
- Each axis represents one metric (normalized to 0-100)
- Larger area = better overall performance
- Compare shapes to see trade-offs

#### Bar Charts
- Direct comparison between scenarios
- Error bars (if shown) indicate uncertainty

#### Pie Charts
- Show proportional distribution
- Useful for mode share and emissions breakdown

---

## 8. Publication Figures

### 8.1 Generating Publication-Ready Figures

Run the publication figure generator:
```bash
python publication_figures.py
```

### 8.2 Output Specifications

| Property | Value |
|----------|-------|
| Font | Times New Roman |
| Font Size | 14pt (body), 16pt (titles) |
| Resolution | 300 DPI |
| Formats | PNG, PDF, SVG |
| Color Scheme | Colorblind-friendly |

### 8.3 Available Figures

| Figure | Filename | Description |
|--------|----------|-------------|
| 1 | `figure1_mode_share` | Mode share comparison bar chart |
| 2 | `figure2_emissions` | CO₂ emissions comparison |
| 3 | `figure3_emissions_breakdown` | Emissions by mode (pie chart) |
| 4 | `figure4_equity` | Cost burden by income group |
| 5 | `figure5_scenario_comparison` | Multi-scenario performance |
| 6 | `figure6_scenario_emissions` | Scenario emissions comparison |
| 7 | `figure7_radar` | Multi-dimensional radar chart |
| 8 | `figure8_mode_shift` | Mode share changes |

### 8.4 Using Figures in Papers

**For Word Documents:**
- Use PNG files
- Insert → Pictures → Select file

**For LaTeX Documents:**
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=\textwidth]{figures/figure1_mode_share.pdf}
    \caption{Transportation mode share comparison between baseline and policy scenarios.}
    \label{fig:mode_share}
\end{figure}
```

**For Web/Presentations:**
- Use SVG for scalability
- Use PNG for compatibility

---

## 9. Regional Contexts

### 9.1 Default Context

Generic urban area parameters suitable for initial analysis:

| Parameter | Value |
|-----------|-------|
| Population | 1,000,000 |
| Daily Trips | 2,500,000 |
| Avg Trip Distance | 12 km |
| Fuel Price | $1.20/liter |
| Transit Fare | $1.50 |
| Avg Hourly Wage | $8.00 |

### 9.2 Malaysia (Klang Valley)

Calibrated for Malaysian context:

| Parameter | Value |
|-----------|-------|
| Currency | MYR |
| Fuel Price | RM 2.05/liter |
| Transit Fare | RM 3.00 |
| Avg Hourly Wage | RM 15.00 |

### 9.3 Thailand (Bangkok)

Calibrated for Thai context:

| Parameter | Value |
|-----------|-------|
| Currency | THB |
| Fuel Price | ฿40/liter |
| Transit Fare | ฿25 |
| Avg Hourly Wage | ฿100 |

### 9.4 Custom Context

To use custom parameters, modify `config.py`:
```python
REGIONAL_CONTEXTS["custom"] = {
    "name": "Your City",
    "currency": "USD",
    "currency_symbol": "$",
    "fuel_price_per_liter": 1.50,
    "public_transit_fare": 2.00,
    "avg_hourly_wage": 10.00,
    "description": "Custom parameters for your analysis"
}
```

---

## 10. Methodology Reference

### 10.1 Emissions Model

**Formula:**
```
Total CO₂ = Σ (trips_by_mode × avg_distance × emission_factor)
```

**Adjustments:**
- Private car emissions adjusted for occupancy (1.3 average)
- Public transit emissions are per-passenger values

**Sources:**
- IPCC Guidelines for National Greenhouse Gas Inventories
- EPA Motor Vehicle Emission Simulator (MOVES)

### 10.2 Cost-Benefit Model

**User Cost Formula:**
```
Cost = fuel_cost + fare + (travel_time × value_of_time)
```

**Value of Time:**
- Calculated as 50% of hourly wage
- Based on US DOT guidance and World Bank standards

**Government Cost:**
```
Annual Cost = subsidy_per_trip × subsidized_trips × 365
```

### 10.3 Equity Model

**Burden Calculation:**
```
Burden = (daily_transport_cost / daily_income) × 100
```

**Income Quintiles:**
| Group | Income Multiplier |
|-------|-------------------|
| Low | 0.4× average |
| Lower-Middle | 0.7× average |
| Middle | 1.0× average |
| Upper-Middle | 1.5× average |
| High | 2.5× average |

**Equity Score:**
```
Equity Score = 1 - Gini coefficient
```

### 10.4 Mode Share Model

**Price Elasticity Formula:**
```
ΔQ/Q = elasticity × ΔP/P
```

**Cross-Elasticities:**
- Car → Transit: 0.3 (transit price up → car use up)
- Transit → Car: 0.2 (car price up → transit use up)

---

## 11. Troubleshooting

### 11.1 Common Issues

#### "GROQ_API_KEY not found"
**Solution:** Check your `.env` file:
1. File must be named exactly `.env` (with the dot)
2. No quotes around the API key
3. File must be in the project root folder

#### "Module not found" errors
**Solution:** Ensure virtual environment is activated:
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

#### Figures not generating
**Solution:** Install kaleido and upgrade plotly:
```bash
pip install kaleido plotly==6.1.1 --upgrade
```

#### Streamlit not opening
**Solution:** Open browser manually to `http://localhost:8501`

### 11.2 Performance Issues

**Slow AI responses:**
- Check internet connection
- Groq API may have temporary delays
- Try refreshing the page

**Memory errors:**
- Close other applications
- Restart the application

### 11.3 Getting Help

1. Check this manual first
2. Review error messages carefully
3. Search for similar issues online
4. Contact the author

---

## 12. Appendix

### 12.1 Complete File List

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application |
| `config.py` | Configuration and settings |
| `models.py` | Simulation models |
| `policies.py` | Policy definitions |
| `agent.py` | Agentic AI orchestrator |
| `llm_helper.py` | LLM integration |
| `visualizations.py` | Interactive charts |
| `publication_figures.py` | Publication exports |
| `requirements.txt` | Dependencies |
| `.env` | API keys (not shared) |

### 12.2 Dependencies
```
streamlit==1.45.0
groq==0.25.0
plotly==6.1.1
pandas==2.2.3
numpy==2.2.6
python-dotenv==1.1.0
pydantic==2.11.7
kaleido==1.2.0
```

### 12.3 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + R` | Refresh page |
| `Ctrl + S` | Save file (in VS Code) |
| `Ctrl + C` | Stop Streamlit server |

### 12.4 Academic References

1. Eliasson, J. (2009). A cost-benefit analysis of the Stockholm congestion charging system. *Transportation Research Part A*.

2. Litman, T. (2022). Evaluating Transportation Equity. *Victoria Transport Policy Institute*.

3. Small, K.A. & Verhoef, E.T. (2007). *Economics of Urban Transportation*. Routledge.

4. Cervero, R. (1990). Transit pricing research: A review and synthesis. *Transportation*.

5. Shoup, D. (2006). Cruising for parking. *Transport Policy*.

---

## Document Information

| Property | Value |
|----------|-------|
| Version | 1.0.0 |
| Last Updated | December 2024 |
| Author | MAHBUB |
| License | MIT |

---

*End of User Manual*
```

Save the file (`Ctrl + S`).

---

## Create `.gitignore`

Create a `.gitignore` file to protect sensitive data:
```
# Environment
.env
venv/
__pycache__/
*.pyc

# IDE
.vscode/
.idea/

# Test files
test_chart.html

# OS files
.DS_Store
Thumbs.db
```

Save the file.

---

## Summary of All Files

Your project now has these files:
```
E:\Mahbub Hassan_Chula\PolicySim_AI\
├── venv/                      # Virtual environment
├── publication_figures/       # Generated figures (PNG, PDF, SVG)
├── .env                       # API key (keep secret!)
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Dependencies
├── config.py                  # Configuration
├── models.py                  # Simulation models
├── policies.py                # Policy definitions
├── agent.py                   # Agentic AI orchestrator
├── llm_helper.py              # LLM integration
├── visualizations.py          # Interactive charts
├── publication_figures.py     # Publication figure generator
├── app.py                     # Main Streamlit application
├── README.md                  # Project overview
└── USER_MANUAL.md             # Comprehensive user guide