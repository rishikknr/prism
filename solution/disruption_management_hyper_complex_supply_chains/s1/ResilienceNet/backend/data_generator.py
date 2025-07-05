
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_supply_chain_data(num_days=365, num_products=10, num_dcs=3, num_stores=10):
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(num_days)]

    data = []
    for date in dates:
        for product_id in range(num_products):
            for dc_id in range(num_dcs):
                # Simulate inventory levels
                inventory = np.random.randint(100, 1000)
                # Simulate demand
                demand = np.random.randint(50, 200)
                # Simulate lead time (days)
                lead_time = np.random.randint(1, 10)
                # Simulate cost
                cost = np.random.uniform(10, 100)
                # Simulate supplier performance (0-100)
                supplier_performance = np.random.randint(70, 100)

                data.append({
                    'date': date,
                    'product_id': f'PROD_{product_id}',
                    'dc_id': f'DC_{dc_id}',
                    'inventory': inventory,
                    'demand': demand,
                    'lead_time': lead_time,
                    'cost': cost,
                    'supplier_performance': supplier_performance
                })

    df = pd.DataFrame(data)

    # Add some anomalies for demonstration
    # Simulate a cost spike for a specific product/DC around a certain date
    anomaly_date = datetime(2024, 6, 15)
    df.loc[(df['date'] > anomaly_date - timedelta(days=5)) & 
           (df['date'] < anomaly_date + timedelta(days=5)) & 
           (df['product_id'] == 'PROD_0') & 
           (df['dc_id'] == 'DC_0'), 'cost'] *= 1.5

    # Simulate a sudden drop in supplier performance
    df.loc[(df['date'] > anomaly_date - timedelta(days=5)) & 
           (df['date'] < anomaly_date + timedelta(days=5)) & 
           (df['product_id'] == 'PROD_1') & 
           (df['dc_id'] == 'DC_1'), 'supplier_performance'] *= 0.5

    return df

if __name__ == '__main__':
    df = generate_supply_chain_data()
    print(df.head())
    print(df.describe())
    df.to_csv('simulated_supply_chain_data.csv', index=False)
    print("Simulated data saved to simulated_supply_chain_data.csv")


