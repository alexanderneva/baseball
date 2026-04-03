data {
  int<lower=1> N;          // Number of players
  array[N] int<lower=0> K; // Total at-bats per player
  array[N] int<lower=0> y; // Hits per player
}
parameters {
  real<lower=0, upper=1> mu;     // League-wide average batting ability
  real<lower=0> kappa;           // Concentration (how similar players are)
  vector<lower=0, upper=1>[N] theta; // Each player's true batting average
}
model {
  // Hyperpriors for the population
  mu ~ beta(2, 8);               // Prior centered around .200
  kappa ~ gamma(1, 0.1);

  // Hierarchical Prior: theta follows a Beta distribution defined by mu and kappa
  theta ~ beta(mu * kappa, (1 - mu) * kappa);

  // Likelihood: Observed hits come from a Binomial distribution
  y ~ binomial(K, theta);
}

