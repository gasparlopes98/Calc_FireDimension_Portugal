import json
import pandas as pd
import numpy as np

path_distance_matrix_location = "../file_info/distance_matrix.txt"
path_resources_by_zone = "../file_info/resources_by_zone.json"
path_resources_by_severity = "severidade_info.json"

num_district=18
rows = num_district+1

# dicionario que contem como indice zona e como objeto a severidade
def process_info(fire_severity_by_zone):
    cols = len(fire_severity_by_zone)+1
    allocation_matrix = np.zeros((cols, 3, rows))
    #get meios usados para severidade
    need = needed_resources = get_needed_resources(fire_severity_by_zone)
    # get meios por zona
    allocation_matrix = get_resources_by_zone(allocation_matrix,cols)
    mean_severity = fire_severity_average(fire_severity_by_zone)
    flag_available_resources = enough_rr(fire_severity_by_zone)
    if (mean_severity < 2 and flag_available_resources== False):
        basic_attribuiton(needed_resources, allocation_matrix, cols)
    else:
        RRbasic_attribuiton(needed_resources, allocation_matrix, cols)
    #print_matrix(cols, allocation_matrix)
    #print("Distance Traveled: {}".format(calculate_distance_traveled(allocation_matrix, need).round()))
    needed_resources = get_needed_resources(fire_severity_by_zone)
    # get meios por zona
    allocation_matrix = get_resources_by_zone(allocation_matrix, cols)

    return allocation_matrix,calculate_distance_traveled(allocation_matrix, need), needed_resources

    
def allocate_resource(nfires,allocation_matrix,fire,fire_index,zones,resource,resource_index):
    if allocation_matrix[nfires-1][resource_index][zones] >= fire[resource]:
        allocation_matrix[fire_index][resource_index][zones]+=fire[resource]
        allocation_matrix[nfires-1][resource_index][zones] -= fire[resource]
        fire[resource] = 0
    else:
        allocation_matrix[fire_index][resource_index][zones]+=allocation_matrix[nfires-1][resource_index][zones]
        fire[resource] -= allocation_matrix[nfires-1][resource_index][zones]
        allocation_matrix[nfires-1][resource_index][zones] = 0
# calcula a severidade média dos incendios para chamar o melhor método
def fire_severity_average(fire_severity_by_zone):
    severity = 0
    average_severity = 0
    for fires in fire_severity_by_zone:
        severity += fires['severity']
        average_severity = severity / len(fire_severity_by_zone)
        #print(average_severity)
    return average_severity

def basic_attribuiton(needed_resources,allocation_matrix,nfires):
    for fire in needed_resources:
        fire_index=list(needed_resources).index(fire)
        resources_full_filled = False
        should_restart = True
        airConter = 0

        # Demand
        allocation_matrix[fire_index][0][num_district]=fire['jeeps']
        allocation_matrix[fire_index][1][num_district]=fire['trucks']
        allocation_matrix[fire_index][2][num_district]=fire['air']

        # Array with nearest zones
        distance_matrix = get_sorted_distances(int(fire['zone'][1:])-1)

        while should_restart:
            for zones in distance_matrix:
                should_restart = False
                if(fire['jeeps']>0):
                    allocate_resource(nfires,allocation_matrix,fire,fire_index,zones,'jeeps',0)
                if(fire['trucks']>0):
                    allocate_resource(nfires,allocation_matrix,fire,fire_index,zones,'trucks',1)
                if(fire['air']>0):
                    airConter += 1
                    if(airConter < 5):
                        allocate_resource(nfires,allocation_matrix,fire,fire_index,zones,'air',2)
                    else: # Convert air resource to land resources
                        fire['jeeps'] += 10*fire['air']
                        fire['trucks'] += 5 * fire['air']
                        allocation_matrix[fire_index][0][num_district] += 10*fire['air']
                        allocation_matrix[fire_index][1][num_district] += 5 * fire['air']
                        allocation_matrix[fire_index][2][num_district]-=fire['air']
                        fire['air'] = 0
                        should_restart = True
                        break
                if(fire['jeeps']+fire['trucks']+fire['air']==0):
                    resources_full_filled = True
                    fire['resources'] = resources_full_filled

def allocate_resourceRR(nfires,allocation_matrix,fire,fire_index,zones,resource,resource_index, amount):
    if allocation_matrix[nfires-1][resource_index][zones]>= amount and fire[resource] >= amount:
        allocation_matrix[fire_index][resource_index][zones]+=amount
        allocation_matrix[nfires-1][resource_index][zones] -= amount
        fire[resource] -= amount
    elif allocation_matrix[nfires-1][resource_index][zones] >= fire[resource]:
        allocation_matrix[fire_index][resource_index][zones]+= fire[resource]
        allocation_matrix[nfires-1][resource_index][zones] -= fire[resource]
        fire[resource] -= fire[resource]
    else:
        allocation_matrix[fire_index][resource_index][zones]+= allocation_matrix[nfires-1][resource_index][zones]
        allocation_matrix[nfires-1][resource_index][zones] -= allocation_matrix[nfires-1][resource_index][zones]
        fire[resource] -= allocation_matrix[nfires-1][resource_index][zones]
        
