data {
  int<lower=1> N;
  array[N] int<lower=0> K;
  array[N] int<lower=0> y;
}
parameters {
  real<lower=0, upper=1> mu;     
  real<lower=0> kappa;           
  vector<lower=0, upper=1>[N] theta; 
}
model {
  // Priors
  mu ~ beta(2, 8);               // Center around .200
  kappa ~ gamma(1, 0.1);         // Concentration
  
  theta ~ beta(mu * kappa, (1 - mu) * kappa);
  y ~ binomial(K, theta);
}
generated quantities {
  // Prior Predictive Samples
  real mu_prior = beta_rng(2, 8);
  real kappa_prior = gamma_rng(1, 0.1);
  
  array[N] real theta_prior;
  array[N] int y_prior;
  
  for (n in 1:N) {
    theta_prior[n] = beta_rng(mu_prior * kappa_prior, (1 - mu_prior) * kappa_prior);
    y_prior[n] = binomial_rng(K[n], theta_prior[n]);
  }
}

