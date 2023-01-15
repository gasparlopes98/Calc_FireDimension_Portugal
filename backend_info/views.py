from django.http import HttpResponse
from .calculate_info import get_info, calculate_index_for_city
from rest_framework.decorators import api_view
from .decision_algorithm.process import process_info,get_needed_resources,calculate_distance_traveled
from .decision_algorithm.optimization_modi import modi_optimization
from .prev_connection_layer import get_severity
import json
import random


district = {}

@api_view(['GET', 'POST', 'DELETE'])
def index(request):
    load_locations()
    request_data = request.data
    saved_fires = get_saved_fires()
    if len(saved_fires)>0:
        flatten(request_data,saved_fires)
    return process_incoming(request_data)


def process_incoming(request_data):
    severity_fire = []
    print(request_data)
    for fire_data in request_data:
        # index = calculate_index_for_city(fire_data["city"])
        severity = get_severity(fire_data["city"])
        severity_fire.append({
            "zone": get_zone_by_city(fire_data["city"]),
            "type": fire_data["type"],
            "severity": severity
        })
    save_fires(request_data)
    fires = get_needed_resources(severity_fire)
    allocation_matrix = process_info(severity_fire)
    allocation_matrix = modi_optimization(allocation_matrix, fires)
    print('Initial Cost: ', int(calculate_distance_traveled(allocation_matrix, fires)))
    test = translate_info(allocation_matrix, request_data)
    return HttpResponse(json.dumps(test))
def flatten(l,la):
    for item in la:
        l.append(item)

@api_view(['GET', 'POST', 'DELETE'])
def delete(request):
    number_to_delete = request.data["fire"]
    firedata = get_saved_fires()
    del firedata[number_to_delete]
    if len(firedata) == 0:
        save_fires(firedata)
        return HttpResponse([])
    return process_incoming(firedata)

def get_saved_fires():
    with open("info.json", "r") as file:
        return json.loads(file.read())

def save_fires(fires):
    with open("info.json", "w") as outfile:
        json.dump(fires, outfile)


def translate_info(allocation_matrix,resource_data):
    information_to_return = []
    for i in range(len(resource_data)):
        resource_list = []
        for j in range(len(district)):
            trucks = allocation_matrix[i][0][j]
            jeep = allocation_matrix[i][1][j]
            helly = allocation_matrix[i][2][j]
            if trucks+jeep+helly>0:
                resource_list.append({
                    "area" : district.get(j+1),
                    "trucks" : trucks,
                    "jipe" : jeep,
                    "hely" :helly
                })
        information_to_return.append({
            "id" : i,
            "latitude":resource_data[i]["latitude"],
        "longitude": resource_data[i]["longitude"],
        "resources_by_area" : resource_list
        })
    return information_to_return            


def get_zone_by_city(city):
    zone = list(district.keys())[list(district.values()).index(city)]
    return 'z' + str(zone)          


def load_locations():
    with open("./backend_info/file_info/locations.json") as j:
        info= json.loads(j.read())
    i=0    
    for location in info:
        i+=1
        district[i] = location['name']
