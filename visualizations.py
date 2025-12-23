"""
PolicySim-AI Visualizations
===========================
Charts and graphs for policy analysis results.
Uses Plotly for interactive visualizations.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List, Optional
import pandas as pd


# =============================================================================
# COLOR SCHEMES
# =============================================================================

COLORS = {
    "primary": "#2E86AB",
    "secondary": "#A23B72",
    "success": "#18A558",
    "warning": "#F18F01",
    "danger": "#C73E1D",
    "neutral": "#6C757D",
    "background": "#F8F9FA",
    
    # Mode colors
    "private_car": "#C73E1D",
    "motorcycle": "#F18F01",
    "public_transit": "#18A558",
    "walking_cycling": "#2E86AB",
    
    # Scenario colors
    "baseline": "#6C757D",
    "policy": "#2E86AB",
    "green": "#18A558",
    "balanced": "#F18F01"
}


# =============================================================================
# COMPARISON CHARTS
# =============================================================================

def create_score_comparison_chart(
    baseline_score: float,
    policy_score: float,
    policy_name: str = "With Policy"
) -> go.Figure:
    """
    Create a simple bar chart comparing overall scores.
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=["Baseline", policy_name],
        y=[baseline_score, policy_score],
        marker_color=[COLORS["baseline"], COLORS["primary"]],
        text=[f"{baseline_score:.1f}", f"{policy_score:.1f}"],
        textposition="outside"
    ))
    
    fig.update_layout(
        title="Overall Policy Score Comparison",
        yaxis_title="Score (0-100)",
        yaxis_range=[0, 100],
        showlegend=False,
        height=400
    )
    
    return fig


def create_metrics_radar_chart(
    baseline_results: Dict,
    policy_results: Dict,
    policy_name: str = "With Policy"
) -> go.Figure:
    """
    Create a radar chart comparing multiple metrics.
    """
    # Normalize metrics to 0-100 scale
    categories = ["Emissions", "User Cost", "Equity", "Efficiency", "Overall"]
    
    # Calculate normalized scores (higher is better for all)
    baseline_values = [
        max(0, 100 - baseline_results["emissions"]["per_trip_co2_kg"] * 50),
        max(0, 100 - baseline_results["cost"]["user_cost_per_trip"] * 10),
        baseline_results["equity"]["equity_score"] * 100,
        max(0, 100 - baseline_results["efficiency"]["avg_travel_time_minutes"]),
        baseline_results["overall_score"]
    ]
    
    policy_values = [
        max(0, 100 - policy_results["emissions"]["per_trip_co2_kg"] * 50),
        max(0, 100 - policy_results["cost"]["user_cost_per_trip"] * 10),
        policy_results["equity"]["equity_score"] * 100,
        max(0, 100 - policy_results["efficiency"]["avg_travel_time_minutes"]),
        policy_results["overall_score"]
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=baseline_values + [baseline_values[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name="Baseline",
        line_color=COLORS["baseline"],
        fillcolor=f"rgba(108, 117, 125, 0.3)"
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=policy_values + [policy_values[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name=policy_name,
        line_color=COLORS["primary"],
        fillcolor=f"rgba(46, 134, 171, 0.3)"
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title="Multi-Metric Policy Comparison",
        height=500
    )
    
    return fig


def create_mode_share_comparison(
    baseline_shares: Dict[str, float],
    policy_shares: Dict[str, float]
) -> go.Figure:
    """
    Create a grouped bar chart comparing mode shares.
    """
    modes = list(baseline_shares.keys())
    mode_labels = [m.replace("_", " ").title() for m in modes]
    
    baseline_values = [baseline_shares[m] * 100 for m in modes]
    policy_values = [policy_shares[m] * 100 for m in modes]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name="Baseline",
        x=mode_labels,
        y=baseline_values,
        marker_color=COLORS["baseline"]
    ))
    
    fig.add_trace(go.Bar(
        name="With Policy",
        x=mode_labels,
        y=policy_values,
        marker_color=COLORS["primary"]
    ))
    
    fig.update_layout(
        title="Mode Share Comparison",
        yaxis_title="Share (%)",
        barmode="group",
        height=400
    )
    
    return fig


def create_mode_shift_chart(shift_percentages: Dict[str, float]) -> go.Figure:
    """
    Create a horizontal bar chart showing mode shift percentages.
    """
    modes = list(shift_percentages.keys())
    mode_labels = [m.replace("_", " ").title() for m in modes]
    values = [shift_percentages[m] for m in modes]
    
    # Color based on positive/negative
    colors = [COLORS["success"] if v > 0 else COLORS["danger"] for v in values]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=mode_labels,
        x=values,
        orientation="h",
        marker_color=colors,
        text=[f"{v:+.1f}%" for v in values],
        textposition="outside"
    ))
    
    fig.update_layout(
        title="Mode Share Changes (%)",
        xaxis_title="Change (%)",
        height=300,
        showlegend=False
    )
    
    # Add vertical line at 0
    fig.add_vline(x=0, line_dash="dash", line_color="gray")
    
    return fig


