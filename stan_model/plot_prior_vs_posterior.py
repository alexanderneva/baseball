import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_comparison():
    # 1. Load the data (skipping Stan comments)
    prior_df = pd.read_csv('prior_results.csv', comment='#')
    post_df = pd.read_csv('results.csv', comment='#')

    plt.figure(figsize=(10, 6))

    # 2. Plot the Prior Distribution of Mu
    sns.kdeplot(prior_df['mu_prior'], fill=True, color="gray", 
                label='Prior (Initial Guess)', alpha=0.3)

    # 3. Plot the Posterior Distribution of Mu
    sns.kdeplot(post_df['mu'], fill=True, color="blue", 
                label='Posterior (After MLB Data)', alpha=0.5)

    # 4. Formatting
    plt.axvline(post_df['mu'].mean(), color='blue', linestyle='--', 
                label=f'Posterior Mean: {post_df["mu"].mean():.3f}')
    
    plt.title("How the MLB Data Updated the League Average ($\mu$)")
    plt.xlabel("Batting Average")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_comparison()

