import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Dict, Tuple
import json

@dataclass
class Agent:
    """Base class for all agents in the simulation"""
    id: str
    agent_type: str
    location: Tuple[float, float]
    capacity: float
    current_load: float = 0.0
    status: str = "active"
    
class SupplierAgent(Agent):
    def __init__(self, id: str, location: Tuple[float, float], capacity: float, reliability: float = 0.9):
        super().__init__(id, "supplier", location, capacity)
        self.reliability = reliability
        self.production_rate = capacity * 0.8  # 80% of capacity as normal production
        self.inventory = capacity * 0.5  # Start with 50% inventory
        
    def produce(self, demand: float) -> float:
        """Produce goods based on demand and reliability"""
        if random.random() > self.reliability:
            # Supplier failure
            self.status = "disrupted"
            return 0.0
        
        production = min(demand, self.production_rate)
        self.inventory += production
        return production
    
    def supply(self, requested_amount: float) -> float:
        """Supply goods from inventory"""
        if self.status == "disrupted":
            return 0.0
            
        supplied = min(requested_amount, self.inventory)
        self.inventory -= supplied
        return supplied

class DistributionCenterAgent(Agent):
    def __init__(self, id: str, location: Tuple[float, float], capacity: float):
        super().__init__(id, "distribution_center", location, capacity)
        self.inventory = {}  # Product ID -> quantity
        self.demand_forecast = {}
        
    def receive_goods(self, product_id: str, quantity: float):
        """Receive goods from suppliers"""
        if product_id not in self.inventory:
            self.inventory[product_id] = 0
        self.inventory[product_id] += quantity
        
    def fulfill_demand(self, product_id: str, demand: float) -> float:
        """Fulfill demand from inventory"""
        if product_id not in self.inventory:
            return 0.0
            
        fulfilled = min(demand, self.inventory[product_id])
        self.inventory[product_id] -= fulfilled
        return fulfilled
        
    def get_inventory_level(self, product_id: str) -> float:
        """Get current inventory level for a product"""
        return self.inventory.get(product_id, 0.0)

class TransportAgent(Agent):
    def __init__(self, id: str, location: Tuple[float, float], capacity: float, speed: float = 50.0):
        super().__init__(id, "transport", location, capacity)
        self.speed = speed  # km/h
        self.route = []
        self.cargo = {}
        
    def calculate_travel_time(self, destination: Tuple[float, float]) -> float:
        """Calculate travel time to destination"""
        distance = np.sqrt((destination[0] - self.location[0])**2 + 
                          (destination[1] - self.location[1])**2)
        return distance / self.speed
        
    def load_cargo(self, product_id: str, quantity: float) -> bool:
        """Load cargo if capacity allows"""
        total_cargo = sum(self.cargo.values())
        if total_cargo + quantity <= self.capacity:
            if product_id not in self.cargo:
                self.cargo[product_id] = 0
            self.cargo[product_id] += quantity
            return True
        return False
        
    def unload_cargo(self, product_id: str = None) -> Dict[str, float]:
        """Unload all or specific cargo"""
        if product_id:
            if product_id in self.cargo:
                quantity = self.cargo.pop(product_id)
                return {product_id: quantity}
            return {}
        else:
            cargo = self.cargo.copy()
            self.cargo.clear()
            return cargo

class DisruptionEvent:
    def __init__(self, event_type: str, affected_agents: List[str], 
                 start_time: int, duration: int, severity: float):
        self.event_type = event_type
        self.affected_agents = affected_agents
        self.start_time = start_time
        self.duration = duration
        self.severity = severity
        self.active = False
        
    def is_active(self, current_time: int) -> bool:
        return self.start_time <= current_time < self.start_time + self.duration

