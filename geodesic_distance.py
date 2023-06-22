# -*- coding: utf-8 -*-
# This script calculates the geodesic distance between each investigator and each survey area,
# and saves the preferences to a file.
from geopy.distance import geodesic

# Read investigator locations (latitude and longitude) from a file
with open('investigator_locations.txt', 'r') as f:
    investigator_locations = [list(map(float, line.strip().split(','))) for line in f]

# Read survey area locations (latitude and longitude) from a file
with open('survey_area_locations.txt', 'r') as f:
    survey_area_locations = [list(map(float, line.strip().split(','))) for line in f]

# Calculate the geodesic distance between each investigator and each survey area,
# and store the distances in order of increasing distance
preferences = {}
for i, investigator_loc in enumerate(investigator_locations):
    distances = []
    for j, survey_area_loc in enumerate(survey_area_locations):
        distance = geodesic(investigator_loc, survey_area_loc).km
        distances.append((j, distance))
    distances.sort(key=lambda x: x[1])
    preferences[i] = [x[0] for x in distances]

# Save the preferences to a file
with open('preferences.txt', 'w') as f:
    for i, pref in preferences.items():
        f.write(f"{i}:{pref}\n")
