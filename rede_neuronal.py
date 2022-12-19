import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import classification_report,confusion_matrix,ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split

# Read Dataset
df = pd.read_csv('datasets/fogos_tratados2.csv') 
df.describe().transpose()

# Creating Arrays for the Features and the Response Variable
target_column = ['ClasseArea'] 
predictors = list(set(list(df.columns))-set(target_column))
df[predictors] = df[predictors]/df[predictors].max()
df.describe().transpose()

# Creating the Training and Test Datasets
X = df[predictors].values
y = df[target_column].values

X_train, X_test, y_train, y_test = train_test_split(X, y.ravel(), test_size=0.25, random_state=40)

# Neural Network
mlp = MLPClassifier(hidden_layer_sizes=(8,8,8), activation='relu', solver='adam', max_iter=5000)
mlp.fit(X_train,y_train)

predict_train = mlp.predict(X_train)
predict_test = mlp.predict(X_test)
cm = confusion_matrix(y_test,predict_test)
print('=== Confusion Matrix ===')
print(cm)
print('\n=== Classification Report ===')
print(classification_report(y_test,predict_test))

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=mlp.classes_)
disp.plot()

plt.show()

# ref: https://www.pluralsight.com/guides/machine-learning-neural-networks-scikit-learn