import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, accuracy_score, classification_report
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
import time

# Ler CSV
df = pd.read_csv("datasets/fogos_tratados3.csv")
df.describe().transpose()

# Creating Arrays for the Features and the Response Variable
target_column = ['ClasseArea'] 
predictors = list(set(list(df.columns))-set(target_column))
df[predictors] = df[predictors]/df[predictors].max()
df.describe().transpose()

# Creating the Training and Test Datasets
X = df[predictors].values
y = df[target_column].values

# SMOTE
sm = SMOTE(random_state=2022)
X, y = sm.fit_resample(X, y)

X_train, X_test, y_train, y_test = train_test_split(X, y.ravel(), test_size=0.25, random_state=2022)

print("Which model do you want to use?")
print("1 - Decision Tree Classifier")
print("2 - Random Forest Model")
modelo = 0

while (modelo != 1 and modelo != 2):
    modelo = int(input("Model: "))
    if (modelo == 1):
        print("Running...")
        tempo0 = time.time()

        # Create an instance of a Decision Tree classifier
        # Defining the random_state for reproducibility
        clf = DecisionTreeClassifier(random_state=2022)

        # Training, i.e., fitting the model (using the training data!!)
        clf.fit(X_train, y_train)

        # Predictions for the test set
        predictions = clf.predict(X_test)
        #print(predictions)

        tempo = time.time() - tempo0
    elif (modelo == 2):
        print("Running...")
        tempo0 = time.time()

        # Fit a Random Forest model
        clf = RandomForestClassifier(n_estimators=100, max_features="auto", class_weight="balanced", random_state=2022)
        clf.fit(X_train, y_train)
        predictions = clf.predict(X_test)

        tempo = time.time() - tempo0
    else:
        print("Please, select a valid option!")

# Classification Report
print(classification_report(y_test, predictions))

# Time it took to run the model
print("It took", round(tempo, 2), "seconds to fit the model")

# Accuracy - The number of all correct predictions divided by the total number of observations
accuracy = accuracy_score(y_test, predictions)
print('Accuracy =', round(accuracy*100, 2), '%')

# Matriz de confusão
matriz_confusao = confusion_matrix(y_test, predictions)
print(matriz_confusao)
disp = ConfusionMatrixDisplay(confusion_matrix=matriz_confusao, display_labels=clf.classes_)
disp.plot()
plt.show()