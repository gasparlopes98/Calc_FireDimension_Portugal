import pandas as pd
import os

#Parte 1 - Converter para csv

#file = pd.read_excel("Misc/Excel/Registos_Incendios_SGIF_2011_2020.xlsx")
#file.to_csv("Registos_Incendios_SGIF_2011_2020.csv",encoding='utf-8', index=False)
#file2 = pd.read_excel("Misc/Excel/Registos_Incendios_SGIF_2021.xlsx")
#file2.to_csv("Registos_Incendios_SGIF_2021.csv",encoding='utf-8', index=False)


#Parte 2 - Concatenar CSV

df = pd.read_csv("Registos_Incendios_SGIF_2011_2020.csv")
df2 = pd.read_csv("Registos_Incendios_SGIF_2021.csv")

mergedData = pd.concat([df,df2], ignore_index=True)

mergedData.to_csv("DadosConcatenados.csv")
