# objective function
import process_annealing as pr
import random
import math

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
        # for resource in range(3):
        rr_available_jeep[dist] += Matrix[fire_len][0][dist]
        rr_available_truck[dist] += Matrix[fire_len][1][dist]
        rr_available_air[dist] += Matrix[fire_len][2][dist]

    return z_sum, rr_available_jeep, rr_available_truck, rr_available_air

def get_max_distance(needed_resources):
    max_distance = 0
    for resources in needed_resources:
        max_distance += resources["jeeps"] * 250
        max_distance += resources["trucks"] * 250
        max_distance += resources["air"] * 350

    return max_distance

def simulated_annealing(allocation_matrix, needed_resources):
    epoch = 50
    temperature = 100
    current_solution = allocation_matrix
    for i in range(temperature, 0, -1):
        while epoch >= 0:
            current_solution_cost = fitness(current_solution, needed_resources)
            new_solution = generate_new_solution(allocation_matrix, needed_resources)
            new_solution_cost = fitness(new_solution, needed_resources)

            delta_cost = new_solution_cost - current_solution_cost
            #if delta_cost < 0:
            if new_solution_cost < current_solution_cost:
                current_solution = new_solution
            elif acceptance_probabilities(i, delta_cost):
                current_solution = new_solution
            epoch -= 1
    return current_solution

def fitness(allocation_matrix, needed_resources):

    missing_trucks = 0
    missing_jeep = 0
    missing_air = 0
    available_jeep = 0
    available_trucks = 0
    available_air = 0
    needed_jeeps = 0
    needed_trucks = 0
    needed_air = 0

    for fire in range(len(needed_resources)):

        available_jeep = allocation_matrix[fire][0][pr.num_district]
        available_trucks = allocation_matrix[fire][1][pr.num_district]
        available_air = allocation_matrix[fire][2][pr.num_district]

        needed_trucks = needed_resources[fire]["trucks"]
        needed_jeeps = needed_resources[fire]["jeeps"]
        needed_air = needed_resources[fire]["air"]

        if needed_trucks > 0:
            missing_trucks += (needed_trucks - available_trucks) / needed_trucks * 100
        if needed_jeeps > 0:
            missing_jeep += (needed_jeeps - available_jeep) / needed_jeeps * 100
        if needed_air > 0:
            missing_air += (needed_air - available_air) / needed_air * 100

        '''
        available_trucks = allocation_matrix[fire][1][pr.num_district]
        available_jeep = allocation_matrix[fire][0][pr.num_district]
        available_air = allocation_matrix[fire][2][pr.num_district]

        needed_trucks = needed_resources[fire]["trucks"]
        needed_jeeps = needed_resources[fire]["jeeps"]
        needed_air = needed_resources[fire]["air"]

        if needed_trucks > 0:
            missing_trucks += (needed_trucks - available_trucks) / needed_trucks * 100
        if needed_jeeps > 0:
            missing_jeep += (needed_jeeps - available_jeep) / needed_jeeps * 100
        if needed_air > 0:
            missing_air += (needed_air - available_air) / needed_air * 100
'''

    average_missing_truck_per_fire = missing_trucks / len(needed_resources)
    average_missing_jeep_per_fire = missing_jeep / len(needed_resources)
    average_missing_air_per_fire = missing_air / len(needed_resources)

    distance = pr.sa_calculate_distance(allocation_matrix, needed_resources) / get_max_distance(needed_resources) * 100
    return average_missing_truck_per_fire * 0.30 + average_missing_jeep_per_fire * 0.30 + average_missing_air_per_fire * 0.30 + distance * 0.10



def generate_new_solution(allocation_matrix, needed_resources):
    new_solution = allocation_matrix

    fire_to_change = random.randint(0, len(needed_resources)-1)
    resources_in_change_fire = []

    '''
    for fire in new_solution[fire_to_change]:
    #for fire in new_solution:
        print(f"fire -> {fire}")
        for i in range(len(fire[0]) - 1):
            if fire[0][i] != 0 or fire[1][i] != 0 or fire[2][i] != 0:
                resources_in_change_fire.append(i)
    '''

    fire = new_solution[fire_to_change]
    for i in range(len(fire[0]) - 1):
        if fire[0][i] != 0 or fire[1][i] != 0 or fire[2][i] != 0:
            resources_in_change_fire.append(i)

    affected_zone = random.randint(0, len(resources_in_change_fire))
    #affected_zone = pr.index_by_zone_fire(needed_resources[fire_to_change]['zone'])
    editable_fires = []

    for i in range(len(needed_resources)):
        zone = int(needed_resources[i]["zone"][1::]) - 1
        dist = pr.get_distances(affected_zone, zone)
        #if dist == 0:
        if pr.get_distances(affected_zone, zone):
            editable_fires.append(i)

    dice = random.randint(1, 6)
    #if dice <= 6:
    jeeps = new_solution[fire_to_change][0][affected_zone]
    trucks = new_solution[fire_to_change][1][affected_zone]
    air = new_solution[fire_to_change][2][affected_zone]

