import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run_visualization(csv_path, player_names):
    # 1. Load data, skipping Stan's comment lines
    df = pd.read_csv(csv_path, comment='#')

    # 2. Extract specific parameters
    # mu and kappa are scalars, theta is a vector (theta.1, theta.2...)
    mu_mean = df['mu'].mean()
    kappa_mean = df['kappa'].mean()
    
    theta_cols = [col for col in df.columns if col.startswith('theta.')]
    theta_means = df[theta_cols].mean().values
    theta_low = df[theta_cols].quantile(0.025).values
    theta_high = df[theta_cols].quantile(0.975).values

    # 3. Create the Plot
    plt.figure(figsize=(10, 6))
    y_pos = np.arange(len(player_names))

    # Plot Stan Estimates (Theta)
    plt.errorbar(theta_means, y_pos, 
                 xerr=[theta_means - theta_low, theta_high - theta_means],
                 fmt='o', color='blue', label='Individual Player (theta)', capsize=5)

    # Plot the Population Mean (Mu) as a vertical dashed line
    plt.axvline(mu_mean, color='green', linestyle='--', alpha=0.6, 
                label=f'League Mean (mu): {mu_mean:.3f}')

    # Formatting
    plt.yticks(y_pos, player_names)
    plt.xlabel('Estimated Batting Average')
    plt.title(f'Hierarchical Model Results (Kappa: {kappa_mean:.1f})')
    plt.legend()
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Ensure this matches the names used in your get_mlb_data.py
    players = ["Mike Trout", "Aaron Judge", "Shohei Ohtani", "Mookie Betts"]
    run_visualization('test.csv', players)

