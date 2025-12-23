# PolicySim-AI System Architecture

## Technical Documentation for Research Publication

---

## 1. System Overview

### 1.1 Architecture Type
PolicySim-AI follows a **modular layered architecture** combined with an **agent-based orchestration pattern**. The system consists of five distinct layers:

1. **Presentation Layer** - User interface (Streamlit)
2. **Agent Layer** - Intelligent orchestration
3. **Service Layer** - LLM integration
4. **Simulation Layer** - Mathematical models
5. **Data Layer** - Configuration and parameters

### 1.2 Design Principles
- **Transparency**: All calculations are explicit and documented
- **Modularity**: Each component is independent and replaceable
- **Reproducibility**: Results can be replicated with same inputs
- **Extensibility**: New policies and models can be easily added

---

## 2. High-Level Architecture Diagram
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           POLICYSIM-AI SYSTEM                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                     PRESENTATION LAYER                                │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐  │  │
│  │  │    Home     │ │   Single    │ │  Scenario   │ │    Natural      │  │  │
│  │  │    Page     │ │   Policy    │ │ Comparison  │ │   Language      │  │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────────┘  │  │
│  │                         Streamlit Web Interface                       │  │
│  └───────────────────────────────────┬───────────────────────────────────┘  │
│                                      │                                      │
│                                      ▼                                      │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                        AGENT LAYER                                    │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │                   PolicySimAgent                                │  │  │
│  │  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │  │  │
│  │  │  │   Request    │ │    Model     │ │      Result              │ │  │  │
│  │  │  │   Analyzer   │ │   Selector   │ │    Synthesizer           │ │  │  │
│  │  │  └──────────────┘ └──────────────┘ └──────────────────────────┘ │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────┬───────────────────────────────────────┘  │
│                                  │                                          │
│         ┌────────────────────────┼────────────────────────┐                 │
│         ▼                        ▼                        ▼                 │
│  ┌─────────────────┐  ┌─────────────────────┐  ┌─────────────────────────┐  │
│  │  SERVICE LAYER  │  │  SIMULATION LAYER   │  │      DATA LAYER         │  │
│  │                 │  │                     │  │                         │  │
│  │  ┌───────────┐  │  │  ┌───────────────┐  │  │  ┌───────────────────┐  │  │
│  │  │    LLM    │  │  │  │   Emissions   │  │  │  │   Configuration   │  │  │
│  │  │  Helper   │  │  │  │    Model      │  │  │  │                   │  │  │
│  │  │  (Groq)   │  │  │  ├───────────────┤  │  │  ├───────────────────┤  │  │
│  │  └───────────┘  │  │  │  Cost-Benefit │  │  │  │  Regional         │  │  │
│  │                 │  │  │    Model      │  │  │  │  Contexts         │  │  │
│  │  Models:        │  │  ├───────────────┤  │  │  ├───────────────────┤  │  │
│  │  - Llama 3.3    │  │  │    Equity     │  │  │  │  Policy           │  │  │
│  │    70B          │  │  │    Model      │  │  │  │  Definitions      │  │  │
│  │  - Llama 3.1    │  │  ├───────────────┤  │  │  ├───────────────────┤  │  │
│  │    8B           │  │  │  Efficiency   │  │  │  │  Default          │  │  │
│  │                 │  │  │    Model      │  │  │  │  Parameters       │  │  │
│  │                 │  │  ├───────────────┤  │  │  │                   │  │  │
│  │                 │  │  │  Mode Share   │  │  │  │                   │  │  │
│  │                 │  │  │    Model      │  │  │  │                   │  │  │
│  │                 │  │  └───────────────┘  │  │  └───────────────────┘  │  │
│  └─────────────────┘  └─────────────────────┘  └─────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Component Descriptions

### 3.1 Presentation Layer (app.py)

| Component | Function | Technology |
|-----------|----------|------------|
| Home Page | System overview and navigation | Streamlit |
| Single Policy Analysis | Individual policy evaluation | Streamlit + Plotly |
| Scenario Comparison | Multi-policy comparison | Streamlit + Plotly |
| Natural Language Query | Free-text policy questions | Streamlit + LLM |
| Methodology View | Model documentation | Streamlit Markdown |

### 3.2 Agent Layer (agent.py)

