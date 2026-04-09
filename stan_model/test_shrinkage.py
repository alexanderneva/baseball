# Shrinkage plot to be used with model.stan
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os

MODEL_RESULTS = "model_results.csv"
MLB_DATA = "../2018_2025.csv"
OUTPUT_DIR = "../efron_plots"

PLAYER_NAMES = ["Mike Trout", "Freddie Freeman", "Shohei Ohtani", "Mookie Betts"]


def load_stan_results(csv_path):
    return pd.read_csv(csv_path, comment="#")


def get_theta_columns(df):
    return [col for col in df.columns if col.startswith("theta.")]


def calculate_posterior_stats(df, theta_cols):
    means = df[theta_cols].mean()
    lower = df[theta_cols].quantile(0.025)
    upper = df[theta_cols].quantile(0.975)
    return means, lower, upper


def load_player_data_from_csv(csv_path, player_names):
    """Load player stats from MLB CSV data for 2025 season"""
    df = pd.read_csv(csv_path, index_col="Name")

    y = []
    K = []
    player_labels = []

    for name in player_names:
        # Find player in 2025 data
        data_2025 = df[(df["Season"] == 2025) & (df.index == name)]
        if len(data_2025) > 0:
            row = data_2025.iloc[0]
            y.append(row["H"])
            K.append(row["AB"])
            # Format: "Player (TEAM)"
            player_labels.append(f"{name} ({row['Team']})")
        else:
            print(f"Warning: {name} not found in 2025 data")
            continue

    return y, K, player_labels


def plot_batting_shrinkage():
    stan_df = load_stan_results(MODEL_RESULTS)
    theta_cols = get_theta_columns(stan_df)
    n_players = len(theta_cols)

    # Use only the player names we have theta for
    player_names = PLAYER_NAMES[:n_players]

    # Load raw data from CSV
    y, K, player_labels = load_player_data_from_csv(MLB_DATA, player_names)

    theta_means, theta_lower, theta_upper = calculate_posterior_stats(
        stan_df, theta_cols
    )

    raw_avgs = np.array(y) / np.array(K)

    mu_mean = stan_df["mu"].mean()

    plt.figure(figsize=(10, 6))
    y_pos = np.arange(n_players)

    plt.scatter(
        raw_avgs, y_pos, color="red", label="Observed (H/AB)", alpha=0.6, zorder=3
    )

    xerr = [
        theta_means.values - theta_lower.values,
        theta_upper.values - theta_means.values,
    ]
    plt.errorbar(
        theta_means.values,
        y_pos,
        xerr=xerr,
        fmt="o",
        color="blue",
        label="Posterior (theta)",
        capsize=5,
    )

    plt.axvline(
        mu_mean, color="black", linestyle="--", label=f"Population Mean: {mu_mean:.3f}"
    )

    for i in range(n_players):
        plt.arrow(
            raw_avgs[i],
            i,
            theta_means.values[i] - raw_avgs[i],
            0,
            head_width=0.003,
            head_length=0.005,
            fc="gray",
            ec="gray",
            alpha=0.4,
        )

    plt.yticks(y_pos, player_labels)
    plt.xlabel("Batting Average")
    plt.title("Efron-Morris: Posterior Shrinkage toward the Mean")
    plt.legend()
    plt.grid(axis="x", alpha=0.3)
    plt.tight_layout()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.savefig(os.path.join(OUTPUT_DIR, "batting_shrinkage.png"), dpi=150)
    print(f"Saved: {OUTPUT_DIR}/batting_shrinkage.png")
    plt.show()


if __name__ == "__main__":
    plot_batting_shrinkage()
