import pandas as pd
import numpy as np

def assign_groups(user_df):
    np.random.seed(42)
    assignments = np.random.choice(['control', 'variant'], size=len(user_df))
    user_df = user_df.copy()
    user_df['group'] = assignments
    return user_df

users = pd.DataFrame({
    'user_id': [101, 102, 103, 104, 105, 106, 107, 108],
    'age': [23, 45, 31, 29, 40, 22, 30, 27],
    'location': ['NY', 'CA', 'TX', 'NY', 'CA', 'TX', 'NY', 'CA']
})

assigned_users = assign_groups(users)
print(assigned_users)
