import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

def simulate_ab_test_data(size_control, size_variant, conv_rate_control, conv_rate_variant, seed=None):
    if seed is not None:
        np.random.seed(seed)
    group = np.array(['control'] * size_control + ['variant'] * size_variant)
    conversion = np.concatenate([
        np.random.binomial(1, conv_rate_control, size_control),
        np.random.binomial(1, conv_rate_variant, size_variant)
    ])
    data = pd.DataFrame({'group': group, 'conversion': conversion})
    return data

def analyze_ab_test(data):
    control = data[data['group'] == 'control']['conversion']
    variant = data[data['group'] == 'variant']['conversion']
    conv_rate_control = control.mean()
    conv_rate_variant = variant.mean()
    diff = conv_rate_variant - conv_rate_control

    # Two-sample z-test for proportions
    n_control = len(control)
    n_variant = len(variant)
    pooled_prob = (control.sum() + variant.sum()) / (n_control + n_variant)
    se = np.sqrt(pooled_prob * (1 - pooled_prob) * (1/n_control + 1/n_variant))
    z_score = diff / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

    # 95% Confidence Interval for the difference in proportions
    se_diff = np.sqrt(
        conv_rate_control * (1 - conv_rate_control) / n_control +
        conv_rate_variant * (1 - conv_rate_variant) / n_variant
    )
    ci_low = diff - 1.96 * se_diff
    ci_high = diff + 1.96 * se_diff

    result = {
        'conv_rate_control': conv_rate_control,
        'conv_rate_variant': conv_rate_variant,
        'difference': diff,
        'z_score': z_score,
        'p_value': p_value,
        'ci_low': ci_low,
        'ci_high': ci_high
    }
    return result

def plot_ab_results(data):
    rates = data.groupby('group')['conversion'].mean()
    errors = data.groupby('group')['conversion'].sem()
    fig, ax = plt.subplots()
    bars = ax.bar(rates.index, rates.values, yerr=errors.values, capsize=8, color=['skyblue', 'salmon'])
    ax.set_ylabel('Conversion Rate')
    ax.set_title('A/B Test Conversion Rates')
    plt.show()

# Simulate data
data = simulate_ab_test_data(
    size_control=1000,
    size_variant=1000,
    conv_rate_control=0.12,
    conv_rate_variant=0.15,
    seed=42
)

# Analyze results
result = analyze_ab_test(data)

# Plot results
plot_ab_results(data)

# Interpretation and Reporting
interpretation = (
    f"Control group conversion rate: {result['conv_rate_control']:.3f}\n"
    f"Variant group conversion rate: {result['conv_rate_variant']:.3f}\n"
    f"Difference: {result['difference']:.3f}\n"
    f"95% Confidence Interval: [{result['ci_low']:.3f}, {result['ci_high']:.3f}]\n"
    f"p-value: {result['p_value']:.4f}\n"
)
print(interpretation)
if result['p_value'] < 0.05:
    conclusion = "The result is statistically significant. The variant outperforms the control."
else:
    conclusion = "The result is not statistically significant. There is no evidence the variant outperforms the control."
print(conclusion)
