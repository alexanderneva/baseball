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


def plot_parameter_update(param_name, df, player_labels=None):
    prior_col = f"{param_name}_prior"

    plt.figure(figsize=(10, 6))

    sns.kdeplot(
        df[prior_col],
        fill=True,
        color="gray",
        label=f"Prior {param_name}",
        alpha=0.3,
    )
    sns.kdeplot(
        df[param_name],
        fill=True,
        color="blue",
        label=f"Posterior {param_name}",
        alpha=0.5,
    )

    post_mean = df[param_name].mean()
    plt.axvline(
        post_mean, color="blue", linestyle="--", label=f"Post. Mean: {post_mean:.3f}"
    )

    plt.title(f"Bayesian Update: Prior vs. Posterior for {param_name}")
    plt.xlabel("Value")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, f"prior_vs_posterior_{param_name}.png")
    plt.savefig(output_path, dpi=150)
    print(f"Saved: {output_path}")
    plt.close()


def plot_theta_prior_posterior(df, player_labels):
    """Plot prior vs posterior for individual player thetas"""
    theta_cols = [col for col in df.columns if col.startswith("theta.")]
    prior_cols = [col for col in df.columns if col.startswith("theta_prior.")]

    n_players = len(theta_cols)
    fig, axes = plt.subplots(1, n_players, figsize=(4 * n_players, 5))

    if n_players == 1:
        axes = [axes]

    for i, (theta_col, prior_col) in enumerate(zip(theta_cols, prior_cols)):
        ax = axes[i]

        sns.kdeplot(
            df[prior_col],
            ax=ax,
            fill=True,
            color="gray",
            label="Prior",
            alpha=0.3,
        )
        sns.kdeplot(
            df[theta_col],
            ax=ax,
            fill=True,
            color="blue",
            label="Posterior",
            alpha=0.5,
        )

        post_mean = df[theta_col].mean()
        ax.axvline(post_mean, color="blue", linestyle="--", label=f"{post_mean:.3f}")

        ax.set_title(player_labels[i])
        ax.set_xlabel("Batting Average")
        ax.set_ylabel("Density")
        ax.legend(fontsize=8)
        ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "prior_vs_posterior_theta.png")
    plt.savefig(output_path, dpi=150)
    print(f"Saved: {output_path}")
    plt.close()


if __name__ == "__main__":
    df = pd.read_csv(MODEL_RESULTS, comment="#")

    plot_parameter_update("mu", df)
    plot_parameter_update("kappa", df)
    plot_theta_prior_posterior(df, PLAYER_LABELS)

    print("\nAll plots generated successfully!")
