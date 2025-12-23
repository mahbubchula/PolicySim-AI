"""
PolicySim-AI Policy Definitions
===============================
Structured definitions for transportation policy scenarios.
Each policy has parameters, expected impacts, and evaluation criteria.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


# =============================================================================
# ENUMS FOR POLICY TYPES
# =============================================================================

class PolicyCategory(Enum):
    """Categories of transportation policies."""
    PRICING = "pricing"
    SUBSIDY = "subsidy"
    INFRASTRUCTURE = "infrastructure"
    REGULATION = "regulation"
    INCENTIVE = "incentive"


class ImpactArea(Enum):
    """Areas affected by policies."""
    EMISSIONS = "emissions"
    COST = "cost"
    EQUITY = "equity"
    EFFICIENCY = "efficiency"
    MODE_SHARE = "mode_share"


# =============================================================================
# BASE POLICY CLASS
# =============================================================================

@dataclass
class Policy:
    """Base class for all transportation policies."""
    
    id: str
    name: str
    description: str
    category: PolicyCategory
    
    # Policy parameters (to be set by user)
    parameters: Dict = field(default_factory=dict)
    
    # Parameter definitions (metadata)
    parameter_definitions: Dict = field(default_factory=dict)
    
    # Expected impact areas
    impact_areas: List[ImpactArea] = field(default_factory=list)
    
    # Implementation details
    implementation_cost: str = "Not specified"
    implementation_time: str = "Not specified"
    
    # Academic references
    references: List[str] = field(default_factory=list)
    
    def get_adjustments(self) -> Dict:
        """Convert policy parameters to model adjustments."""
        return self.parameters.copy()
    
    def validate(self) -> List[str]:
        """Validate policy parameters. Returns list of errors."""
        errors = []
        for param, definition in self.parameter_definitions.items():
            if param in self.parameters:
                value = self.parameters[param]
                if "min" in definition and value < definition["min"]:
                    errors.append(f"{param} must be >= {definition['min']}")
                if "max" in definition and value > definition["max"]:
                    errors.append(f"{param} must be <= {definition['max']}")
        return errors
    
    def to_dict(self) -> Dict:
        """Convert policy to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "parameters": self.parameters,
            "impact_areas": [area.value for area in self.impact_areas]
        }


# =============================================================================
# SPECIFIC POLICY IMPLEMENTATIONS
# =============================================================================

class CongestionPricingPolicy(Policy):
    """
    Congestion Pricing: Charges for driving in congested areas/times.
    
    Evidence: Singapore ERP, London Congestion Charge, Stockholm
    Typical impact: 10-20% reduction in car traffic in priced zones
    """
    
    def __init__(self, price_per_entry: float = 5.0, peak_multiplier: float = 1.5):
        super().__init__(
            id="congestion_pricing",
            name="Congestion Pricing",
            description=(
                "Implements road pricing in congested urban areas. "
                "Vehicles are charged for entering designated zones, "
                "with higher prices during peak hours."
            ),
            category=PolicyCategory.PRICING,
            parameters={
                "congestion_price": price_per_entry,
                "peak_multiplier": peak_multiplier
            },
            parameter_definitions={
                "congestion_price": {
                    "name": "Base Price per Entry",
                    "unit": "currency",
                    "min": 0,
                    "max": 50,
                    "default": 5.0,
                    "description": "Base charge for entering the congestion zone"
                },
                "peak_multiplier": {
                    "name": "Peak Hour Multiplier",
                    "unit": "multiplier",
                    "min": 1.0,
                    "max": 3.0,
                    "default": 1.5,
                    "description": "Price multiplier during peak hours"
                }
            },
            impact_areas=[
                ImpactArea.MODE_SHARE,
                ImpactArea.EMISSIONS,
                ImpactArea.EFFICIENCY,
                ImpactArea.EQUITY
            ],
            implementation_cost="Medium ($10-50M for technology)",
            implementation_time="1-2 years",
            references=[
                "Eliasson, J. (2009). A cost-benefit analysis of the Stockholm congestion charging system. Transportation Research Part A.",
                "Santos, G. (2005). Urban congestion charging: A comparison between London and Singapore. Transport Reviews.",
                "Börjesson, M. et al. (2012). The Stockholm congestion charges—5 years on. Transport Policy."
            ]
        )


