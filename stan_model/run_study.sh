#!/bin/bash

# Stan Model Workflow for Baseball Batting Average Estimation
# Run from stan_model directory: ./run_study.sh

echo "=== Baseball Hierarchical Model Pipeline ==="
echo ""

# 1. Fetch MLB data from parent directory
echo "1. Fetching MLB data..."
uv run python get_mlb_data.py
echo "   -> Saved to player_data.json"

# 2. Use pre-compiled models from bin/
echo ""
echo "2. Using pre-compiled Stan models from bin/"

# 3. Choose model
echo ""
echo "3. Select model to run:"
echo "   1) model (basic hierarchical)"
echo "   2) model_with_prior (includes prior predictive sampling)"
read -p "Enter choice [1/2]: " choice

case $choice in
  1)
    MODEL="./bin/model"
    OUTPUT="model_results.csv"
    ;;
  2)
    MODEL="./bin/model_with_prior"
    OUTPUT="model_with_prior_results.csv"
    ;;
  *)
    echo "Invalid choice. Running basic model."
    MODEL="./bin/model"
    OUTPUT="model_results.csv"
    ;;
esac

# 4. Run the model
echo ""
echo "4. Running Stan model..."
$MODEL sample data file=player_data.json output file=$OUTPUT

# 5. Generate summary
echo ""
echo "5. Generating model summary..."
SUMMARY="${OUTPUT%.csv}_summary.txt"
./bin/stansummary $OUTPUT --sig_figs=3 > "$SUMMARY"
echo "   -> Saved to $SUMMARY"

echo ""
echo "=== Pipeline complete ==="
echo "Output files:"
echo "  - $OUTPUT"
echo "  - $SUMMARY"
echo ""
echo "To visualize:"
echo "  uv run python run_visualization.py"
echo "  (Use $OUTPUT when prompted for CSV path)"
echo ""
if [ "$OUTPUT" = "model_with_prior_results.csv" ]; then
    echo "To visualize prior vs posterior:"
    echo "  uv run python plot_prior_vs_posterior.py"
    echo "  uv run python plot_prior_vs_posterior_2.py"
    echo ""
fi
echo "Plots are saved to: ../efron_plots/"
