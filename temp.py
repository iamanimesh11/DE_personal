s ="2025-03-04 20:56:03,188 - ERROR - error creating index ' traffic_Data_road_id_idx' : relation \"traffic_data_road_id_idx\" already exists"
import re
x=s.split(" - ")[-3]  # Get JSON string\
print(x)