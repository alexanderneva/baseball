import matplotlib.pyplot as plt
import numpy as np

# Example data - Replace these with your actual model outputs
players = ['Mike Trout', 'Aaron Judge', 'Shohei Ohtani', 'Mookie Betts']
raw_avg = [0.263, 0.267, 0.304, 0.307]  # Raw H/AB
stan_mean = [0.272, 0.274, 0.298, 0.301] # Model estimated means
ci_lower = [0.245, 0.248, 0.275, 0.278] # 95% CI lower bounds
ci_upper = [0.301, 0.303, 0.322, 0.325] # 95% CI upper bounds

def plot_batting_shrinkage():
    plt.figure(figsize=(10, 6))
    y_pos = np.arange(len(players))

    # 1. Plot raw averages as red dots
    plt.scatter(raw_avg, y_pos, color='red', label='Raw Average (H/AB)', zorder=3)

    # 2. Plot Stan estimates with 95% CI error bars
    xerr = [np.array(stan_mean) - np.array(ci_lower), 
            np.array(ci_upper) - np.array(stan_mean)]
    plt.errorbar(stan_mean, y_pos, xerr=xerr, fmt='o', color='blue', 
                 label='Stan Estimate (95% CI)', capsize=5)

    # Styling the plot
    plt.yticks(y_pos, players)
    plt.xlabel('Batting Average')
    plt.title('Shrinkage: Raw vs. Stan Estimated Batting Averages')
    plt.legend()
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Use plt.show() to open an interactive window or plt.savefig() for a file
    plt.show() 

if __name__ == "__main__":
    plot_batting_shrinkage()

