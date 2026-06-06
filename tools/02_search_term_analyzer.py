#!/usr/bin/env python3
"""
MasudLaBs PPC Portfolio - Tool 2
Search Term Report Analyzer

Purpose:
- Analyze Amazon Search Term Reports
- Identify high-performing terms vs wasted spend
- Generate prioritized negative keyword recommendations
- Provide actionable insights with scoring

This is a practical starter version for portfolio demonstration.
In real use, feed it your exported Search Term Report CSV.
"""

import pandas as pd
import numpy as np
from typing import Dict, List


def analyze_search_terms(df: pd.DataFrame) -> Dict:
    """
    Main analysis function for Amazon Search Term Reports.
    
    Expected columns (Amazon default):
    - Search Term
    - Impressions
    - Clicks
    - Spend
    - Sales
    - Orders
    - CTR
    - CPC
    - CVR
    """
    
    # Standardize column names (handle slight variations)
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    
    # Calculate key metrics if not present
    if "cvr" not in df.columns and "orders" in df.columns and "clicks" in df.columns:
        df["cvr"] = np.where(df["clicks"] > 0, (df["orders"] / df["clicks"]) * 100, 0)
    
    if "acos" not in df.columns and "spend" in df.columns and "sales" in df.columns:
        df["acos"] = np.where(df["sales"] > 0, (df["spend"] / df["sales"]) * 100, 100)
    
    # Create performance score (higher = better)
    df["performance_score"] = (
        (df.get("cvr", 0) * 0.5) + 
        (np.where(df.get("acos", 100) < 30, 30, 0)) - 
        (df.get("acos", 100) * 0.3)
    ).clip(0, 100)
    
    # Categorize terms
    def categorize(row):
        if row.get("acos", 100) <= 15 and row.get("cvr", 0) >= 15:
            return "High Performer"
        elif row.get("acos", 100) <= 25 and row.get("clicks", 0) >= 10:
            return "Good Performer"
        elif row.get("spend", 0) > 5 and row.get("orders", 0) == 0:
            return "Wasted Spend - Strong Negative"
        elif row.get("acos", 100) > 50 and row.get("clicks", 0) >= 5:
            return "Poor Performer - Review"
        else:
            return "Monitor / Low Data"
    
    df["category"] = df.apply(categorize, axis=1)
    
    # Negative keyword recommendations
    negative_candidates = df[
        (df["category"] == "Wasted Spend - Strong Negative") |
        ((df["acos"] > 40) & (df["clicks"] >= 5))
    ].sort_values("spend", ascending=False)
    
    return {
        "full_analysis": df,
        "high_performers": df[df["category"] == "High Performer"].sort_values("performance_score", ascending=False),
        "wasted_spend": df[df["category"] == "Wasted Spend - Strong Negative"].sort_values("spend", ascending=False),
        "negative_recommendations": negative_candidates[["search_term", "spend", "clicks", "orders", "acos"]].head(30),
        "summary": {
            "total_terms": len(df),
            "high_performers_count": len(df[df["category"] == "High Performer"]),
            "wasted_spend_terms": len(df[df["category"] == "Wasted Spend - Strong Negative"]),
            "total_spend_analyzed": df["spend"].sum() if "spend" in df.columns else 0
        }
    }


def generate_negative_keyword_list(negative_df: pd.DataFrame, min_spend: float = 3.0) -> List[str]:
    """Generate clean list of negative keywords from wasted spend terms."""
    if negative_df.empty:
        return []
    
    negatives = []
    for _, row in negative_df.iterrows():
        term = str(row.get("search_term", "")).strip().lower()
        if term and row.get("spend", 0) >= min_spend:
            negatives.append(term)
    return list(set(negatives))   # Remove duplicates


def run_search_term_analysis(
    input_file: str,
    output_prefix: str = "search_term_analysis"
) -> Dict:
    """Main function to run full analysis from a CSV file."""
    print(f"Loading Search Term Report: {input_file}")
    
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error loading file: {e}")
        return {}
    
    print("Analyzing search terms...")
    results = analyze_search_terms(df)
    
    # Export results
    results["full_analysis"].to_csv(f"{output_prefix}_full.csv", index=False)
    results["high_performers"].to_csv(f"{output_prefix}_high_performers.csv", index=False)
    results["wasted_spend"].to_csv(f"{output_prefix}_wasted_spend.csv", index=False)
    
    # Export negative recommendations
    neg_list = generate_negative_keyword_list(results["negative_recommendations"])
    with open(f"{output_prefix}_negatives.txt", "w") as f:
        f.write("# Recommended Negative Keywords from Search Term Analysis\n")
        f.write("# Add these as Negative Exact Match\n\n")
        for neg in neg_list:
            f.write(f"{neg}\n")
    
    print(f"\nAnalysis complete!")
    print(f"- Full report: {output_prefix}_full.csv")
    print(f"- High performers: {output_prefix}_high_performers.csv")
    print(f"- Wasted spend terms: {output_prefix}_wasted_spend.csv")
    print(f"- Negative keywords: {output_prefix}_negatives.txt")
    
    print("\n=== Summary ===")
    print(results["summary"])
    
    return results


if __name__ == "__main__":
    print("MasudLaBs - Search Term Report Analyzer")
    print("=" * 55)
    
    # Example usage with sample data (replace with your real export)
    print("\nNote: In real use, provide your Amazon Search Term Report CSV file.")
    print("Creating sample data for demonstration...\n")
    
    # Create sample data for demo
    sample_data = {
        "Search Term": [
            "wireless earbuds noise cancelling", "bluetooth earbuds cheap", "earbuds for running",
            "true wireless earbuds pro", "earbuds case", "wireless headphones review",
            "noise cancelling earbuds black", "cheap bluetooth earbuds bulk", "best earbuds 2025"
        ],
        "Impressions": [12500, 8200, 4500, 9800, 3100, 5600, 7200, 2900, 13400],
        "Clicks": [420, 380, 95, 310, 180, 210, 285, 165, 520],
        "Spend": [185.50, 142.30, 38.20, 165.80, 95.40, 78.90, 132.60, 88.75, 245.00],
        "Sales": [1250, 180, 42, 980, 15, 320, 890, 22, 1450],
        "Orders": [48, 7, 2, 35, 1, 12, 31, 1, 52]
    }
    
    sample_df = pd.DataFrame(sample_data)
    sample_df.to_csv("sample_search_term_report.csv", index=False)
    
    results = run_search_term_analysis("sample_search_term_report.csv", "demo_search_term_analysis")
    
    print("\n=== High Performers ===")
    print(results["high_performers"][["search_term", "spend", "sales", "acos", "category"]].head(5).to_string(index=False))