class SupplyChainSimulation:
    def __init__(self):
        self.suppliers = {}
        self.distribution_centers = {}
        self.transport_agents = {}
        self.disruption_events = []
        self.time_step = 0
        self.simulation_data = []
        
    def add_supplier(self, supplier: SupplierAgent):
        self.suppliers[supplier.id] = supplier
        
    def add_distribution_center(self, dc: DistributionCenterAgent):
        self.distribution_centers[dc.id] = dc
        
    def add_transport_agent(self, transport: TransportAgent):
        self.transport_agents[transport.id] = transport
        
    def add_disruption_event(self, event: DisruptionEvent):
        self.disruption_events.append(event)
        
    def apply_disruptions(self):
        """Apply active disruptions to agents"""
        for event in self.disruption_events:
            if event.is_active(self.time_step):
                for agent_id in event.affected_agents:
                    # Apply disruption to suppliers
                    if agent_id in self.suppliers:
                        supplier = self.suppliers[agent_id]
                        if event.event_type == "supplier_failure":
                            supplier.status = "disrupted"
                            supplier.reliability *= (1 - event.severity)
                    
                    # Apply disruption to transport
                    elif agent_id in self.transport_agents:
                        transport = self.transport_agents[agent_id]
                        if event.event_type == "transport_delay":
                            transport.speed *= (1 - event.severity)
                            transport.status = "delayed"
                    
                    # Apply disruption to distribution centers
                    elif agent_id in self.distribution_centers:
                        dc = self.distribution_centers[agent_id]
                        if event.event_type == "facility_closure":
                            dc.status = "closed"
            else:
                # Reset agents when disruption ends
                for agent_id in event.affected_agents:
                    if agent_id in self.suppliers:
                        self.suppliers[agent_id].status = "active"
                        self.suppliers[agent_id].reliability = 0.9  # Reset to default
                    elif agent_id in self.transport_agents:
                        self.transport_agents[agent_id].status = "active"
                        self.transport_agents[agent_id].speed = 50.0  # Reset to default
                    elif agent_id in self.distribution_centers:
                        self.distribution_centers[agent_id].status = "active"
    
    def simulate_demand(self, product_id: str) -> Dict[str, float]:
        """Simulate customer demand for each DC"""
        demand = {}
        for dc_id in self.distribution_centers:
            # Base demand with some randomness
            base_demand = random.uniform(50, 150)
            # Add seasonal variation
            seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * self.time_step / 365)
            demand[dc_id] = base_demand * seasonal_factor
        return demand
    
    def optimize_supply_allocation(self, product_id: str, total_supply: float, 
                                 demand: Dict[str, float]) -> Dict[str, float]:
        """Optimize supply allocation using simple proportional allocation"""
        total_demand = sum(demand.values())
        if total_demand == 0:
            return {dc_id: 0 for dc_id in demand}
        
        allocation = {}
        for dc_id, dc_demand in demand.items():
            proportion = dc_demand / total_demand
            allocation[dc_id] = min(total_supply * proportion, dc_demand)
        
        return allocation
    
    def step(self):
        """Execute one simulation step"""
        self.time_step += 1
        
        # Apply disruptions
        self.apply_disruptions()
        
        # Simulate for each product (simplified to one product for demo)
        product_id = "PROD_ELECTRONICS"
        
        # Generate demand
        demand = self.simulate_demand(product_id)
        
        # Suppliers produce goods
        total_production = 0
        for supplier in self.suppliers.values():
            production = supplier.produce(100)  # Request 100 units
            total_production += production
        
        # Allocate supply to DCs
        allocation = self.optimize_supply_allocation(product_id, total_production, demand)
        
        # Transport goods to DCs
        for dc_id, allocated_amount in allocation.items():
            if allocated_amount > 0:
                dc = self.distribution_centers[dc_id]
                dc.receive_goods(product_id, allocated_amount)
        
        # Fulfill customer demand
        total_fulfilled = 0
        total_stockout = 0
        for dc_id, dc_demand in demand.items():
            dc = self.distribution_centers[dc_id]
            fulfilled = dc.fulfill_demand(product_id, dc_demand)
            total_fulfilled += fulfilled
            total_stockout += max(0, dc_demand - fulfilled)
        
        # Calculate metrics
        service_level = total_fulfilled / sum(demand.values()) if sum(demand.values()) > 0 else 1.0
        total_inventory = sum(dc.get_inventory_level(product_id) for dc in self.distribution_centers.values())
        
        # Record simulation data
        step_data = {
            "time_step": self.time_step,
            "total_production": total_production,
            "total_demand": sum(demand.values()),
            "total_fulfilled": total_fulfilled,
            "total_stockout": total_stockout,
            "service_level": service_level,
            "total_inventory": total_inventory,
            "active_disruptions": len([e for e in self.disruption_events if e.is_active(self.time_step)])
        }
        self.simulation_data.append(step_data)
        
        return step_data
    
    def run_simulation(self, num_steps: int):
        """Run simulation for specified number of steps"""
        print(f"Starting simulation for {num_steps} time steps...")
        
        for step in range(num_steps):
            step_data = self.step()
            if step % 10 == 0:  # Print progress every 10 steps
                print(f"Step {step}: Service Level = {step_data['service_level']:.2%}, "
                      f"Stockouts = {step_data['total_stockout']:.1f}")
        
        print("Simulation completed!")
        return self.simulation_data
    
    def get_simulation_results(self) -> pd.DataFrame:
        """Get simulation results as DataFrame"""
        return pd.DataFrame(self.simulation_data)
    
    def plot_results(self, save_path: str = "simulation_results.png"):
        """Plot simulation results"""
        df = self.get_simulation_results()
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Service Level
        axes[0, 0].plot(df["time_step"], df["service_level"])
        axes[0, 0].set_title("Service Level Over Time")
        axes[0, 0].set_ylabel("Service Level")
        axes[0, 0].grid(True)
        
        # Inventory Levels
        axes[0, 1].plot(df["time_step"], df["total_inventory"])
        axes[0, 1].set_title("Total Inventory Over Time")
        axes[0, 1].set_ylabel("Inventory Units")
        axes[0, 1].grid(True)
        
        # Stockouts
        axes[1, 0].plot(df["time_step"], df["total_stockout"], color="red")
        axes[1, 0].set_title("Stockouts Over Time")
        axes[1, 0].set_ylabel("Stockout Units")
        axes[1, 0].set_xlabel("Time Step")
        axes[1, 0].grid(True)
        
        # Production vs Demand
        axes[1, 1].plot(df["time_step"], df["total_production"], label="Production", color="green")
        axes[1, 1].plot(df["time_step"], df["total_demand"], label="Demand", color="blue")
        axes[1, 1].set_title("Production vs Demand")
        axes[1, 1].set_ylabel("Units")
        axes[1, 1].set_xlabel("Time Step")
        axes[1, 1].legend()
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"Results plotted and saved to {save_path}")

