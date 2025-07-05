import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
import json
from typing import Dict, List, Tuple, Any

class ExplainableAI:
    """
    Explainable AI system for supply chain decision support
    """
    
    def __init__(self):
        self.models = {}
        self.feature_importance = {}
        self.explanations = {}
        
    def train_risk_prediction_model(self, data: pd.DataFrame):
        """Train a model to predict supply chain risk"""
        # Prepare features
        features = ['supplier_reliability', 'transport_capacity', 'inventory_level', 
                   'demand_volatility', 'geopolitical_risk', 'weather_risk']
        
        X = data[features]
        y = data['risk_score']
        
        # Train Random Forest model (interpretable)
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        
        self.models['risk_prediction'] = model
        
        # Calculate feature importance
        importance = model.feature_importances_
        self.feature_importance['risk_prediction'] = dict(zip(features, importance))
        
        return model
    
    def explain_risk_prediction(self, input_data: Dict[str, float]) -> Dict[str, Any]:
        """Explain why a particular risk score was predicted"""
        if 'risk_prediction' not in self.models:
            return {"error": "Risk prediction model not trained"}
        
        model = self.models['risk_prediction']
        features = ['supplier_reliability', 'transport_capacity', 'inventory_level', 
                   'demand_volatility', 'geopolitical_risk', 'weather_risk']
        
        # Make prediction
        X = np.array([[input_data[f] for f in features]])
        risk_score = model.predict(X)[0]
        
        # Generate explanation
        explanation = {
            "predicted_risk_score": round(risk_score, 2),
            "risk_level": self._categorize_risk(risk_score),
            "key_factors": self._identify_key_factors(input_data),
            "recommendations": self._generate_recommendations(input_data, risk_score),
            "feature_contributions": self._calculate_feature_contributions(input_data),
            "confidence": self._calculate_confidence(input_data)
        }
        
        return explanation
    
    def _categorize_risk(self, risk_score: float) -> str:
        """Categorize risk score into levels"""
        if risk_score < 30:
            return "Low"
        elif risk_score < 60:
            return "Medium"
        elif risk_score < 80:
            return "High"
        else:
            return "Critical"
    
    def _identify_key_factors(self, input_data: Dict[str, float]) -> List[Dict[str, Any]]:
        """Identify the most important factors contributing to risk"""
        factors = []
        
        # Supplier reliability
        if input_data['supplier_reliability'] < 0.8:
            factors.append({
                "factor": "Supplier Reliability",
                "value": input_data['supplier_reliability'],
                "impact": "High",
                "description": "Low supplier reliability significantly increases supply chain risk"
            })
        
        # Transport capacity
        if input_data['transport_capacity'] < 0.7:
            factors.append({
                "factor": "Transport Capacity",
                "value": input_data['transport_capacity'],
                "impact": "Medium",
                "description": "Limited transport capacity may cause delivery delays"
            })
        
        # Inventory level
        if input_data['inventory_level'] < 0.3:
            factors.append({
                "factor": "Inventory Level",
                "value": input_data['inventory_level'],
                "impact": "High",
                "description": "Low inventory levels increase stockout risk"
            })
        
        # Geopolitical risk
        if input_data['geopolitical_risk'] > 0.6:
            factors.append({
                "factor": "Geopolitical Risk",
                "value": input_data['geopolitical_risk'],
                "impact": "High",
                "description": "High geopolitical tensions may disrupt supply routes"
            })
        
        return factors
    
    def _generate_recommendations(self, input_data: Dict[str, float], risk_score: float) -> List[Dict[str, Any]]:
        """Generate actionable recommendations based on risk factors"""
        recommendations = []
        
        if input_data['supplier_reliability'] < 0.8:
            recommendations.append({
                "action": "Diversify Supplier Base",
                "priority": "High",
                "timeframe": "1-2 weeks",
                "description": "Identify and onboard alternative suppliers to reduce dependency",
                "expected_impact": "Reduce risk by 15-20%"
            })
        
        if input_data['inventory_level'] < 0.3:
            recommendations.append({
                "action": "Increase Safety Stock",
                "priority": "High",
                "timeframe": "3-5 days",
                "description": "Increase inventory levels for critical products",
                "expected_impact": "Reduce stockout risk by 25%"
            })
        
        if input_data['transport_capacity'] < 0.7:
            recommendations.append({
                "action": "Secure Additional Transport",
                "priority": "Medium",
                "timeframe": "1 week",
                "description": "Contract additional transport capacity or alternative routes",
                "expected_impact": "Improve delivery reliability by 20%"
            })
        
        if input_data['geopolitical_risk'] > 0.6:
            recommendations.append({
                "action": "Route Diversification",
                "priority": "High",
                "timeframe": "2-3 weeks",
                "description": "Establish alternative supply routes to avoid high-risk regions",
                "expected_impact": "Reduce geopolitical exposure by 40%"
            })
        
        return recommendations
    
    def _calculate_feature_contributions(self, input_data: Dict[str, float]) -> Dict[str, float]:
        """Calculate how much each feature contributes to the risk score"""
        if 'risk_prediction' not in self.feature_importance:
            return {}
        
        contributions = {}
        importance = self.feature_importance['risk_prediction']
        
        for feature, value in input_data.items():
            if feature in importance:
                # Simplified contribution calculation
                # In practice, this would use SHAP values or similar
                contribution = importance[feature] * (1 - value if feature in ['supplier_reliability', 'transport_capacity', 'inventory_level'] else value)
                contributions[feature] = round(contribution * 100, 2)
        
        return contributions
    
    def _calculate_confidence(self, input_data: Dict[str, float]) -> float:
        """Calculate confidence in the prediction"""
        # Simplified confidence calculation based on data quality
        confidence = 0.9  # Base confidence
        
        # Reduce confidence for extreme values
        for feature, value in input_data.items():
            if value < 0.1 or value > 0.9:
                confidence -= 0.05
        
        return max(0.5, min(1.0, confidence))
    
    def generate_what_if_analysis(self, base_scenario: Dict[str, float], 
                                 variations: Dict[str, List[float]]) -> Dict[str, Any]:
        """Generate what-if analysis for different scenarios"""
        if 'risk_prediction' not in self.models:
            return {"error": "Risk prediction model not trained"}
        
        model = self.models['risk_prediction']
        features = ['supplier_reliability', 'transport_capacity', 'inventory_level', 
                   'demand_volatility', 'geopolitical_risk', 'weather_risk']
        
        scenarios = []
        
        for var_feature, var_values in variations.items():
            for var_value in var_values:
                scenario = base_scenario.copy()
                scenario[var_feature] = var_value
                
                X = np.array([[scenario[f] for f in features]])
                risk_score = model.predict(X)[0]
                
                scenarios.append({
                    "scenario": f"{var_feature} = {var_value}",
                    "risk_score": round(risk_score, 2),
                    "risk_level": self._categorize_risk(risk_score),
                    "change_from_base": round(risk_score - model.predict(np.array([[base_scenario[f] for f in features]]))[0], 2)
                })
        
        return {
            "base_scenario": base_scenario,
            "base_risk_score": round(model.predict(np.array([[base_scenario[f] for f in features]]))[0], 2),
            "scenarios": scenarios
        }
    
    def create_decision_tree_explanation(self, input_data: Dict[str, float]) -> Dict[str, Any]:
        """Create a decision tree-like explanation for the prediction"""
        explanation = {
            "decision_path": [],
            "final_decision": "",
            "confidence": self._calculate_confidence(input_data)
        }
        
        # Simplified decision tree logic
        if input_data['supplier_reliability'] < 0.7:
            explanation["decision_path"].append("Supplier reliability is low (< 70%)")
            if input_data['inventory_level'] < 0.3:
                explanation["decision_path"].append("AND inventory level is critically low (< 30%)")
                explanation["final_decision"] = "HIGH RISK: Immediate action required"
            else:
                explanation["final_decision"] = "MEDIUM RISK: Monitor closely and prepare contingencies"
        elif input_data['geopolitical_risk'] > 0.7:
            explanation["decision_path"].append("Geopolitical risk is high (> 70%)")
            explanation["final_decision"] = "HIGH RISK: Diversify supply routes immediately"
        else:
            explanation["decision_path"].append("Core risk factors are within acceptable ranges")
            explanation["final_decision"] = "LOW-MEDIUM RISK: Continue monitoring"
        
        return explanation

