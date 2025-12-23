"""
PolicySim-AI Publication Figures
================================
Generate publication-grade figures for research papers.
- High resolution (300 DPI)
- Times New Roman font
- Proper sizing for journals
- Clean, professional styling
"""

import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import os
from typing import Dict, List
from models import PolicySimulator
from policies import ScenarioLibrary

# =============================================================================
# PUBLICATION SETTINGS
# =============================================================================

# Create output directory
OUTPUT_DIR = "publication_figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Publication-grade settings
PUB_SETTINGS = {
    "font_family": "Times New Roman",
    "font_size": 14,
    "title_font_size": 16,
    "axis_font_size": 12,
    "legend_font_size": 11,
    "width": 800,
    "height": 600,
    "dpi": 600,
    "format": "png",  # or "pdf", "svg"
}

# Color palette (colorblind-friendly, journal-appropriate)
PUB_COLORS = {
    "primary": "#2C3E50",      # Dark blue-gray
    "secondary": "#E74C3C",    # Red
    "tertiary": "#27AE60",     # Green
    "quaternary": "#F39C12",   # Orange
    "quinary": "#9B59B6",      # Purple
    "baseline": "#7F8C8D",     # Gray
    
    # Mode colors
    "private_car": "#E74C3C",
    "motorcycle": "#F39C12", 
    "public_transit": "#27AE60",
    "walking_cycling": "#3498DB",
}

# Publication layout template
def get_pub_layout():
    """Get publication-ready layout settings."""
    return go.Layout(
        font=dict(
            family=PUB_SETTINGS["font_family"],
            size=PUB_SETTINGS["font_size"],
            color="black"
        ),
        title_font=dict(
            family=PUB_SETTINGS["font_family"],
            size=PUB_SETTINGS["title_font_size"],
            color="black"
        ),
        legend=dict(
            font=dict(
                family=PUB_SETTINGS["font_family"],
                size=PUB_SETTINGS["legend_font_size"]
            ),
            bordercolor="black",
            borderwidth=1
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        width=PUB_SETTINGS["width"],
        height=PUB_SETTINGS["height"],
        margin=dict(l=80, r=40, t=60, b=80)
    )


def save_figure(fig: go.Figure, filename: str, formats: List[str] = None):
    """Save figure in multiple formats."""
    formats = formats or ["png", "pdf", "svg"]
    
    for fmt in formats:
        filepath = os.path.join(OUTPUT_DIR, f"{filename}.{fmt}")
        
        if fmt == "png":
            fig.write_image(filepath, scale=3)  # High resolution
        elif fmt == "pdf":
            fig.write_image(filepath)
        elif fmt == "svg":
            fig.write_image(filepath)
        elif fmt == "html":
            fig.write_html(filepath)
        
        print(f"  ✓ Saved: {filepath}")


# =============================================================================
# FIGURE 1: MODE SHARE COMPARISON
# =============================================================================

def create_figure1_mode_share(baseline: Dict, policy: Dict, policy_name: str = "With Policy") -> go.Figure:
    """
    Figure 1: Mode Share Comparison Bar Chart
    """
    modes = ["private_car", "motorcycle", "public_transit", "walking_cycling"]
    mode_labels = ["Private Car", "Motorcycle", "Public Transit", "Walking/Cycling"]
    
    baseline_values = [baseline["mode_share"]["baseline_shares"][m] * 100 for m in modes]
    policy_values = [policy["mode_share"]["projected_shares"][m] * 100 for m in modes]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name="Baseline",
        x=mode_labels,
        y=baseline_values,
        marker_color=PUB_COLORS["baseline"],
        text=[f"{v:.1f}%" for v in baseline_values],
        textposition="outside",
        textfont=dict(family=PUB_SETTINGS["font_family"], size=11)
    ))
    
    fig.add_trace(go.Bar(
        name=policy_name,
        x=mode_labels,
        y=policy_values,
        marker_color=PUB_COLORS["primary"],
        text=[f"{v:.1f}%" for v in policy_values],
        textposition="outside",
        textfont=dict(family=PUB_SETTINGS["font_family"], size=11)
    ))
    
    fig.update_layout(get_pub_layout())
    fig.update_layout(
        title=dict(
            text="<b>Figure 1.</b> Transportation Mode Share Comparison",
            x=0.5,
            xanchor="center"
        ),
        yaxis_title="Mode Share (%)",
        xaxis_title="Transportation Mode",
        yaxis_range=[0, 55],
        barmode="group",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )
    
    # Add gridlines
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="lightgray")
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black")
    fig.update_yaxes(showline=True, linewidth=1, linecolor="black")
    
    return fig


