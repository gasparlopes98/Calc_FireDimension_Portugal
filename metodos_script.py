import algoritmos_aprendizagem.arvore_decisao as ad
import algoritmos_aprendizagem.rede_neuronal as rn

print("Which algorithm method do you want to use?")
print("1 - Decision Tree")
print("2 - Neural Network")

algoritmo = 0

while algoritmo not in (1, 2):
    algoritmo = int(input('Method: '))

    if algoritmo == 1: # Decision Tree
        ad.modelo_arvore()
    elif algoritmo == 2: # Neural Network
        rn.modelo_rede()
    else:
        print("Please, select a valid option!")