import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

MODEL_RESULTS = "model_with_prior_results.csv"
OUTPUT_DIR = "../efron_plots"
PLAYER_LABELS = [
    "Mike Trout (LAA)",
    "Freddie Freeman (LAD)",
    "Shohei Ohtani (LAD)",
    "Mookie Betts (LAD)",
]


def plot_comparison():
    df = pd.read_csv(MODEL_RESULTS, comment="#")

    plt.figure(figsize=(10, 6))

    sns.kdeplot(
        df["mu_prior"],
        fill=True,
        color="gray",
        label="Prior",
        alpha=0.3,
    )

    sns.kdeplot(
        df["mu"],
        fill=True,
        color="blue",
        label="Posterior",
        alpha=0.5,
    )

    plt.axvline(
        df["mu"].mean(),
        color="blue",
        linestyle="--",
        label=f"Posterior Mean: {df['mu'].mean():.3f}",
    )

    plt.title("How the MLB Data Updated the League Average (mu)")
    plt.xlabel("Batting Average")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "prior_vs_posterior_mu.png")
    plt.savefig(output_path, dpi=150)
    print(f"Saved: {output_path}")
    plt.close()


if __name__ == "__main__":
    plot_comparison()