# =============================================================================
# EMISSIONS CHARTS
# =============================================================================

def create_emissions_breakdown_chart(
    co2_by_mode: Dict[str, float],
    title: str = "CO2 Emissions by Mode"
) -> go.Figure:
    """
    Create a pie chart showing emissions breakdown by mode.
    """
    modes = list(co2_by_mode.keys())
    values = list(co2_by_mode.values())
    labels = [m.replace("_", " ").title() for m in modes]
    colors = [COLORS.get(m, COLORS["neutral"]) for m in modes]
    
    fig = go.Figure()
    
    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker_colors=colors,
        textinfo="label+percent",
        hole=0.4
    ))
    
    fig.update_layout(
        title=title,
        height=400
    )
    
    return fig


def create_emissions_comparison_bar(
    baseline_emissions: float,
    policy_emissions: float
) -> go.Figure:
    """
    Create a bar chart comparing total emissions.
    """
    reduction = baseline_emissions - policy_emissions
    reduction_pct = (reduction / baseline_emissions) * 100
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=["Baseline", "With Policy"],
        y=[baseline_emissions, policy_emissions],
        marker_color=[COLORS["danger"], COLORS["success"]],
        text=[f"{baseline_emissions:,.0f}", f"{policy_emissions:,.0f}"],
        textposition="outside"
    ))
    
    fig.update_layout(
        title=f"Daily CO2 Emissions (Reduction: {reduction_pct:.1f}%)",
        yaxis_title="kg CO2/day",
        height=400,
        showlegend=False
    )
    
    return fig


# =============================================================================
# EQUITY CHARTS
# =============================================================================

def create_equity_burden_chart(burden_by_income: Dict[str, float]) -> go.Figure:
    """
    Create a bar chart showing transportation cost burden by income group.
    """
    groups = list(burden_by_income.keys())
    group_labels = [g.replace("_", " ").title() for g in groups]
    values = list(burden_by_income.values())
    
    # Color gradient from green (low burden) to red (high burden)
    colors = [
        COLORS["success"] if v < 10 else 
        COLORS["warning"] if v < 20 else 
        COLORS["danger"] 
        for v in values
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=group_labels,
        y=values,
        marker_color=colors,
        text=[f"{v:.1f}%" for v in values],
        textposition="outside"
    ))
    
    fig.update_layout(
        title="Transportation Cost as % of Income by Group",
        yaxis_title="Cost Burden (%)",
        height=400,
        showlegend=False
    )
    
    return fig


# =============================================================================
# SCENARIO COMPARISON CHARTS
# =============================================================================

