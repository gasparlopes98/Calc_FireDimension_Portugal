import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cv2
'''
def sub_regioes(argument):
    switcher = {
        "ALTO MINHO": 0,
        'ALTO TÂMEGA':1,
        "ÁREA METROPOLITANA DO PORTO":2,
        'AVE':3,
        "CÁVADO":4,
        'DOURO':5,
        'TÂMEGA E SOUSA':6,
        'TERRAS DE TRÁS OS MONTES':7,
        'BEIRA BAIXA':8,
        'BEIRAS E SERRA DA ESTRELA':9,
        'MÉDIO TEJO':10,
        'OESTE':11,
        "REGIÃO DE AVEIRO":12,
        "REGIÃO DE COIMBRA": 13,
        "REGIÃO DE LEIRIA": 14,
        'VISEU DÃO LAFÕES':15,
        "ÁREA METROPOLITANA DE LISBOA":16,
        'ALENTEJO CENTRAL':17,
        'ALENTEJO LITORAL':18,
        'ALTO ALENTEJO':19,
        'BAIXO ALENTEJO':20,
        'LEZÍRIA DO TEJO':21,
        'ALGARVE':22,
    }
    return switcher.get(argument,0)
gama_incendios = {'[100 a 500 ha]', '[500 a 1000 ha]','[superior a 1000 ha]'}

df1 = pd.read_csv('datasets/eucaliptos.csv')
df3 = pd.read_csv('datasets/pinheiro_bravo.csv')
regioes = list(df1['Regiões'])
hect = list(df1['2015_hec_k'])
hect_p = list(df3['2015_hec_k'])

df2 = pd.read_csv('datasets/fogos_tratado.csv')
fogos = [0] * len(regioes)

for i in range(len(df2)):
    if(df2.loc[i, 'Ano'] == 2015 and df2.loc[i, 'ClasseArea'] in gama_incendios):
        fogos[sub_regioes(df2.loc[i,'Sub_Região'])]+=1

# fogos1=list(map(lambda x: float(x)*0.1, fogos))
# fig = plt.figure(figsize = (10, 5))
'''
# creating the bar plot
df = pd.read_csv("datasets/datasetDadosTratados.csv")
#print(df.columns)

#Plot FFMC
plt.xlabel("Burned Area")
plt.title("Relation between feature BUI and Burned area class")
plot = df.groupby(['ClasseArea'])['FFMC'].mean()
plt.bar(plot.keys(),plot.values)
plt.show()

#plot ISI
plt.xlabel("Burned Area")
plt.title("Relation between feature ISI and Burned area class")
plot = df.groupby(['ClasseArea'])['ISI'].mean()
plt.bar(plot.keys(),plot.values)
plt.show()

#plot DSR
plt.xlabel("Burned Area")
plt.title("Relation between feature DSR and Burned area class")
plot = df.groupby(['ClasseArea'])['DSR'].mean()
plt.bar(plot.keys(),plot.values)
plt.show()

#plot FWI
plt.xlabel("Burned Area")
plt.title("Relation between feature FWI and Burned area class")
plot = df.groupby(['ClasseArea'])['FWI'].mean()
plt.bar(plot.keys(),plot.values)
plt.show()

#plot DC
plt.xlabel("Burned Area")
plt.title("Relation between feature DC and Burned area class")
plot = df.groupby(['ClasseArea'])['DC'].mean()
plt.bar(plot.keys(),plot.values)
plt.show()

#plot DMC
plt.xlabel("Burned Area")
plt.title("Relation between feature DMC and Burned area class")
plot = df.groupby(['ClasseArea'])['DMC'].mean()
plt.bar(plot.keys(),plot.values)
plt.show()

#plot BUI
plt.xlabel("Burned Area")
plt.title("Relation between feature BUI and Burned area class")
plot = df.groupby(['ClasseArea'])['BUI'].mean()
plt.bar(plot.keys(),plot.values)
plt.show()

'''
for key in plot.keys():
    keys.append(key)
for value in plot.values:
    values.append(value)

keys.pop(0)
values.pop(0)
'''

'''
X_axis = np.arange(len(regioes))
  
plt.bar(X_axis - 0.1, hect, 0.2, label = 'Eucaliptos [k ha] em 2015')
plt.bar(X_axis - 0.3, hect_p, 0.2, label = 'Pinheiro Bravo [k ha] em 2015')
plt.bar(X_axis + 0.2, fogos, 0.4, label = 'Fogos de 2015 > 100 ha', color = 'red')

plt.xticks(X_axis, regioes)
plt.xlabel("Regiões")
plt.title("Relação fogos e região")
plt.xticks(rotation = 90)
plt.subplots_adjust(bottom=0.3)
plt.legend()
plt.show()
'''