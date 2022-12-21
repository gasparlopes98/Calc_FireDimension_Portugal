import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Read Dataset
df = pd.read_csv('datasets/fogos_tratados2.csv')
#df.describe().transpose()
#Visualising the data using heatmap

plt.figure()
sns.heatmap(df.corr(),cmap='coolwarm')
#plt.show()

#Selecting the required parameters
target_column = ['ClasseArea']
predictors = list(set(list(df.columns))-set(target_column))
df[predictors] = df[predictors]/df[predictors].max()
#df.describe().transpose()

# Creating the Training and Test Datasets
x = df[predictors].values
y = df[target_column].values

#Split the data into training and testing dataset
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2,random_state = 0)

y_train = y_train.reshape(-1,1)
y_test = y_test.reshape(-1,1)

#Fit the model over the training dataset
model = LinearRegression()
model.fit(x_train,y_train)

#Calculate intercept and coefficient
print(model.intercept_)
print(model.coef_)

pred=model.predict(x_test)
predictions = pred.reshape(-1,1)

#Calculate root mean squared error to evaluate model performance
print('MSE : ', mean_squared_error(y_test,predictions))
print('RMSE : ', np.sqrt(mean_squared_error(y_test,predictions)))