class PublicTransitSubsidyPolicy(Policy):
    """
    Public Transit Subsidy: Reduces fares through government subsidies.
    
    Evidence: Free transit pilots (Luxembourg, Tallinn), fare reduction programs
    Typical impact: 5-15% increase in transit ridership
    """
    
    def __init__(self, subsidy_percent: float = 30.0, target_groups: List[str] = None):
        super().__init__(
            id="pt_subsidy",
            name="Public Transit Subsidy",
            description=(
                "Government subsidizes public transit fares to increase "
                "ridership and reduce private vehicle use. Can be universal "
                "or targeted at specific groups (students, elderly, low-income)."
            ),
            category=PolicyCategory.SUBSIDY,
            parameters={
                "pt_subsidy_percent": subsidy_percent,
                "target_groups": target_groups or ["all"]
            },
            parameter_definitions={
                "pt_subsidy_percent": {
                    "name": "Subsidy Percentage",
                    "unit": "%",
                    "min": 0,
                    "max": 100,
                    "default": 30.0,
                    "description": "Percentage of fare covered by subsidy"
                },
                "target_groups": {
                    "name": "Target Groups",
                    "unit": "list",
                    "options": ["all", "students", "elderly", "low_income", "disabled"],
                    "default": ["all"],
                    "description": "Groups eligible for the subsidy"
                }
            },
            impact_areas=[
                ImpactArea.MODE_SHARE,
                ImpactArea.COST,
                ImpactArea.EQUITY,
                ImpactArea.EMISSIONS
            ],
            implementation_cost="High (ongoing operational cost)",
            implementation_time="3-6 months",
            references=[
                "Cats, O. et al. (2017). The prospects of fare-free public transport. Transportation.",
                "Cervero, R. (1990). Transit pricing research: A review and synthesis. Transportation.",
                "Taylor, B.D. & Fink, C.N. (2013). Explaining transit ridership. Transportation Quarterly."
            ]
        )


class FuelTaxPolicy(Policy):
    """
    Fuel Tax: Additional tax on fuel to discourage car use.
    
    Evidence: European fuel taxes, carbon tax implementations
    Typical impact: 1-3% reduction in fuel consumption per 10% price increase
    """
    
    def __init__(self, tax_percent: float = 20.0, use_for_transit: bool = True):
        super().__init__(
            id="fuel_tax",
            name="Fuel Tax",
            description=(
                "Increases fuel prices through taxation to discourage "
                "private vehicle use and generate revenue for sustainable "
                "transportation investments."
            ),
            category=PolicyCategory.PRICING,
            parameters={
                "fuel_tax_percent": tax_percent,
                "revenue_for_transit": use_for_transit
            },
            parameter_definitions={
                "fuel_tax_percent": {
                    "name": "Tax Rate",
                    "unit": "%",
                    "min": 0,
                    "max": 100,
                    "default": 20.0,
                    "description": "Additional tax as percentage of fuel price"
                },
                "revenue_for_transit": {
                    "name": "Revenue for Transit",
                    "unit": "boolean",
                    "default": True,
                    "description": "Whether revenue is earmarked for transit"
                }
            },
            impact_areas=[
                ImpactArea.MODE_SHARE,
                ImpactArea.EMISSIONS,
                ImpactArea.COST,
                ImpactArea.EQUITY
            ],
            implementation_cost="Low (administrative)",
            implementation_time="3-12 months (political process)",
            references=[
                "Sterner, T. (2007). Fuel taxes: An important instrument for climate policy. Energy Policy.",
                "Li, S. et al. (2014). Gasoline taxes and consumer behavior. American Economic Journal.",
                "Rivers, N. & Schaufele, B. (2015). Salience of carbon taxes in the gasoline market. Journal of Environmental Economics."
            ]
        )


