from flask import Blueprint, request, jsonify
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

supply_chain_bp = Blueprint('supply_chain', __name__)

# Mock data for demonstration
MOCK_SKUS = [
    {"id": "ELEC001", "name": "Samsung Galaxy A54", "category": "Electronics", "revenue_rank": 1, "base_demand": 1000, "current_stock": 850},
    {"id": "ELEC002", "name": "iPhone 14", "category": "Electronics", "revenue_rank": 2, "base_demand": 800, "current_stock": 600},
    {"id": "ELEC003", "name": "OnePlus Nord 3", "category": "Electronics", "revenue_rank": 3, "base_demand": 750, "current_stock": 700},
    {"id": "APPR001", "name": "Levi's Jeans", "category": "Apparel", "revenue_rank": 4, "base_demand": 500, "current_stock": 400},
    {"id": "APPR002", "name": "Nike Air Max", "category": "Apparel", "revenue_rank": 5, "base_demand": 450, "current_stock": 380},
    {"id": "HOME001", "name": "Philips Air Fryer", "category": "Home", "revenue_rank": 6, "base_demand": 300, "current_stock": 250},
    {"id": "ELEC004", "name": "LG Smart TV 55\"", "category": "Electronics", "revenue_rank": 7, "base_demand": 200, "current_stock": 150},
    {"id": "APPR003", "name": "Adidas T-Shirt", "category": "Apparel", "revenue_rank": 8, "base_demand": 600, "current_stock": 500},
    {"id": "HOME002", "name": "Dyson Vacuum", "category": "Home", "revenue_rank": 9, "base_demand": 150, "current_stock": 120},
    {"id": "ELEC005", "name": "Sony Headphones", "category": "Electronics", "revenue_rank": 10, "base_demand": 400, "current_stock": 350}
]

DISRUPTION_TYPES = {
    "port_blockage": {
        "name": "Port Blockage",
        "affected_categories": ["Electronics", "Home"],
        "severity_multiplier": 0.6,
        "duration_days": 15
    },
    "cyclone": {
        "name": "Cyclone",
        "affected_categories": ["Electronics", "Apparel"],
        "severity_multiplier": 0.35,
        "duration_days": 10
    },
    "supplier_strike": {
        "name": "Supplier Strike",
        "affected_categories": ["Apparel"],
        "severity_multiplier": 0.8,
        "duration_days": 7
    },
    "customs_delay": {
        "name": "Customs Delay",
        "affected_categories": ["Electronics"],
        "severity_multiplier": 0.5,
        "duration_days": 12
    }
}

INTERVENTION_STRATEGIES = {
    "air_freight": {
        "name": "Air Freight Critical Items",
        "cost_per_unit": 150,
        "recovery_rate": 0.8,
        "implementation_days": 2
    },
    "reroute_port": {
        "name": "Reroute Through Alternative Port",
        "cost_per_unit": 50,
        "recovery_rate": 0.6,
        "implementation_days": 5
    },
    "expedite_production": {
        "name": "Expedite Supplier Production",
        "cost_per_unit": 75,
        "recovery_rate": 0.4,
        "implementation_days": 8
    },
    "increase_safety_stock": {
        "name": "Increase Safety Stock",
        "cost_per_unit": 25,
        "recovery_rate": 0.3,
        "implementation_days": 1
    }
}

def calculate_stockout_probability(sku, disruption_impact, days_until_recovery):
    """Calculate stockout probability based on current stock, demand, and disruption impact"""
    daily_demand = sku["base_demand"] / 30  # Convert monthly to daily
    affected_demand = daily_demand * (1 + disruption_impact)
    
    # Calculate days until stockout
    days_until_stockout = sku["current_stock"] / affected_demand
    
    if days_until_stockout >= days_until_recovery:
        return 0.05  # Minimal risk
    elif days_until_stockout <= 0:
        return 0.95  # Almost certain stockout
    else:
        # Linear interpolation between recovery time and stockout time
        risk_factor = 1 - (days_until_stockout / days_until_recovery)
        return min(0.9, max(0.1, risk_factor))

