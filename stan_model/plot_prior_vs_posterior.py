import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "efron_plots")
os.makedirs(output_dir, exist_ok=True)


def plot_comparison():
    csv_path = (
        input("Path to CSV [model_with_prior_results.csv]: ").strip()
        or "model_with_prior_results.csv"
    )
    df = pd.read_csv(csv_path, comment="#")

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

    output_path = os.path.join(output_dir, "prior_vs_posterior_mu.png")
    plt.savefig(output_path, dpi=150)
    print(f"Saved: {output_path}")
    plt.show()


if __name__ == "__main__":
    plot_comparison()