def create_scenario_comparison_chart(scenarios: List[Dict]) -> go.Figure:
    """
    Create a grouped bar chart comparing multiple scenarios.
    """
    scenario_names = [s["name"] for s in scenarios]
    
    metrics = {
        "Overall Score": [s["overall_score"] for s in scenarios],
        "Equity Score": [s["equity_score"] * 100 for s in scenarios],
    }
    
    fig = go.Figure()
    
    colors = [COLORS["primary"], COLORS["success"]]
    
    for i, (metric, values) in enumerate(metrics.items()):
        fig.add_trace(go.Bar(
            name=metric,
            x=scenario_names,
            y=values,
            marker_color=colors[i]
        ))
    
    fig.update_layout(
        title="Scenario Score Comparison",
        yaxis_title="Score",
        yaxis_range=[0, 100],
        barmode="group",
        height=400
    )
    
    return fig


def create_scenario_emissions_chart(scenarios: List[Dict]) -> go.Figure:
    """
    Create a bar chart comparing emissions across scenarios.
    """
    scenario_names = [s["name"] for s in scenarios]
    emissions = [s["emissions"] for s in scenarios]
    
    # Find baseline for comparison
    baseline_emissions = emissions[0] if scenarios else 0
    
    colors = []
    for e in emissions:
        if e == baseline_emissions:
            colors.append(COLORS["baseline"])
        elif e < baseline_emissions:
            colors.append(COLORS["success"])
        else:
            colors.append(COLORS["danger"])
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=scenario_names,
        y=emissions,
        marker_color=colors,
        text=[f"{e:,.0f}" for e in emissions],
        textposition="outside"
    ))
    
    fig.update_layout(
        title="Daily CO2 Emissions by Scenario",
        yaxis_title="kg CO2/day",
        height=400,
        showlegend=False
    )
    
    return fig


def create_scenario_cost_chart(scenarios: List[Dict]) -> go.Figure:
    """
    Create a bar chart comparing user costs across scenarios.
    """
    scenario_names = [s["name"] for s in scenarios]
    costs = [s["user_cost"] for s in scenarios]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=scenario_names,
        y=costs,
        marker_color=COLORS["primary"],
        text=[f"${c:.2f}" for c in costs],
        textposition="outside"
    ))
    
    fig.update_layout(
        title="Average User Cost per Trip by Scenario",
        yaxis_title="Cost ($)",
        height=400,
        showlegend=False
    )
    
    return fig


# =============================================================================
# SENSITIVITY ANALYSIS CHARTS
# =============================================================================

