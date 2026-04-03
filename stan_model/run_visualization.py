import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from get_stan_results import extract_stan_results

output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "efron_plots")
os.makedirs(output_dir, exist_ok=True)


def run_visualization(csv_path, player_names):
    df = pd.read_csv(csv_path, comment="#")

    mu_mean = df["mu"].mean()
    kappa_mean = df["kappa"].mean()

    stan_results = extract_stan_results(csv_path)
    theta_means = np.array(stan_results["means"])
    theta_low = np.array(stan_results["lower_ci"])
    theta_high = np.array(stan_results["upper_ci"])

    plt.figure(figsize=(10, 6))
    y_pos = np.arange(len(player_names))

    plt.errorbar(
        theta_means,
        y_pos,
        xerr=[theta_means - theta_low, theta_high - theta_means],
        fmt="o",
        color="blue",
        label="Individual Player (theta)",
        capsize=5,
    )

    plt.axvline(
        mu_mean,
        color="green",
        linestyle="--",
        alpha=0.6,
        label=f"League Mean (mu): {mu_mean:.3f}",
    )

    plt.yticks(y_pos, player_names)
    plt.xlabel("Estimated Batting Average")
    plt.title(f"Hierarchical Model Results (Kappa: {kappa_mean:.1f})")
    plt.legend()
    plt.grid(axis="x", alpha=0.3)
    plt.tight_layout()

    output_path = os.path.join(output_dir, "hierarchical_model_results.png")
    plt.savefig(output_path, dpi=150)
    print(f"Saved: {output_path}")
    plt.show()


if __name__ == "__main__":
    csv_path = input("Path to CSV: ").strip() or "player_data_results.csv"
    players_input = input(
        "Player names (comma-separated, or press Enter for defaults): "
    ).strip()
    default_players = [
        "Ronald Acuna Jr.",
        "Freddie Freeman",
        "Mookie Betts",
        "Shohei Ohtani",
    ]
    players = (
        [p.strip() for p in players_input.split(",")]
        if players_input
        else default_players
    )
    run_visualization(csv_path, players)