def RRbasic_attribuiton(needed_resources,allocation_matrix,nfires):
    occurance=True
    count= np.zeros(nfires-1)
    # Demand
    fire_index=0
    for fire in needed_resources:
        allocation_matrix[fire_index][0][num_district]=fire['jeeps']
        allocation_matrix[fire_index][1][num_district]=fire['trucks']
        allocation_matrix[fire_index][2][num_district]=fire['air']
        fire_index+=1
    
    while occurance:
        for fire in needed_resources:
            fire_index=list(needed_resources).index(fire)
            if(count[fire_index]==0):
                if(fire['air']>0):
                    district_with_air=get_district_resource(int(fire['zone'][1:])-1,2,allocation_matrix,nfires)
                    if district_with_air == num_district:
                        fire['jeeps'] += 10*fire['air']
                        fire['trucks'] += 5 * fire['air']
                        allocation_matrix[fire_index][0][num_district] += 10*fire['air']
                        allocation_matrix[fire_index][1][num_district] += 5*fire['air']
                        allocation_matrix[fire_index][2][num_district] -= fire['air']
                        fire['air'] = 0
                    else:
                        allocate_resourceRR(nfires,allocation_matrix,fire,fire_index,district_with_air,'air',2,1)
                if(fire['jeeps']>0):
                    district_with_jeep=get_district_resource(int(fire['zone'][1:])-1,0,allocation_matrix,nfires)
                    if district_with_jeep == num_district:
                        fire['resources'] =False
                        fire['jeeps'] =0
                    else:
                        allocate_resourceRR(nfires,allocation_matrix,fire,fire_index,district_with_jeep,'jeeps',0,10)
                if(fire['trucks']>0):
                    district_with_truck=get_district_resource(int(fire['zone'][1:])-1,1,allocation_matrix,nfires)
                    if district_with_truck == num_district:
                        fire['resources'] =False
                        fire['trucks'] =0
                    else:
                        allocate_resourceRR(nfires,allocation_matrix,fire,fire_index,district_with_truck,'trucks',1,5)
                if(fire['jeeps']+fire['trucks']+fire['air']==0): 
                    count[fire_index]=1
                if all(count):
                    occurance = False
                    break;
                
def get_district_resource(zone,resource_index,allocation_matrix,nfires):
    distances = get_sorted_distances(zone)
    for i in distances:
        if(allocation_matrix[nfires-1][resource_index][i]>0):
            return i  
    return num_district

def get_needed_resources(occurrences):
    needed_resources_by_zone= []
    resources_by_severity_info = get_needed_resources_by_fire_severity()
    for fires in occurrences:
        resource_index = (fires["severity"])
        if (fires['type']=='F'):
            resource_index += 5
        resources = resources_by_severity_info[resource_index]    
        needed_resources_by_zone.append({"zone" : fires['zone'],"jeeps":resources['jeeps'],"trucks":resources['trucks'],"air" : resources['air'],"resources": True})
    
    return needed_resources_by_zone

def get_needed_resources_by_fire_severity():
    with open(path_resources_by_severity, 'r') as j:
     return json.loads(j.read())

def get_resources_by_zone(allocation_matrix,cols):
    with open(path_resources_by_zone, 'r') as j:
        resource= json.loads(j.read())
    for zone in range(num_district):
        allocation_matrix[cols-1][0][zone]=resource[zone]['jeeps']
        allocation_matrix[cols-1][1][zone]=resource[zone]['trucks']
        allocation_matrix[cols-1][2][zone]=resource[zone]['air']
    return allocation_matrix

def get_sorted_distances(zone):
    df = pd.read_csv(path_distance_matrix_location, header=None)
    df=df[zone].sort_values()
    return df.index

def get_distances(zone1, zone2):
    df = pd.read_csv(path_distance_matrix_location, header=None)
    return df[zone1][zone2]

def print_matrix(cols, matrix):
    print("{0:14}".format(" "),end="")
    for fire in range(cols):
        if(fire < cols-1):
            print("Fire {0:1}".format(fire+1),end="")
            print("{0:12}".format(" "),end="")  
        else:
            print("Available",end="")
            print("{0:12}".format(" "),end="")
        
    print("")
    print("{0:12}".format(" "),end="")
    for i in range(cols):
        print(" j     t    a     ",end="")
    print("")
    for zone in range(rows):
        if(zone == num_district):
            print("Demand :",end="")
        else:
            print("Zone {0:2}:".format(zone+1),end="")
        for fire in range(cols):
            print(" {0:5}".format(int(matrix[fire][0][zone])),end="")
            print(" {0:5}".format(int(matrix[fire][1][zone])),end="")
            print(" {0:4}|".format(int(matrix[fire][2][zone])),end="")
        print("")   
