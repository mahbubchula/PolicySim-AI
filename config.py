"""
PolicySim-AI Configuration
==========================
Central configuration file for all settings and parameters.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# =============================================================================
# API CONFIGURATION
# =============================================================================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# LLM Model Settings
LLM_MODELS = {
    "main": "llama-3.3-70b-versatile",      # For detailed analysis
    "fast": "llama-3.1-8b-instant"           # For quick tasks
}

# =============================================================================
# APPLICATION SETTINGS
# =============================================================================
APP_CONFIG = {
    "title": "PolicySim-AI",
    "subtitle": "Transportation Policy Simulation & Analysis Tool",
    "version": "1.0.0",
    "author": "MAHBUB"
}

# =============================================================================
# DEFAULT SIMULATION PARAMETERS
# =============================================================================
DEFAULT_PARAMS = {
    # Population and travel demand
    "population": 1_000_000,
    "daily_trips": 2_500_000,
    
    # Mode shares (must sum to 1.0)
    "mode_share": {
        "private_car": 0.45,
        "motorcycle": 0.25,
        "public_transit": 0.20,
        "walking_cycling": 0.10
    },
    
    # Average trip characteristics
    "avg_trip_distance_km": 12.0,
    "avg_trip_time_minutes": 35.0,
    
    # Vehicle characteristics
    "avg_vehicle_occupancy": 1.3,
    "fuel_efficiency_km_per_liter": 12.0,
    
    # Cost parameters (USD)
    "fuel_price_per_liter": 1.20,
    "public_transit_fare": 1.50,
    "avg_hourly_wage": 8.00,
    
    # Emission factors (kg CO2 per km)
    "emission_factors": {
        "private_car": 0.21,
        "motorcycle": 0.10,
        "public_transit": 0.05,  # Per passenger
        "walking_cycling": 0.00
    }
}

# =============================================================================
# REGIONAL CONTEXTS (Templates)
# =============================================================================
REGIONAL_CONTEXTS = {
    "default": {
        "name": "Default Context",
        "currency": "USD",
        "currency_symbol": "$",
        "description": "Generic urban area parameters"
    },
    "malaysia": {
        "name": "Malaysia (Klang Valley)",
        "currency": "MYR",
        "currency_symbol": "RM",
        "fuel_price_per_liter": 2.05,  # MYR
        "public_transit_fare": 3.00,   # MYR
        "avg_hourly_wage": 15.00,      # MYR
        "description": "Parameters based on Klang Valley, Malaysia"
    },
    "thailand": {
        "name": "Thailand (Bangkok)",
        "currency": "THB",
        "currency_symbol": "฿",
        "fuel_price_per_liter": 40.0,  # THB
        "public_transit_fare": 25.0,   # THB
        "avg_hourly_wage": 100.0,      # THB
        "description": "Parameters based on Bangkok Metropolitan Region"
    },
    "custom": {
        "name": "Custom Context",
        "currency": "USD",
        "currency_symbol": "$",
        "description": "User-defined parameters"
    }
}

# =============================================================================
# POLICY TYPES
# =============================================================================
POLICY_TYPES = {
    "congestion_pricing": {
        "name": "Congestion Pricing",
        "description": "Charges for driving in congested areas/times",
        "parameters": ["price_per_km", "peak_hours", "zone_coverage"]
    },
    "pt_subsidy": {
        "name": "Public Transit Subsidy",
        "description": "Reduces public transit fares through subsidies",
        "parameters": ["subsidy_percent", "target_modes", "budget_limit"]
    },
    "fuel_tax": {
        "name": "Fuel Tax",
        "description": "Additional tax on fuel to discourage car use",
        "parameters": ["tax_per_liter", "exemptions"]
    },
    "ev_incentive": {
        "name": "EV Incentive",
        "description": "Subsidies and benefits for electric vehicles",
        "parameters": ["purchase_subsidy", "tax_reduction", "charging_infrastructure"]
    },
    "parking_policy": {
        "name": "Parking Management",
        "description": "Pricing and availability of parking spaces",
        "parameters": ["hourly_rate", "max_duration", "restricted_zones"]
    }
}

# =============================================================================
# EVALUATION METRICS
# =============================================================================
EVALUATION_METRICS = {
    "emissions": {
        "name": "Environmental Impact",
        "unit": "kg CO2/day",
        "description": "Total CO2 emissions from transportation"
    },
    "cost_user": {
        "name": "User Cost",
        "unit": "currency/trip",
        "description": "Average cost per trip for users"
    },
    "cost_government": {
        "name": "Government Cost",
        "unit": "currency/year",
        "description": "Annual cost to government for implementation"
    },
    "equity": {
        "name": "Equity Index",
        "unit": "0-1 scale",
        "description": "Distribution of benefits across income groups"
    },
    "efficiency": {
        "name": "System Efficiency",
        "unit": "minutes/trip",
        "description": "Average travel time including all modes"
    },
    "mode_shift": {
        "name": "Mode Shift",
        "unit": "percentage",
        "description": "Change in mode share distribution"
    }
}

# =============================================================================
# HELPER FUNCTION
# =============================================================================
def get_context_params(context_name: str) -> dict:
    """
    Get parameters for a specific regional context.
    Merges regional overrides with default parameters.
    """
    params = DEFAULT_PARAMS.copy()
    
    if context_name in REGIONAL_CONTEXTS:
        context = REGIONAL_CONTEXTS[context_name]
        # Override defaults with regional values
        for key, value in context.items():
            if key in params:
                params[key] = value
        params["context_info"] = context
    
    return params


# =============================================================================
# VALIDATION
# =============================================================================
def validate_config():
    """Check if configuration is valid."""
    errors = []
    
    if not GROQ_API_KEY:
        errors.append("GROQ_API_KEY not found in .env file")
    
    mode_share_sum = sum(DEFAULT_PARAMS["mode_share"].values())
    if abs(mode_share_sum - 1.0) > 0.01:
        errors.append(f"Mode shares must sum to 1.0, got {mode_share_sum}")
    
    return errors


# Run validation when module is imported
if __name__ == "__main__":
    errors = validate_config()
    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("Configuration is valid!")
        print(f"App: {APP_CONFIG['title']} v{APP_CONFIG['version']}")
        print(f"API Key: {'✓ Found' if GROQ_API_KEY else '✗ Missing'}")