#!/usr/bin/env python3
"""
MasudLaBs PPC Portfolio - Tool 4
Bid Strategy Simulator

Purpose:
- Simulate impact of different bidding strategies
- Compare Dynamic Bids vs Fixed Bids vs Rule-based
- Project changes in ACoS, ROAS, volume, and spend
- Help make data-driven bidding decisions

Useful for testing strategies before applying them in campaigns.
"""

import pandas as pd
import numpy as np
from typing import Dict


def simulate_dynamic_bids(
    current_spend: float,
    current_sales: float,
    current_acos: float,
    bid_increase: float = 0.15,
    elasticity: float = 0.65
) -> Dict:
    """
    Simulate Dynamic Bidding (up & down).
    Assumes higher bids = more impressions/clicks but higher CPC.
    """
    new_spend = current_spend * (1 + bid_increase)
    new_sales = current_sales * (1 + bid_increase * elasticity)
    
    new_acos = (new_spend / new_sales * 100) if new_sales > 0 else 100
    new_roas = new_sales / new_spend if new_spend > 0 else 0
    
    return {
        "strategy": "Dynamic Bids (Aggressive)",
        "spend_change": f"+{bid_increase*100:.0f}%",
        "sales_change": f"+{bid_increase * elasticity * 100:.0f}%",
        "new_acos": round(new_acos, 2),
        "new_roas": round(new_roas, 2),
        "recommendation": "Good for scaling winners with room in ACoS target"
    }

def simulate_fixed_bids(
    current_spend: float,
    current_sales: float,
    target_acos: float = 25.0
) -> Dict:
    """Simulate conservative Fixed Bidding."""
    # Fixed bids usually result in more stable but lower volume
    new_spend = current_spend * 0.85
    new_sales = current_sales * 0.80
    
    new_acos = (new_spend / new_sales * 100) if new_sales > 0 else 100
    new_roas = new_sales / new_spend if new_spend > 0 else 0
    
    return {
        "strategy": "Fixed Bids (Conservative)",
        "spend_change": "-15%",
        "sales_change": "-20%",
        "new_acos": round(new_acos, 2),
        "new_roas": round(new_roas, 2),
        "recommendation": "Best for protecting ACoS on new or volatile campaigns"
    }

def simulate_rule_based_bidding(
    current_acos: float,
    target_acos: float = 22.0
) -> Dict:
    """Rule-based bidding simulation (increase on good terms, decrease on bad)."""
    if current_acos < target_acos * 0.7:
        action = "Increase bids 20-30% on top performers"
        expected_acos_impact = "+3-5% ACoS but +25% sales"
    elif current_acos > target_acos * 1.4:
        action = "Decrease bids 25-40% or add negatives"
        expected_acos_impact = "-8-12% ACoS, protect budget"
    else:
        action = "Fine-tune: +10% on best terms, -15% on poor terms"
        expected_acos_impact = "Stable ACoS with better efficiency"
    
    return {
        "strategy": "Rule-Based / Portfolio Bidding",
        "action": action,
        "expected_impact": expected_acos_impact,
        "recommendation": "Most effective long-term strategy when combined with search term analysis"
    }

def compare_strategies(
    current_spend: float,
    current_sales: float,
    current_acos: float,
    target_acos: float = 22.0
) -> pd.DataFrame:
    """Compare multiple bidding strategies side by side."""
    
    dynamic = simulate_dynamic_bids(current_spend, current_sales, current_acos)
    fixed = simulate_fixed_bids(current_spend, current_sales, target_acos)
    rule_based = simulate_rule_based_bidding(current_acos, target_acos)
    
    comparison = pd.DataFrame([
        {
            "Strategy": dynamic["strategy"],
            "Projected ACoS": dynamic["new_acos"],
            "Projected ROAS": dynamic["new_roas"],
            "Volume Impact": dynamic["sales_change"],
            "Best For": "Scaling proven winners"
        },
        {
            "Strategy": fixed["strategy"],
            "Projected ACoS": fixed["new_acos"],
            "Projected ROAS": fixed["new_roas"],
            "Volume Impact": fixed["sales_change"],
            "Best For": "New campaigns / ACoS protection"
        },
        {
            "Strategy": rule_based["strategy"],
            "Projected ACoS": "Variable",
            "Projected ROAS": "Variable",
            "Volume Impact": "Optimized efficiency",
            "Best For": rule_based["recommendation"]
        }
    ])
    
    return comparison


if __name__ == "__main__":
    print("MasudLaBs - Bid Strategy Simulator")
    print("=" * 50)
    
    current_spend = 185.50
    current_sales = 1250.00
    current_acos = (current_spend / current_sales) * 100
    
    print(f"Current Situation: Spend=${current_spend}, Sales=${current_sales}, ACoS={current_acos:.1f}%\n")
    
    comparison = compare_strategies(current_spend, current_sales, current_acos, target_acos=22.0)
    print(comparison.to_string(index=False))
    
    print("\n=== Rule-Based Recommendation ===")
    rule = simulate_rule_based_bidding(current_acos, target_acos=22.0)
    print(f"Action: {rule['action']}")
    print(f"Expected Impact: {rule['expected_impact']}")
