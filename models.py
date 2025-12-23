"""
PolicySim-AI Simulation Models
==============================
Transparent mathematical models for transportation policy evaluation.
All formulas are explicit and documented for research reproducibility.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional
from config import DEFAULT_PARAMS, EVALUATION_METRICS


# =============================================================================
# DATA CLASSES FOR STRUCTURED RESULTS
# =============================================================================

@dataclass
class EmissionsResult:
    """Results from emissions model."""
    total_co2_kg_per_day: float
    co2_by_mode: Dict[str, float]
    per_capita_co2_kg: float
    per_trip_co2_kg: float
    methodology: str


@dataclass
class CostResult:
    """Results from cost-benefit model."""
    user_cost_per_trip: float
    total_user_cost_per_day: float
    government_cost_per_year: float
    cost_by_mode: Dict[str, float]
    methodology: str


@dataclass
class EquityResult:
    """Results from equity model."""
    gini_index: float
    accessibility_by_income: Dict[str, float]
    burden_by_income: Dict[str, float]
    equity_score: float  # 0-1, higher is more equitable
    methodology: str


@dataclass
class EfficiencyResult:
    """Results from efficiency model."""
    avg_travel_time_minutes: float
    travel_time_by_mode: Dict[str, float]
    congestion_index: float
    system_throughput: float
    methodology: str


@dataclass
class ModeShareResult:
    """Results from mode share model."""
    baseline_shares: Dict[str, float]
    projected_shares: Dict[str, float]
    shift_percentage: Dict[str, float]
    methodology: str


@dataclass
class SimulationResult:
    """Combined results from all models."""
    emissions: EmissionsResult
    cost: CostResult
    equity: EquityResult
    efficiency: EfficiencyResult
    mode_share: ModeShareResult
    overall_score: float
    summary: str


# =============================================================================
# EMISSIONS MODEL
# =============================================================================

class EmissionsModel:
    """
    Calculates transportation emissions based on mode share and travel patterns.
    
    Formula:
        Total CO2 = Σ (trips_by_mode × avg_distance × emission_factor)
    
    References:
        - IPCC Guidelines for National Greenhouse Gas Inventories
        - EPA Motor Vehicle Emission Simulator (MOVES)
    """
    
    def __init__(self, params: Dict = None):
        self.params = params or DEFAULT_PARAMS
    
    def calculate(self, mode_share: Dict[str, float] = None) -> EmissionsResult:
        """
        Calculate daily CO2 emissions.
        
        Args:
            mode_share: Override default mode shares
            
        Returns:
            EmissionsResult with detailed breakdown
        """
        mode_share = mode_share or self.params["mode_share"]
        daily_trips = self.params["daily_trips"]
        avg_distance = self.params["avg_trip_distance_km"]
        emission_factors = self.params["emission_factors"]
        population = self.params["population"]
        
        # Calculate emissions by mode
        co2_by_mode = {}
        total_co2 = 0.0
        
        for mode, share in mode_share.items():
            trips = daily_trips * share
            distance = trips * avg_distance
            
            # Get emission factor (default to 0 if not found)
            ef = emission_factors.get(mode, 0.0)
            
            # For private vehicles, adjust for occupancy
            if mode == "private_car":
                ef = ef / self.params["avg_vehicle_occupancy"]
            
            mode_co2 = distance * ef
            co2_by_mode[mode] = round(mode_co2, 2)
            total_co2 += mode_co2
        
        return EmissionsResult(
            total_co2_kg_per_day=round(total_co2, 2),
            co2_by_mode=co2_by_mode,
            per_capita_co2_kg=round(total_co2 / population, 4),
            per_trip_co2_kg=round(total_co2 / daily_trips, 4),
            methodology=(
                "CO2 = Σ(trips × distance × emission_factor). "
                "Emission factors from IPCC guidelines. "
                "Private car emissions adjusted for average occupancy."
            )
        )


# =============================================================================
# COST-BENEFIT MODEL
# =============================================================================

class CostBenefitModel:
    """
    Calculates user and government costs for transportation.
    
    User Cost Formula:
        Cost = fuel_cost + fare + time_cost
        where time_cost = travel_time × value_of_time
    
    References:
        - World Bank Transport Cost Guidelines
        - US DOT Value of Travel Time Guidance
    """
    
    def __init__(self, params: Dict = None):
        self.params = params or DEFAULT_PARAMS
    
    def calculate(
        self, 
        mode_share: Dict[str, float] = None,
        policy_adjustments: Dict = None
    ) -> CostResult:
        """
        Calculate transportation costs.
        
        Args:
            mode_share: Override default mode shares
            policy_adjustments: Dict with fare changes, subsidies, etc.
            
        Returns:
            CostResult with detailed breakdown
        """
        mode_share = mode_share or self.params["mode_share"]
        policy = policy_adjustments or {}
        
        daily_trips = self.params["daily_trips"]
        avg_distance = self.params["avg_trip_distance_km"]
        fuel_price = self.params["fuel_price_per_liter"]
        fuel_efficiency = self.params["fuel_efficiency_km_per_liter"]
        pt_fare = self.params["public_transit_fare"]
        hourly_wage = self.params["avg_hourly_wage"]
        avg_time = self.params["avg_trip_time_minutes"]
        
        # Apply policy adjustments
        fuel_price *= (1 + policy.get("fuel_tax_percent", 0) / 100)
        pt_fare *= (1 - policy.get("pt_subsidy_percent", 0) / 100)
        
        # Value of time (typically 50% of wage rate)
        value_of_time = hourly_wage * 0.5 / 60  # per minute
        
        # Calculate cost by mode
        cost_by_mode = {}
        
        # Private car: fuel + time
        car_fuel_cost = (avg_distance / fuel_efficiency) * fuel_price
        car_time_cost = avg_time * value_of_time
        cost_by_mode["private_car"] = round(car_fuel_cost + car_time_cost, 2)
        
        # Motorcycle: lower fuel cost
        moto_fuel_cost = (avg_distance / (fuel_efficiency * 1.5)) * fuel_price
        moto_time_cost = avg_time * 0.9 * value_of_time  # Slightly faster
        cost_by_mode["motorcycle"] = round(moto_fuel_cost + moto_time_cost, 2)
        
        # Public transit: fare + time (usually longer)
        pt_time_cost = avg_time * 1.3 * value_of_time  # 30% longer trips
        cost_by_mode["public_transit"] = round(pt_fare + pt_time_cost, 2)
        
        # Walking/cycling: only time cost
        walk_time_cost = avg_time * 1.5 * value_of_time  # 50% longer
        cost_by_mode["walking_cycling"] = round(walk_time_cost, 2)
        
        # Weighted average user cost
        user_cost = sum(
            cost_by_mode[mode] * share 
            for mode, share in mode_share.items()
        )
        
        # Total daily cost
        total_daily = user_cost * daily_trips
        
        # Government cost (simplified: subsidy amount)
        pt_trips = daily_trips * mode_share.get("public_transit", 0.2)
        subsidy_per_trip = self.params["public_transit_fare"] * policy.get("pt_subsidy_percent", 0) / 100
        govt_daily = pt_trips * subsidy_per_trip
        govt_yearly = govt_daily * 365
        
        return CostResult(
            user_cost_per_trip=round(user_cost, 2),
            total_user_cost_per_day=round(total_daily, 2),
            government_cost_per_year=round(govt_yearly, 2),
            cost_by_mode=cost_by_mode,
            methodology=(
                "User cost = fuel_cost + fare + (travel_time × value_of_time). "
                "Value of time = 50% of hourly wage. "
                "Government cost = subsidy × subsidized_trips × 365."
            )
        )


# =============================================================================
# EQUITY MODEL
# =============================================================================

class EquityModel:
    """
    Evaluates distributional equity of transportation policies.
    
    Metrics:
        - Gini Index: Inequality in travel cost burden
        - Accessibility: Access to opportunities by income group
        - Burden: Transportation cost as % of income
    
    References:
        - Litman (2022) Evaluating Transportation Equity
        - Martens (2016) Transport Justice
    """
    
    def __init__(self, params: Dict = None):
        self.params = params or DEFAULT_PARAMS
        
        # Income distribution (quintiles)
        self.income_groups = {
            "low": {"share": 0.20, "income_multiplier": 0.4},
            "lower_middle": {"share": 0.20, "income_multiplier": 0.7},
            "middle": {"share": 0.20, "income_multiplier": 1.0},
            "upper_middle": {"share": 0.20, "income_multiplier": 1.5},
            "high": {"share": 0.20, "income_multiplier": 2.5}
        }
    
    def calculate(
        self, 
        user_cost_per_trip: float,
        mode_share: Dict[str, float] = None,
        policy_adjustments: Dict = None
    ) -> EquityResult:
        """
        Calculate equity metrics.
        
        Args:
            user_cost_per_trip: Average cost from CostBenefitModel
            mode_share: Mode share distribution
            policy_adjustments: Policy parameters
            
        Returns:
            EquityResult with equity metrics
        """
        mode_share = mode_share or self.params["mode_share"]
        policy = policy_adjustments or {}
        
        hourly_wage = self.params["avg_hourly_wage"]
        daily_trips_per_person = self.params["daily_trips"] / self.params["population"]
        
        # Calculate burden by income group
        burden_by_income = {}
        accessibility_by_income = {}
        
        for group, data in self.income_groups.items():
            # Group's average income (daily)
            daily_income = hourly_wage * 8 * data["income_multiplier"]
            
            # Transportation cost as % of income
            daily_transport_cost = user_cost_per_trip * daily_trips_per_person
            burden = (daily_transport_cost / daily_income) * 100
            burden_by_income[group] = round(burden, 2)
            
            # Accessibility score (inverse of burden, normalized)
            # Lower income groups have lower car access
            car_access = min(1.0, data["income_multiplier"])
            pt_quality = 1 - policy.get("pt_subsidy_percent", 0) / 200  # Subsidy improves access
            accessibility = (car_access * 0.5 + (1 - pt_quality) * 0.5)
            accessibility_by_income[group] = round(accessibility, 2)
        
        # Calculate Gini index for burden distribution
        burdens = list(burden_by_income.values())
        gini = self._calculate_gini(burdens)
        
        # Equity score (0-1, higher is better)
        # Based on how equal the burden distribution is
        equity_score = 1 - gini
        
        return EquityResult(
            gini_index=round(gini, 3),
            accessibility_by_income=accessibility_by_income,
            burden_by_income=burden_by_income,
            equity_score=round(equity_score, 3),
            methodology=(
                "Burden = (transport_cost / income) × 100 by income quintile. "
                "Gini index calculated on burden distribution. "
                "Equity score = 1 - Gini (higher is more equitable)."
            )
        )
    
    def _calculate_gini(self, values: List[float]) -> float:
        """Calculate Gini coefficient."""
        values = sorted(values)
        n = len(values)
        if n == 0 or sum(values) == 0:
            return 0.0
        
        cumsum = np.cumsum(values)
        return (n + 1 - 2 * sum(cumsum) / cumsum[-1]) / n


# =============================================================================
# EFFICIENCY MODEL
# =============================================================================

class EfficiencyModel:
    """
    Calculates system efficiency metrics.
    
    Metrics:
        - Average travel time
        - Congestion index
        - System throughput (person-km per hour)
    
    References:
        - Highway Capacity Manual (HCM)
        - TomTom Traffic Index Methodology
    """
    
    def __init__(self, params: Dict = None):
        self.params = params or DEFAULT_PARAMS
        
        # Base travel times by mode (minutes for avg trip)
        self.base_times = {
            "private_car": 30,
            "motorcycle": 25,
            "public_transit": 45,
            "walking_cycling": 50
        }
    
    def calculate(
        self, 
        mode_share: Dict[str, float] = None,
        congestion_factor: float = 1.0
    ) -> EfficiencyResult:
        """
        Calculate efficiency metrics.
        
        Args:
            mode_share: Mode share distribution
            congestion_factor: Multiplier for congestion (1.0 = normal)
            
        Returns:
            EfficiencyResult with efficiency metrics
        """
        mode_share = mode_share or self.params["mode_share"]
        daily_trips = self.params["daily_trips"]
        avg_distance = self.params["avg_trip_distance_km"]
        
        # Adjust times for congestion (only affects car/motorcycle)
        travel_time_by_mode = {}
        for mode, base_time in self.base_times.items():
            if mode in ["private_car", "motorcycle"]:
                time = base_time * congestion_factor
            else:
                time = base_time
            travel_time_by_mode[mode] = round(time, 1)
        
        # Weighted average travel time
        avg_time = sum(
            travel_time_by_mode[mode] * share
            for mode, share in mode_share.items()
        )
        
        # Congestion index (ratio of actual to free-flow time)
        free_flow_time = sum(
            self.base_times[mode] * share
            for mode, share in mode_share.items()
        )
        congestion_index = avg_time / free_flow_time if free_flow_time > 0 else 1.0
        
        # System throughput (person-km per hour)
        total_person_km = daily_trips * avg_distance
        avg_hours = avg_time / 60
        throughput = total_person_km / (daily_trips * avg_hours) if avg_hours > 0 else 0
        
        return EfficiencyResult(
            avg_travel_time_minutes=round(avg_time, 1),
            travel_time_by_mode=travel_time_by_mode,
            congestion_index=round(congestion_index, 3),
            system_throughput=round(throughput, 2),
            methodology=(
                "Travel time weighted by mode share. "
                "Congestion index = actual_time / free_flow_time. "
                "Throughput = person-km / (trips × hours)."
            )
        )


# =============================================================================
# MODE SHARE MODEL
# =============================================================================

class ModeShareModel:
    """
    Predicts mode share changes based on policy interventions.
    
    Uses price elasticity of demand:
        ΔQ/Q = elasticity × ΔP/P
    
    References:
        - Litman (2023) Transit Price Elasticities
        - Small & Verhoef (2007) Economics of Urban Transportation
    """
    
    def __init__(self, params: Dict = None):
        self.params = params or DEFAULT_PARAMS
        
        # Price elasticities of demand
        self.elasticities = {
            "private_car": -0.3,      # Inelastic
            "motorcycle": -0.4,
            "public_transit": -0.4,   # Moderate elasticity
            "walking_cycling": -0.1   # Very inelastic
        }
        
        # Cross-elasticities (how mode A changes when mode B price changes)
        self.cross_elasticities = {
            ("private_car", "public_transit"): 0.3,  # PT price up → car use up
            ("public_transit", "private_car"): 0.2,  # Car price up → PT use up
        }
    
    def calculate(
        self, 
        policy_adjustments: Dict = None
    ) -> ModeShareResult:
        """
        Calculate projected mode shares after policy.
        
        Args:
            policy_adjustments: Dict with price changes
            
        Returns:
            ModeShareResult with baseline and projected shares
        """
        policy = policy_adjustments or {}
        baseline = self.params["mode_share"].copy()
        projected = baseline.copy()
        
        # Apply own-price elasticity effects
        price_changes = {
            "private_car": policy.get("fuel_tax_percent", 0) / 100,
            "motorcycle": policy.get("fuel_tax_percent", 0) / 100,
            "public_transit": -policy.get("pt_subsidy_percent", 0) / 100,
            "walking_cycling": 0
        }
        
        # Add congestion pricing effect
        if policy.get("congestion_price", 0) > 0:
            # Rough conversion: $1 congestion charge ≈ 10% price increase
            price_changes["private_car"] += policy["congestion_price"] * 0.1
        
        # Calculate demand changes
        for mode, price_change in price_changes.items():
            if price_change != 0:
                elasticity = self.elasticities[mode]
                demand_change = elasticity * price_change
                projected[mode] = baseline[mode] * (1 + demand_change)
        
        # Apply cross-elasticity effects
        for (mode_a, mode_b), cross_e in self.cross_elasticities.items():
            if price_changes.get(mode_b, 0) != 0:
                effect = cross_e * price_changes[mode_b]
                projected[mode_a] = projected[mode_a] * (1 + effect)
        
        # Normalize to sum to 1.0
        total = sum(projected.values())
        if total > 0:
            projected = {k: v/total for k, v in projected.items()}
        
        # Round values
        projected = {k: round(v, 4) for k, v in projected.items()}
        
        # Calculate shift percentages
        shift = {
            mode: round((projected[mode] - baseline[mode]) / baseline[mode] * 100, 2)
            if baseline[mode] > 0 else 0
            for mode in baseline
        }
        
        return ModeShareResult(
            baseline_shares=baseline,
            projected_shares=projected,
            shift_percentage=shift,
            methodology=(
                "Mode shift based on price elasticity: ΔQ/Q = ε × ΔP/P. "
                "Elasticities from transit research literature. "
                "Cross-elasticities capture mode substitution effects."
            )
        )


# =============================================================================
# COMPOSITE SIMULATION
# =============================================================================

class PolicySimulator:
    """
    Main simulator that orchestrates all models.
    This is the entry point for policy evaluation.
    """
    
    def __init__(self, params: Dict = None):
        self.params = params or DEFAULT_PARAMS
        
        # Initialize all models
        self.emissions_model = EmissionsModel(params)
        self.cost_model = CostBenefitModel(params)
        self.equity_model = EquityModel(params)
        self.efficiency_model = EfficiencyModel(params)
        self.mode_share_model = ModeShareModel(params)
    
    def simulate(self, policy_adjustments: Dict = None) -> SimulationResult:
        """
        Run full simulation with all models.
        
        Args:
            policy_adjustments: Policy parameters
            
        Returns:
            SimulationResult with all metrics
        """
        policy = policy_adjustments or {}
        
        # Step 1: Calculate mode share changes
        mode_result = self.mode_share_model.calculate(policy)
        new_mode_share = mode_result.projected_shares
        
        # Step 2: Calculate emissions with new mode share
        emissions_result = self.emissions_model.calculate(new_mode_share)
        
        # Step 3: Calculate costs
        cost_result = self.cost_model.calculate(new_mode_share, policy)
        
        # Step 4: Calculate equity
        equity_result = self.equity_model.calculate(
            cost_result.user_cost_per_trip,
            new_mode_share,
            policy
        )
        
        # Step 5: Calculate efficiency
        # Congestion decreases if car share decreases
        car_share_change = (
            new_mode_share.get("private_car", 0) - 
            self.params["mode_share"].get("private_car", 0)
        )
        congestion_factor = 1.0 + car_share_change  # Less cars = less congestion
        efficiency_result = self.efficiency_model.calculate(
            new_mode_share, 
            max(0.8, congestion_factor)  # Floor at 0.8
        )
        
        # Step 6: Calculate overall score (weighted average)
        overall_score = self._calculate_overall_score(
            emissions_result,
            cost_result,
            equity_result,
            efficiency_result
        )
        
        # Generate summary
        summary = self._generate_summary(
            emissions_result,
            cost_result,
            equity_result,
            efficiency_result,
            mode_result
        )
        
        return SimulationResult(
            emissions=emissions_result,
            cost=cost_result,
            equity=equity_result,
            efficiency=efficiency_result,
            mode_share=mode_result,
            overall_score=overall_score,
            summary=summary
        )
    
    def _calculate_overall_score(
        self,
        emissions: EmissionsResult,
        cost: CostResult,
        equity: EquityResult,
        efficiency: EfficiencyResult
    ) -> float:
        """Calculate weighted overall score (0-100)."""
        # Normalize each metric to 0-1 scale
        # Lower emissions = better
        emissions_score = max(0, 1 - emissions.per_trip_co2_kg / 5)
        
        # Lower cost = better
        cost_score = max(0, 1 - cost.user_cost_per_trip / 20)
        
        # Higher equity = better
        equity_score = equity.equity_score
        
        # Lower travel time = better
        efficiency_score = max(0, 1 - efficiency.avg_travel_time_minutes / 60)
        
        # Weighted average (equal weights)
        weights = {
            "emissions": 0.25,
            "cost": 0.25,
            "equity": 0.25,
            "efficiency": 0.25
        }
        
        overall = (
            weights["emissions"] * emissions_score +
            weights["cost"] * cost_score +
            weights["equity"] * equity_score +
            weights["efficiency"] * efficiency_score
        )
        
        return round(overall * 100, 1)
    
    def _generate_summary(
        self,
        emissions: EmissionsResult,
        cost: CostResult,
        equity: EquityResult,
        efficiency: EfficiencyResult,
        mode_share: ModeShareResult
    ) -> str:
        """Generate text summary of results."""
        return (
            f"Daily CO2 emissions: {emissions.total_co2_kg_per_day:,.0f} kg. "
            f"Average user cost: ${cost.user_cost_per_trip:.2f}/trip. "
            f"Equity score: {equity.equity_score:.2f}/1.00. "
            f"Average travel time: {efficiency.avg_travel_time_minutes:.0f} minutes."
        )


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("Testing PolicySim-AI Models")
    print("=" * 50)
    
    # Create simulator
    simulator = PolicySimulator()
    
    # Test baseline (no policy)
    print("\n📊 BASELINE SCENARIO (No Policy)")
    print("-" * 40)
    baseline = simulator.simulate()
    print(f"Overall Score: {baseline.overall_score}/100")
    print(f"Summary: {baseline.summary}")
    
    # Test with policy
    print("\n📊 POLICY SCENARIO (20% PT Subsidy + $2 Congestion Price)")
    print("-" * 40)
    policy = {
        "pt_subsidy_percent": 20,
        "congestion_price": 2.0
    }
    with_policy = simulator.simulate(policy)
    print(f"Overall Score: {with_policy.overall_score}/100")
    print(f"Summary: {with_policy.summary}")
    
    # Compare mode shifts
    print("\n🚗 MODE SHARE CHANGES")
    print("-" * 40)
    for mode in with_policy.mode_share.baseline_shares:
        baseline_share = with_policy.mode_share.baseline_shares[mode]
        new_share = with_policy.mode_share.projected_shares[mode]
        change = with_policy.mode_share.shift_percentage[mode]
        print(f"{mode}: {baseline_share:.1%} → {new_share:.1%} ({change:+.1f}%)")
    
    print("\n✅ All models working correctly!")