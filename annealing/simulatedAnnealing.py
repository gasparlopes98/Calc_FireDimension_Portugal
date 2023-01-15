#objective function
import numpy as np
import process_annealing as pr
import json
from scipy import optimize


def objective(rr_available, needed_resources):
    #a = np.reshape(rr_available, (3, 18))
    #b = np.reshape(needed_resources, (4, 9))
    #zones = b[3]
    #b = np.delete(b,3,0)

    index = [0] * 18
    n_district = 18

    print(f"Available resources -> {rr_available}")
    print(f"Needed resources -> {needed_resources}")
    #print(f"zones -> {zones}")

    for i in range(len(needed_resources)):
        for d in range(len(n_district)):
            pass
            #index_zonefire = pr.index_by_zone_fire(zones[i])
            #distance = pr.get_distances(index_zonefire, n_district)

    return 0

def resource_by_dist(Matrix):
    z_sum = [0] * 18
    rr_available_jeep = [0] * 18
    rr_available_truck = [0] * 18
    rr_available_air = [0] * 18
    fire_len = len(dict_fire)

    # 1 - Fogo | 2 - j t a | 3- dist
    for dist in range(0, 18):
        for fire in range(len(dict_fire)):
            for resource in range(3):
                z_sum[dist] += Matrix[fire][resource][dist]

    for dist in range(0, 18):
        #for resource in range(3):
        rr_available_jeep[dist] += Matrix[fire_len][0][dist]
        rr_available_truck[dist] += Matrix[fire_len][1][dist]
        rr_available_air[dist] += Matrix[fire_len][2][dist]

    return z_sum, rr_available_jeep,rr_available_truck,rr_available_air

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
    '''
    print(f"Result jeep -> {result_resource_jeep}")
    print(f"Result truck -> {result_resource_truck}")
    print(f"Result air -> {result_resource_air}")


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
def enough_rr(z_sum,rr_available):

    pass


if __name__ == "__main__":

    #my_dict = {"zone":"","type":"","severity":"",}

    #print("Insert Fire data ")
    #my_dict["zone"] = input("Zone: ")
    #my_dict["type"] = input("type: ")
    #my_dict["severity"] = input("severity: ")

    path_distance_matrix_location = "../file_info/distance_matrix.txt.txt"

    path_distance_matrix_location = "../file_info/distance_matrix.txt"

    path_resources_by_severity = "severidade_info.json"
    path_resources_by_zone = "../file_info/resources_by_zone.json"

    # print(f"Soma recursos {z_sum}")
    # print(f"Recursos Available jeep {rr_available_jeep}")
    # print(f"Recursos Available truck {rr_available_truck}")
    # print(f"Recursos Available air {rr_available_air}")

    # Flag = pr.enough_rr(dict_fire)
    dict_fire = [{
        'zone': 'Z1',
        'type': 'F',
        'severity': 4
    }, {
        'zone': 'Z1',
        'type': 'F',
        'severity': 3
    }, {
        'zone': 'Z1',
        'type': 'F',
        'severity': 4
    }, {
        'zone': 'Z10',
        'type': 'F',
        'severity': 1
    }, {
        'zone': 'Z9',
        'type': 'F',
        'severity': 4
    }, {
        'zone': 'Z10',
        'type': 'F',
        'severity': 4
    }, {
        'zone': 'Z18',
        'type': 'F',
        'severity': 4
    }, {
        'zone': 'Z18',
        'type': 'F',
        'severity': 4
    }, {
        'zone': 'Z18',
        'type': 'F',
        'severity': 4
    }
    ]

    path_distance_matrix_location = "../file_info/distance_matrix.txt"
    path_resources_by_severity = "severidade_info.json"
    path_resources_by_zone = "../file_info/resources_by_zone.json"
    rr_fire_jeep = [0] * len(dict_fire)
    rr_fire_truck = [0] * len(dict_fire)
    rr_fire_air = [0] * len(dict_fire)
    rr_fire_zone = [0] * len(dict_fire)


    #Matriz de alocação (serve de comparacao)
    allocation_matrix, dist_total = pr.process_info(dict_fire)
    cols = len(allocation_matrix)

    z_sum, rr_available = resource_by_dist(allocation_matrix)
    print(f"Soma recursos {z_sum}")
    print(f"Recursos Available {rr_available}")
    Flag = enough_rr(dict_fire)

    print(Flag)


    #Retorna soma de recursos por distrito, como individualmente
    z_sum, rr_available_jeep,rr_available_truck,rr_available_air = resource_by_dist(allocation_matrix)

    #Retorna os recursos necessarios por fogo
    needed_resources = pr.get_needed_resources(dict_fire)

    #Ciclo para separar individualmente os recursos
    for i in range(len(needed_resources)):
        #index = pr.index_by_zone_fire(needed_resources[i]["zone"])
        #print(f"recursos por fogo ->  {rr_available[index]}")
        rr_fire_jeep[i] = needed_resources[i]['jeeps']
        rr_fire_truck[i] = needed_resources[i]['trucks']
        rr_fire_air[i] = needed_resources[i]['air']
        rr_fire_zone[i] = needed_resources[i]['zone']

    #Criacao da matriz dos disponiveis e dos necessarios para a funcao objetivo
    #m_rr_available = np.array([[rr_available_jeep], [rr_available_truck], [rr_available_air]])
    #m_rr_fire = np.array([[rr_fire_jeep], [rr_fire_truck], [rr_fire_air] ,[rr_fire_zone]])
    #objective(rr_available_jeep,rr_fire_jeep)
    #objective(rr_available_truck, rr_fire_truck)
    #objective(rr_available_air, rr_fire_air)

    #res = optimize.dual_annealing(objective(rr_available,needed_resources))

    '''
    # define range for input
    bounds = asarray([[0, 4]])

    #generate initial point
    best = bounds[:,0] + rand(len(bounds)) * (bounds[:,1] - bounds [:,0])

    # evaluate the initial point
    best_eval = objective(best)

    # current working solution
    curr, curr_eval = best, best_eval

    # run the algorithm
    for i in range(n_iterations):
        # take a step
        candidate = solution + randn(len(bounds)) * step_size

        # evaluate candidate point
        candidate_eval = objective(candidate)

        # check for new best solution
        if candidate_eval < best_eval:
            # store new best point
            best, best_eval = candidate, candidate_eval
            # report progress
            # print(f">{i} f({best}) = {best_eval}")
            print('>%d f(%s) = %.5f' % (i, best, best_eval))

            # difference between candidate and current point evaluation
            diff = candidate_eval - curr_eval

            # calculate temperature for current epoch
            t = temp / float(i + 1)

            # calculate metropolis acceptance criterion
            metropolis = exp(-diff / t)

            # check if we should keep the new point
            if diff < 0 or rand() < metropolis:
                # store the new current point
                curr, curr_eval = candidate, candidate_eval
'''
