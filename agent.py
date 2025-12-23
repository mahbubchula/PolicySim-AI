"""
PolicySim-AI Agent Orchestrator
===============================
The main "agentic" component that coordinates all other modules.
This agent:
1. Understands user requests
2. Decides which models to run
3. Executes simulations
4. Explains results using LLM
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

from config import DEFAULT_PARAMS, get_context_params, REGIONAL_CONTEXTS
from models import PolicySimulator, SimulationResult
from policies import (
    Policy, PolicyRegistry, PolicyScenario, ScenarioLibrary,
    CongestionPricingPolicy, PublicTransitSubsidyPolicy,
    FuelTaxPolicy, EVIncentivePolicy, ParkingManagementPolicy
)
from llm_helper import LLMHelper


# =============================================================================
# AGENT STATE
# =============================================================================

class AgentState(Enum):
    """Current state of the agent."""
    IDLE = "idle"
    ANALYZING_REQUEST = "analyzing_request"
    SELECTING_MODELS = "selecting_models"
    RUNNING_SIMULATION = "running_simulation"
    GENERATING_EXPLANATION = "generating_explanation"
    COMPLETE = "complete"
    ERROR = "error"


@dataclass
class AgentAction:
    """Record of an agent action."""
    state: AgentState
    action: str
    details: Dict
    

@dataclass
class AgentResponse:
    """Complete response from the agent."""
    success: bool
    message: str
    results: Optional[Dict] = None
    explanation: Optional[str] = None
    actions_taken: List[AgentAction] = None
    comparison: Optional[Dict] = None


# =============================================================================
# MAIN AGENT CLASS
# =============================================================================

class PolicySimAgent:
    """
    Main agent that orchestrates policy simulation and analysis.
    
    This is the "agentic AI" component that:
    - Interprets user requests
    - Decides which analyses to run
    - Coordinates model execution
    - Generates explanations
    
    All decision logic is explicit and inspectable.
    """
    
    def __init__(self, context: str = "default"):
        """
        Initialize the agent.
        
        Args:
            context: Regional context (default, malaysia, thailand, custom)
        """
        self.context = context
        self.params = get_context_params(context)
        self.simulator = PolicySimulator(self.params)
        self.llm = LLMHelper()
        
        # Track agent actions for transparency
        self.action_log: List[AgentAction] = []
        self.state = AgentState.IDLE
    
    def _log_action(self, action: str, details: Dict = None):
        """Log an agent action for transparency."""
        self.action_log.append(AgentAction(
            state=self.state,
            action=action,
            details=details or {}
        ))
    
    def _set_state(self, state: AgentState):
        """Update agent state."""
        self.state = state
        self._log_action(f"State changed to {state.value}")
    
    # =========================================================================
    # CORE AGENT METHODS
    # =========================================================================
    
    def analyze_policy(
        self,
        policy_type: str,
        parameters: Dict = None,
        explain: bool = True
    ) -> AgentResponse:
        """
        Analyze a single policy.
        
        Args:
            policy_type: Type of policy (congestion_pricing, pt_subsidy, etc.)
            parameters: Policy parameters
            explain: Whether to generate LLM explanation
            
        Returns:
            AgentResponse with results and explanation
        """
        self.action_log = []  # Reset log
        
        try:
            # Step 1: Analyze request
            self._set_state(AgentState.ANALYZING_REQUEST)
            self._log_action("Received policy analysis request", {
                "policy_type": policy_type,
                "parameters": parameters
            })
            
            # Step 2: Create policy
            policy = PolicyRegistry.get_policy(policy_type, **(parameters or {}))
            self._log_action("Created policy instance", {"policy_name": policy.name})
            
            # Step 3: Run baseline simulation
            self._set_state(AgentState.RUNNING_SIMULATION)
            baseline = self.simulator.simulate({})
            self._log_action("Completed baseline simulation", {
                "overall_score": baseline.overall_score
            })
            
            # Step 4: Run policy simulation
            policy_adjustments = policy.get_adjustments()
            with_policy = self.simulator.simulate(policy_adjustments)
            self._log_action("Completed policy simulation", {
                "overall_score": with_policy.overall_score
            })
            
            # Step 5: Generate explanation
            explanation = None
            if explain:
                self._set_state(AgentState.GENERATING_EXPLANATION)
                explanation = self.llm.explain_simulation_results(
                    baseline_results=self._result_to_dict(baseline),
                    policy_results=self._result_to_dict(with_policy),
                    policy_description=policy.description
                )
                self._log_action("Generated LLM explanation")
            
            # Complete
            self._set_state(AgentState.COMPLETE)
            
            return AgentResponse(
                success=True,
                message=f"Successfully analyzed {policy.name}",
                results={
                    "baseline": self._result_to_dict(baseline),
                    "with_policy": self._result_to_dict(with_policy),
                    "policy_info": policy.to_dict(),
                    "improvement": {
                        "score_change": with_policy.overall_score - baseline.overall_score,
                        "emissions_change_percent": self._calc_change(
                            baseline.emissions.total_co2_kg_per_day,
                            with_policy.emissions.total_co2_kg_per_day
                        ),
                        "cost_change_percent": self._calc_change(
                            baseline.cost.user_cost_per_trip,
                            with_policy.cost.user_cost_per_trip
                        )
                    }
                },
                explanation=explanation,
                actions_taken=self.action_log.copy()
            )
            
        except Exception as e:
            self._set_state(AgentState.ERROR)
            self._log_action("Error occurred", {"error": str(e)})
            return AgentResponse(
                success=False,
                message=f"Error analyzing policy: {str(e)}",
                actions_taken=self.action_log.copy()
            )
    
    def compare_scenarios(
        self,
        scenario_names: List[str] = None,
        custom_scenarios: List[PolicyScenario] = None,
        explain: bool = True
    ) -> AgentResponse:
        """
        Compare multiple policy scenarios.
        
        Args:
            scenario_names: Names of pre-built scenarios to compare
            custom_scenarios: Custom scenario objects
            explain: Whether to generate LLM explanation
            
        Returns:
            AgentResponse with comparison results
        """
        self.action_log = []
        
        try:
            self._set_state(AgentState.ANALYZING_REQUEST)
            
            # Gather scenarios
            scenarios = []
            
            # Add pre-built scenarios
            if scenario_names:
                scenario_map = {
                    "baseline": ScenarioLibrary.get_baseline,
                    "green_transport": ScenarioLibrary.get_green_transport,
                    "equity_focused": ScenarioLibrary.get_equity_focused,
                    "balanced": ScenarioLibrary.get_balanced
                }
                for name in scenario_names:
                    if name in scenario_map:
                        scenarios.append(scenario_map[name]())
            
            # Add custom scenarios
            if custom_scenarios:
                scenarios.extend(custom_scenarios)
            
            if not scenarios:
                scenarios = [
                    ScenarioLibrary.get_baseline(),
                    ScenarioLibrary.get_green_transport(),
                    ScenarioLibrary.get_balanced()
                ]
            
            self._log_action("Prepared scenarios for comparison", {
                "count": len(scenarios),
                "names": [s.name for s in scenarios]
            })
            
            # Run simulations
            self._set_state(AgentState.RUNNING_SIMULATION)
            results = []
            
            for scenario in scenarios:
                adjustments = scenario.get_combined_adjustments()
                sim_result = self.simulator.simulate(adjustments)
                
                results.append({
                    "name": scenario.name,
                    "description": scenario.description,
                    "policies": [p.name for p in scenario.policies],
                    "adjustments": adjustments,
                    "overall_score": sim_result.overall_score,
                    "emissions": sim_result.emissions.total_co2_kg_per_day,
                    "user_cost": sim_result.cost.user_cost_per_trip,
                    "equity_score": sim_result.equity.equity_score,
                    "travel_time": sim_result.efficiency.avg_travel_time_minutes,
                    "mode_share": sim_result.mode_share.projected_shares
                })
                
                self._log_action(f"Simulated scenario: {scenario.name}", {
                    "score": sim_result.overall_score
                })
            
            # Generate comparison explanation
            explanation = None
            if explain:
                self._set_state(AgentState.GENERATING_EXPLANATION)
                explanation = self.llm.compare_scenarios(results)
                self._log_action("Generated comparison explanation")
            
            # Find best scenario for each metric
            comparison = self._analyze_comparison(results)
            
            self._set_state(AgentState.COMPLETE)
            
            return AgentResponse(
                success=True,
                message=f"Successfully compared {len(scenarios)} scenarios",
                results={"scenarios": results},
                explanation=explanation,
                comparison=comparison,
                actions_taken=self.action_log.copy()
            )
            
        except Exception as e:
            self._set_state(AgentState.ERROR)
            return AgentResponse(
                success=False,
                message=f"Error comparing scenarios: {str(e)}",
                actions_taken=self.action_log.copy()
            )
    
    def natural_language_query(self, query: str) -> AgentResponse:
        """
        Process a natural language query about transportation policy.
        This demonstrates the "agentic" capability of understanding requests.
        
        Args:
            query: Natural language question or request
            
        Returns:
            AgentResponse with appropriate analysis
        """
        self.action_log = []
        
        try:
            self._set_state(AgentState.ANALYZING_REQUEST)
            self._log_action("Received natural language query", {"query": query})
            
            # Step 1: Interpret the query
            interpreted = self.llm.interpret_user_policy_request(query)
            self._log_action("Interpreted query", {"interpretation": interpreted})
            
            if not interpreted:
                # Couldn't interpret - provide helpful response
                return AgentResponse(
                    success=True,
                    message="I couldn't identify specific policy parameters in your query.",
                    explanation=(
                        "Try asking about specific policies like:\n"
                        "- 'What if we implement a $5 congestion charge?'\n"
                        "- 'How would a 30% transit subsidy affect emissions?'\n"
                        "- 'Compare congestion pricing with fuel tax'"
                    ),
                    actions_taken=self.action_log.copy()
                )
            
            # Step 2: Determine what analysis to run
            policy_type = interpreted.get("policy_type")
            
            if policy_type:
                # Single policy analysis
                # Map interpreted params to policy constructor params
                param_mapping = {
                    "pt_subsidy_percent": "subsidy_percent",
                    "congestion_price": "price_per_entry",
                    "fuel_tax_percent": "tax_percent",
                    "parking_hourly_rate": "hourly_rate"
                }
                
                params = {}
                for k, v in interpreted.items():
                    if k != "policy_type":
                        # Use mapped name if exists, otherwise use original
                        mapped_key = param_mapping.get(k, k)
                        params[mapped_key] = v
                
                return self.analyze_policy(policy_type, params, explain=True)
            else:
                # Run with interpreted parameters
                self._set_state(AgentState.RUNNING_SIMULATION)
                baseline = self.simulator.simulate({})
                with_policy = self.simulator.simulate(interpreted)
                
                self._set_state(AgentState.GENERATING_EXPLANATION)
                explanation = self.llm.explain_simulation_results(
                    baseline_results=self._result_to_dict(baseline),
                    policy_results=self._result_to_dict(with_policy),
                    policy_description=f"Custom policy with parameters: {interpreted}"
                )
                
                self._set_state(AgentState.COMPLETE)
                
                return AgentResponse(
                    success=True,
                    message="Analyzed your policy query",
                    results={
                        "baseline": self._result_to_dict(baseline),
                        "with_policy": self._result_to_dict(with_policy),
                        "interpreted_params": interpreted
                    },
                    explanation=explanation,
                    actions_taken=self.action_log.copy()
                )
                
        except Exception as e:
            self._set_state(AgentState.ERROR)
            return AgentResponse(
                success=False,
                message=f"Error processing query: {str(e)}",
                actions_taken=self.action_log.copy()
            )
    
    def get_policy_recommendations(
        self,
        target: str = "emissions",
        budget_constraint: float = None
    ) -> AgentResponse:
        """
        Get AI-powered policy recommendations.
        
        Args:
            target: What to optimize (emissions, cost, equity, efficiency)
            budget_constraint: Maximum government spending
            
        Returns:
            AgentResponse with recommendations
        """
        self.action_log = []
        
        try:
            self._set_state(AgentState.ANALYZING_REQUEST)
            self._log_action("Generating policy recommendations", {
                "target": target,
                "budget": budget_constraint
            })
            
            # Test different policy combinations
            self._set_state(AgentState.RUNNING_SIMULATION)
            
            test_policies = [
                ("Low Congestion Price", {"congestion_price": 2.0}),
                ("Medium Congestion Price", {"congestion_price": 5.0}),
                ("High Congestion Price", {"congestion_price": 10.0}),
                ("Low PT Subsidy", {"pt_subsidy_percent": 20}),
                ("Medium PT Subsidy", {"pt_subsidy_percent": 40}),
                ("High PT Subsidy", {"pt_subsidy_percent": 60}),
                ("Low Fuel Tax", {"fuel_tax_percent": 10}),
                ("High Fuel Tax", {"fuel_tax_percent": 30}),
                ("Combined Moderate", {"congestion_price": 3.0, "pt_subsidy_percent": 25}),
                ("Combined Aggressive", {"congestion_price": 8.0, "pt_subsidy_percent": 50, "fuel_tax_percent": 20})
            ]
            
            results = []
            baseline = self.simulator.simulate({})
            
            for name, params in test_policies:
                result = self.simulator.simulate(params)
                
                # Calculate government cost (rough estimate)
                govt_cost = result.cost.government_cost_per_year
                
                # Skip if over budget
                if budget_constraint and govt_cost > budget_constraint:
                    continue
                
                results.append({
                    "name": name,
                    "params": params,
                    "overall_score": result.overall_score,
                    "emissions": result.emissions.total_co2_kg_per_day,
                    "emissions_reduction": self._calc_change(
                        baseline.emissions.total_co2_kg_per_day,
                        result.emissions.total_co2_kg_per_day
                    ),
                    "user_cost": result.cost.user_cost_per_trip,
                    "govt_cost": govt_cost,
                    "equity": result.equity.equity_score
                })
            
            # Sort by target metric
            if target == "emissions":
                results.sort(key=lambda x: x["emissions"])
            elif target == "cost":
                results.sort(key=lambda x: x["user_cost"])
            elif target == "equity":
                results.sort(key=lambda x: -x["equity"])  # Higher is better
            else:
                results.sort(key=lambda x: -x["overall_score"])
            
            # Get top 3 recommendations
            top_3 = results[:3]
            
            self._set_state(AgentState.GENERATING_EXPLANATION)
            
            # Generate explanation
            explanation = f"""Based on optimizing for **{target}**, here are the top recommendations:

