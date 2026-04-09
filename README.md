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

## Results

The model successfully estimates all parameters:
- Posterior `mu` (league average): ~0.269
- Posterior `kappa` (concentration): ~24.8

The increase in `kappa` from prior (~10) to posterior (~25) indicates strong shrinkage—players with extreme batting averages are pulled toward the population mean, with more shrinkage applied to players with smaller sample sizes.