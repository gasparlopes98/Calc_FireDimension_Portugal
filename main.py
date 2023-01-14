from sys import exit
import json
import predictions.predictions as pre
import backend_info.decision_algorithm.process as pro
import backend_info.decision_algorithm.optimization_modi as md
pred = pre.PREVISOES()

def get_locations():
    with open("backend_info/file_info/locations.json", 'r') as j:
        return json.loads(j.read())

def menu():
    print("H - Help")
    print("I - Insert Fire")
    print("R - Remove Fire")
    print("S - Start Allocation Process")
    print("P - Print Allocations")
    print("Q - Quit")
    
fires = [
    {
        'zone': 'Z1',
        'type': 'F',
        'severity': 4
    }
]      

menu() 

while(True):
    
    inp = input("Select Command: ").upper()
    
    if inp == 'I':
        fire,distrito = pred.tratamento_dados()
        severity = pre.previsoes(fire)
        print("Severity:",severity)
        
        typefire = ""
        while typefire not in ("F", "U"):
            typefire = input("Area of the Fire (F - Forest, U - Urban): ").upper()
        
        locations = get_locations()
        for i in locations:
            if(i["name"] == distrito):
                fires.append({'zone': '{}'.format(i["zone"]),'type': typefire,'severity': severity})
                break
        print("Fire Added: ",fires[-1])
        
    elif inp == "R":
        if fires:
            index_fire = -1

            while int(index_fire) < 0 or int(index_fire) > len(fires):
                index_fire = int(input("Which Fire? (Index): "))

            if 'allocation_matrix' in globals():
                allocation_matrix = pro.removeFire(allocation_matrix, int(index_fire), fires)
                print("Fire removed successfully")
            else:
                fires.pop(index_fire)
                print("Fire removed successfully")
        else:
            print("To remove a fire, you need to insert one first!")

    elif inp == "S":
        if fires:
            allocation_matrix = pro.process_info(fires)
            print('Initial Cost: ', int(pro.calculate_distance_traveled(allocation_matrix,fires)))
            allocation_matrix = md.modi_optimization(allocation_matrix, fires)
            print('Initial Cost: ', int(pro.calculate_distance_traveled(allocation_matrix,fires)))
        else:
            print("To start an Allocation Process, you need to insert a fire first!")
    
    elif inp == "P":
        if 'allocation_matrix' in globals():
            pro.print_matrix(allocation_matrix)
        else:
            print("Allocation Matrix is not defined yet, please, insert a fire first and start its Allocation Process!")
    
    elif inp == "H":
        menu()
    
    elif inp == "Q":
        exit()
    
    else:
        print("Please choose a correct answer")