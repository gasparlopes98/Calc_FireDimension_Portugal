import numpy as np
import pandas as pd
from datetime import datetime

#df = pd.read_csv("datasets/DadosConcatenados.csv")
#print(df.columns)

def pop():
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
    df.pop('TipoCausa')
    df.pop('GrupoCausa')
    df.pop('DescricaoCausa')
    df.pop('FonteAlerta') 

def classe_fogo(argument):
    switcher = {
        "]0 a 1 ha[": 0,
        "[1 a 10 ha]": 1,
        "[10 a 20 ha]": 2,
        "[20 a 50 ha]": 3,
        "[50 a 100 ha]": 4,
        "[100 a 500 ha]":5,
        "[500 a 1000 ha]":6,
        "[superior a 1000 ha]":7,
    }
    return switcher.get(argument, "nothing")

##############
# Tratamento
##############
'''
# Removing irrelevant data
pop()

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

# Change classe_fogo with number
for i in range(len(df)):
    df.loc[i, 'ClasseArea'] = classe_fogo(df.loc[i, 'ClasseArea'])
'''


df = pd.read_csv("datasets/fogos_tratados.csv")
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

#df.to_csv('datasets/fogos_tratados.csv', index = False)