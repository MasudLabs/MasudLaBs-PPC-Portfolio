#!/usr/bin/env python3
"""
MasudLaBs PPC Portfolio - Tool 3
ACoS / ROAS Calculator + Optimizer

Purpose:
- Calculate current ACoS and ROAS accurately
- Determine break-even ACoS based on profit margins
- Provide target ACoS recommendations
- Suggest bid adjustments based on performance
- Scenario modeling ("What if" analysis)

Very useful for daily/weekly optimization decisions.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional


def calculate_acos_roas(spend: float, sales: float) -> Dict[str, float]:
    """Calculate ACoS and ROAS from spend and sales."""
    if sales <= 0:
        return {"acos": 100.0, "roas": 0.0}
    
    acos = (spend / sales) * 100
    roas = sales / spend if spend > 0 else 0
    
    return {
        "acos": round(acos, 2),
        "roas": round(roas, 2)
    }


def calculate_break_even_acos(
    product_price: float,
    product_cost: float,
    target_profit_margin: float = 0.15
) -> float:
    """
    Calculate the maximum ACoS you can afford to hit your target profit margin.
    
    Args:
        product_price: Selling price
        product_cost: Your cost (COGS + fees + shipping)
        target_profit_margin: Desired profit margin (e.g. 0.15 = 15%)
    """
    if product_price <= 0:
        return 0.0
    
    profit_per_sale = product_price * target_profit_margin
    max_acos = ((product_price - product_cost - profit_per_sale) / product_price) * 100
    return max(round(max_acos, 2), 0)


def get_bid_recommendation(
    current_acos: float,
    target_acos: float,
    current_bid: float,
    performance_trend: str = "stable"
) -> Dict:
    """
    Suggest bid changes based on ACoS vs target.
    """
    if current_acos <= target_acos * 0.8:
        action = "Increase bid"
        suggested_bid = round(current_bid * 1.15, 2)
        reason = "Strong performance - scale up"
    elif current_acos <= target_acos:
        action = "Maintain or slight increase"
        suggested_bid = round(current_bid * 1.05, 2)
        reason = "Within target range"
    elif current_acos <= target_acos * 1.3:
        action = "Slight decrease"
        suggested_bid = round(current_bid * 0.90, 2)
        reason = "Slightly over target"
    else:
        action = "Significant decrease or pause"
        suggested_bid = round(current_bid * 0.70, 2)
        reason = "Poor efficiency - protect budget"
    
    return {
        "action": action,
        "current_bid": current_bid,
        "suggested_bid": suggested_bid,
        "reason": reason
    }


def run_acos_analysis(
    spend: float,
    sales: float,
    product_price: float = 29.99,
    product_cost: float = 12.50,
    target_margin: float = 0.20,
    current_bid: float = 0.75
) -> Dict:
    """Full ACoS/ROAS analysis with recommendations."""
    
    metrics = calculate_acos_roas(spend, sales)
    break_even = calculate_break_even_acos(product_price, product_cost, target_margin)
    
    # Use break-even as target if not specified
    target_acos = break_even
    
    bid_rec = get_bid_recommendation(
        current_acos=metrics["acos"],
        target_acos=target_acos,
        current_bid=current_bid
    )
    
    return {
        "current_acos": metrics["acos"],
        "current_roas": metrics["roas"],
        "break_even_acos": break_even,
        "target_acos": round(target_acos, 2),
        "bid_recommendation": bid_rec,
        "is_profitable": metrics["acos"] <= break_even
    }


def scenario_modeling(
    current_spend: float,
    current_sales: float,
    bid_change_percent: float = 0.20
) -> Dict:
    """Simulate what happens if you change bids."""
    current = calculate_acos_roas(current_spend, current_sales)
    
    # Simple model: assume +20% bid = +15% spend & +12% sales (example elasticity)
    new_spend = current_spend * (1 + bid_change_percent)
    new_sales = current_sales * (1 + bid_change_percent * 0.6)   # Assume lower elasticity on sales
    
    new_metrics = calculate_acos_roas(new_spend, new_sales)
    
    return {
        "current": current,
        "new": new_metrics,
        "spend_change": f"+{bid_change_percent*100:.0f}%",
        "projected_impact": "Improved volume but check efficiency"
    }


if __name__ == "__main__":
    print("MasudLaBs - ACoS / ROAS Calculator & Optimizer")
    print("=" * 55)
    
    # Example usage
    result = run_acos_analysis(
        spend=185.50,
        sales=1250.00,
        product_price=29.99,
        product_cost=12.50,
        target_margin=0.18,
        current_bid=0.68
    )
    
    print(f"\nCurrent ACoS: {result['current_acos']}%")
    print(f"Current ROAS: {result['current_roas']}x")
    print(f"Break-even ACoS: {result['break_even_acos']}%")
    print(f"Target ACoS: {result['target_acos']}%")
    print(f"Profitable? {'Yes' if result['is_profitable'] else 'No'}")
    print(f"\nBid Recommendation: {result['bid_recommendation']['action']}")
    print(f"Suggested Bid: ${result['bid_recommendation']['suggested_bid']}")
    print(f"Reason: {result['bid_recommendation']['reason']}")
