#!/bin/bash

# 1. Run the Python script to fetch the latest MLB data
echo "Fetching MLB data..."
uv run get_mlb_data.py

# 2. Check if data.json was created successfully
if [ ! -f "data.json" ]; then
    echo "Error: data.json not found!"
    exit 1
fi

# 3. Compile the Stan model (if not already compiled)
# Replace 'batting_model' with your actual .stan filename
echo "Compiling Stan model..."
make batting_model

# 4. Run the model using the generated JSON data
echo "Running Stan MCMC sampling..."
./batting_model sample data file=data.json output file=results.csv

echo "Study complete. Results saved to results.csv."

# 5. Visualize the results
echo "Generating visualization..."
python3 visualize_results.py

echo "Running Prior Predictive Check..."
./batting_model sample algorithm=fixed_param data file=data.json output file=prior_results.csv

# Optional: Run a quick summary to see the range of mu_prior
bin/stansummary prior_results.csv --sig_figs 3 | grep "mu_prior"

python3 plot_prior_vs_posterior.py


