import numpy as np
import pandas as pd
from datetime import datetime
import cv2

df = pd.read_csv("DadosConcatenados.csv")

# Removing irrelevant data (Only for the first time!)
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

#Creating new Column
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

# Saving new data base
df.to_csv('datasetDadosTratados.csv')


