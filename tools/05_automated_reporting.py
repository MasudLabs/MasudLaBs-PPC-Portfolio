#!/usr/bin/env python3
"""
MasudLaBs PPC Portfolio - Tool 6
Automated Reporting Script

Purpose:
- Generate clean daily or weekly performance reports from Amazon exports
- Highlight key metrics, trends, and anomalies
- Flag campaigns/terms that need attention
- Easy to schedule or run manually

This is a starter version. Can be extended with email alerts or Google Sheets integration.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict


def generate_performance_summary(df: pd.DataFrame, period: str = "Daily") -> Dict:
    """
    Generate a clean performance summary from campaign or search term data.
    """
    summary = {
        "report_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "period": period,
        "total_spend": round(df["spend"].sum(), 2) if "spend" in df.columns else 0,
        "total_sales": round(df["sales"].sum(), 2) if "sales" in df.columns else 0,
        "total_clicks": int(df["clicks"].sum()) if "clicks" in df.columns else 0,
        "total_orders": int(df["orders"].sum()) if "orders" in df.columns else 0,
    }
    
    if summary["total_sales"] > 0 and summary["total_spend"] > 0:
        summary["overall_acos"] = round((summary["total_spend"] / summary["total_sales"]) * 100, 2)
        summary["overall_roas"] = round(summary["total_sales"] / summary["total_spend"], 2)
    else:
        summary["overall_acos"] = 0
        summary["overall_roas"] = 0
    
    # Top performers
    if "campaign_name" in df.columns or "search_term" in df.columns:
        identifier = "campaign_name" if "campaign_name" in df.columns else "search_term"
        top = df.nlargest(5, "sales")[[identifier, "spend", "sales", "acos"]] if "acos" in df.columns else df.nlargest(5, "sales")
        summary["top_performers"] = top.to_dict("records")
    
    # Alerts
    alerts = []
    if summary["overall_acos"] > 35:
        alerts.append("High ACoS detected - Review underperforming terms")
    if summary["total_clicks"] > 0 and (summary["total_orders"] / summary["total_clicks"]) < 0.05:
        alerts.append("Low CVR - Consider adding negative keywords or improving targeting")
    
    summary["alerts"] = alerts
    
    return summary

def create_report(
    input_file: str,
    output_file: str = "performance_report.txt",
    period: str = "Daily"
):
    """Generate and save a formatted performance report."""
    print(f"Generating {period} Performance Report...")
    
    df = pd.read_csv(input_file)
    
    # Standardize columns
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    
    summary = generate_performance_summary(df, period)
    
    # Write report
    with open(output_file, "w") as f:
        f.write("=" * 60 + "\n")
        f.write(f" MasudLaBs PPC - {period.upper()} PERFORMANCE REPORT\n")
        f.write(f" Generated: {summary['report_date']}\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("KEY METRICS\n")
        f.write("-" * 20 + "\n")
        f.write(f"Total Spend: ${summary['total_spend']}\n")
        f.write(f"Total Sales:  ${summary['total_sales']}\n")
        f.write(f"Overall ACoS: {summary['overall_acos']}%\n")
        f.write(f"Overall ROAS: {summary['overall_roas']}x\n")
        f.write(f"Total Clicks: {summary['total_clicks']}\n")
        f.write(f"Total Orders: {summary['total_orders']}\n\n")
        
        if summary["alerts"]:
            f.write("ALERTS / ACTION ITEMS\n")
            f.write("-" * 20 + "\n")
            for alert in summary["alerts"]:
                f.write(f"- {alert}\n")
            f.write("\n")
        
        f.write("TOP 5 PERFORMERS\n")
        f.write("-" * 20 + "\n")
        for item in summary.get("top_performers", []):
            f.write(f"- {item}\n")
    
    print(f"Report saved to: {output_file}")
    return summary


if __name__ == "__main__":
    print("MasudLaBs - Automated Reporting Script")
    print("=" * 50)
    
    # Create sample data for demo
    sample = pd.DataFrame({
        "campaign_name": ["Brand Defense", "Category Broad", "Long Tail", "Competitor Conquest"],
        "spend": [45.20, 98.50, 32.80, 67.40],
        "sales": [312.00, 485.00, 210.00, 285.00],
        "clicks": [125, 380, 95, 210],
        "orders": [12, 18, 8, 9]
    })
    sample.to_csv("sample_campaign_report.csv", index=False)
    
    report = create_report("sample_campaign_report.csv", "demo_daily_report.txt", period="Daily")
    
    print("\nReport Preview:")
    print(open("demo_daily_report.txt").read())