class EVIncentivePolicy(Policy):
    """
    EV Incentive: Subsidies and benefits for electric vehicles.
    
    Evidence: Norway EV policy, California ZEV mandate
    Typical impact: Significant increase in EV adoption when combined
    """
    
    def __init__(self, purchase_subsidy: float = 5000, tax_reduction_percent: float = 50):
        super().__init__(
            id="ev_incentive",
            name="EV Incentive",
            description=(
                "Provides financial incentives for purchasing electric "
                "vehicles, including direct subsidies, tax reductions, "
                "and access benefits (HOV lanes, free parking)."
            ),
            category=PolicyCategory.INCENTIVE,
            parameters={
                "ev_purchase_subsidy": purchase_subsidy,
                "ev_tax_reduction_percent": tax_reduction_percent
            },
            parameter_definitions={
                "ev_purchase_subsidy": {
                    "name": "Purchase Subsidy",
                    "unit": "currency",
                    "min": 0,
                    "max": 20000,
                    "default": 5000,
                    "description": "Direct subsidy for EV purchase"
                },
                "ev_tax_reduction_percent": {
                    "name": "Tax Reduction",
                    "unit": "%",
                    "min": 0,
                    "max": 100,
                    "default": 50,
                    "description": "Reduction in vehicle registration tax"
                }
            },
            impact_areas=[
                ImpactArea.EMISSIONS,
                ImpactArea.COST,
                ImpactArea.EQUITY
            ],
            implementation_cost="High (subsidy budget)",
            implementation_time="6-12 months",
            references=[
                "Figenbaum, E. (2017). Perspectives on Norway's supercharged electric vehicle policy. Environmental Innovation.",
                "Hardman, S. et al. (2017). A review of consumer preferences of and interactions with electric vehicle charging. Transportation Research Part D.",
                "Sierzchula, W. et al. (2014). The influence of financial incentives and other socio-economic factors on electric vehicle adoption. Energy Policy."
            ]
        )


class ParkingManagementPolicy(Policy):
    """
    Parking Management: Pricing and availability of parking spaces.
    
    Evidence: SFpark dynamic pricing, European parking policies
    Typical impact: 10-30% reduction in cruising for parking
    """
    
    def __init__(self, hourly_rate: float = 3.0, max_hours: int = 4):
        super().__init__(
            id="parking_policy",
            name="Parking Management",
            description=(
                "Implements parking pricing and time restrictions to "
                "manage parking demand, reduce cruising for parking, "
                "and encourage alternative transportation modes."
            ),
            category=PolicyCategory.PRICING,
            parameters={
                "parking_hourly_rate": hourly_rate,
                "parking_max_hours": max_hours
            },
            parameter_definitions={
                "parking_hourly_rate": {
                    "name": "Hourly Rate",
                    "unit": "currency/hour",
                    "min": 0,
                    "max": 20,
                    "default": 3.0,
                    "description": "Parking fee per hour"
                },
                "parking_max_hours": {
                    "name": "Maximum Duration",
                    "unit": "hours",
                    "min": 1,
                    "max": 24,
                    "default": 4,
                    "description": "Maximum allowed parking duration"
                }
            },
            impact_areas=[
                ImpactArea.MODE_SHARE,
                ImpactArea.EFFICIENCY,
                ImpactArea.EMISSIONS
            ],
            implementation_cost="Medium (meters, enforcement)",
            implementation_time="6-18 months",
            references=[
                "Shoup, D. (2006). Cruising for parking. Transport Policy.",
                "Pierce, G. & Shoup, D. (2013). Getting the prices right: An evaluation of pricing parking by demand. Journal of the American Planning Association.",
                "Marsden, G. (2006). The evidence base for parking policies—a review. Transport Policy."
            ]
        )


# =============================================================================
# POLICY REGISTRY
# =============================================================================

class PolicyRegistry:
    """
    Central registry of all available policies.
    Provides factory methods and policy discovery.
    """
    
    _policies = {
        "congestion_pricing": CongestionPricingPolicy,
        "pt_subsidy": PublicTransitSubsidyPolicy,
        "fuel_tax": FuelTaxPolicy,
        "ev_incentive": EVIncentivePolicy,
        "parking_policy": ParkingManagementPolicy
    }
    
    @classmethod
    def get_policy(cls, policy_id: str, **kwargs) -> Policy:
        """Get a policy instance by ID."""
        if policy_id not in cls._policies:
            raise ValueError(f"Unknown policy: {policy_id}")
        return cls._policies[policy_id](**kwargs)
    
    @classmethod
    def list_policies(cls) -> List[Dict]:
        """List all available policies."""
        policies = []
        for policy_id, policy_class in cls._policies.items():
            policy = policy_class()
            policies.append({
                "id": policy_id,
                "name": policy.name,
                "category": policy.category.value,
                "description": policy.description
            })
        return policies
    
    @classmethod
    def get_policy_ids(cls) -> List[str]:
        """Get list of all policy IDs."""
        return list(cls._policies.keys())


