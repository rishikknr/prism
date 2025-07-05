
import pandas as pd

def suggest_mitigation_strategies(impacted_nodes, disruption_type=\"stockout\"):
    strategies = []
    for node in impacted_nodes:
        if \"DC\" in node:
            strategies.append(f"For DC {node}, consider rerouting shipments to alternative DCs or expediting inventory from other sources.")
        elif \"PROD\" in node:
            strategies.append(f"For Product {node}, explore alternative suppliers, prioritize production, or implement temporary substitutes.")
    
    if disruption_type == \"cost_spike\":
        strategies.append("Negotiate with alternative suppliers for better rates or explore hedging strategies for raw materials.")
    elif disruption_type == \"stockout\":
        strategies.append("Implement dynamic inventory adjustments and consider safety stock increases for critical products.")

    return strategies

if __name__ == \"__main__\":
    # Example usage
    impacted_dcs = [\"DC_0\"]
    impacted_products = [\"PROD_0\", \"PROD_1\"]
    
    print("Mitigation strategies for DC disruption:")
    dc_strategies = suggest_mitigation_strategies(impacted_dcs, disruption_type=\"stockout\")
    for strategy in dc_strategies:
        print(f"- {strategy}")

    print("\nMitigation strategies for Product disruption:")
    product_strategies = suggest_mitigation_strategies(impacted_products, disruption_type=\"stockout\")
    for strategy in product_strategies:
        print(f"- {strategy}")

    print("\nMitigation strategies for Cost Spike:")
    cost_spike_strategies = suggest_mitigation_strategies([], disruption_type=\"cost_spike\")
    for strategy in cost_spike_strategies:
        print(f"- {strategy}")


