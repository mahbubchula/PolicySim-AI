"""
PolicySim-AI - Main Application
===============================
Transportation Policy Simulation & Analysis Tool
An agentic AI system for evaluating transportation policies.

Author: MAHBUB
"""

import streamlit as st
import json
from typing import Dict, List

# Import our modules
from config import APP_CONFIG, REGIONAL_CONTEXTS, POLICY_TYPES, validate_config
from models import PolicySimulator
from policies import PolicyRegistry, ScenarioLibrary, PolicyScenario
from agent import PolicySimAgent, AgentResponse
from visualizations import (
    create_results_dashboard,
    create_scenario_comparison_chart,
    create_scenario_emissions_chart,
    create_scenario_cost_chart,
    create_sensitivity_chart
)
from llm_helper import LLMHelper


# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title=APP_CONFIG["title"],
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E86AB;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6C757D;
        margin-top: 0;
    }
    .metric-card {
        background-color: #F8F9FA;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #2E86AB;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #6C757D;
    }
    .success-box {
        background-color: #D4EDDA;
        border: 1px solid #C3E6CB;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #D1ECF1;
        border: 1px solid #BEE5EB;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #FFF3CD;
        border: 1px solid #FFEEBA;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================

def init_session_state():
    """Initialize session state variables."""
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "context" not in st.session_state:
        st.session_state.context = "default"
    if "last_results" not in st.session_state:
        st.session_state.last_results = None
    if "comparison_results" not in st.session_state:
        st.session_state.comparison_results = None


# =============================================================================
# SIDEBAR
# =============================================================================

def render_sidebar():
    """Render the sidebar with settings and info."""
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/road.png", width=80)
        st.markdown("## PolicySim-AI")
        st.markdown(f"*v{APP_CONFIG['version']}*")
        
        st.markdown("---")
        
        # Context Selection
        st.markdown("### 🌍 Regional Context")
        context_options = {
            "default": "🌐 Default (Generic)",
            "malaysia": "🇲🇾 Malaysia (Klang Valley)",
            "thailand": "🇹🇭 Thailand (Bangkok)",
            "custom": "⚙️ Custom Parameters"
        }
        
        selected_context = st.selectbox(
            "Select Region",
            options=list(context_options.keys()),
            format_func=lambda x: context_options[x],
            key="context_selector"
        )
        
        if selected_context != st.session_state.context:
            st.session_state.context = selected_context
            st.session_state.agent = PolicySimAgent(context=selected_context)
        
        # Initialize agent if not exists
        if st.session_state.agent is None:
            st.session_state.agent = PolicySimAgent(context=selected_context)
        
        # Show context info
        context_info = REGIONAL_CONTEXTS.get(selected_context, {})
        st.info(f"**{context_info.get('name', 'Unknown')}**\n\n{context_info.get('description', '')}")
        
        st.markdown("---")
        
        # About section
        st.markdown("### ℹ️ About")
        st.markdown("""
        **PolicySim-AI** is an agentic AI tool for transportation policy analysis.
        
        **Features:**
        - 🔬 Transparent simulation models
        - 🤖 AI-powered explanations
        - 📊 Interactive visualizations
        - 📋 Pre-built scenarios
        
        **Models:**
        - Emissions (CO2)
        - Cost-Benefit
        - Equity Analysis
        - System Efficiency
        - Mode Share Prediction
        """)
        
        st.markdown("---")
        st.markdown(f"*Created by {APP_CONFIG['author']}*")


# =============================================================================
# MAIN PAGES
# =============================================================================

def render_home_page():
    """Render the home/overview page."""
    st.markdown('<p class="main-header">🚗 PolicySim-AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transportation Policy Simulation & Analysis Tool</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Introduction
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Welcome to PolicySim-AI
        
        This tool helps researchers and planners **systematically evaluate transportation policies** using:
        
        1. **Transparent Mathematical Models** - All calculations are explicit and documented
        2. **AI-Powered Explanations** - Open-source LLM explains results in plain language
        3. **Comparative Analysis** - Compare multiple policy scenarios side-by-side
        4. **Research-Ready Outputs** - Export results for academic publications
        
        ---
        
        ### 🚀 Quick Start
        
        Use the **navigation menu** on the left to:
        
        - **Single Policy Analysis** - Evaluate one policy in detail
        - **Scenario Comparison** - Compare multiple policies
        - **Natural Language Query** - Ask questions in plain English
        - **Methodology** - View model documentation
        """)
    
    with col2:
        st.markdown("### 📊 Available Policies")
        for policy_id, policy_info in POLICY_TYPES.items():
            st.markdown(f"**{policy_info['name']}**")
            st.caption(policy_info['description'][:80] + "...")
            st.markdown("")


def render_single_policy_page():
    """Render the single policy analysis page."""
    st.markdown("## 🔬 Single Policy Analysis")
    st.markdown("Evaluate the impact of a single transportation policy.")
    
    st.markdown("---")
    
    # Policy Selection
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Select Policy")
        
        policy_options = {
            "congestion_pricing": "🚗 Congestion Pricing",
            "pt_subsidy": "🚌 Public Transit Subsidy",
            "fuel_tax": "⛽ Fuel Tax",
            "ev_incentive": "🔋 EV Incentive",
            "parking_policy": "🅿️ Parking Management"
        }
        
        selected_policy = st.selectbox(
            "Policy Type",
            options=list(policy_options.keys()),
            format_func=lambda x: policy_options[x]
        )
        
        # Show policy description
        policy_info = POLICY_TYPES.get(selected_policy, {})
        st.info(policy_info.get("description", ""))
    
    with col2:
        st.markdown("### Set Parameters")
        
        # Dynamic parameter inputs based on policy type
        params = {}
        
        if selected_policy == "congestion_pricing":
            params["price_per_entry"] = st.slider(
                "Congestion Charge ($)",
                min_value=1.0, max_value=20.0, value=5.0, step=0.5
            )
            params["peak_multiplier"] = st.slider(
                "Peak Hour Multiplier",
                min_value=1.0, max_value=3.0, value=1.5, step=0.1
            )
            
        elif selected_policy == "pt_subsidy":
            params["subsidy_percent"] = st.slider(
                "Subsidy Percentage (%)",
                min_value=0, max_value=100, value=30, step=5
            )
            
        elif selected_policy == "fuel_tax":
            params["tax_percent"] = st.slider(
                "Additional Fuel Tax (%)",
                min_value=0, max_value=100, value=20, step=5
            )
            
        elif selected_policy == "ev_incentive":
            params["purchase_subsidy"] = st.slider(
                "EV Purchase Subsidy ($)",
                min_value=0, max_value=15000, value=5000, step=500
            )
            
        elif selected_policy == "parking_policy":
            params["hourly_rate"] = st.slider(
                "Parking Rate ($/hour)",
                min_value=0.5, max_value=10.0, value=3.0, step=0.5
            )
    
    st.markdown("---")
    
    # Run Analysis Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        run_analysis = st.button("🚀 Run Analysis", type="primary", use_container_width=True)
    
    if run_analysis:
        with st.spinner("Running simulation and generating AI explanation..."):
            # Run the agent
            response = st.session_state.agent.analyze_policy(
                policy_type=selected_policy,
                parameters=params,
                explain=True
            )
            
            st.session_state.last_results = response
        
        if response.success:
            st.success(f"✅ {response.message}")
            
            # Display results
            render_policy_results(response)
        else:
            st.error(f"❌ {response.message}")


def render_policy_results(response: AgentResponse):
    """Render the results of a policy analysis."""
    results = response.results
    baseline = results["baseline"]
    with_policy = results["with_policy"]
    improvement = results["improvement"]
    
    st.markdown("---")
    st.markdown("### 📊 Results Summary")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        score_change = improvement["score_change"]
        st.metric(
            "Overall Score",
            f"{with_policy['overall_score']:.1f}/100",
            f"{score_change:+.1f}",
            delta_color="normal"
        )
    
    with col2:
        emissions_change = improvement["emissions_change_percent"]
        st.metric(
            "CO2 Emissions",
            f"{with_policy['emissions']['total_co2_kg_per_day']:,.0f} kg",
            f"{emissions_change:+.1f}%",
            delta_color="inverse"
        )
    
    with col3:
        cost_change = improvement["cost_change_percent"]
        st.metric(
            "User Cost/Trip",
            f"${with_policy['cost']['user_cost_per_trip']:.2f}",
            f"{cost_change:+.1f}%",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            "Equity Score",
            f"{with_policy['equity']['equity_score']:.2f}/1.00",
            delta_color="normal"
        )
    
    st.markdown("---")
    
    # AI Explanation
    st.markdown("### 🤖 AI Analysis")
    st.markdown(response.explanation)
    
    st.markdown("---")
    
    # Visualizations
    st.markdown("### 📈 Visualizations")
    
    charts = create_results_dashboard(baseline, with_policy, "With Policy")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🚗 Mode Share", "🌍 Emissions", "⚖️ Equity"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(charts["score_comparison"], use_container_width=True)
        with col2:
            st.plotly_chart(charts["metrics_radar"], use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(charts["mode_share"], use_container_width=True)
        with col2:
            st.plotly_chart(charts["mode_shift"], use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(charts["emissions_comparison"], use_container_width=True)
        with col2:
            st.plotly_chart(charts["emissions_breakdown"], use_container_width=True)
    
    with tab4:
        st.plotly_chart(charts["equity_burden"], use_container_width=True)
    
    st.markdown("---")
    
    # Methodology (expandable)
    with st.expander("📖 View Methodology Details"):
        st.markdown("#### Emissions Model")
        st.code(with_policy["emissions"]["methodology"])
        
        st.markdown("#### Cost Model")
        st.code(with_policy["cost"]["methodology"])
        
        st.markdown("#### Equity Model")
        st.code(with_policy["equity"]["methodology"])
        
        st.markdown("#### Mode Share Model")
        st.code(with_policy["mode_share"]["methodology"])
    
    # Agent transparency
    with st.expander("🔍 View Agent Actions (Transparency Log)"):
        for action in response.actions_taken:
            st.markdown(f"**[{action.state.value}]** {action.action}")
            if action.details:
                st.json(action.details)


def render_scenario_comparison_page():
    """Render the scenario comparison page."""
    st.markdown("## 📊 Scenario Comparison")
    st.markdown("Compare multiple policy scenarios side-by-side.")
    
    st.markdown("---")
    
    # Scenario Selection
    st.markdown("### Select Scenarios to Compare")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Pre-built Scenarios:**")
        use_baseline = st.checkbox("📍 Baseline (No Policy)", value=True)
        use_green = st.checkbox("🌿 Green Transport", value=True)
        use_balanced = st.checkbox("⚖️ Balanced Approach", value=True)
        use_equity = st.checkbox("🤝 Equity Focused", value=False)
    
    with col2:
        st.markdown("**Scenario Descriptions:**")
        st.caption("**Baseline:** Current conditions, no changes")
        st.caption("**Green Transport:** Aggressive emission reduction")
        st.caption("**Balanced:** Moderate interventions")
        st.caption("**Equity Focused:** Prioritize affordability")
    
    st.markdown("---")
    
    # Build scenario list
    scenario_names = []
    if use_baseline:
        scenario_names.append("baseline")
    if use_green:
        scenario_names.append("green_transport")
    if use_balanced:
        scenario_names.append("balanced")
    if use_equity:
        scenario_names.append("equity_focused")
    
    if len(scenario_names) < 2:
        st.warning("Please select at least 2 scenarios to compare.")
        return
    
    # Run Comparison Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        run_comparison = st.button("🔄 Compare Scenarios", type="primary", use_container_width=True)
    
    if run_comparison:
        with st.spinner("Running simulations and generating comparison..."):
            response = st.session_state.agent.compare_scenarios(
                scenario_names=scenario_names,
                explain=True
            )
            st.session_state.comparison_results = response
        
        if response.success:
            st.success(f"✅ {response.message}")
            render_comparison_results(response)
        else:
            st.error(f"❌ {response.message}")


def render_comparison_results(response: AgentResponse):
    """Render scenario comparison results."""
    scenarios = response.results["scenarios"]
    comparison = response.comparison
    
    st.markdown("---")
    st.markdown("### 🏆 Best Performers")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Best Overall", comparison["best_overall"])
    with col2:
        st.metric("Best Emissions", comparison["best_emissions"])
    with col3:
        st.metric("Best Cost", comparison["best_cost"])
    with col4:
        st.metric("Best Equity", comparison["best_equity"])
    with col5:
        st.metric("Best Efficiency", comparison["best_efficiency"])
    
    st.markdown("---")
    
    # AI Comparison
    st.markdown("### 🤖 AI Comparative Analysis")
    st.markdown(response.explanation)
    
    st.markdown("---")
    
    # Comparison Charts
    st.markdown("### 📈 Comparison Charts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(
            create_scenario_comparison_chart(scenarios),
            use_container_width=True
        )
    
    with col2:
        st.plotly_chart(
            create_scenario_emissions_chart(scenarios),
            use_container_width=True
        )
    
    st.plotly_chart(
        create_scenario_cost_chart(scenarios),
        use_container_width=True
    )
    
    st.markdown("---")
    
    # Detailed table
    st.markdown("### 📋 Detailed Comparison Table")
    
    import pandas as pd
    
    df_data = []
    for s in scenarios:
        df_data.append({
            "Scenario": s["name"],
            "Overall Score": f"{s['overall_score']:.1f}",
            "CO2 (kg/day)": f"{s['emissions']:,.0f}",
            "User Cost ($)": f"{s['user_cost']:.2f}",
            "Equity Score": f"{s['equity_score']:.2f}",
            "Travel Time (min)": f"{s['travel_time']:.0f}"
        })
    
    df = pd.DataFrame(df_data)
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_natural_language_page():
    """Render the natural language query page."""
    st.markdown("## 💬 Natural Language Query")
    st.markdown("Ask questions about transportation policies in plain English.")
    
    st.markdown("---")
    
    st.markdown("### Ask a Question")
    
    # Example queries
    st.markdown("**Example queries:**")
    example_queries = [
        "What if we implement a $10 congestion charge?",
        "How would a 50% transit subsidy affect emissions?",
        "What's the impact of a 25% fuel tax?",
        "Compare high parking fees with transit subsidies"
    ]
    
    col1, col2 = st.columns(2)
    for i, query in enumerate(example_queries):
        with col1 if i % 2 == 0 else col2:
            if st.button(f"📝 {query}", key=f"example_{i}"):
                st.session_state.nl_query = query
    
    st.markdown("---")
    
    # Query input
    query = st.text_area(
        "Your Question",
        value=st.session_state.get("nl_query", ""),
        placeholder="e.g., What if we implement a 30% public transit subsidy?",
        height=100
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        run_query = st.button("🔍 Analyze", type="primary", use_container_width=True)
    
    if run_query and query:
        with st.spinner("Processing your query..."):
            response = st.session_state.agent.natural_language_query(query)
        
        if response.success:
            st.success(f"✅ {response.message}")
            
            if response.results:
                render_policy_results(response)
            elif response.explanation:
                st.markdown("### 🤖 Response")
                st.markdown(response.explanation)
        else:
            st.error(f"❌ {response.message}")


def render_methodology_page():
    """Render the methodology documentation page."""
    st.markdown("## 📖 Methodology Documentation")
    st.markdown("Transparent documentation of all simulation models.")
    
    st.markdown("---")
    
    llm = LLMHelper()
    
    tabs = st.tabs(["Emissions", "Cost-Benefit", "Equity", "Efficiency", "Mode Share"])
    
    with tabs[0]:
        st.markdown("### 🌍 Emissions Model")
        st.markdown(llm.explain_methodology("emissions"))
        
    with tabs[1]:
        st.markdown("### 💰 Cost-Benefit Model")
        st.markdown(llm.explain_methodology("cost_benefit"))
        
    with tabs[2]:
        st.markdown("### ⚖️ Equity Model")
        st.markdown(llm.explain_methodology("equity"))
        
    with tabs[3]:
        st.markdown("### 🚀 Efficiency Model")
        st.markdown(llm.explain_methodology("efficiency"))
        
    with tabs[4]:
        st.markdown("### 🚗 Mode Share Model")
        st.markdown(llm.explain_methodology("mode_share"))
    
    st.markdown("---")
    
    st.markdown("### 📚 Academic References")
    st.markdown("""
    - IPCC Guidelines for National Greenhouse Gas Inventories
    - World Bank Transport Cost Guidelines
    - Litman (2022) Evaluating Transportation Equity
    - Small & Verhoef (2007) Economics of Urban Transportation
    - Highway Capacity Manual (HCM)
    """)


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application entry point."""
    # Initialize
    init_session_state()
    
    # Validate configuration
    config_errors = validate_config()
    if config_errors:
        st.error("Configuration Error!")
        for error in config_errors:
            st.error(f"- {error}")
        st.stop()
    
    # Render sidebar
    render_sidebar()
    
    # Navigation
    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Home", "🔬 Single Policy", "📊 Compare Scenarios", "💬 Natural Language", "📖 Methodology"],
        label_visibility="collapsed"
    )
    
    # Render selected page
    if page == "🏠 Home":
        render_home_page()
    elif page == "🔬 Single Policy":
        render_single_policy_page()
    elif page == "📊 Compare Scenarios":
        render_scenario_comparison_page()
    elif page == "💬 Natural Language":
        render_natural_language_page()
    elif page == "📖 Methodology":
        render_methodology_page()


if __name__ == "__main__":
    main()