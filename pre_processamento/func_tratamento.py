import numpy as np
import pandas as pd
from datetime import datetime
from numpy.random import RandomState

# Delete Irrelevant Data
def delete_column(df):
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
    df.pop('Duracao_Horas')
    return df

def new_column(df):
    df['tempoAlertaIntervencao'] = 0
    df['AreaVegetacao'] = 0
    df['D0'] = 0
    df['D1'] = 0
    df['D2'] = 0
    df['D3'] = 0
    df['D4'] = 0
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
    return switcher.get(argument, 18)

#Definição das Classes!
def classe_fogo(argument):
    switcher = {
        "]0 a 1 ha[" : 0,
        "[1 a 10 ha]": 0,
        "[10 a 20 ha]": 1,
        "[20 a 50 ha]": 1,
        "[50 a 100 ha]": 2,
        "[100 a 500 ha]":2,
        "[500 a 1000 ha]":3,
        "[superior a 1000 ha]":4,
    }
    return switcher.get(argument, 8)
"""
def sub_regioes(argument):
    switcher = {
        'Porto': "ÁREA METROPOLITANA DO PORTO",
        'Leiria': "REGIÃO DE LEIRIA",
        'Viana do Castelo': "ALTO MINHO",
        'Coimbra': "REGIÃO DE COIMBRA",
        'Aveiro': "REGIÃO DE AVEIRO",
        'Lisboa':"ÁREA METROPOLITANA DE LISBOA",
        'Braga':"CÁVADO",
        'Guarda':'BEIRAS E SERRA DA ESTRELA',
        'Castelo Branco':'BEIRA BAIXA',
        'Viseu':'VISEU DÃO LAFÕES',
        'Santarém':'LEZÍRIA DO TEJO',
        'Vila Real':'DOURO',
        'Setúbal':'ÁREA METROPOLITANA DE LISBOA',
        'Faro':'ALGARVE',
        'Évora':'ALENTEJO CENTRAL',
        'Bragança':'TERRAS DE TRÁS OS MONTES',
        'Beja':'BAIXO ALENTEJO',
        'Portalegre':'ALTO ALENTEJO',
        'Grandola':'ALENTEJO LITORAL',
        'Caldas da Rainha':'OESTE',
        'Tomar':'MÉDIO TEJO',
        'Penafiel':'TÂMEGA E SOUSA',
        'Guimarães':'AVE',
        'Chaves':'ALTO TÂMEGA',
    }
    return switcher.get(argument, "npthing")

def sub_regioes(argument):
    switcher = {
        "ÁREA METROPOLITANA DO PORTO":82.99,
        "REGIÃO DE LEIRIA":127.73,
        "ALTO MINHO":71.85,
        "REGIÃO DE COIMBRA":233.07,
        "REGIÃO DE AVEIRO":80.53,
        "ÁREA METROPOLITANA DE LISBOA":66.26,
        "CÁVADO":40.35,
        'BEIRAS E SERRA DA ESTRELA':111.60,
        'BEIRA BAIXA':185.77,
        'VISEU DÃO LAFÕES':138.88,
        'LEZÍRIA DO TEJO':204.85,
        'DOURO':70.13,
        'ALGARVE':145.2,
        'ALENTEJO CENTRAL':338.53,
        'TERRAS DE TRÁS OS MONTES':144.49,
        'BAIXO ALENTEJO':244.67,
        'ALTO ALENTEJO':255.37,
        'ALENTEJO LITORAL':291.16,
        'OESTE':61.69,
        'MÉDIO TEJO':153.86,
        'TÂMEGA E SOUSA':58.84,
        'AVE':45.13,
        'ALTO TÂMEGA':70.97,
    }
    return switcher.get(argument, 1)
"""
def are_vegetacao(argument):
    switcher = {
        'Porto': 82.99,
        'Leiria': 127.73,
        'Viana do Castelo': 71.85,
        'Coimbra': 233.07,
        'Aveiro': 80.53,
        'Lisboa':36.26,
        'Braga':40.35,
        'Guarda':111.60,
        'Castelo Branco':185.77,
        'Viseu':138.88,
        'Santarém':204.85,
        'Vila Real':70.13,
        'Setúbal':100,
        'Faro':145.2,
        'Évora':338.53,
        'Bragança':144.49,
        'Beja':244.67,
        'Portalegre':255.37,
        'Grandola':201.16,
        'Caldas da Rainha':61.69,
        'Tomar':153.86,
        'Penafiel':58.84,
        'Guimarães':45.13,
        'Chaves':70.97,
    }
    return switcher.get(argument, 1)

# ID para primeira coluna
def nomeColuna(argument):
    argument.columns.values[0] = "id"
    res = argument.columns.values[0]
    # displaying column
    # print("Displaying column names : ",res)
    return res
    
# Delete Outliers
def apagar_dados(df,i):
    #if (df.loc[i, 'AreaTotal_ha'] < 0.1 or df.loc[i, 'GrupoCausa'] == "Reacendimentos" or df.loc[i, 'DSR'] == 'A' or df.loc[i, 'Duracao_Horas'] == 'A'):
    #    df = df.drop(i)
    if(df.loc[i, 'DSR'] == 'A'):
        df=df.drop(i)
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




# Remove extra Data
classe0 = 13
classe1 = 23
classe2 = 2
classe3 = 18

def dec(df,i):
    if(df.loc[i,'ClasseArea']==0):
        dec.i0-=1
        if(dec.i0>0):
            return True
        dec.i0=classe0    
    elif(df.loc[i,'ClasseArea']==1):
        dec.i1-=1
        if(dec.i1>0):
            return True
        dec.i1=classe1
    elif(df.loc[i,'ClasseArea']==2):
        dec.i2-=1
        if(dec.i2>0):
            return True
        dec.i2=classe2
    elif(df.loc[i,'ClasseArea']==3):
        dec.i3-=1
        if(dec.i3>10):
            return True
        elif(dec.i3>0):
            return False
        dec.i3=classe3
    return False

dec.i0=classe0
dec.i1=classe1
dec.i2=classe2
dec.i3=classe3