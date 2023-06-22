# -*- coding: utf-8 -*-
import simplekml
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371e3
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

with open('ttc_cycle_pairs.txt') as f:
    ttc_cycle_pairs = [tuple(map(int, line.strip().split(','))) for line in f]
with open('investigator_locations.txt') as f:
    investigator_locations = [tuple(map(float, line.strip().split(','))) for line in f]
with open('survey_area_locations.txt') as f:
    survey_area_locations = [tuple(map(float, line.strip().split(','))) for line in f]

# KML
kml = simplekml.Kml()
for ttc, cycle in ttc_cycle_pairs:
    lat, lon = investigator_locations[ttc]
    lat2, lon2 = survey_area_locations[cycle]
    pnt = kml.newpoint(name=f'investigator{ttc}', coords=[(lon, lat)])
    pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/man.png'
    pnt = kml.newpoint(name=f'survey_area{cycle}', coords=[(lon2, lat2)])
    pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
    line = kml.newlinestring(coords=[(lon, lat), (lon2, lat2)])
    
    distance = haversine(lat, lon, lat2, lon2)
    
    if distance >= 9000:
        line.style.linestyle.color = simplekml.Color.red
        line.description = f"Distance: {distance:.0f}m (>=9000m)"
    elif distance >= 5000:
        line.style.linestyle.color = simplekml.Color.orange
        line.description = f"Distance: {distance:.0f}m (>=5000m)"
    else:
        line.description = f"Distance: {distance:.0f}m"

kml.save('investigators_and_survey_areas_map.kml')
