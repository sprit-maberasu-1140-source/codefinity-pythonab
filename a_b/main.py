import pandas as pd
import matplotlib.pyplot as plt

def interpret_ab_results(results_df):
    recommendations = []
    for idx, row in results_df.iterrows():
        p = row['p_value']
        ci_low, ci_high = row['confidence_interval']
        # Recommendation logic
        if p < 0.05:
            if ci_low > 0:
                rec = "Recommend rollout: Statistically significant improvement."
            elif ci_high < 0:
                rec = "Do not rollout: Statistically significant decline."
            else:
                rec = "Statistically significant but effect crosses zero; investigate further."
        else:
            rec = "No statistically significant difference; maintain current version."
        recommendations.append(rec)
    results_df['recommendation'] = recommendations
    return results_df

# Example grid of test results
results_data = {
    "test_scenario": ["Homepage Button", "Signup Flow", "Pricing Page"],
    "p_value": [0.03, 0.21, 0.002],
    "confidence_interval": [(0.01, 0.07), (-0.02, 0.04), (0.03, 0.10)],
    "mean_difference": [0.04, 0.01, 0.065]
}
results_df = pd.DataFrame(results_data)

interpreted_df = interpret_ab_results(results_df)

# Visualization
fig, ax = plt.subplots(figsize=(7, 4))
ax.errorbar(
    x=interpreted_df['test_scenario'],
    y=interpreted_df['mean_difference'],
    yerr=[interpreted_df['mean_difference'] - interpreted_df['confidence_interval'].apply(lambda ci: ci[0]),
          interpreted_df['confidence_interval'].apply(lambda ci: ci[1]) - interpreted_df['mean_difference']],
    fmt='o',
    capsize=8
)
ax.axhline(0, color='gray', linestyle='--', linewidth=1)
ax.set_ylabel("Mean Difference (B - A)")
ax.set_title("A/B Test Result Grid with 95% Confidence Intervals")
plt.show()

for i, row in interpreted_df.iterrows():
    scenario = row['test_scenario']
    rec = row['recommendation']
    print(f"Scenario: {scenario} -> {rec}")
