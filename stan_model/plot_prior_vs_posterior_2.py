import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_parameter_update(param_name):
    """
    Compares prior vs posterior for a given parameter.
    param_name: 'mu' or 'kappa'
    """
    # 1. Load data
    prior_df = pd.read_csv('test.csv', comment='#')
    post_df = pd.read_csv('results.csv', comment='#')

    # 2. Map the prior column name (Stan appends _prior in our generated quantities)
    prior_col = f"{param_name}_prior"
    
    plt.figure(figsize=(10, 6))

    # 3. Plot Densities
    sns.kdeplot(prior_df[prior_col], fill=True, color="gray", label=f'Prior {param_name}', alpha=0.3)
    sns.kdeplot(post_df[param_name], fill=True, color="blue", label=f'Posterior {param_name}', alpha=0.5)

    # 4. Add a vertical line for the posterior mean
    post_mean = post_df[param_name].mean()
    plt.axvline(post_mean, color='blue', linestyle='--', label=f'Post. Mean: {post_mean:.3f}')

    # 5. Dynamic Titles/Labels
    plt.title(f"Bayesian Update: Prior vs. Posterior for {param_name}")
    plt.xlabel("Value")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Choose which one to see, or call both!
    choice = input("Which parameter to plot? (mu/kappa): ").strip().lower()
    if choice in ['mu', 'kappa']:
        plot_parameter_update(choice)
    else:
        print("Invalid choice. Please pick 'mu' or 'kappa'.")