# =============================================================================
# FIGURE 2: EMISSIONS COMPARISON
# =============================================================================

def create_figure2_emissions(baseline: Dict, policy: Dict) -> go.Figure:
    """
    Figure 2: CO2 Emissions Comparison
    """
    baseline_total = baseline["emissions"]["total_co2_kg_per_day"] / 1000  # Convert to tonnes
    policy_total = policy["emissions"]["total_co2_kg_per_day"] / 1000
    
    reduction = baseline_total - policy_total
    reduction_pct = (reduction / baseline_total) * 100
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=["Baseline", "With Policy"],
        y=[baseline_total, policy_total],
        marker_color=[PUB_COLORS["baseline"], PUB_COLORS["tertiary"]],
        text=[f"{baseline_total:,.0f}", f"{policy_total:,.0f}"],
        textposition="outside",
        textfont=dict(family=PUB_SETTINGS["font_family"], size=12),
        width=0.5
    ))
    
    fig.update_layout(get_pub_layout())
    fig.update_layout(
        title=dict(
            text=f"<b>Figure 2.</b> Daily CO₂ Emissions (Reduction: {reduction_pct:.1f}%)",
            x=0.5,
            xanchor="center"
        ),
        yaxis_title="CO₂ Emissions (tonnes/day)",
        xaxis_title="Scenario",
        showlegend=False
    )
    
    # Add gridlines
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="lightgray")
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black")
    fig.update_yaxes(showline=True, linewidth=1, linecolor="black")
    
    return fig


# =============================================================================
# FIGURE 3: EMISSIONS BY MODE (PIE CHART)
# =============================================================================

def create_figure3_emissions_breakdown(results: Dict) -> go.Figure:
    """
    Figure 3: Emissions Breakdown by Mode
    """
    co2_by_mode = results["emissions"]["co2_by_mode"]
    
    modes = list(co2_by_mode.keys())
    values = [co2_by_mode[m] / 1000 for m in modes]  # Convert to tonnes
    labels = ["Private Car", "Motorcycle", "Public Transit", "Walking/Cycling"]
    colors = [PUB_COLORS[m] for m in modes]
    
    fig = go.Figure()
    
    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker_colors=colors,
        textinfo="label+percent",
        textfont=dict(family=PUB_SETTINGS["font_family"], size=12),
        hole=0.3,
        pull=[0.02, 0, 0, 0]  # Slightly pull out the largest slice
    ))
    
    fig.update_layout(get_pub_layout())
    fig.update_layout(
        title=dict(
            text="<b>Figure 3.</b> CO₂ Emissions Distribution by Transportation Mode",
            x=0.5,
            xanchor="center"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig


# =============================================================================
# FIGURE 4: EQUITY BURDEN CHART
# =============================================================================

def create_figure4_equity(results: Dict) -> go.Figure:
    """
    Figure 4: Transportation Cost Burden by Income Group
    """
    burden = results["equity"]["burden_by_income"]
    
    groups = list(burden.keys())
    group_labels = ["Low\nIncome", "Lower\nMiddle", "Middle\nIncome", "Upper\nMiddle", "High\nIncome"]
    values = list(burden.values())
    
    # Color gradient based on burden level
    colors = []
    for v in values:
        if v > 15:
            colors.append(PUB_COLORS["secondary"])  # High burden - red
        elif v > 10:
            colors.append(PUB_COLORS["quaternary"])  # Medium - orange
        else:
            colors.append(PUB_COLORS["tertiary"])  # Low - green
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=group_labels,
        y=values,
        marker_color=colors,
        text=[f"{v:.1f}%" for v in values],
        textposition="outside",
        textfont=dict(family=PUB_SETTINGS["font_family"], size=11),
        width=0.6
    ))
    
    fig.update_layout(get_pub_layout())
    fig.update_layout(
        title=dict(
            text="<b>Figure 4.</b> Transportation Cost as Percentage of Income by Group",
            x=0.5,
            xanchor="center"
        ),
        yaxis_title="Transportation Cost (% of Income)",
        xaxis_title="Income Group",
        showlegend=False
    )
    
    # Add reference line at 10%
    fig.add_hline(y=10, line_dash="dash", line_color="gray",
                  annotation_text="10% threshold", annotation_position="right")
    
    # Add gridlines
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="lightgray")
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black")
    fig.update_yaxes(showline=True, linewidth=1, linecolor="black")
    
    return fig


