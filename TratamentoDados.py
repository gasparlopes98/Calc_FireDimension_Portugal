import numpy as np
import pandas as pd
from datetime import datetime
import cv2
import matplotlib.pyplot as plt

#df = pd.read_csv("datasets/DadosConcatenados.csv")
#print(df.columns)

# Removing irrelevant data and  (Only for the first time!)
'''
df.pop('Codigo_SGIF')
df.pop('Codigo_ANEPC')
df.pop('Ano')
df.pop('Mes')
df.pop('Dia')
df.pop('Hora')
df.pop('IncSup24horas')
df.pop('DTCCFR')
df.pop('Local')
df.pop('X_Militar')
df.pop('Y_Militar')
df.pop('X_ETRS89')
df.pop('Y_ETRS89')
#df.pop('TipoCausa')
#df.pop('GrupoCausa')
#df.pop('DescricaoCausa')
#df.pop('FonteAlerta')


#Criacao TempoAlertaIntervencao

df['tempoAlertaIntervencao'] = 0

for i in range(len(df)):
    #print(df.loc[i, 'DataHoraAlerta'])
    try:
        dAlerta = datetime.strptime(df.loc[i, 'DataHoraAlerta'], "%Y-%m-%d %H:%M:%S")
        dIntervencao = datetime.strptime(df.loc[i, 'DataHora_PrimeiraIntervencao'], "%Y-%m-%d %H:%M:%S")
        print(f"Year {dIntervencao.year} Month {dIntervencao.month} Day {dIntervencao.day}")
        df.loc[i,'tempoAlertaIntervencao'] = dIntervencao-dAlerta
    except:
        pass

#Definição das Classes!

for i in range(len(df)):
    if df.loc[i, 'ClasseArea'] == "]0 a 1 ha[":
       df.loc[i, 'ClasseArea'] = 0

    elif df.loc[i, 'ClasseArea'] == "[1 a 10 ha]":
        df.loc[i, 'ClasseArea'] = 1

    elif df.loc[i, 'ClasseArea'] == "[10 a 20 ha]":
        df.loc[i, 'ClasseArea'] = 2

    elif df.loc[i, 'ClasseArea'] == "[20 a 50 ha]":
        df.loc[i, 'ClasseArea'] = 3

    elif df.loc[i, 'ClasseArea'] == "[50 a 100 ha]":
        df.loc[i, 'ClasseArea'] = 4

    elif df.loc[i, 'ClasseArea'] == "[100 a 500 ha]":
        df.loc[i, 'ClasseArea'] = 5

    elif df.loc[i, 'ClasseArea'] == "[500 a 1000 ha]":
        df.loc[i, 'ClasseArea'] = 6

    elif df.loc[i, 'ClasseArea'] == "[superior a 1000 ha]":
        df.loc[i, 'ClasseArea'] = 7
'''


df = pd.read_csv("datasets/datasetDadosTratados.csv")
#print(df.columns)

#ID para primeira coluna
'''
df.columns.values[0] = "id"
res = df.columns.values[0]
# displaying column
print("Displaying column names : ",res)
'''

#Saving new data base
j = 0
aux = 0
for i in range(len(df)):
    if df.loc[i, 'AreaTotal_ha'] < 0.01:
        aux += 1
        print("DMC ->" + str(df.loc[i,'DMC']))

    if df.loc[i, 'AreaTotal_ha'] < 0.01 and df.loc[i, 'TipoCausa'] == "Desconhecida":
        j+= 1
        #print(df.loc[i, 'AreaTotal_ha'])
        #print(df.loc[i, 'TipoCausa'])

print(j)
print(aux)

#df.to_csv('datasets/datasetDadosTratados.csv', index = False)