The **PolicySimAgent** is the core intelligent component that orchestrates all operations:
```
┌─────────────────────────────────────────────────────────────────┐
│                      PolicySimAgent                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │   ANALYZE   │───▶│   SELECT    │───▶│      EXECUTE        │  │
│  │   REQUEST   │    │   MODELS    │    │    SIMULATIONS      │  │
│  └─────────────┘    └─────────────┘    └──────────┬──────────┘  │
│        ▲                                          │             │
│        │                                          ▼             │
│  ┌─────┴─────┐                          ┌─────────────────────┐ │
│  │   USER    │                          │     GENERATE        │ │
│  │   INPUT   │◀─────────────────────────│    EXPLANATION      │ │
│  └───────────┘                          └─────────────────────┘ │
│                                                                 │
│  State Machine: IDLE → ANALYZING → SELECTING → RUNNING →       │
│                 EXPLAINING → COMPLETE                           │
└─────────────────────────────────────────────────────────────────┘
```

**Agent Capabilities:**

| Method | Description | Input | Output |
|--------|-------------|-------|--------|
| `analyze_policy()` | Single policy evaluation | Policy type, parameters | Results + AI explanation |
| `compare_scenarios()` | Multi-scenario comparison | Scenario list | Comparison + rankings |
| `natural_language_query()` | NL understanding | Text query | Interpreted analysis |
| `get_policy_recommendations()` | AI recommendations | Target metric | Ranked policies |

### 3.3 Service Layer (llm_helper.py)

**LLM Integration Architecture:**
```
┌─────────────────────────────────────────────────────────────────┐
│                       LLM Helper                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐         ┌─────────────────────────────┐   │
│  │  Main Model     │         │      Functions              │   │
│  │  Llama 3.3 70B  │────────▶│  - explain_simulation()     │   │
│  │  (Complex)      │         │  - compare_scenarios()      │   │
│  └─────────────────┘         │  - generate_policy_brief()  │   │
│                              │  - suggest_improvements()   │   │
│  ┌─────────────────┐         └─────────────────────────────┘   │
│  │  Fast Model     │                                           │
│  │  Llama 3.1 8B   │────────▶│  - select_relevant_models() │   │
│  │  (Quick tasks)  │         │  - interpret_user_request() │   │
│  └─────────────────┘         └─────────────────────────────┘   │
│                                                                 │
│                    ┌─────────────────┐                         │
│                    │    Groq API     │                         │
│                    │  (Inference)    │                         │
│                    └─────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

### 3.4 Simulation Layer (models.py)

**Mathematical Models Architecture:**
```
┌─────────────────────────────────────────────────────────────────┐
│                    PolicySimulator                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    simulate(policy)                      │   │
│  └─────────────────────────────┬───────────────────────────┘   │
│                                │                               │
│     ┌──────────────────────────┼──────────────────────────┐    │
│     ▼                          ▼                          ▼    │
│  ┌──────────┐           ┌──────────┐              ┌──────────┐ │
│  │  Mode    │           │Emissions │              │  Cost    │ │
│  │  Share   │──────────▶│  Model   │              │ Benefit  │ │
│  │  Model   │           │          │              │  Model   │ │
│  └──────────┘           └──────────┘              └──────────┘ │
│       │                      │                          │      │
│       │                      ▼                          │      │
│       │               ┌──────────┐                      │      │
│       └──────────────▶│  Equity  │◀─────────────────────┘      │
│                       │  Model   │                             │
│                       └──────────┘                             │
│                             │                                  │
│                             ▼                                  │
│                      ┌──────────┐                              │
│                      │Efficiency│                              │
│                      │  Model   │                              │
│                      └──────────┘                              │
│                             │                                  │
│                             ▼                                  │
│                   ┌─────────────────┐                          │
│                   │ SimulationResult│                          │
│                   └─────────────────┘                          │
└─────────────────────────────────────────────────────────────────┘
```

### 3.5 Data Layer (config.py, policies.py)
```
┌─────────────────────────────────────────────────────────────────┐
│                        Data Layer                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────┐    ┌─────────────────────────────────┐│
│  │   Configuration     │    │      Policy Registry            ││
│  │                     │    │                                 ││
│  │  - API Settings     │    │  ┌─────────────────────────┐    ││
│  │  - App Config       │    │  │  Congestion Pricing     │    ││
│  │  - Default Params   │    │  ├─────────────────────────┤    ││
│  │                     │    │  │  PT Subsidy             │    ││
│  └─────────────────────┘    │  ├─────────────────────────┤    ││
│                             │  │  Fuel Tax               │    ││
│  ┌─────────────────────┐    │  ├─────────────────────────┤    ││
│  │  Regional Contexts  │    │  │  EV Incentive           │    ││
│  │                     │    │  ├─────────────────────────┤    ││
│  │  - Default (USD)    │    │  │  Parking Management     │    ││
│  │  - Malaysia (MYR)   │    │  └─────────────────────────┘    ││
│  │  - Thailand (THB)   │    │                                 ││
│  │  - Custom           │    │  ┌─────────────────────────┐    ││
│  └─────────────────────┘    │  │   Scenario Library      │    ││
│                             │  │  - Baseline             │    ││
│                             │  │  - Green Transport      │    ││
│                             │  │  - Balanced             │    ││
│                             │  │  - Equity Focus         │    ││
│                             │  └─────────────────────────┘    ││
│                             └─────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Data Flow Diagram

