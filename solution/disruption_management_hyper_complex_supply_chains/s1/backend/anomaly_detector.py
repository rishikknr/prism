
import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

def detect_anomalies(df):
    # For simplicity, we'll focus on 'cost' and 'supplier_performance' for anomaly detection
    # In a real scenario, this would be more sophisticated, considering multiple features

    # Anomaly detection for 'cost'
    model_cost = IsolationForest(random_state=42, contamination=0.01) # contamination is the proportion of outliers in the data set
    df["anomaly_cost"] = model_cost.fit_predict(df[["cost"]])
    df["anomaly_cost_score"] = model_cost.decision_function(df[["cost"]])

    # Anomaly detection for 'supplier_performance'
    model_supplier = IsolationForest(random_state=42, contamination=0.01)
    df["anomaly_supplier"] = model_supplier.fit_predict(df[["supplier_performance"]])
    df["anomaly_supplier_score"] = model_supplier.decision_function(df[["supplier_performance"]])

    return df

def visualize_anomalies(df, feature, anomaly_column, score_column):
    plt.figure(figsize=(15, 7))
    plt.plot(df["date"], df[feature], label=feature)
    anomalies = df[df[anomaly_column] == -1]
    plt.scatter(anomalies["date"], anomalies[feature], color='red', label='Anomaly')
    plt.title(f'Anomaly Detection for {feature}')
    plt.xlabel('Date')
    plt.ylabel(feature)
    plt.legend()
    plt.grid(True)
    plt.savefig(f'anomaly_detection_{feature}.png')
    plt.close()

    plt.figure(figsize=(15, 7))
    plt.scatter(df["date"], df[score_column], c=df[anomaly_column], cmap='coolwarm')
    plt.title(f'Anomaly Score for {feature}')
    plt.xlabel('Date')
    plt.ylabel('Anomaly Score')
    plt.colorbar(label='Anomaly (-1) / Normal (1)')
    plt.grid(True)
    plt.savefig(f'anomaly_score_{feature}.png')
    plt.close()

if __name__ == '__main__':
    df = pd.read_csv('simulated_supply_chain_data.csv')
    df["date"] = pd.to_datetime(df["date"])

    df_anomalies = detect_anomalies(df.copy())

    print("Anomalies in cost:")
    print(df_anomalies[df_anomalies["anomaly_cost"] == -1].head())

    print("Anomalies in supplier performance:")
    print(df_anomalies[df_anomalies["anomaly_supplier"] == -1].head())

    visualize_anomalies(df_anomalies, 'cost', 'anomaly_cost', 'anomaly_cost_score')
    visualize_anomalies(df_anomalies, 'supplier_performance', 'anomaly_supplier', 'anomaly_supplier_score')

    df_anomalies.to_csv('simulated_supply_chain_data_with_anomalies.csv', index=False)
    print("Simulated data with anomalies saved to simulated_supply_chain_data_with_anomalies.csv")


