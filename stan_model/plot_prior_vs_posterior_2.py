import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "efron_plots")
os.makedirs(output_dir, exist_ok=True)


def plot_parameter_update(param_name, df):
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

    output_path = os.path.join(output_dir, f"prior_vs_posterior_{param_name}.png")
    plt.savefig(output_path, dpi=150)
    print(f"Saved: {output_path}")
    plt.show()


if __name__ == "__main__":
    csv_path = (
        input("Path to CSV [model_with_prior_results.csv]: ").strip()
        or "model_with_prior_results.csv"
    )
    df = pd.read_csv(csv_path, comment="#")

    plot_parameter_update("mu", df)
    plot_parameter_update("kappa", df)
