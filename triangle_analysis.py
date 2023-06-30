# -*- coding: utf-8 -*-
import random
from math import radians, sin, cos, sqrt, atan2, acos, degrees
from simplekml import Kml

def distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def angle(a,b,c):
    ab=distance(*a,*b)
    bc=distance(*b,*c)
    ac=distance(*a,*c)
    
    if ab==0 or bc==0 or ac==0:
        return 0
    
    angle_b=degrees(acos((ab**2+bc**2-ac**2)/(2*ab*bc)))
    angle_c=degrees(acos((ac**2+bc**2-ab**2)/(2*ac*bc)))
    angle_a=degrees(acos((ab**2+ac**2-bc**2)/(2*ab*ac)))
    
    return min(angle_a , angle_b , angle_c)

def centroid(a,b,c):
    lat=(a[0]+b[0]+c[0])/3
    lon=(a[1]+b[1]+c[1])/3
    return lat , lon

def area(a,b,c):
    ab=distance(*a,*b)
    bc=distance(*b,*c)
    ac=distance(*a,*c)
    
    s=(ab+bc+ac)/2
    
    return sqrt(s*(s-ab)*(s-bc)*(s-ac))

def max_side_length(a,b,c):
    ab=distance(*a,*b)
    bc=distance(*b,*c)
    ac=distance(*a,*c)
    
    return max(ab,bc,ac)

def is_sliver(a,b,c):
    
    if angle(a,b,c)<10:
        return True
    
    return False

def process_data():
    
    with open('original_survey_area_locations.txt','r') as f:
        data = []
        data_dict = {}
        for i, line in enumerate(f):
            if not line.startswith('x'):
                point = tuple(map(float, line.strip().split(',')))
                data.append(point)
                data_dict[point] = i + 1
    
    best_groups=[]
    best_discarded_points=[]
    
    min_sliver_count=float('inf')
    min_area_sum=float('inf')
    min_max_side_length=float('inf')
    
    for _ in range(10):
        
        groups=[]
        discarded_points=[]
        data_copy=data[:]
        
        while data_copy:
            point_a=random.choice(data_copy)
            data_copy.remove(point_a)
            distances=sorted([(distance(point_a[0],point_a[1],point[0],point[1]),point) for point in data_copy])
            
            if not distances or distances[0][0]>2:
                discarded_points.append(point_a)
                continue
            
            point_b=distances.pop(0)[1]
            data_copy.remove(point_b)
            
            if not distances or distances[0][0]>2:
                discarded_points.append(point_a)
                discarded_points.append(point_b)
                continue
            
            point_c=distances.pop(0)[1]
            data_copy.remove(point_c)
            
            if angle(point_a , point_b , point_c)<0:
                discarded_points.extend([point_a , point_b , point_c])
                continue
            
            if area(point_a , point_b , point_c)>340000:
                discarded_points.extend([point_a , point_b , point_c])
                continue
            
            if max_side_length(point_a , point_b , point_c)>1.8:
                discarded_points.extend([point_a , point_b , point_c])
                continue
            
            groups.append((point_a , point_b , point_c))
        
        sliver_count=sum(is_sliver(*group) for group in groups)
        area_sum=sum(area(*group) for group in groups)
        max_side_length_group=max(max_side_length(*group) for group in groups)
        
        if sliver_count<min_sliver_count and area_sum<min_area_sum and max_side_length_group<min_max_side_length:
            min_sliver_count=sliver_count
            min_area_sum=area_sum
            min_max_side_length=max_side_length_group
            best_groups=groups
            best_discarded_points=discarded_points
    
    kml=Kml()
    
    for i , group in enumerate(best_groups):
        coords=[(point[1],point[0]) for point in group]
        pol=kml.newpolygon(name=f'Group {i+1}',outerboundaryis=coords)
        pol.style.polystyle.color='7dff0000'
        description=f'G{i+1}\n'
        description+=f'A: {data_dict[group[0]]}\n'
        description+=f'B: {data_dict[group[1]]}\n'
        description+=f'C: {data_dict[group[2]]}\n'
        pol.description=description
    
    for point in best_discarded_points:
        pnt=kml.newpoint(coords=[(point[1],point[0])])
        pnt.description=f'Line {data_dict[point]}'
    
    kml.save('triangles.kml')
    
    with open('groups.txt','w') as f:
        for i , group in enumerate(best_groups):
            gravity=centroid(*group)
            f.write(f'{i+1}, {gravity[0]}, {gravity[1]}, {data_dict[group[0]]}, {data_dict[group[1]]}, {data_dict[group[2]]}\n')
    print(f'Number of triangles: {len(best_groups)}')

process_data()
