import pandas as pd

# Read input files
group_and_unit = pd.read_csv('group_and_unit.txt')
lon_and_lat = pd.read_csv('lon_and_lat.txt')

# Merge data
merged_data = pd.merge(group_and_unit, lon_and_lat, on='u', how='left')
merged_data.columns = ['group', 'unit', 'longitude', 'latitude']

# Calculate gravity
merged_data['gravity_lat'] = merged_data.groupby('group')['latitude'].transform('mean')
merged_data['gravity_lon'] = merged_data.groupby('group')['longitude'].transform('mean')

# Write gravity values only on top of the groups
merged_data['gravity_lat'] = merged_data['gravity_lat'].where(merged_data['group'] != merged_data['group'].shift(), '')
merged_data['gravity_lon'] = merged_data['gravity_lon'].where(merged_data['group'] != merged_data['group'].shift(), '')

# Write output file
merged_data.to_csv('gravity.txt', index=False)