# =============================================================================
# FIGURE 5: MULTI-SCENARIO COMPARISON
# =============================================================================

def create_figure5_scenario_comparison(scenarios: List[Dict]) -> go.Figure:
    """
    Figure 5: Multi-Scenario Performance Comparison
    """
    scenario_names = [s["name"] for s in scenarios]
    
    # Normalize metrics to 0-100 scale for comparison
    metrics = {
        "Overall Score": [s["overall_score"] for s in scenarios],
        "Equity (×100)": [s["equity_score"] * 100 for s in scenarios],
    }
    
    fig = go.Figure()
    
    colors = [PUB_COLORS["primary"], PUB_COLORS["tertiary"]]
    
    for i, (metric, values) in enumerate(metrics.items()):
        fig.add_trace(go.Bar(
            name=metric,
            x=scenario_names,
            y=values,
            marker_color=colors[i],
            text=[f"{v:.1f}" for v in values],
            textposition="outside",
            textfont=dict(family=PUB_SETTINGS["font_family"], size=10)
        ))
    
    fig.update_layout(get_pub_layout())
    fig.update_layout(
        title=dict(
            text="<b>Figure 5.</b> Policy Scenario Performance Comparison",
            x=0.5,
            xanchor="center"
        ),
        yaxis_title="Score (0-100)",
        xaxis_title="Policy Scenario",
        yaxis_range=[0, 100],
        barmode="group",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )
    
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="lightgray")
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black")
    fig.update_yaxes(showline=True, linewidth=1, linecolor="black")
    
    return fig


# =============================================================================
# FIGURE 6: SCENARIO EMISSIONS COMPARISON
# =============================================================================

def create_figure6_scenario_emissions(scenarios: List[Dict]) -> go.Figure:
    """
    Figure 6: CO2 Emissions Across Policy Scenarios
    """
    scenario_names = [s["name"] for s in scenarios]
    emissions = [s["emissions"] / 1000 for s in scenarios]  # Convert to tonnes
    
    # Find baseline for color coding
    baseline_emissions = emissions[0] if scenarios else 0
    
    colors = []
    for e in emissions:
        if e == baseline_emissions:
            colors.append(PUB_COLORS["baseline"])
        elif e < baseline_emissions:
            colors.append(PUB_COLORS["tertiary"])
        else:
            colors.append(PUB_COLORS["secondary"])
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=scenario_names,
        y=emissions,
        marker_color=colors,
        text=[f"{e:,.0f}" for e in emissions],
        textposition="outside",
        textfont=dict(family=PUB_SETTINGS["font_family"], size=11),
        width=0.6
    ))
    
    fig.update_layout(get_pub_layout())
    fig.update_layout(
        title=dict(
            text="<b>Figure 6.</b> Daily CO₂ Emissions by Policy Scenario",
            x=0.5,
            xanchor="center"
        ),
        yaxis_title="CO₂ Emissions (tonnes/day)",
        xaxis_title="Policy Scenario",
        showlegend=False
    )
    
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="lightgray")
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black")
    fig.update_yaxes(showline=True, linewidth=1, linecolor="black")
    
    return fig


# =============================================================================
# FIGURE 7: RADAR CHART
# =============================================================================

