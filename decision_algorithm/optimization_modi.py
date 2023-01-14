import process as pro
import numpy as np
import modi

district = 18
def modi_optimization(initial_matrix,fires):
    # initialization
    cols = len(initial_matrix)
    suply = np.zeros((1, 3, district))
    flag = 0
    
    # Atribution of supply
    suply= pro.get_resources_by_zone(suply,1)
    suply= np.squeeze(suply)
    costs = np.zeros((district,cols-1))

    # Atribution of costs (distances)
    i=0
    for fire in fires:
        for j in range(district):
            costs[j][i] = pro.get_distances(j,int(fire['zone'][1:])-1)
        i+=1
        
    # MODI process for each resource
    for resource in range(3):
        demand = [0] * (cols-1)
        
        # Select the resource from the supply matrix
        supply = list(suply[:][resource])
        
        # Atribution of demand
        for i in range(cols-1):
            demand[i] = initial_matrix[i][resource][district]
        demand = list(demand)

        # Balance supply or demand (creating a ghost consumer/producer)
        if(sum(supply)>sum(demand)):
            demand.append(sum(supply)-sum(demand))
            v = np.zeros((district, 1))
            costs = np.c_[costs, v]
            flag=1    
        elif(sum(supply)<sum(demand)):
            supply.append(sum(demand)-sum(supply))
            v = np.zeros((1,cols-1))
            costs = np.r_[costs, v]
            flag=0

        try:
            # MODI
            ans = modi.transportation_method(supply, demand, costs)

            # Delete Balancer consumer/producer 
            ans = np.delete(ans, ans.shape[flag]-1, flag)
            costs = np.delete(costs, costs.shape[flag]-1, flag)
            
            # Update Allocation Matrix
            dist=0
            for res in ans:
                fire_index=0
                initial_matrix[len(fires)][resource][dist]=supply[dist]
                for fire in res:
                    initial_matrix[fire_index][resource][dist]= fire
                    initial_matrix[len(fires)][resource][dist]-= fire
                    fire_index+=1
                dist+=1
        except:
            pass
        
    return initial_matrix


fires = [{
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

allocation_matrix=pro.process_info(fires)
print('Initial Cost: ', int(pro.calculate_distance_traveled(allocation_matrix,fires)))
# pro.print_matrix(allocation_matrix)

modi_matrix=modi_optimization(allocation_matrix, fires)
print('Optimal cost: ', int(pro.calculate_distance_traveled(modi_matrix,fires)))
# pro.print_matrix(modi_matrix)