############################
#  Tratamento do Dataset   #
############################

import numpy as np
import pandas as pd
from datetime import datetime
from numpy.random import RandomState

# Delete Irrelevant Data
def pop(df):
    df.pop('Codigo_SGIF')
    df.pop('Codigo_ANEPC')
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
    df.pop('AreaPov_ha') 
    df.pop('AreaMato_ha') 
    df.pop('AreaAgric_ha') 
    df.pop('DataHoraAlerta') 
    df.pop('DataHora_PrimeiraIntervencao') 
    df.pop('DataHora_Extincao') 
    df.pop('Distrito') 
    df.pop('Concelho') 
    df.pop('Freguesia') 
    df.pop('RNAP') 
    df.pop('RNMPF') 
    df.pop('Latitude') 
    df.pop('Longitude') 
    df.pop('CodCausa')
    df.pop('AreaTotal_ha')
    return df
    
def distritos(argument):
    switcher = {
        'Porto': 0,
        'Leiria': 1,
        'Viana do Castelo': 2,
        'Coimbra':3,
        'Aveiro': 4,
        'Lisboa': 5,
        'Braga': 6,
        'Guarda': 7,
        'Castelo Branco': 8,
        'Viseu': 9,
        'Santarém': 10,
        'Vila Real': 11,
        'Setúbal': 12,
        'Faro': 13,
        'Évora': 14,
        'Bragança': 15,
        'Beja': 16,
        'Portalegre': 17,
    }
    return switcher.get(argument, "nothing")

#Definição das Classes!
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
    return switcher.get(argument, 8)

# ID para primeira coluna
def nomeColuna(argument):
    argument.columns.values[0] = "id"
    res = argument.columns.values[0]
    # displaying column
    # print("Displaying column names : ",res)
    return res
    
# Delete Outliers
def apagar_dados(df,i):
    if (df.loc[i, 'AreaTotal_ha'] < 0.1 or df.loc[i, 'GrupoCausa'] == "Reacendimentos" or df.loc[i, 'DSR'] == 'A' or df.loc[i, 'Duracao_Horas'] == 'A'):
        df = df.drop(i)
    return df

# Criacao TempoAlertaIntervencao
def tempo_alerta(df,i):
    #print(df.loc[i, 'DataHoraAlerta'])
    try:
        dAlerta = datetime.strptime(df.loc[i, 'DataHoraAlerta'], "%Y-%m-%d %H:%M:%S")
        dIntervencao = datetime.strptime(df.loc[i, 'DataHora_PrimeiraIntervencao'], "%Y-%m-%d %H:%M:%S")
        df.loc[i,'tempoAlertaIntervencao'] = abs(dAlerta - dIntervencao).total_seconds() / 3600.0
    except:
        pass
    return df

# Binary Encoding
def distrto_binario(df,i):
    dist = distritos(df.loc[i,'Distrito'])
    df.loc[i,'D0']= format(dist, '08b')[3]
    df.loc[i,'D1']= format(dist, '08b')[4]
    df.loc[i,'D2']= format(dist, '08b')[5]
    df.loc[i,'D3']= format(dist, '08b')[6]
    df.loc[i,'D4']= format(dist, '08b')[7]
    return df

if __name__ == "__main__":
    df = pd.read_csv("datasets/dadosConcatenados.csv")
    
    df['tempoAlertaIntervencao'] = 0
    df['D0'] = 0
    df['D1'] = 0
    df['D2'] = 0
    df['D3'] = 0
    df['D4'] = 0
    
    # Change classe_fogo with number
    for i in range(len(df)):
        if(i%100 ==0):
            print(i)
        df.loc[i,'ClasseArea']=classe_fogo(df.loc[i,'ClasseArea'])
        df = tempo_alerta(df,i)
        df = apagar_dados(df,i)
    # df= nomeColuna(df)
    
    # Removing irrelevant data
    df =pop(df)
    
    # Save dataset
    df.to_csv('datasets/fogos_tratados2.csv')
    df = pd.read_csv("datasets/fogos_tratados2.csv")
    df.pop('Unnamed: 0')
    df.to_csv('datasets/fogos_tratados2.csv')