#-----------------------------Jeeps---------------------------------------------
    if jeeps > 0 :
        jeeps_to_allocate = random.randint(0, jeeps) // len(editable_fires)
        if(jeeps_to_allocate > needed_resources[fire_to_change]['jeeps']):
            jeeps_to_allocate = needed_resources[fire_to_change]['jeeps']
        #print(f"Demand {allocation_matrix[0][0][18]}")
        #jeeps_to_allocate = needed_resources[fire_to_change]['jeeps']
        #if jeeps - jeeps_to_allocate < 0:
            #jeeps_to_allocate = jeeps
    else:
        jeeps_to_allocate = 0

# -----------------------------Trucks---------------------------------------------
    if trucks > 0:
        trucks_to_allocate = random.randint(0, trucks) // len(editable_fires)
        if (trucks_to_allocate > needed_resources[fire_to_change]['trucks']):
            trucks_to_allocate = needed_resources[fire_to_change]['trucks']
        #trucks_to_allocate = needed_resources[fire_to_change]['trucks']
        #if trucks - trucks_to_allocate <0:
            #trucks_to_allocate = trucks
    else:
        trucks_to_allocate = 0

# -----------------------------Air---------------------------------------------
    if air > 0:
        air_to_allocate = random.randint(0, air) // len(editable_fires)
        if (air_to_allocate > needed_resources[fire_to_change]['air']):
            air_to_allocate = needed_resources[fire_to_change]['air']
        #air_to_allocate = needed_resources[fire_to_change]['air']
        #if air - air_to_allocate <0:
            #air_to_allocate = air
    else:
        air_to_allocate = 0

#-----------------------------------------------------------------------------

    for editable_fire in editable_fires:
        if editable_fire != fire_to_change:
            new_solution[editable_fire][0][affected_zone] += jeeps_to_allocate
            new_solution[editable_fire][1][affected_zone] += trucks_to_allocate
            new_solution[editable_fire][2][affected_zone] += air_to_allocate

    new_solution[fire_to_change][0][affected_zone] -= jeeps_to_allocate * len(editable_fires)
    new_solution[fire_to_change][1][affected_zone] -= trucks_to_allocate * len(editable_fires)
    new_solution[fire_to_change][2][affected_zone] -= air_to_allocate * len(editable_fires)

    re_calculate_last_line_of_matrix(new_solution)

    return new_solution

'''
    else:
        for editable_fire in editable_fires:
            jeeps = new_solution[editable_fire][0][affected_zone]

            if (jeeps > 0):
                lost_jeeps = random.randint(0, jeeps)
                if new_solution[fire_to_change][0][pr.num_district] + lost_jeeps > needed_resources[fire_to_change][
                    "jeeps"]:
                    lost_jeeps = needed_resources[fire_to_change]["jeeps"] - new_solution[fire_to_change][0][
                        pr.num_district]
                new_solution[editable_fire][0][affected_zone] -= lost_jeeps
                new_solution[fire_to_change][1][affected_zone] += lost_jeeps

            trucks = new_solution[editable_fire][1][affected_zone]
            if(trucks > 0):
                lost_trucks = random.randint(0, trucks)
                if new_solution[fire_to_change][1][pr.num_district] + lost_trucks > needed_resources[fire_to_change][
                    "trucks"]:
                    lost_trucks = needed_resources[fire_to_change]["trucks"] - new_solution[fire_to_change][1][
                        pr.num_district]
                new_solution[editable_fire][1][affected_zone] -= lost_trucks
                new_solution[fire_to_change][2][affected_zone] += lost_trucks

            air = new_solution[editable_fire][2][affected_zone]
            if(air > 0):
                lost_air = random.randint(0, air)
                if new_solution[fire_to_change][2][pr.num_district] + lost_air > needed_resources[fire_to_change]["air"]:
                    lost_air = needed_resources[fire_to_change]["air"] - new_solution[fire_to_change][2][pr.num_district]
                new_solution[editable_fire][2][affected_zone] -= lost_air
                new_solution[fire_to_change][2][affected_zone] += lost_air
'''


def re_calculate_last_line_of_matrix(allocation_matrix):
    for i in range(len(allocation_matrix)):
        allocation_matrix[i][0][pr.num_district] = 0
        allocation_matrix[i][1][pr.num_district] = 0
        allocation_matrix[i][2][pr.num_district] = 0

    for i in range(len(allocation_matrix)):
        for j in range(len(allocation_matrix[i][0])-1):
            allocation_matrix[i][0][pr.num_district] += allocation_matrix[i][0][j]
            allocation_matrix[i][1][pr.num_district] += allocation_matrix[i][1][j]
            allocation_matrix[i][2][pr.num_district] += allocation_matrix[i][2][j]
    return allocation_matrix


def acceptance_probabilities(temperature, delta_cost):
    return random.uniform(0, 1) < math.exp(-delta_cost / temperature)

if __name__ == "__main__":

    # my_dict = {"zone":"","type":"","severity":"",}


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
    district = 18

    allocation_matrix, dist_total, needed_resources = pr.process_info(dict_fire)
    anneal_solution = simulated_annealing(allocation_matrix,needed_resources)
    pr.print_matrix(len(anneal_solution),anneal_solution)
    print(f"Final Cost: {int(pr.sa_calculate_distance(anneal_solution,dict_fire))}")


    #print(f"Shape -> {np.shape(allocation_matrix)}")


