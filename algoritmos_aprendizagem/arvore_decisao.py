import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, accuracy_score, classification_report
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, AdaBoostClassifier, BaggingClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
import time

def modelo_arvore():

    # Ler CSV
    df = pd.read_csv("datasets/fogos_tratados.csv")
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

    X_train, X_test, y_train, y_test = train_test_split(X, y.ravel(), test_size=0.25, random_state=2022) # 25% para teste, 75% para treino

    print("Which model do you want to use?")
    print("1 - Decision Tree Classifier")
    print("2 - Random Forest Classifier")
    print("3 - Extremely Randomized Trees Classifier")
    print("4 - Adaptive Booster Classifier")
    print("5 - Bagging Classifier")
    print("6 - Gradient Boosting Classifier")
    print("7 - XGBoost Classifier")

    '''
    Treino:
    1 - Decision Tree Classifier                ~77.40% em ~3.16s
    2 - Random Forest Classifier                ~88.55% em ~50.34s
    3 - Extremely Randomized Trees Classifier   ~89.28% em ~19.65s
    4 - Adaptive Booster Classifier             ~30,25% em ~33.77s
    5 - Bagging Classifier                      ~87.63% em ~203.94s
    6 - Gradient Boosting Classifier            ~46.29% em ~581.21s
    7 - XGBoost Classifier                      ~71.34% em ~64.56s
    '''

    modelo = 0

    while modelo not in (1, 2, 3, 4, 5, 6, 7):
        modelo = int(input("Model: "))
        if (modelo == 1): # Decision Tree classifier
            print("Running...")
            tempo0 = time.time()

            # Defining the random_state for reproducibility
            clf = DecisionTreeClassifier(random_state=2022)

            # Training, i.e., fitting the model (using the training data!!)
            clf.fit(X_train, y_train)

            # Predictions for the test set
            predictions = clf.predict(X_test)

            tempo = time.time() - tempo0
        elif (modelo == 2): # Random Forest Classifier
            print("Running...")
            tempo0 = time.time()

            clf = RandomForestClassifier(n_estimators=100, max_features="auto", class_weight="balanced", random_state=2022)
            clf.fit(X_train, y_train)
            predictions = clf.predict(X_test)

            tempo = time.time() - tempo0
        elif (modelo == 3): # Extremely Randomized Trees Classifier
            print("Running...")
            tempo0 = time.time()

            clf = ExtraTreesClassifier(n_estimators=100, random_state=2022)
            clf.fit(X_train, y_train)
            predictions = clf.predict(X_test)

            tempo = time.time() - tempo0
        elif (modelo == 4): # Adaptive Booster Classifier
            print("Running...")
            tempo0 = time.time()

            clf = AdaBoostClassifier(n_estimators=100, learning_rate=1, random_state=2022)
            clf.fit(X_train, y_train)
            predictions = clf.predict(X_test)
        
            tempo = time.time() - tempo0
        elif (modelo == 5): # Bagging Classifier
            print("Running...")
            tempo0 = time.time()

            clf = BaggingClassifier(n_estimators=100, random_state=2022)
            clf.fit(X_train, y_train)
            predictions = clf.predict(X_test)
        
            tempo = time.time() - tempo0
        elif (modelo == 6): # Gradient Boosting Classifier
            print("Running...")
            tempo0 = time.time()

            clf = GradientBoostingClassifier(n_estimators=100, random_state=2022)
            clf.fit(X_train, y_train)
            predictions = clf.predict(X_test)
        
            tempo = time.time() - tempo0
        elif (modelo == 7): # XGBoost Classifier
            print("Running...")
            tempo0 = time.time()

            clf = XGBClassifier()
            clf.fit(X_train, y_train)
            predictions = clf.predict(X_test)

            tempo = time.time() - tempo0
        else:
            print("Please, select a valid option!")

    # Classification Report
    print('\n=== Classification Report ===')
    print(classification_report(y_test, predictions))

    # Time it took to run the model
    print("It took", round(tempo, 2), "seconds to fit the model")

    # Accuracy - The number of all correct predictions divided by the total number of observations
    accuracy = accuracy_score(y_test, predictions)
    print('Accuracy =', round(accuracy*100, 2), '%')

    # Matriz de confusão
    matriz_confusao = confusion_matrix(y_test, predictions)
    print('=== Confusion Matrix ===')
    print(matriz_confusao)
    disp = ConfusionMatrixDisplay(confusion_matrix=matriz_confusao, display_labels=clf.classes_)
    disp.plot()
    plt.show()