def create_figure7_radar(baseline: Dict, policy: Dict, policy_name: str = "With Policy") -> go.Figure:
    """
    Figure 7: Multi-Dimensional Policy Impact Assessment
    """
    categories = ["Emissions<br>Reduction", "Cost<br>Efficiency", "Equity", 
                  "Travel Time<br>Efficiency", "Overall<br>Score"]
    
    # Calculate normalized scores (0-100, higher is better)
    baseline_values = [
        max(0, 100 - baseline["emissions"]["per_trip_co2_kg"] * 50),
        max(0, 100 - baseline["cost"]["user_cost_per_trip"] * 10),
        baseline["equity"]["equity_score"] * 100,
        max(0, 100 - baseline["efficiency"]["avg_travel_time_minutes"]),
        baseline["overall_score"]
    ]
    
    policy_values = [
        max(0, 100 - policy["emissions"]["per_trip_co2_kg"] * 50),
        max(0, 100 - policy["cost"]["user_cost_per_trip"] * 10),
        policy["equity"]["equity_score"] * 100,
        max(0, 100 - policy["efficiency"]["avg_travel_time_minutes"]),
        policy["overall_score"]
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=baseline_values + [baseline_values[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name="Baseline",
        line_color=PUB_COLORS["baseline"],
        fillcolor="rgba(127, 140, 141, 0.3)"
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=policy_values + [policy_values[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name=policy_name,
        line_color=PUB_COLORS["primary"],
        fillcolor="rgba(44, 62, 80, 0.3)"
    ))
    
    fig.update_layout(get_pub_layout())
    fig.update_layout(
        title=dict(
            text="<b>Figure 7.</b> Multi-Dimensional Policy Impact Assessment",
            x=0.5,
            xanchor="center"
        ),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(family=PUB_SETTINGS["font_family"], size=10)
            ),
            angularaxis=dict(
                tickfont=dict(family=PUB_SETTINGS["font_family"], size=11)
            )
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5
        ),
        height=650
    )
    
    return fig


# =============================================================================
# FIGURE 8: MODE SHIFT WATERFALL
# =============================================================================

def create_figure8_mode_shift(results: Dict) -> go.Figure:
    """
    Figure 8: Mode Share Changes (Horizontal Bar)
    """
    shift = results["mode_share"]["shift_percentage"]
    
    modes = list(shift.keys())
    mode_labels = ["Private Car", "Motorcycle", "Public Transit", "Walking/Cycling"]
    values = [shift[m] for m in modes]
    
    colors = [PUB_COLORS["tertiary"] if v > 0 else PUB_COLORS["secondary"] for v in values]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=mode_labels,
        x=values,
        orientation="h",
        marker_color=colors,
        text=[f"{v:+.1f}%" for v in values],
        textposition="outside",
        textfont=dict(family=PUB_SETTINGS["font_family"], size=12)
    ))
    
    fig.update_layout(get_pub_layout())
    fig.update_layout(
        title=dict(
            text="<b>Figure 8.</b> Projected Mode Share Changes Under Policy Intervention",
            x=0.5,
            xanchor="center"
        ),
        xaxis_title="Change in Mode Share (%)",
        yaxis_title="Transportation Mode",
        showlegend=False,
        height=450
    )
    
    # Add vertical line at 0
    fig.add_vline(x=0, line_width=2, line_color="black")
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="lightgray")
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black")
    fig.update_yaxes(showline=True, linewidth=1, linecolor="black")
    
    return fig


# =============================================================================
# MAIN: GENERATE ALL FIGURES
# =============================================================================