def create_sensitivity_chart(
    parameter_name: str,
    parameter_values: List[float],
    metric_values: List[float],
    metric_name: str = "Overall Score"
) -> go.Figure:
    """
    Create a line chart showing sensitivity of a metric to a parameter.
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=parameter_values,
        y=metric_values,
        mode="lines+markers",
        line=dict(color=COLORS["primary"], width=3),
        marker=dict(size=10)
    ))
    
    fig.update_layout(
        title=f"Sensitivity Analysis: {metric_name} vs {parameter_name}",
        xaxis_title=parameter_name,
        yaxis_title=metric_name,
        height=400
    )
    
    return fig


# =============================================================================
# DASHBOARD LAYOUT
# =============================================================================

def create_results_dashboard(
    baseline_results: Dict,
    policy_results: Dict,
    policy_name: str = "With Policy"
) -> Dict[str, go.Figure]:
    """
    Create a complete dashboard of charts for policy analysis.
    
    Returns:
        Dictionary of chart names to Plotly figures
    """
    charts = {}
    
    # Score comparison
    charts["score_comparison"] = create_score_comparison_chart(
        baseline_results["overall_score"],
        policy_results["overall_score"],
        policy_name
    )
    
    # Radar chart
    charts["metrics_radar"] = create_metrics_radar_chart(
        baseline_results,
        policy_results,
        policy_name
    )
    
    # Mode share comparison
    charts["mode_share"] = create_mode_share_comparison(
        baseline_results["mode_share"]["baseline_shares"],
        policy_results["mode_share"]["projected_shares"]
    )
    
    # Mode shift
    charts["mode_shift"] = create_mode_shift_chart(
        policy_results["mode_share"]["shift_percentage"]
    )
    
    # Emissions comparison
    charts["emissions_comparison"] = create_emissions_comparison_bar(
        baseline_results["emissions"]["total_co2_kg_per_day"],
        policy_results["emissions"]["total_co2_kg_per_day"]
    )
    
    # Emissions breakdown
    charts["emissions_breakdown"] = create_emissions_breakdown_chart(
        policy_results["emissions"]["co2_by_mode"]
    )
    
    # Equity burden
    charts["equity_burden"] = create_equity_burden_chart(
        policy_results["equity"]["burden_by_income"]
    )
    
    return charts


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("Testing PolicySim-AI Visualizations")
    print("=" * 50)
    
    # Create sample data
    baseline = {
        "overall_score": 66.7,
        "emissions": {
            "total_co2_kg_per_day": 3230769,
            "per_trip_co2_kg": 1.29,
            "co2_by_mode": {
                "private_car": 2100000,
                "motorcycle": 625000,
                "public_transit": 250000,
                "walking_cycling": 0
            }
        },
        "cost": {"user_cost_per_trip": 3.57},
        "equity": {
            "equity_score": 0.67,
            "burden_by_income": {
                "low": 22.5,
                "lower_middle": 12.8,
                "middle": 9.0,
                "upper_middle": 6.0,
                "high": 3.6
            }
        },
        "efficiency": {"avg_travel_time_minutes": 34},
        "mode_share": {
            "baseline_shares": {
                "private_car": 0.45,
                "motorcycle": 0.25,
                "public_transit": 0.20,
                "walking_cycling": 0.10
            },
            "projected_shares": {
                "private_car": 0.45,
                "motorcycle": 0.25,
                "public_transit": 0.20,
                "walking_cycling": 0.10
            },
            "shift_percentage": {
                "private_car": 0,
                "motorcycle": 0,
                "public_transit": 0,
                "walking_cycling": 0
            }
        }
    }
    
    policy = {
        "overall_score": 67.2,
        "emissions": {
            "total_co2_kg_per_day": 3099877,
            "per_trip_co2_kg": 1.24,
            "co2_by_mode": {
                "private_car": 1900000,
                "motorcycle": 650000,
                "public_transit": 290000,
                "walking_cycling": 0
            }
        },
        "cost": {"user_cost_per_trip": 3.53},
        "equity": {
            "equity_score": 0.67,
            "burden_by_income": {
                "low": 21.5,
                "lower_middle": 12.3,
                "middle": 8.6,
                "upper_middle": 5.7,
                "high": 3.4
            }
        },
        "efficiency": {"avg_travel_time_minutes": 34},
        "mode_share": {
            "baseline_shares": {
                "private_car": 0.45,
                "motorcycle": 0.25,
                "public_transit": 0.20,
                "walking_cycling": 0.10
            },
            "projected_shares": {
                "private_car": 0.409,
                "motorcycle": 0.257,
                "public_transit": 0.231,
                "walking_cycling": 0.103
            },
            "shift_percentage": {
                "private_car": -9.1,
                "motorcycle": 2.8,
                "public_transit": 15.5,
                "walking_cycling": 2.9
            }
        }
    }
    
    # Create dashboard
    print("\n📊 Creating visualization dashboard...")
    charts = create_results_dashboard(baseline, policy, "Congestion Pricing")
    
    print(f"\n✅ Created {len(charts)} charts:")
    for name in charts.keys():
        print(f"   - {name}")
    
    # Save one chart as HTML for testing
    print("\n💾 Saving sample chart to 'test_chart.html'...")
    charts["metrics_radar"].write_html("test_chart.html")
    print("   Open 'test_chart.html' in your browser to see the chart!")
    
    print("\n✅ Visualizations module working correctly!")