def calculate_intervention_impact(sku, intervention, disruption_severity):
    """Calculate the impact of an intervention on stockout probability"""
    base_recovery = intervention["recovery_rate"]
    cost_per_unit = intervention["cost_per_unit"]
    implementation_days = intervention["implementation_days"]
    
    # Calculate total cost for this SKU
    affected_units = sku["base_demand"] * disruption_severity
    total_cost = affected_units * cost_per_unit
    
    # Calculate new stockout probability after intervention
    recovery_factor = base_recovery * (1 - disruption_severity * 0.5)
    new_disruption_impact = disruption_severity * (1 - recovery_factor)
    
    new_stockout_prob = calculate_stockout_probability(
        sku, new_disruption_impact, implementation_days
    )
    
    return {
        "new_stockout_probability": new_stockout_prob,
        "cost": total_cost,
        "recovery_factor": recovery_factor
    }

@supply_chain_bp.route('/skus', methods=['GET'])
def get_skus():
    """Get list of top SKUs"""
    return jsonify(MOCK_SKUS)

@supply_chain_bp.route('/disruption-types', methods=['GET'])
def get_disruption_types():
    """Get available disruption types"""
    return jsonify(DISRUPTION_TYPES)

@supply_chain_bp.route('/interventions', methods=['GET'])
def get_interventions():
    """Get available intervention strategies"""
    return jsonify(INTERVENTION_STRATEGIES)

@supply_chain_bp.route('/simulate-disruption', methods=['POST'])
def simulate_disruption():
    """Simulate the impact of a disruption on supply chain"""
    data = request.get_json()
    
    disruption_type = data.get('disruption_type')
    severity = data.get('severity', 0.5)  # 0-1 scale
    duration = data.get('duration', 10)  # days
    
    if disruption_type not in DISRUPTION_TYPES:
        return jsonify({"error": "Invalid disruption type"}), 400
    
    disruption = DISRUPTION_TYPES[disruption_type]
    affected_categories = disruption["affected_categories"]
    
    results = []
    total_revenue_at_risk = 0
    
    for sku in MOCK_SKUS:
        if sku["category"] in affected_categories:
            # Calculate disruption impact
            disruption_impact = severity * disruption["severity_multiplier"]
            stockout_prob = calculate_stockout_probability(sku, disruption_impact, duration)
            
            # Calculate revenue at risk
            monthly_revenue = sku["base_demand"] * 100  # Assuming ₹100 average price
            revenue_at_risk = monthly_revenue * stockout_prob * (duration / 30)
            total_revenue_at_risk += revenue_at_risk
            
            results.append({
                "sku_id": sku["id"],
                "sku_name": sku["name"],
                "category": sku["category"],
                "stockout_probability": round(stockout_prob, 3),
                "revenue_at_risk": round(revenue_at_risk, 2),
                "current_stock": sku["current_stock"],
                "daily_demand": round(sku["base_demand"] / 30, 1)
            })
        else:
            # Not affected by this disruption
            results.append({
                "sku_id": sku["id"],
                "sku_name": sku["name"],
                "category": sku["category"],
                "stockout_probability": 0.05,
                "revenue_at_risk": 0,
                "current_stock": sku["current_stock"],
                "daily_demand": round(sku["base_demand"] / 30, 1)
            })
    
    return jsonify({
        "disruption": {
            "type": disruption_type,
            "name": disruption["name"],
            "severity": severity,
            "duration": duration,
            "affected_categories": affected_categories
        },
        "impact": {
            "total_revenue_at_risk": round(total_revenue_at_risk, 2),
            "affected_skus": len([r for r in results if r["stockout_probability"] > 0.1]),
            "high_risk_skus": len([r for r in results if r["stockout_probability"] > 0.5])
        },
        "sku_impacts": results
    })

