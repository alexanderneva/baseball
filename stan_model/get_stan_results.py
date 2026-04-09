import pandas as pd
import numpy as np

def extract_stan_results(csv_path):
    # Load the CSV, skipping Stan's header comments
    df = pd.read_csv(csv_path, comment='#')
    
    # Dynamically find all columns that start with 'theta.'
    theta_cols = [col for col in df.columns if 'theta.' in col]
    
    # Calculate summary statistics across all MCMC draws
    results = {
        "means": df[theta_cols].mean().tolist(),
        "lower_ci": df[theta_cols].quantile(0.025).tolist(),
        "upper_ci": df[theta_cols].quantile(0.975).tolist()
    }
    return results

# Example usage to update your plot variables
data = extract_stan_results("summary.csv")
stan_mean = data["means"]
ci_lower = data["lower_ci"]
ci_upper = data["upper_ci"]

