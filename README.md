# Bayesian Hierarchical Modeling in Baseball

This project implements a Bayesian hierarchical model for estimating baseball batting averages, based on the Efron-Morris methodology. The goal is to address the challenge of small sample sizes by applying shrinkage estimation—pulling extreme observations toward the population mean.

## Overview

The model uses a Beta-Binomial hierarchical structure:
- `y_i ~ Binomial(K_i, theta_i)` — observed hits given at-bats
- `theta_i ~ Beta(mu * kappa, (1 - mu) * kappa)` — player ability
- `mu ~ Beta(2, 8)` — league average prior
- `kappa ~ Gamma(1, 0.1)` — concentration parameter

The concentration parameter `kappa` controls shrinkage strength: larger values mean more shrinkage toward the population mean.

## Implementation Options

### Stan Models

For the Stan implementation with full Bayesian inference, see [stan_model/README.md](stan_model/README.md).

### PyMC Alternative

For a Python-native implementation using PyMC, see `efronmorris_cleaned.ipynb`.

Note: The notebook uses [ArviZ](https://arviz-devs.github.io/ArviZ/) for visualization of prior/posterior distributions and credible intervals.

## Results

The model successfully estimates all parameters:
- Posterior `mu` (league average): ~0.269
- Posterior `kappa` (concentration): ~24.8

The increase in `kappa` from prior (~10) to posterior (~25) indicates strong shrinkage—players with extreme batting averages are pulled toward the population mean, with more shrinkage applied to players with smaller sample sizes.



## Part B 
### HMC to predicting batting average

This part of the project is made up of 3 files

1. Final_AVG_Model.ipynb - This is the final iteration of our modelling process. The script:
  - Calls data from pybaseball
  - Constructs and filters the dataset into a training and validation set
  - Runs the PyMC model
  - Analyzes prior and posterior distributions
  - Explores validation using 2025 averages
  - Plots visualizations and investigates model performance metrics
  - Conducts residual analysis of model predictions
  - 
2. 2026_Predictive_Model.ipynb - is a modified version of Final_AVG_Model.ipynb. Some unnecessary components were trimmed out. It also contains an additional function "get_AVG(player_name)" which pulls any available player from the dataset and prints their predicted 2026 average. It also contains an analysis of the players with the greatest estimated change in average between 2025 and 2026.

3. FeatureSelection_LOOCV.v2.ipynb - is the final version of our Leave One Out Cross Validation for feature selection. The script:
  - Calls data from pybaseball
  - Constructs and filters the dataset into a training and validation set
  - Checks the correlation between all features of interest
  - Defines a large sample of different feature combinations
  - Runs the model with each different set of features
  - Prints a table and plot indicating which feature sets performed the best using az.compare()