@supply_chain_bp.route('/simulate-intervention', methods=['POST'])
def simulate_intervention():
    """Simulate the impact of intervention strategies"""
    data = request.get_json()
    
    disruption_data = data.get('disruption')
    intervention_ids = data.get('interventions', [])
    
    if not disruption_data or not intervention_ids:
        return jsonify({"error": "Missing disruption data or interventions"}), 400
    
    disruption_type = disruption_data['type']
    severity = disruption_data['severity']
    duration = disruption_data['duration']
    
    if disruption_type not in DISRUPTION_TYPES:
        return jsonify({"error": "Invalid disruption type"}), 400
    
    disruption = DISRUPTION_TYPES[disruption_type]
    affected_categories = disruption["affected_categories"]
    
    # Calculate baseline impact (without intervention)
    baseline_results = []
    baseline_revenue_at_risk = 0
    
    for sku in MOCK_SKUS:
        if sku["category"] in affected_categories:
            disruption_impact = severity * disruption["severity_multiplier"]
            stockout_prob = calculate_stockout_probability(sku, disruption_impact, duration)
            monthly_revenue = sku["base_demand"] * 100
            revenue_at_risk = monthly_revenue * stockout_prob * (duration / 30)
            baseline_revenue_at_risk += revenue_at_risk
            
            baseline_results.append({
                "sku_id": sku["id"],
                "baseline_stockout_prob": stockout_prob,
                "baseline_revenue_at_risk": revenue_at_risk
            })
    
    # Calculate intervention impact
    intervention_results = []
    total_intervention_cost = 0
    total_revenue_saved = 0
    
    for intervention_id in intervention_ids:
        if intervention_id not in INTERVENTION_STRATEGIES:
            continue
            
        intervention = INTERVENTION_STRATEGIES[intervention_id]
        intervention_cost = 0
        revenue_saved = 0
        
        for i, sku in enumerate(MOCK_SKUS):
            if sku["category"] in affected_categories:
                baseline = baseline_results[i]
                
                # Calculate intervention impact
                impact = calculate_intervention_impact(
                    sku, intervention, severity * disruption["severity_multiplier"]
                )
                
                intervention_cost += impact["cost"]
                
                # Calculate revenue saved
                revenue_reduction = (baseline["baseline_stockout_prob"] - 
                                   impact["new_stockout_probability"]) * sku["base_demand"] * 100 * (duration / 30)
                revenue_saved += max(0, revenue_reduction)
        
        total_intervention_cost += intervention_cost
        total_revenue_saved += revenue_saved
        
        intervention_results.append({
            "intervention_id": intervention_id,
            "intervention_name": intervention["name"],
            "cost": round(intervention_cost, 2),
            "revenue_saved": round(revenue_saved, 2),
            "roi": round((revenue_saved - intervention_cost) / intervention_cost * 100, 1) if intervention_cost > 0 else 0,
            "implementation_days": intervention["implementation_days"]
        })
    
    # Calculate combined impact
    net_benefit = total_revenue_saved - total_intervention_cost
    overall_roi = (net_benefit / total_intervention_cost * 100) if total_intervention_cost > 0 else 0
    
    return jsonify({
        "baseline": {
            "total_revenue_at_risk": round(baseline_revenue_at_risk, 2)
        },
        "intervention_summary": {
            "total_cost": round(total_intervention_cost, 2),
            "total_revenue_saved": round(total_revenue_saved, 2),
            "net_benefit": round(net_benefit, 2),
            "overall_roi": round(overall_roi, 1)
        },
        "interventions": intervention_results,
        "recommendation": {
            "recommended": net_benefit > 0,
            "confidence": "High" if abs(overall_roi) > 50 else "Medium" if abs(overall_roi) > 20 else "Low",
            "priority_interventions": sorted(intervention_results, key=lambda x: x["roi"], reverse=True)[:2]
        }
    })

@supply_chain_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

