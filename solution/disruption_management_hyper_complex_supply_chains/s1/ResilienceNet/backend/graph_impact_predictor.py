
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

def create_supply_chain_graph(df):
    G = nx.DiGraph()

    # Add nodes for DCs and Products
    for dc_id in df["dc_id"].unique():
        G.add_node(dc_id, type="DC")
    for prod_id in df["product_id"].unique():
        G.add_node(prod_id, type="Product")

    # Add edges: DC -> Product (representing products available at a DC)
    # In a real scenario, this would be more complex, involving suppliers, routes, etc.
    for _, row in df.iterrows():
        G.add_edge(row["dc_id"], row["product_id"], weight=row["inventory"])

    return G

def predict_cascading_impact(graph, disrupted_node, impact_type="stockout", threshold=50):
    impacted_nodes = set()
    if disrupted_node in graph:
        # Simulate impact propagation using shortest path or reachability
        # For simplicity, we consider all nodes reachable from the disrupted node as potentially impacted
        # In a real scenario, this would involve more sophisticated graph algorithms and domain logic
        for node in nx.descendants(graph, disrupted_node):
            impacted_nodes.add(node)

        # Further refine impact based on product type or other attributes
        # Example: if a DC is disrupted, which products are affected?
        if graph.nodes[disrupted_node]["type"] == "DC":
            for neighbor in graph.successors(disrupted_node):
                if graph.nodes[neighbor]["type"] == "Product":
                    # Simulate stockout if inventory falls below threshold
                    # This is a simplified example, actual stockout prediction would be more complex
                    if graph[disrupted_node][neighbor]["weight"] < threshold:
                        impacted_nodes.add(neighbor)

    return list(impacted_nodes)

def visualize_graph(graph, disrupted_node=None, impacted_nodes=None, filename="supply_chain_graph.png"):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph, k=0.5, iterations=50)  # positions for all nodes

    node_colors = []
    for node in graph.nodes():
        if node == disrupted_node:
            node_colors.append("red")
        elif impacted_nodes and node in impacted_nodes:
            node_colors.append("orange")
        elif graph.nodes[node]["type"] == "DC":
            node_colors.append("skyblue")
        else:
            node_colors.append("lightgreen")

    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=3000)
    nx.draw_networkx_edges(graph, pos, edge_color="gray", alpha=0.5)
    nx.draw_networkx_labels(graph, pos, font_size=10, font_weight="bold")

    plt.title("Supply Chain Graph with Disruption Impact")
    plt.axis("off")
    plt.savefig(filename)
    plt.close()

if __name__ == "__main__":
    df = pd.read_csv("simulated_supply_chain_data.csv")

    # Use a subset of data for graph creation to keep it manageable for visualization
    df_subset = df[df["date"] == df["date"].min()].head(20) 

    G = create_supply_chain_graph(df_subset)
    print("Number of nodes:", G.number_of_nodes())
    print("Number of edges:", G.number_of_edges())

    # Example disruption: DC_0 is disrupted
    disrupted_dc = "DC_0"
    impacted = predict_cascading_impact(G, disrupted_dc)
    print(f"Nodes impacted by disruption at {disrupted_dc}: {impacted}")

    visualize_graph(G, disrupted_node=disrupted_dc, impacted_nodes=impacted, filename="supply_chain_disruption_impact.png")

    # Example disruption: PROD_0 is disrupted (e.g., supplier issue)
    disrupted_product = "PROD_0"
    impacted_prod = predict_cascading_impact(G, disrupted_product)
    print(f"Nodes impacted by disruption at {disrupted_product}: {impacted_prod}")

    visualize_graph(G, disrupted_node=disrupted_product, impacted_nodes=impacted_prod, filename="product_disruption_impact.png")