### 4.1 Single Policy Analysis Flow
```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  User    │     │  Agent   │     │ Simulator│     │   LLM    │
│Interface │     │          │     │          │     │  Helper  │
└────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │                │
     │ 1. Select      │                │                │
     │    Policy      │                │                │
     │───────────────▶│                │                │
     │                │                │                │
     │                │ 2. Validate    │                │
     │                │    Request     │                │
     │                │────────────────│                │
     │                │                │                │
     │                │ 3. Run         │                │
     │                │    Baseline    │                │
     │                │───────────────▶│                │
     │                │                │                │
     │                │◀───────────────│                │
     │                │   Baseline     │                │
     │                │   Results      │                │
     │                │                │                │
     │                │ 4. Run Policy  │                │
     │                │    Simulation  │                │
     │                │───────────────▶│                │
     │                │                │                │
     │                │◀───────────────│                │
     │                │   Policy       │                │
     │                │   Results      │                │
     │                │                │                │
     │                │ 5. Generate    │                │
     │                │    Explanation │                │
     │                │───────────────────────────────▶│
     │                │                │                │
     │                │◀───────────────────────────────│
     │                │                │   AI Text     │
     │                │                │                │
     │◀───────────────│                │                │
     │  6. Display    │                │                │
     │     Results    │                │                │
     │                │                │                │
```

