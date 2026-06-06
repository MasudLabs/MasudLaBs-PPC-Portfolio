#!/usr/bin/env python3
"""
MasudLaBs PPC Portfolio - Tool 1
Keyword Research Tool + Negative Keyword Generator

Purpose:
- Generate Broad, Phrase, and Exact match keywords from seed terms
- Suggest negative keywords based on common patterns and user input
- Export clean CSV ready for Amazon Sponsored Products

This is a starter version for portfolio demonstration.
Future improvements: Integrate with search term reports for smarter negatives.
"""

import pandas as pd
from typing import List, Dict


def generate_match_types(seed_keywords: List[str]) -> pd.DataFrame:
    """
    Generate Broad, Phrase, and Exact match versions of keywords.
    
    Args:
        seed_keywords: List of base keywords (e.g. ["wireless earbuds", "bluetooth headphones"])
    
    Returns:
        DataFrame with columns: Keyword, Match Type, Suggested Bid (placeholder)
    """
    rows = []
    for seed in seed_keywords:
        seed = seed.strip().lower()
        if not seed:
            continue
        
        # Broad Match
        rows.append({
            "Keyword": seed,
            "Match Type": "Broad",
            "Suggested Bid": 0.50,   # Placeholder - user should adjust
            "Notes": "Broad match for discovery"
        })
        
        # Phrase Match
        rows.append({
            "Keyword": f'"{seed}"',
            "Match Type": "Phrase",
            "Suggested Bid": 0.65,
            "Notes": "Phrase match for better control"
        })
        
        # Exact Match
        rows.append({
            "Keyword": f'[{seed}]',
            "Match Type": "Exact",
            "Suggested Bid": 0.85,
            "Notes": "Exact match for high intent"
        })
    
    return pd.DataFrame(rows)


def suggest_negative_keywords(
    seed_keywords: List[str], 
    custom_negatives: List[str] = None
) -> List[str]:
    """
    Generate negative keyword suggestions.
    
    This is a basic version. In production, this would analyze
    actual search term reports for low-converting terms.
    """
    negatives = set()
    
    # Common negative patterns for many products
    common_negatives = [
        "free", "cheap", "wholesale", "bulk", "used", "refurbished",
        "case", "cover", "accessory", "replacement", "manual", "instructions",
        "review", "unboxing", "vs", "versus", "comparison"
    ]
    
    negatives.update(common_negatives)
    
    # Add product-specific negatives based on seeds (simple heuristic)
    for seed in seed_keywords:
        words = seed.lower().split()
        if len(words) > 1:
            # Example: if someone searches for parts of the product
            negatives.add(words[0])   # first word as potential negative in some contexts
    
    if custom_negatives:
        negatives.update([n.lower().strip() for n in custom_negatives])
    
    return sorted(list(negatives))


def create_keyword_portfolio(
    seed_keywords: List[str],
    custom_negatives: List[str] = None,
    output_file: str = "keyword_research_output.csv"
) -> Dict:
    """
    Main function to generate full keyword + negative keyword package.
    
    Returns dict with keywords DataFrame and list of negatives.
    Also exports to CSV.
    """
    print("Generating keyword variations...")
    keywords_df = generate_match_types(seed_keywords)
    
    print("Generating negative keyword suggestions...")
    negatives = suggest_negative_keywords(seed_keywords, custom_negatives)
    
    # Export keywords
    keywords_df.to_csv(output_file, index=False)
    print(f"\nKeywords exported to: {output_file}")
    
    # Export negatives as simple text file
    neg_file = output_file.replace(".csv", "_negatives.txt")
    with open(neg_file, "w") as f:
        f.write("# Negative Keywords - Add these as Negative Exact or Phrase\n")
        for neg in negatives:
            f.write(f"{neg}\n")
    
    print(f"Negative keywords exported to: {neg_file}")
    
    return {
        "keywords": keywords_df,
        "negatives": negatives,
        "keyword_file": output_file,
        "negative_file": neg_file
    }


if __name__ == "__main__":
    # ==================== EXAMPLE USAGE ====================
    print("MasudLaBs - Keyword Research Tool")
    print("=" * 50)
    
    # Example seed keywords (replace with your own)
    seeds = [
        "wireless earbuds",
        "bluetooth headphones noise cancelling",
        "true wireless earbuds",
        "earbuds for running"
    ]
    
    custom_negs = ["kids", "children", "toy", "gaming"]   # Optional
    
    result = create_keyword_portfolio(
        seed_keywords=seeds,
        custom_negatives=custom_negs,
        output_file="example_keyword_research.csv"
    )
    
    print("\n=== Sample Output ===")
    print(result["keywords"].head(12).to_string(index=False))
    print("\n=== Top Negative Keywords ===")
    print(result["negatives"][:15])
