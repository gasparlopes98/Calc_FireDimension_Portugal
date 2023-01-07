import json
import geopy.distance
json_location = "../file_info/locations.json"
info_location = "../file_info/distance_matrix.txt"


def generate():
   json_content = get_json_contents()
   distance_matrix = []
   for zone in json_content:
    temp = []
    
    coords_1 = (zone['latitude'],zone["longitude"])
    for zone2 in json_content:
        coords_2 = (zone2['latitude'],zone2["longitude"])
        temp.append(geopy.distance.geodesic(coords_1,coords_2).kilometers)
    distance_matrix.append(temp)
   write_to_file(distance_matrix)
     

def get_json_contents():
    with open(json_location, 'r') as j:
     return json.loads(j.read())

def write_to_file(info_matrix):
    f = open(info_location,"w")
    for line in info_matrix:
        for item in line:
            f.write(str(item))
            f.write(',')
        f.write('\n')
    f.close()        


generate()