**1. {top_3[0]['name']}**
   - Parameters: {top_3[0]['params']}
   - Overall Score: {top_3[0]['overall_score']}/100
   - Emissions Reduction: {top_3[0]['emissions_reduction']:.1f}%
   
**2. {top_3[1]['name']}**
   - Parameters: {top_3[1]['params']}
   - Overall Score: {top_3[1]['overall_score']}/100
   - Emissions Reduction: {top_3[1]['emissions_reduction']:.1f}%

**3. {top_3[2]['name']}**
   - Parameters: {top_3[2]['params']}
   - Overall Score: {top_3[2]['overall_score']}/100
   - Emissions Reduction: {top_3[2]['emissions_reduction']:.1f}%

The top recommendation achieves the best {target} outcome while maintaining balance across other metrics."""

            self._set_state(AgentState.COMPLETE)
            
            return AgentResponse(
                success=True,
                message=f"Generated {len(results)} policy options, showing top 3",
                results={
                    "recommendations": top_3,
                    "all_tested": results,
                    "baseline_score": baseline.overall_score
                },
                explanation=explanation,
                actions_taken=self.action_log.copy()
            )
            
        except Exception as e:
            self._set_state(AgentState.ERROR)
            return AgentResponse(
                success=False,
                message=f"Error generating recommendations: {str(e)}",
                actions_taken=self.action_log.copy()
            )
    
    # =========================================================================
    # HELPER METHODS
    # =========================================================================
    
    def _result_to_dict(self, result: SimulationResult) -> Dict:
        """Convert SimulationResult to dictionary."""
        return {
            "overall_score": result.overall_score,
            "summary": result.summary,
            "emissions": {
                "total_co2_kg_per_day": result.emissions.total_co2_kg_per_day,
                "per_trip_co2_kg": result.emissions.per_trip_co2_kg,
                "co2_by_mode": result.emissions.co2_by_mode,
                "methodology": result.emissions.methodology
            },
            "cost": {
                "user_cost_per_trip": result.cost.user_cost_per_trip,
                "total_user_cost_per_day": result.cost.total_user_cost_per_day,
                "government_cost_per_year": result.cost.government_cost_per_year,
                "cost_by_mode": result.cost.cost_by_mode,
                "methodology": result.cost.methodology
            },
            "equity": {
                "equity_score": result.equity.equity_score,
                "gini_index": result.equity.gini_index,
                "burden_by_income": result.equity.burden_by_income,
                "methodology": result.equity.methodology
            },
            "efficiency": {
                "avg_travel_time_minutes": result.efficiency.avg_travel_time_minutes,
                "congestion_index": result.efficiency.congestion_index,
                "travel_time_by_mode": result.efficiency.travel_time_by_mode,
                "methodology": result.efficiency.methodology
            },
            "mode_share": {
                "baseline_shares": result.mode_share.baseline_shares,
                "projected_shares": result.mode_share.projected_shares,
                "shift_percentage": result.mode_share.shift_percentage,
                "methodology": result.mode_share.methodology
            }
        }
    
    def _calc_change(self, baseline: float, new_value: float) -> float:
        """Calculate percentage change."""
        if baseline == 0:
            return 0.0
        return round((new_value - baseline) / baseline * 100, 2)
    
    def _analyze_comparison(self, results: List[Dict]) -> Dict:
        """Analyze comparison results to find best performers."""
        if not results:
            return {}
        
        comparison = {
            "best_overall": max(results, key=lambda x: x["overall_score"])["name"],
            "best_emissions": min(results, key=lambda x: x["emissions"])["name"],
            "best_cost": min(results, key=lambda x: x["user_cost"])["name"],
            "best_equity": max(results, key=lambda x: x["equity_score"])["name"],
            "best_efficiency": min(results, key=lambda x: x["travel_time"])["name"]
        }
        
        return comparison
    
    def get_action_log(self) -> List[Dict]:
        """Get the action log for transparency."""
        return [
            {
                "state": action.state.value,
                "action": action.action,
                "details": action.details
            }
            for action in self.action_log
        ]


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("Testing PolicySim-AI Agent")
    print("=" * 50)
    
    # Initialize agent
    agent = PolicySimAgent(context="default")
    print("✅ Agent initialized")
    
    # Test 1: Analyze single policy
    print("\n" + "=" * 50)
    print("TEST 1: Single Policy Analysis")
    print("=" * 50)
    
    response = agent.analyze_policy(
        policy_type="congestion_pricing",
        parameters={"price_per_entry": 5.0},
        explain=True
    )
    
    print(f"\nSuccess: {response.success}")
    print(f"Message: {response.message}")
    print(f"\nScore Change: {response.results['improvement']['score_change']:+.1f}")
    print(f"Emissions Change: {response.results['improvement']['emissions_change_percent']:+.1f}%")
    print(f"\nExplanation Preview:")
    print(response.explanation[:500] + "..." if response.explanation else "No explanation")
    
    # Test 2: Compare scenarios
    print("\n" + "=" * 50)
    print("TEST 2: Scenario Comparison")
    print("=" * 50)
    
    response = agent.compare_scenarios(
        scenario_names=["baseline", "green_transport", "balanced"],
        explain=True
    )
    
    print(f"\nSuccess: {response.success}")
    print(f"Scenarios compared: {len(response.results['scenarios'])}")
    print(f"\nBest performers:")
    for metric, winner in response.comparison.items():
        print(f"  {metric}: {winner}")
    
    # Test 3: Natural language query
    print("\n" + "=" * 50)
    print("TEST 3: Natural Language Query")
    print("=" * 50)
    
    response = agent.natural_language_query(
        "What if we implement a 30% public transit subsidy?"
    )
    
    print(f"\nSuccess: {response.success}")
    print(f"Message: {response.message}")
    if response.explanation:
        print(f"\nExplanation Preview:")
        print(response.explanation[:400] + "..." if len(response.explanation) > 400 else response.explanation)
    
    # Test 4: Show action log (transparency)
    print("\n" + "=" * 50)
    print("TEST 4: Agent Action Log (Transparency)")
    print("=" * 50)
    
    for action in agent.get_action_log()[:5]:
        print(f"  [{action['state']}] {action['action']}")
    
    print("\n✅ All agent tests completed!")