import pandas as pd
import matplotlib.pyplot as plt
import time
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix,ConfusionMatrixDisplay, accuracy_score
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

def modelo_rede():
    # Read Dataset
    df = pd.read_csv('datasets/fogos_tratados.csv') 
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

    X_train, X_test, y_train, y_test = train_test_split(X, y.ravel(), test_size=0.25, random_state=40)

    # Neural Network
    print("Running...")
    tempo0 = time.time()
    mlp = MLPClassifier(hidden_layer_sizes=(8,8,8), activation='relu', solver='adam', max_iter=5000, learning_rate='adaptive')
    mlp.fit(X_train,y_train)
    predict_test = mlp.predict(X_test)
    tempo = time.time() - tempo0

    # Classification Report
    print('\n=== Classification Report ===')
    print(classification_report(y_test,predict_test))

    # Time it took to run the model
    print("It took", round(tempo, 2), "seconds to fit the model")

    # Accuracy - The number of all correct predictions divided by the total number of observations
    accuracy = accuracy_score(y_test, predict_test)
    print('Accuracy =', round(accuracy*100, 2), '%')

    # Matriz de confusão
    cm = confusion_matrix(y_test,predict_test)
    print('=== Confusion Matrix ===')
    print(cm)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=mlp.classes_)
    disp.plot()
    plt.show()

    # ref: https://www.pluralsight.com/guides/machine-learning-neural-networks-scikit-learn