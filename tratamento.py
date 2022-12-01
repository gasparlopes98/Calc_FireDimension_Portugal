import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cv2


# Function to convert number into string
# Switcher is dictionary data type here
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
    return switcher.get(argument, "nothing")

concelhos = {'Caldas da Rainha', 'Tomar', 'Penafiel', 'Guimarães', 'Chaves'}

df = pd.read_csv('datasets/fogos.csv')

# Removing irrelevant data
# df.pop('title')

# Creating new Column
df['Sub_Região'] = 0

# Adding values to contrast
for i in range(len(df)):
    if(df.loc[i, 'Concelho'] in concelhos):
        df.loc[i, 'Sub_Região'] = sub_regioes(df.loc[i, 'Concelho'])
    else:
        df.loc[i, 'Sub_Região'] = sub_regioes(df.loc[i, 'Distrito'])
 
# Saving new data base
df.to_csv('datasets/fogos_tratado.csv')