"""
PolicySim-AI LLM Helper
=======================
Handles all interactions with the Groq LLM API.
Uses open-source Llama models for transparent, reproducible AI explanations.
"""

import json
from typing import Dict, List, Optional
from groq import Groq
from config import GROQ_API_KEY, LLM_MODELS


# =============================================================================
# GROQ CLIENT
# =============================================================================

class LLMHelper:
    """
    Helper class for LLM interactions.
    Provides structured prompts and response parsing.
    """
    
    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found. Please check your .env file.")
        
        self.client = Groq(api_key=GROQ_API_KEY)
        self.main_model = LLM_MODELS["main"]
        self.fast_model = LLM_MODELS["fast"]
    
    def _call_llm(
        self, 
        prompt: str, 
        system_prompt: str = None,
        use_fast_model: bool = False,
        temperature: float = 0.3,
        max_tokens: int = 2000
    ) -> str:
        """
        Make a call to the Groq LLM.
        
        Args:
            prompt: User prompt
            system_prompt: System instructions
            use_fast_model: Use faster, smaller model
            temperature: Creativity (0-1)
            max_tokens: Maximum response length
            
        Returns:
            LLM response text
        """
        model = self.fast_model if use_fast_model else self.main_model
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling LLM: {str(e)}"
    
    # =========================================================================
    # POLICY ANALYSIS PROMPTS
    # =========================================================================
    
    def explain_simulation_results(
        self, 
        baseline_results: Dict,
        policy_results: Dict,
        policy_description: str
    ) -> str:
        """
        Generate a plain-language explanation of simulation results.
        
        Args:
            baseline_results: Results without policy
            policy_results: Results with policy
            policy_description: Description of the policy
            
        Returns:
            Human-readable explanation
        """
        system_prompt = """You are an expert transportation policy analyst. 
Your role is to explain simulation results in clear, accessible language.
Focus on:
1. Key changes and their magnitude
2. Trade-offs between different objectives
3. Who benefits and who bears costs
4. Practical implications for decision-makers

Be objective and balanced. Acknowledge uncertainties.
Use specific numbers from the results to support your points.
Keep your explanation concise but comprehensive (2-3 paragraphs)."""

        prompt = f"""Analyze these transportation policy simulation results:

POLICY BEING EVALUATED:
{policy_description}

BASELINE SCENARIO (No Policy):
- Overall Score: {baseline_results.get('overall_score', 'N/A')}/100
- Daily CO2 Emissions: {baseline_results.get('emissions', {}).get('total_co2_kg_per_day', 'N/A'):,} kg
- Average User Cost: ${baseline_results.get('cost', {}).get('user_cost_per_trip', 'N/A'):.2f} per trip
- Equity Score: {baseline_results.get('equity', {}).get('equity_score', 'N/A')}/1.00
- Average Travel Time: {baseline_results.get('efficiency', {}).get('avg_travel_time_minutes', 'N/A')} minutes

WITH POLICY:
- Overall Score: {policy_results.get('overall_score', 'N/A')}/100
- Daily CO2 Emissions: {policy_results.get('emissions', {}).get('total_co2_kg_per_day', 'N/A'):,} kg
- Average User Cost: ${policy_results.get('cost', {}).get('user_cost_per_trip', 'N/A'):.2f} per trip
- Equity Score: {policy_results.get('equity', {}).get('equity_score', 'N/A')}/1.00
- Average Travel Time: {policy_results.get('efficiency', {}).get('avg_travel_time_minutes', 'N/A')} minutes

MODE SHARE CHANGES:
{json.dumps(policy_results.get('mode_share', {}).get('shift_percentage', {}), indent=2)}

Please provide a clear, balanced analysis of these results for a policy-maker."""

        return self._call_llm(prompt, system_prompt)
    
    def compare_scenarios(
        self,
        scenarios: List[Dict]
    ) -> str:
        """
        Compare multiple policy scenarios.
        
        Args:
            scenarios: List of scenario results with names
            
        Returns:
            Comparative analysis
        """
        system_prompt = """You are an expert transportation policy analyst.
Compare multiple policy scenarios objectively.
Identify:
1. Which scenario performs best on each metric
2. Overall trade-offs between scenarios
3. Recommendations based on different policy priorities

Be concise and use a structured format.
Present information that helps decision-makers choose."""

        scenario_text = ""
        for i, scenario in enumerate(scenarios, 1):
            scenario_text += f"""
SCENARIO {i}: {scenario.get('name', f'Scenario {i}')}
- Overall Score: {scenario.get('overall_score', 'N/A')}/100
- CO2 Emissions: {scenario.get('emissions', 'N/A'):,} kg/day
- User Cost: ${scenario.get('user_cost', 'N/A'):.2f}/trip
- Equity Score: {scenario.get('equity_score', 'N/A')}/1.00
- Travel Time: {scenario.get('travel_time', 'N/A')} min
"""

        prompt = f"""Compare these transportation policy scenarios:
{scenario_text}

Provide a comparative analysis with clear recommendations."""

        return self._call_llm(prompt, system_prompt)
    
    def suggest_policy_improvements(
        self,
        current_results: Dict,
        policy_description: str,
        target_metric: str = "overall"
    ) -> str:
        """
        Suggest improvements to a policy based on results.
        
        Args:
            current_results: Current simulation results
            policy_description: Current policy description
            target_metric: Which metric to optimize
            
        Returns:
            Improvement suggestions
        """
        system_prompt = """You are an expert transportation policy advisor.
Based on simulation results, suggest specific improvements to the policy.
Focus on:
1. Parameter adjustments that could improve outcomes
2. Complementary policies that could enhance effectiveness
3. Potential unintended consequences to monitor

Be specific and actionable. Reference evidence where possible."""

        prompt = f"""Current policy: {policy_description}

Current Results:
- Overall Score: {current_results.get('overall_score', 'N/A')}/100
- Emissions: {current_results.get('emissions', {}).get('total_co2_kg_per_day', 'N/A'):,} kg/day
- User Cost: ${current_results.get('cost', {}).get('user_cost_per_trip', 'N/A'):.2f}/trip
- Equity Score: {current_results.get('equity', {}).get('equity_score', 'N/A')}/1.00

Target for improvement: {target_metric}

Suggest specific improvements to enhance this policy's effectiveness."""

        return self._call_llm(prompt, system_prompt)
    
    def generate_policy_brief(
        self,
        scenario_name: str,
        results: Dict,
        policies: List[str],
        context: str = "urban area"
    ) -> str:
        """
        Generate a formal policy brief.
        
        Args:
            scenario_name: Name of the scenario
            results: Simulation results
            policies: List of policies in the scenario
            context: Geographic/demographic context
            
        Returns:
            Formatted policy brief
        """
        system_prompt = """You are a senior transportation policy analyst.
Write a professional policy brief suitable for government decision-makers.
Include:
1. Executive Summary (2-3 sentences)
2. Key Findings (bullet points)
3. Implications (who is affected and how)
4. Recommendations (clear action items)

Use formal, professional language. Be concise but thorough."""

        prompt = f"""Generate a policy brief for:

Scenario: {scenario_name}
Context: {context}
Policies Included: {', '.join(policies)}

Simulation Results:
- Overall Score: {results.get('overall_score', 'N/A')}/100
- CO2 Reduction: {results.get('emissions_change', 'N/A')}%
- Cost Impact: {results.get('cost_change', 'N/A')}%
- Equity Impact: {results.get('equity_score', 'N/A')}/1.00
- Mode Shift: Private car {results.get('car_shift', 'N/A')}%, Public transit {results.get('pt_shift', 'N/A')}%

Generate a professional policy brief."""

        return self._call_llm(prompt, system_prompt, max_tokens=3000)
    
    # =========================================================================
    # AGENT DECISION PROMPTS
    # =========================================================================
    
    def select_relevant_models(
        self,
        user_query: str,
        available_models: List[str]
    ) -> List[str]:
        """
        Determine which simulation models are relevant for a query.
        This is part of the "agentic" behavior.
        
        Args:
            user_query: What the user wants to analyze
            available_models: List of available model names
            
        Returns:
            List of relevant model names
        """
        system_prompt = """You are an AI assistant helping select relevant analysis models.
Given a user query about transportation policy, determine which models should be run.
Return ONLY a JSON array of model names, nothing else.
Available models: emissions, cost_benefit, equity, efficiency, mode_share"""

        prompt = f"""User query: "{user_query}"

Available models: {available_models}

Which models are relevant for this analysis? Return as JSON array.
Example: ["emissions", "cost_benefit"]"""

        response = self._call_llm(prompt, system_prompt, use_fast_model=True, temperature=0.1)
        
        try:
            # Try to parse JSON response
            models = json.loads(response)
            # Validate models exist
            return [m for m in models if m in available_models]
        except json.JSONDecodeError:
            # If parsing fails, return all models
            return available_models
    
    def interpret_user_policy_request(
        self,
        user_input: str
    ) -> Dict:
        """
        Interpret a natural language policy request.
        
        Args:
            user_input: User's description of what they want to analyze
            
        Returns:
            Structured policy parameters
        """
        system_prompt = """You are an AI assistant that interprets transportation policy requests.
Convert natural language into structured policy parameters.
Return ONLY valid JSON with these possible fields:
- policy_type: one of [congestion_pricing, pt_subsidy, fuel_tax, ev_incentive, parking_policy]
- congestion_price: number (0-50)
- pt_subsidy_percent: number (0-100)
- fuel_tax_percent: number (0-100)
- parking_hourly_rate: number (0-20)

Only include fields that are mentioned or implied."""

        prompt = f"""User request: "{user_input}"

Convert this to structured policy parameters. Return only JSON."""

        response = self._call_llm(prompt, system_prompt, use_fast_model=True, temperature=0.1)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {}
    
    # =========================================================================
    # METHODOLOGY EXPLANATION
    # =========================================================================
    
    def explain_methodology(self, model_name: str) -> str:
        """
        Explain the methodology of a specific model.
        
        Args:
            model_name: Name of the model to explain
            
        Returns:
            Methodology explanation
        """
        methodologies = {
            "emissions": """
The emissions model calculates transportation CO2 using:
CO2 = Σ(trips_by_mode × avg_distance × emission_factor)

Emission factors are from IPCC guidelines:
- Private car: 0.21 kg CO2/km (adjusted for occupancy)
- Motorcycle: 0.10 kg CO2/km
- Public transit: 0.05 kg CO2/passenger-km
- Walking/cycling: 0 kg CO2/km
""",
            "cost_benefit": """
The cost-benefit model calculates:
User Cost = fuel_cost + fare + (travel_time × value_of_time)

Where value_of_time = 50% of hourly wage (standard transport economics assumption).
Government cost = subsidy per trip × subsidized trips × 365 days.
""",
            "equity": """
The equity model uses:
- Burden = (transport_cost / income) × 100 for each income quintile
- Gini coefficient on burden distribution
- Equity score = 1 - Gini (higher is more equitable)

Income quintiles: low (0.4×), lower-middle (0.7×), middle (1.0×), 
upper-middle (1.5×), high (2.5×) of average wage.
""",
            "efficiency": """
The efficiency model calculates:
- Average travel time weighted by mode share
- Congestion index = actual_time / free_flow_time
- System throughput = person-km / (trips × travel_hours)

Base times: car 30min, motorcycle 25min, transit 45min, walk/cycle 50min.
""",
            "mode_share": """
Mode share changes use price elasticity:
ΔQ/Q = elasticity × ΔP/P

Elasticities from transport research:
- Private car: -0.3 (inelastic)
- Public transit: -0.4
- Cross-elasticity (car→transit): 0.2-0.3
"""
        }
        
        return methodologies.get(model_name, f"Methodology for {model_name} not found.")


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("Testing PolicySim-AI LLM Helper")
    print("=" * 50)
    
    try:
        llm = LLMHelper()
        print("✅ LLM Helper initialized successfully")
        print(f"   Main model: {llm.main_model}")
        print(f"   Fast model: {llm.fast_model}")
        
        # Test a simple call
        print("\n🧪 Testing LLM call...")
        print("-" * 40)
        
        response = llm._call_llm(
            "What is congestion pricing in transportation? Answer in 2 sentences.",
            use_fast_model=True
        )
        print(f"Response: {response[:300]}...")
        
        # Test model selection (agentic behavior)
        print("\n🤖 Testing Agentic Model Selection...")
        print("-" * 40)
        
        query = "How will a fuel tax affect emissions and costs?"
        models = llm.select_relevant_models(
            query,
            ["emissions", "cost_benefit", "equity", "efficiency", "mode_share"]
        )
        print(f"Query: {query}")
        print(f"Selected models: {models}")
        
        print("\n✅ LLM Helper working correctly!")
        
    except Exception as e:
        print(f"❌ Error: {e}")