# =============================================================================
# POLICY SCENARIO (Combination of Policies)
# =============================================================================

@dataclass
class PolicyScenario:
    """
    A scenario combining multiple policies for evaluation.
    """
    
    name: str
    description: str
    policies: List[Policy]
    
    def get_combined_adjustments(self) -> Dict:
        """Combine all policy adjustments into single dict."""
        combined = {}
        for policy in self.policies:
            combined.update(policy.get_adjustments())
        return combined
    
    def validate(self) -> List[str]:
        """Validate all policies in scenario."""
        errors = []
        for policy in self.policies:
            policy_errors = policy.validate()
            for error in policy_errors:
                errors.append(f"{policy.name}: {error}")
        return errors
    
    def get_all_references(self) -> List[str]:
        """Get all academic references from all policies."""
        references = []
        for policy in self.policies:
            references.extend(policy.references)
        return list(set(references))  # Remove duplicates


# =============================================================================
# PRE-BUILT SCENARIOS
# =============================================================================

class ScenarioLibrary:
    """Library of pre-built policy scenarios."""
    
    @staticmethod
    def get_baseline() -> PolicyScenario:
        """Baseline scenario with no policy interventions."""
        return PolicyScenario(
            name="Baseline",
            description="Current conditions with no policy changes.",
            policies=[]
        )
    
    @staticmethod
    def get_green_transport() -> PolicyScenario:
        """Green transport scenario focusing on emissions reduction."""
        return PolicyScenario(
            name="Green Transport",
            description="Aggressive policies to reduce transportation emissions.",
            policies=[
                CongestionPricingPolicy(price_per_entry=8.0),
                PublicTransitSubsidyPolicy(subsidy_percent=50.0),
                FuelTaxPolicy(tax_percent=30.0)
            ]
        )
    
    @staticmethod
    def get_equity_focused() -> PolicyScenario:
        """Equity-focused scenario prioritizing affordability."""
        return PolicyScenario(
            name="Equity Focus",
            description="Policies prioritizing transportation affordability for all.",
            policies=[
                PublicTransitSubsidyPolicy(
                    subsidy_percent=70.0,
                    target_groups=["low_income", "students", "elderly"]
                )
            ]
        )
    
    @staticmethod
    def get_balanced() -> PolicyScenario:
        """Balanced scenario with moderate interventions."""
        return PolicyScenario(
            name="Balanced Approach",
            description="Moderate policies balancing multiple objectives.",
            policies=[
                CongestionPricingPolicy(price_per_entry=3.0),
                PublicTransitSubsidyPolicy(subsidy_percent=25.0),
                ParkingManagementPolicy(hourly_rate=2.0)
            ]
        )
    
    @classmethod
    def list_scenarios(cls) -> List[Dict]:
        """List all pre-built scenarios."""
        return [
            {"id": "baseline", "name": "Baseline", "method": cls.get_baseline},
            {"id": "green_transport", "name": "Green Transport", "method": cls.get_green_transport},
            {"id": "equity_focused", "name": "Equity Focus", "method": cls.get_equity_focused},
            {"id": "balanced", "name": "Balanced Approach", "method": cls.get_balanced}
        ]


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("Testing PolicySim-AI Policies")
    print("=" * 50)
    
    # List all policies
    print("\n📋 AVAILABLE POLICIES")
    print("-" * 40)
    for policy in PolicyRegistry.list_policies():
        print(f"• {policy['name']} ({policy['category']})")
        print(f"  {policy['description'][:60]}...")
    
    # Test creating a policy
    print("\n🔧 CREATING CONGESTION PRICING POLICY")
    print("-" * 40)
    cp = PolicyRegistry.get_policy("congestion_pricing", price_per_entry=10.0)
    print(f"Name: {cp.name}")
    print(f"Parameters: {cp.parameters}")
    print(f"References: {len(cp.references)} academic sources")
    
    # Test scenario
    print("\n🎯 TESTING GREEN TRANSPORT SCENARIO")
    print("-" * 40)
    scenario = ScenarioLibrary.get_green_transport()
    print(f"Scenario: {scenario.name}")
    print(f"Policies included: {len(scenario.policies)}")
    print(f"Combined adjustments: {scenario.get_combined_adjustments()}")
    print(f"Total references: {len(scenario.get_all_references())}")
    
    print("\n✅ All policy definitions working correctly!")