def enough_rr(fires):
    dist_initial_resource_jeep = [0] * 18
    dist_initial_resource_truck = [0] * 18
    dist_initial_resource_air = [0] * 18
    Fire_resource_jeep = [0] * len(fires)
    Fire_resource_truck = [0] * len(fires)
    Fire_resource_air = [0] * len(fires)
    result_resource_jeep = [0] * 18
    result_resource_truck = [0] * 18
    result_resource_air = [0] * 18

    json_resourceZone = get_json_contents("../file_info/resources_by_zone.json")
    json_severidade = get_json_contents("severidade_info.json")

    for f in range(len(fires)):
        for j in range(len(json_severidade)):
            if(fires[f]['type'] == json_severidade[j]['type'] and fires[f]['severity'] == json_severidade[j]['severity']):
                Fire_resource_jeep[f] = json_severidade[j]['jeeps']
                Fire_resource_truck[f] = json_severidade[j]['trucks']
                Fire_resource_air[f] = json_severidade[j]['air']
                break
            else:
                continue

    for dist in range(0,18):
        dist_initial_resource_jeep[dist] = json_resourceZone[dist]["jeeps"]
        dist_initial_resource_truck[dist] = json_resourceZone[dist]["trucks"]
        dist_initial_resource_air[dist] = json_resourceZone[dist]["air"]

    result_resource_jeep = dist_initial_resource_jeep
    result_resource_truck = dist_initial_resource_truck
    result_resource_air = dist_initial_resource_air

    for i in range(len(fires)):
        zone = fires[i]['zone']
        index = index_by_zone_fire(zone)
        #result_resource_jeep[index] = dist_initial_resource_jeep[index] - Fire_resource_jeep[i]
        #result_resource_truck[index] = dist_initial_resource_truck[index] - Fire_resource_truck[i]
        #result_resource_air[index] = dist_initial_resource_air[index] - Fire_resource_air[i]
        result_resource_jeep[index] = result_resource_jeep[index] - Fire_resource_jeep[i]
        result_resource_truck[index] = result_resource_truck[index] - Fire_resource_truck[i]
        result_resource_air[index] = result_resource_air[index] - Fire_resource_air[i]

    '''
    print(f"distrito jeep -> {dist_initial_resource_jeep}")
    print(f"distrito truck -> {dist_initial_resource_truck}")
    print(f"distrito air -> {dist_initial_resource_air}")
    print(f"Fogo jeep -> {Fire_resource_jeep}")
    print(f"Fogo truck -> {Fire_resource_truck}")
    print(f"Fogo air -> {Fire_resource_air}")

    print(f"Result jeep -> {result_resource_jeep}")
    print(f"Result truck -> {result_resource_truck}")
    print(f"Result air -> {result_resource_air}")
    '''

    for n in range(0,18):
        if(result_resource_jeep[n] <0 or result_resource_truck[n] <0 or result_resource_air[n] <0):
            return False
        else:
            continue
    return True

def get_json_contents(path):
    json_location = path
    with open(json_location, 'r') as j:
     return json.loads(j.read())

def index_by_zone_fire(argument):
    switcher = {
        'Z1': 0,
        'Z2': 1,
        'Z3': 2,
        'Z4': 3,
        'Z5': 4,
        'Z6': 5,
        'Z7': 6,
        'Z8': 7,
        'Z9': 8,
        'Z10': 9,
        'Z11': 10,
        'Z12': 11,
        'Z13': 12,
        'Z14': 13,
        'Z15': 14,
        'Z16': 15,
        'Z17': 16,
        'Z18': 17,
    }
    return switcher.get(argument, 18)

def calculate_distance_traveled(allocation_matrix,needed_resources):
    fire_index = distance_traveled = 0
    for fire in needed_resources:
        fire_zone=int(fire['zone'][1:])-1
        for district in range(num_district):
            resources=allocation_matrix[fire_index][0][district]+allocation_matrix[fire_index][1][district]+allocation_matrix[fire_index][2][district]
            distance=get_distances(fire_zone,district)
            distance_traveled+=(resources*distance)
        fire_index+=1
    return distance_traveled

'''
process_info([{
    'zone' : 'Z1',
    'type' : 'F',
    'severity' : 4
},{
    'zone' : 'Z1',
    'type' : 'F',
    'severity' : 3
},{
    'zone' : 'Z1',
    'type' : 'F',
    'severity' : 4
},{
    'zone' : 'Z10',
    'type' : 'F',
    'severity' : 1
},{
    'zone' : 'Z9',
    'type' : 'F',
    'severity' : 4
},{
    'zone' : 'Z10',
    'type' : 'F',
    'severity' : 4
},{
    'zone' : 'Z18',
    'type' : 'F',
    'severity' : 4
},{
    'zone' : 'Z18',
    'type' : 'F',
    'severity' : 4
},{
    'zone' : 'Z18',
    'type' : 'F',
    'severity' : 4
}
])
'''