### 4.2 Natural Language Query Flow
```
┌─────────────────────────────────────────────────────────────────┐
│                  Natural Language Processing Flow               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   "What if we implement a 30% transit subsidy?"                 │
│                           │                                     │
│                           ▼                                     │
│              ┌─────────────────────────┐                        │
│              │   LLM Interpretation    │                        │
│              │   (Llama 3.1 8B Fast)   │                        │
│              └───────────┬─────────────┘                        │
│                          │                                      │
│                          ▼                                      │
│              ┌─────────────────────────┐                        │
│              │  Structured Output:     │                        │
│              │  {                      │                        │
│              │    "policy_type":       │                        │
│              │      "pt_subsidy",      │                        │
│              │    "subsidy_percent":   │                        │
│              │      30                 │                        │
│              │  }                      │                        │
│              └───────────┬─────────────┘                        │
│                          │                                      │
│                          ▼                                      │
│              ┌─────────────────────────┐                        │
│              │   PolicySimAgent        │                        │
│              │   analyze_policy()      │                        │
│              └───────────┬─────────────┘                        │
│                          │                                      │
│                          ▼                                      │
│              ┌─────────────────────────┐                        │
│              │   Simulation Results    │                        │
│              │   + AI Explanation      │                        │
│              └─────────────────────────┘                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Mathematical Models Specification

### 5.1 Model Formulas

| Model | Formula | Variables |
|-------|---------|-----------|
| **Emissions** | $CO_2 = \sum_{m} (T_m \times D \times EF_m)$ | T=trips, D=distance, EF=emission factor |
| **User Cost** | $C = C_{fuel} + C_{fare} + (t \times VOT)$ | t=time, VOT=value of time |
| **Equity** | $E = 1 - G$ where $G = \frac{\sum_{i}\sum_{j}|x_i - x_j|}{2n^2\bar{x}}$ | G=Gini coefficient |
| **Mode Shift** | $\frac{\Delta Q}{Q} = \epsilon \times \frac{\Delta P}{P}$ | ε=elasticity, P=price |

### 5.2 Model Parameters

**Emission Factors (kg CO₂/km):**
| Mode | Factor | Source |
|------|--------|--------|
| Private Car | 0.21 | IPCC Guidelines |
| Motorcycle | 0.10 | IPCC Guidelines |
| Public Transit | 0.05 | Per passenger-km |
| Walking/Cycling | 0.00 | Zero emissions |

**Price Elasticities:**
| Mode | Own Elasticity | Cross Elasticity |
|------|----------------|------------------|
| Private Car | -0.3 | +0.2 (to PT) |
| Public Transit | -0.4 | +0.3 (to Car) |
| Motorcycle | -0.4 | - |

---

## 6. Technology Stack
```
┌─────────────────────────────────────────────────────────────────┐
│                      Technology Stack                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Frontend          │  Streamlit 1.45.0                  │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │  Visualization     │  Plotly 6.1.1                      │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │  LLM Provider      │  Groq API (Llama 3.3 70B, 3.1 8B)  │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │  Data Processing   │  Pandas 2.2.3, NumPy 2.2.6         │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │  Backend           │  Python 3.9+                       │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │  Deployment        │  Streamlit Cloud                   │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │  Version Control   │  Git + GitHub                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. File Structure
```
PolicySim-AI/
│
├── app.py                    # Presentation Layer
│   ├── render_home_page()
│   ├── render_single_policy_page()
│   ├── render_scenario_comparison_page()
│   ├── render_natural_language_page()
│   └── render_methodology_page()
│
├── agent.py                  # Agent Layer
│   ├── PolicySimAgent
│   │   ├── analyze_policy()
│   │   ├── compare_scenarios()
│   │   ├── natural_language_query()
│   │   └── get_policy_recommendations()
│   ├── AgentState (Enum)
│   └── AgentResponse (Dataclass)
│
├── llm_helper.py             # Service Layer
│   └── LLMHelper
│       ├── explain_simulation_results()
│       ├── compare_scenarios()
│       ├── suggest_policy_improvements()
│       ├── select_relevant_models()
│       └── interpret_user_policy_request()
│
├── models.py                 # Simulation Layer
│   ├── EmissionsModel
│   ├── CostBenefitModel
│   ├── EquityModel
│   ├── EfficiencyModel
│   ├── ModeShareModel
│   └── PolicySimulator
│
├── policies.py               # Data Layer (Policies)
│   ├── Policy (Base Class)
│   ├── CongestionPricingPolicy
│   ├── PublicTransitSubsidyPolicy
│   ├── FuelTaxPolicy
│   ├── EVIncentivePolicy
│   ├── ParkingManagementPolicy
│   ├── PolicyRegistry
│   └── ScenarioLibrary
│
├── config.py                 # Data Layer (Configuration)
│   ├── APP_CONFIG
│   ├── DEFAULT_PARAMS
│   ├── REGIONAL_CONTEXTS
│   └── POLICY_TYPES
│
├── visualizations.py         # Visualization Module
│   ├── create_score_comparison_chart()
│   ├── create_metrics_radar_chart()
│   ├── create_mode_share_comparison()
│   ├── create_emissions_breakdown_chart()
│   └── create_results_dashboard()
│
└── publication_figures.py    # Publication Export
    ├── create_figure1_mode_share()
    ├── create_figure2_emissions()
    ├── ...
    └── generate_all_publication_figures()
```

---

## 8. Agentic AI Behavior

