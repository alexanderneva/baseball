# Stan Model for Bayesian Hierarchical Batting Averages

This directory contains the Stan implementations of the Beta-Binomial hierarchical model for estimating baseball batting averages.

## Installation

1. Download and install CmdStan from https://mc-stan.org/install/
2. Clone this repository into your CmdStan directory:

```bash
# From your CmdStan directory (e.g., cmdstan-2.37.0)
git clone https://github.com/your-repo/stan_model.git
```

## Dependencies

This project uses [uv](https://github.com/astral-sh/uv) for dependency management:

```bash
uv sync
```

For other package managers, use `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Stan Model Files

The Stan model files are located in:

```
stan_model/stan_model_files/
├── model.stan              # Basic hierarchical model (posterior only)
└── model_with_prior.stan  # Includes prior predictive sampling
```

## Compiling the Models

From your CmdStan directory:

```bash
# Compile the basic hierarchical model
make stan_model/stan_model_files/model

# Compile the model with prior predictive sampling
make stan_model/stan_model_files/model_with_prior
```

Enable threading for larger datasets:

```bash
make STAN_THREADS=true stan_model/stan_model_files/model
make STAN_THREADS=true stan_model/stan_model_files/model_with_prior
```

## Data Preparation

The script `get_mlb_data.py` fetches player statistics from the MLB Stats API and generates the JSON input file:

```bash
cd stan_model
python get_mlb_data.py
```

This produces `player_data.json` with the following format:

```json
{
  "N": 4,
  "K": [456, 556, 611, 589],
  "y": [106, 164, 172, 152]
}
```

Where:
- `N`: Number of players
- `K`: Array of at-bats for each player
- `y`: Array of hits for each player

## Running the Models

From your CmdStan directory (where the compiled binaries are located):

```bash
# Basic model - for shrinkage plots
./model sample data file=stan_model/player_data.json output file=output.csv

# With prior predictive sampling - for prior vs posterior plots
./model_with_prior sample data file=stan_model/player_data.json output file=output.csv
```

Rename the output to match the expected CSV filename for the visualization scripts:

```bash
# If using model.stan (for shrinkage plots):
mv output.csv stan_model/model_results.csv

# If using model_with_prior.stan (for prior vs posterior plots):
mv output.csv stan_model/model_with_prior_results.csv
```

## Analyzing Results

### Using stansummary

For multiple chains, run:

```bash
./model num_chains=4 sample data file=stan_model/player_data.json output file=output.csv
```

Generate summary statistics across all chains:

```bash
./bin/stansummary output_* > summary.txt
cat summary.txt
```

Export as CSV:

```bash
./bin/stansummary output_*.csv -c summary.csv
```

Note: The visualization scripts are currently set up for single chain - you will need to concatenate the chain outputs into a single CSV first (e.g., `cat output_*.csv > combined.csv`).

### Visualization Scripts

The repository includes Python scripts for visualizing results (run from `stan_model/` directory):

| Script | Use With | Expected CSV |
|--------|---------|------------|
| `test_shrinkage.py` | `model.stan` | `model_results.csv` |
| `plot_prior_vs_posterior.py` | `model_with_prior.stan` | `model_with_prior_results.csv` |
| `plot_prior_vs_posterior_2.py` | `model_with_prior.stan` | `model_with_prior_results.csv` |

Running the scripts:

```bash
cd stan_model
python plot_prior_vs_posterior.py
python plot_prior_vs_posterior_2.py
python test_shrinkage.py
```

Plots are saved to `report/efron_plots/`.

Note: This directory also contains plots from the PyMC notebook (`efron_plot_*.png`).

## Results

The model successfully estimates all parameters:
- Posterior `mu` (league average): ~0.269
- Posterior `kappa` (concentration): ~24.8

The increase in `kappa` from prior (~10) to posterior (~25) indicates strong shrinkage—players with extreme batting averages are pulled toward the population mean, with more shrinkage applied to players with smaller sample sizes.