def create_sample_simulation():
    """Create a sample simulation with predefined agents and disruptions"""
    sim = SupplyChainSimulation()
    
    # Add suppliers
    suppliers = [
        SupplierAgent("SUP_001", (0, 0), 200, 0.95),
        SupplierAgent("SUP_002", (10, 5), 150, 0.90),
        SupplierAgent("SUP_003", (5, 10), 180, 0.85)
    ]
    for supplier in suppliers:
        sim.add_supplier(supplier)
    
    # Add distribution centers
    dcs = [
        DistributionCenterAgent("DC_MUMBAI", (20, 20), 500),
        DistributionCenterAgent("DC_DELHI", (25, 30), 400),
        DistributionCenterAgent("DC_BANGALORE", (15, 25), 350),
        DistributionCenterAgent("DC_CHENNAI", (18, 15), 300)
    ]
    for dc in dcs:
        sim.add_distribution_center(dc)
    
    # Add transport agents
    transports = [
        TransportAgent("TRANS_001", (10, 10), 100, 60),
        TransportAgent("TRANS_002", (15, 15), 120, 55),
        TransportAgent("TRANS_003", (12, 18), 80, 65)
    ]
    for transport in transports:
        sim.add_transport_agent(transport)
    
    # Add disruption events
    disruptions = [
        DisruptionEvent("supplier_failure", ["SUP_002"], 30, 10, 0.8),  # Supplier failure at step 30
        DisruptionEvent("transport_delay", ["TRANS_001"], 50, 15, 0.6),  # Transport delay at step 50
        DisruptionEvent("facility_closure", ["DC_MUMBAI"], 70, 5, 1.0)   # DC closure at step 70
    ]
    for disruption in disruptions:
        sim.add_disruption_event(disruption)
    
    return sim

if __name__ == "__main__":
    # Create and run sample simulation
    simulation = create_sample_simulation()
    
    # Run simulation for 100 time steps
    results = simulation.run_simulation(100)
    
    # Plot results
    simulation.plot_results("multi_agent_simulation_results.png")
    
    # Save results to CSV
    df = simulation.get_simulation_results()
    df.to_csv("simulation_results.csv", index=False)
    print("Simulation results saved to simulation_results.csv")
    
    # Print summary statistics
    print("\n=== Simulation Summary ===")
    print(f"Average Service Level: {df['service_level'].mean():.2%}")
    print(f"Total Stockouts: {df['total_stockout'].sum():.1f}")
    print(f"Average Inventory: {df['total_inventory'].mean():.1f}")
    print(f"Disruption Events: {len(simulation.disruption_events)}")