### 8.1 What Makes This "Agentic"?
```
┌─────────────────────────────────────────────────────────────────┐
│                    Agentic AI Characteristics                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. AUTONOMY                                                    │
│     ┌─────────────────────────────────────────────────────┐    │
│     │  Agent decides WHICH models to run based on query   │    │
│     │  Agent decides HOW to interpret natural language    │    │
│     │  Agent decides WHAT to include in explanation       │    │
│     └─────────────────────────────────────────────────────┘    │
│                                                                 │
│  2. GOAL-ORIENTED                                               │
│     ┌─────────────────────────────────────────────────────┐    │
│     │  Goal: Provide accurate policy analysis             │    │
│     │  Sub-goals: Simulate → Compare → Explain → Report   │    │
│     └─────────────────────────────────────────────────────┘    │
│                                                                 │
│  3. REACTIVE                                                    │
│     ┌─────────────────────────────────────────────────────┐    │
│     │  Responds to user queries in real-time              │    │
│     │  Adapts analysis based on input type                │    │
│     └─────────────────────────────────────────────────────┘    │
│                                                                 │
│  4. TRANSPARENT                                                 │
│     ┌─────────────────────────────────────────────────────┐    │
│     │  All decisions are logged in action_log             │    │
│     │  All calculations are documented                    │    │
│     │  Users can inspect agent reasoning                  │    │
│     └─────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 Agent State Machine
```
                    ┌─────────┐
                    │  IDLE   │
                    └────┬────┘
                         │ User Input
                         ▼
              ┌─────────────────────┐
              │  ANALYZING_REQUEST  │
              └──────────┬──────────┘
                         │ Parse Query
                         ▼
              ┌─────────────────────┐
              │  SELECTING_MODELS   │
              └──────────┬──────────┘
                         │ Choose Models
                         ▼
              ┌─────────────────────┐
              │ RUNNING_SIMULATION  │
              └──────────┬──────────┘
                         │ Execute Models
                         ▼
              ┌─────────────────────┐
              │GENERATING_EXPLANATION│
              └──────────┬──────────┘
                         │ LLM Call
                         ▼
                  ┌─────────────┐
           ┌──────│  COMPLETE   │──────┐
           │      └─────────────┘      │
           │                           │
           ▼                           ▼
    ┌─────────────┐             ┌─────────────┐
    │   SUCCESS   │             │    ERROR    │
    └─────────────┘             └─────────────┘
```

---

## 9. Deployment Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                    Deployment Architecture                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│     ┌─────────────────┐                                        │
│     │     Users       │                                        │
│     │  (Web Browser)  │                                        │
│     └────────┬────────┘                                        │
│              │ HTTPS                                           │
│              ▼                                                  │
│     ┌─────────────────────────────────────┐                    │
│     │        Streamlit Cloud              │                    │
│     │   policysim-ai.streamlit.app        │                    │
│     │                                     │                    │
│     │  ┌───────────────────────────────┐  │                    │
│     │  │      PolicySim-AI App         │  │                    │
│     │  │      (Python Runtime)         │  │                    │
│     │  └───────────────┬───────────────┘  │                    │
│     │                  │                  │                    │
│     └──────────────────┼──────────────────┘                    │
│                        │ API Calls                             │
│                        ▼                                       │
│     ┌─────────────────────────────────────┐                    │
│     │           Groq Cloud API            │                    │
│     │                                     │                    │
│     │  ┌─────────────┐ ┌─────────────┐   │                    │
│     │  │ Llama 3.3   │ │ Llama 3.1   │   │                    │
│     │  │    70B      │ │    8B       │   │                    │
│     │  └─────────────┘ └─────────────┘   │                    │
│     │                                     │                    │
│     └─────────────────────────────────────┘                    │
│                                                                 │
│     ┌─────────────────────────────────────┐                    │
│     │           GitHub Repository         │                    │
│     │   github.com/mahbubchula/PolicySim-AI                    │
│     │                                     │                    │
│     │   - Source Code                     │                    │
│     │   - Documentation                   │                    │
│     │   - Version Control                 │                    │
│     └─────────────────────────────────────┘                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. Summary Table

| Component | File | Purpose | Key Classes/Functions |
|-----------|------|---------|----------------------|
| Presentation | `app.py` | User interface | `render_*_page()` functions |
| Agent | `agent.py` | Orchestration | `PolicySimAgent` |
| LLM Service | `llm_helper.py` | AI integration | `LLMHelper` |
| Simulation | `models.py` | Mathematical models | `PolicySimulator`, `*Model` |
| Policies | `policies.py` | Policy definitions | `PolicyRegistry`, `*Policy` |
| Configuration | `config.py` | Settings | `DEFAULT_PARAMS`, `REGIONAL_CONTEXTS` |
| Visualization | `visualizations.py` | Charts | `create_*_chart()` functions |
| Publication | `publication_figures.py` | Paper figures | `create_figure*()` functions |

---

*Document Version: 1.0.0*
*Last Updated: December 2024*
*Author: MAHBUB*
