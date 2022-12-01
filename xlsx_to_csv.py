# importing pandas module
import pandas as pd

# Reading an excel file
excelFile = pd.read_excel("excel/pinheiro_bravo.xlsx")

# Converting excel file into CSV file
excelFile.to_csv("datasets/pinheiro_bravo.csv", index = None, header=True)

# Reading and Converting the output csv file into a dataframe object
dataframeObject = pd.DataFrame(pd.read_csv("datasets/pinheiro_bravo.csv"))

# Displaying the dataframe object
dataframeObject