def create_sample_data():
    """Create sample data for training the explainable AI model"""
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'supplier_reliability': np.random.beta(2, 1, n_samples),
        'transport_capacity': np.random.beta(2, 1, n_samples),
        'inventory_level': np.random.beta(1.5, 1.5, n_samples),
        'demand_volatility': np.random.beta(1, 2, n_samples),
        'geopolitical_risk': np.random.beta(1, 3, n_samples),
        'weather_risk': np.random.beta(1, 2, n_samples)
    }
    
    # Calculate risk score based on features
    risk_scores = []
    for i in range(n_samples):
        risk = (
            (1 - data['supplier_reliability'][i]) * 30 +
            (1 - data['transport_capacity'][i]) * 20 +
            (1 - data['inventory_level'][i]) * 25 +
            data['demand_volatility'][i] * 15 +
            data['geopolitical_risk'][i] * 20 +
            data['weather_risk'][i] * 10
        )
        # Add some noise
        risk += np.random.normal(0, 5)
        risk_scores.append(max(0, min(100, risk)))
    
    data['risk_score'] = risk_scores
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    # Create and train explainable AI system
    explainer = ExplainableAI()
    
    # Generate sample training data
    print("Generating sample training data...")
    training_data = create_sample_data()
    
    # Train the model
    print("Training risk prediction model...")
    explainer.train_risk_prediction_model(training_data)
    
    # Example scenario for explanation
    scenario = {
        'supplier_reliability': 0.65,  # Low reliability
        'transport_capacity': 0.8,
        'inventory_level': 0.25,       # Low inventory
        'demand_volatility': 0.4,
        'geopolitical_risk': 0.7,      # High geopolitical risk
        'weather_risk': 0.3
    }
    
    # Generate explanation
    print("\nGenerating explanation for scenario...")
    explanation = explainer.explain_risk_prediction(scenario)
    
    # Print explanation
    print(f"\n=== Risk Assessment Explanation ===")
    print(f"Predicted Risk Score: {explanation['predicted_risk_score']}")
    print(f"Risk Level: {explanation['risk_level']}")
    print(f"Confidence: {explanation['confidence']:.2%}")
    
    print(f"\nKey Risk Factors:")
    for factor in explanation['key_factors']:
        print(f"- {factor['factor']}: {factor['value']:.2f} ({factor['impact']} impact)")
        print(f"  {factor['description']}")
    
    print(f"\nRecommendations:")
    for i, rec in enumerate(explanation['recommendations'], 1):
        print(f"{i}. {rec['action']} (Priority: {rec['priority']})")
        print(f"   Timeframe: {rec['timeframe']}")
        print(f"   Expected Impact: {rec['expected_impact']}")
    
    # Generate what-if analysis
    print(f"\n=== What-If Analysis ===")
    variations = {
        'supplier_reliability': [0.7, 0.8, 0.9],
        'inventory_level': [0.3, 0.5, 0.7]
    }
    
    what_if = explainer.generate_what_if_analysis(scenario, variations)
    print(f"Base Risk Score: {what_if['base_risk_score']}")
    print(f"\nScenario Analysis:")
    for scenario_result in what_if['scenarios']:
        print(f"- {scenario_result['scenario']}: Risk = {scenario_result['risk_score']} "
              f"(Change: {scenario_result['change_from_base']:+.1f})")
    
    # Generate decision tree explanation
    print(f"\n=== Decision Tree Explanation ===")
    decision_tree = explainer.create_decision_tree_explanation(scenario)
    print("Decision Path:")
    for step in decision_tree['decision_path']:
        print(f"- {step}")
    print(f"Final Decision: {decision_tree['final_decision']}")
    
    # Save explanation to JSON
    with open('explanation_example.json', 'w') as f:
        json.dump(explanation, f, indent=2)
    print(f"\nDetailed explanation saved to explanation_example.json")