def generate_all_publication_figures():
    """Generate all publication-grade figures."""
    
    print("=" * 60)
    print("PolicySim-AI Publication Figure Generator")
    print("=" * 60)
    print(f"\nOutput directory: {os.path.abspath(OUTPUT_DIR)}")
    print(f"Font: {PUB_SETTINGS['font_family']}")
    print(f"Resolution: {PUB_SETTINGS['dpi']} DPI")
    print()
    
    # Initialize simulator
    print("Initializing simulator...")
    simulator = PolicySimulator()
    
    # Run baseline simulation
    print("Running baseline simulation...")
    baseline_result = simulator.simulate({})
    baseline = result_to_dict(baseline_result)
    
    # Run policy simulation (congestion pricing + PT subsidy)
    print("Running policy simulation (Congestion Pricing + PT Subsidy)...")
    policy_params = {
        "congestion_price": 5.0,
        "pt_subsidy_percent": 30
    }
    policy_result = simulator.simulate(policy_params)
    policy = result_to_dict(policy_result)
    
    # Run scenario comparisons
    print("Running scenario comparisons...")
    scenarios_data = []
    
    scenario_configs = [
        ("Baseline", {}),
        ("Green Transport", {"congestion_price": 8.0, "pt_subsidy_percent": 50, "fuel_tax_percent": 30}),
        ("Balanced", {"congestion_price": 3.0, "pt_subsidy_percent": 25}),
        ("Equity Focus", {"pt_subsidy_percent": 70})
    ]
    
    for name, params in scenario_configs:
        result = simulator.simulate(params)
        scenarios_data.append({
            "name": name,
            "overall_score": result.overall_score,
            "emissions": result.emissions.total_co2_kg_per_day,
            "user_cost": result.cost.user_cost_per_trip,
            "equity_score": result.equity.equity_score,
            "travel_time": result.efficiency.avg_travel_time_minutes
        })
    
    # Generate figures
    print("\n" + "-" * 40)
    print("Generating publication figures...")
    print("-" * 40)
    
    figures = {}
    
    # Figure 1: Mode Share Comparison
    print("\n📊 Figure 1: Mode Share Comparison")
    figures["figure1_mode_share"] = create_figure1_mode_share(baseline, policy, "With Policy")
    save_figure(figures["figure1_mode_share"], "figure1_mode_share", ["png", "pdf", "svg"])
    
    # Figure 2: Emissions Comparison
    print("\n📊 Figure 2: Emissions Comparison")
    figures["figure2_emissions"] = create_figure2_emissions(baseline, policy)
    save_figure(figures["figure2_emissions"], "figure2_emissions", ["png", "pdf", "svg"])
    
    # Figure 3: Emissions Breakdown
    print("\n📊 Figure 3: Emissions Breakdown by Mode")
    figures["figure3_emissions_breakdown"] = create_figure3_emissions_breakdown(policy)
    save_figure(figures["figure3_emissions_breakdown"], "figure3_emissions_breakdown", ["png", "pdf", "svg"])
    
    # Figure 4: Equity Burden
    print("\n📊 Figure 4: Equity Burden by Income")
    figures["figure4_equity"] = create_figure4_equity(policy)
    save_figure(figures["figure4_equity"], "figure4_equity", ["png", "pdf", "svg"])
    
    # Figure 5: Scenario Comparison
    print("\n📊 Figure 5: Scenario Performance Comparison")
    figures["figure5_scenario_comparison"] = create_figure5_scenario_comparison(scenarios_data)
    save_figure(figures["figure5_scenario_comparison"], "figure5_scenario_comparison", ["png", "pdf", "svg"])
    
    # Figure 6: Scenario Emissions
    print("\n📊 Figure 6: Scenario Emissions Comparison")
    figures["figure6_scenario_emissions"] = create_figure6_scenario_emissions(scenarios_data)
    save_figure(figures["figure6_scenario_emissions"], "figure6_scenario_emissions", ["png", "pdf", "svg"])
    
    # Figure 7: Radar Chart
    print("\n📊 Figure 7: Multi-Dimensional Assessment (Radar)")
    figures["figure7_radar"] = create_figure7_radar(baseline, policy, "With Policy")
    save_figure(figures["figure7_radar"], "figure7_radar", ["png", "pdf", "svg"])
    
    # Figure 8: Mode Shift
    print("\n📊 Figure 8: Mode Share Changes")
    figures["figure8_mode_shift"] = create_figure8_mode_shift(policy)
    save_figure(figures["figure8_mode_shift"], "figure8_mode_shift", ["png", "pdf", "svg"])
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ ALL FIGURES GENERATED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\n📁 Output location: {os.path.abspath(OUTPUT_DIR)}")
    print(f"\n📄 Generated {len(figures)} figures in PNG, PDF, and SVG formats")
    print("\nFigures ready for publication:")
    for name in figures.keys():
        print(f"  • {name}")
    
    print("\n💡 Tips for your paper:")
    print("  - Use PNG for Word documents")
    print("  - Use PDF for LaTeX documents")
    print("  - Use SVG for web or editing")
    
    return figures


def result_to_dict(result) -> Dict:
    """Convert SimulationResult to dictionary."""
    return {
        "overall_score": result.overall_score,
        "emissions": {
            "total_co2_kg_per_day": result.emissions.total_co2_kg_per_day,
            "per_trip_co2_kg": result.emissions.per_trip_co2_kg,
            "co2_by_mode": result.emissions.co2_by_mode,
        },
        "cost": {
            "user_cost_per_trip": result.cost.user_cost_per_trip,
        },
        "equity": {
            "equity_score": result.equity.equity_score,
            "burden_by_income": result.equity.burden_by_income,
        },
        "efficiency": {
            "avg_travel_time_minutes": result.efficiency.avg_travel_time_minutes,
        },
        "mode_share": {
            "baseline_shares": result.mode_share.baseline_shares,
            "projected_shares": result.mode_share.projected_shares,
            "shift_percentage": result.mode_share.shift_percentage,
        }
    }


# =============================================================================
# RUN
# =============================================================================

if __name__ == "__main__":
    generate_all_publication_figures()