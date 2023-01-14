import process as pro
import pandas as pd
import numpy as np
import modi

fires=[{
    'zone' : 'Z1',
    'type' : 'F',
    'severity' : 4
},{
    'zone' : 'Z1',
    'type' : 'F',
    'severity' : 3
},{
    'zone' : 'Z10',
    'type' : 'F',
    'severity' : 3
},{
    'zone' : 'Z11',
    'type' : 'F',
    'severity' : 3
},{
    'zone' : 'Z1',
    'type' : 'F',
    'severity' : 3
}
]
allocation_matrix,cols=pro.process_info(fires)
# pro.print_matrix(allocation_matrix)

# initialization
suply = np.zeros((1, 3, 18))
flag =0
# distance = 0

# Atribution of supply (work just with jeeps)
suply= pro.get_resources_by_zone(suply,1)
suply= np.squeeze(suply)
print('Initial Cost: ', int(pro.calculate_distance_traveled(allocation_matrix,fires)))

for resource in range(3):
    initial = np.zeros((18, cols-1))
    demand = [0] * (cols-1)
    costs = np.zeros((18,cols-1))
    
    # Atribution of distances
    i=0
    for fire in fires:
        for j in range(18):
            costs[j][i] = pro.get_distances(j,int(fire['zone'][1:])-1)
        i+=1
    
    # Atribution of demand
    for i in range(cols-1):
        demand[i] = allocation_matrix[i][resource][18]
    demand = list(demand)
        
    # Initial atribution from process.py
    for i in range(cols-1): 
        for j in range(18):
            initial[j][i] = allocation_matrix[i][resource][j]

    supply = list(suply[:][resource])
    
    # Balancear supply e demand
    if(sum(supply)>sum(demand)):
        demand.append(sum(supply)-sum(demand))
        v = np.zeros((18, 1))
        costs = np.c_[costs, v]
        initial = np.c_[initial, v]
        flag=1
    else:
        supply.append(sum(demand)-sum(supply))
        v = np.zeros((1,cols-1))
        costs = np.r_[costs, v]
        initial = np.r_[initial, v]
        flag=0
      
    # MODI
    ans = modi.transportation_method(supply, demand, costs, initial)
    # distance += modi.get_total_cost(costs, ans)
    
    # ELiminar Coluna/Linha  de Balanceamento
    ans = np.delete(ans, ans.shape[flag]-1, flag)
    
    # Update Allocation Matrix
    dist=0
    for res in ans:
        fire_index=0
        allocation_matrix[len(fires)][resource][dist]=supply[dist]
        for fire in res:
            allocation_matrix[fire_index][resource][dist]= fire
            allocation_matrix[len(fires)][resource][dist]-= fire
            fire_index+=1
        dist+=1
    
print('Optimal cost: ', int(pro.calculate_distance_traveled(allocation_matrix,fires)))
# print('total optimal cost: ', int(distance))
pro.print_matrix(allocation_matrix)
