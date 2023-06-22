# survey_area_allocation
Assign surveyors to survey areas based on selection.

## geodesic_distance.py
The script calculates the geodetic distance between each surveyor and each survey area and stores provisional preferences on file, under the assumption that surveyors prefer the survey area to be closer to their homes.

### Constraints
* Both input files are two-column CSVs with comma-separated latitude and longitude.
* The number of rows in both input files must match.
* It may be necessary to make adjustments, such as grouping the number of survey areas to match the number of surveyors.

## ttc.py
Allocates surveyors to survey areas based on TTC algorithm.

## cycle_pairs.py
Rewrites the circulation of the innermost list into a representation of two pairs.

## map_investigators_and_survey_areas.py
Reads data from three text files, `ttc_cycle_pairs.txt`, `investigator_locations.txt`, and `survey_area_locations.txt`, and create a KML file. The KML file displays surveyors and survey areas on a map, with lines connecting corresponding surveyors and survey areas. The lines are color-coded based on the distance between them.
