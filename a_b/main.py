def classify_ab_test_outcome(true_effect, observed_significance):
    if true_effect and observed_significance:
        return "Correct Decision"
    elif not true_effect and not observed_significance:
        return "Correct Decision"
    elif not true_effect and observed_significance:
        return "Type I Error"
    elif true_effect and not observed_significance:
        return "Type II Error"

# Sample calls
outcome1 = classify_ab_test_outcome(True, True)
outcome2 = classify_ab_test_outcome(False, False)
outcome3 = classify_ab_test_outcome(False, True)
outcome4 = classify_ab_test_outcome(True, False)

print(outcome1)
print(outcome2)
print(outcome3)
print(outcome4)
