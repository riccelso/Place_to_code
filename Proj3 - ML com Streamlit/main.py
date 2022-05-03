from typing import Union
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.svm import SVC # Suport Vector Machine
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    plot_confusion_matrix,
    plot_roc_curve,
    plot_precision_recall_curve,
    precision_score,
    recall_score
)
from sklearn.model_selection import train_test_split as tts
import warnings
import sys


@st.cache(persist=True)
def load(url: str, columns_names=None) -> pd.DataFrame:
    data = pd.read_csv(url, header=None, names=columns_names)
    df_origin = data.copy()

    lab = LabelEncoder()

    for c in data.columns: 
        data[c] = lab.fit_transform(data[c])
    
    return data, df_origin


@st.cache(persist=True)
def split(df: Union[pd.DataFrame, np.ndarray]) -> tuple:
    y = df.target
    X = df.drop('target', axis=1)
    Xtrain, Xtest, ytrain, ytest = tts(X, y, test_size=0.4, random_state=23)

    return Xtrain, Xtest, ytrain, ytest


def plotmetrics(metrics: Union[tuple, list, set, np.ndarray], model, X, y):
    if "Confusion Matrix" in metrics:
        st.subheader("Confusion Matrix")
        plot_confusion_matrix(model, X, y)
        st.pyplot()
    if "ROC Curve" in metrics:
        st.subheader("ROC Curve")
        plot_roc_curve(model, X, y)
        st.pyplot()
    if "Precision Recall Curve" in metrics:
        st.subheader("Precision Recall Curve")
        plot_precision_recall_curve(model, X, y)
        st.pyplot()
    




if __name__ == '__main__':
    if not sys.warnoptions:
        warnings.simplefilter("ignore")

    url = r'https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data'
    
    columns_names = [
        'target',
        'cap-share',
        'cap-surface',
        'cap-color',
        'bruises',
        'odor',
        'gill-attachment',
        'gill-spacing',
        'gill-size',
        'gill-color',
        'stalk-shape',
        'stalk-root',
        'stalk-surface-above-ring',
        'stalk-surface-below-ring',
        'stalk-color-above-ring',
        'stalk-color-below-ring',
        'veil-type',
        'veil-color',
        'ring-number',
        'ring-type',
        'spore-print-color',
        'population',
        'habitat'
    ]

    df, df_origin = load(url, columns_names)

    Xtrain, Xtest, ytrain, ytest = split(df)

    if st.sidebar.checkbox("Ver dados:", False):
        st.subheader("Vizualização dos dados:")
        st.write(df_origin)
        st.subheader("Dados Pre-Processados:")
        st.write(df)
    
    class_names = ["Comestível", "Venenoso"]

    st.set_option('deprecation.showPyplotGlobalUse', False)

    st.sidebar.subheader("Escolha o modelo preditivo de classificação:")
    class_model = st.sidebar.selectbox(
        "Classificador",
        ("Support Vector Machine", "Logistic Regression", "Random Forest")
        )
    
    if class_model == "Support Vector Machine":
        st.sidebar.subheader("Hyperparâmetros")
        c = st.sidebar.number_input("C (Parâmetro de regulação)", 0.01, 10.0, step=0.01, key="C")
        kernel = st.sidebar.radio("Kernel", ("rbf", "linear"), key="kernel")
        gamma = st.sidebar.radio("Gamma (Coefficiente do kernel)", ("scale", "auto"), key="gamma")
        metrics = st.sidebar.multiselect("Qual métrica usar?", ("Confusion Matrix", "ROC Curve", "Precision-Recall Curve"))
        st.set_option("deprecation.showPyplotGlobalUse", False)

        if st.sidebar.button("Classify", key="classify"):
            st.subheader("Support Vector Machine -> resultados:")
            model = SVC(C=c, kernel=kernel, gamma=gamma)
            model.fit(Xtrain, ytrain)
            accuracy = model.score(Xtest, ytest)
            ypred = model.predict(Xtest)
            st.write("Accuracy: ", accuracy.round(2))
            st.write("Precision: ", precision_score(ytest, ypred, labels=class_names).round(2))
            st.write("Recall: ", recall_score(ytest, ypred, labels=class_names).round(2))
            plotmetrics(metrics, model, Xtest, ytest)

    
    if class_model == "Logistic Regression":
        st.sidebar.subheader("Hyperparâmetros")
        c = st.sidebar.number_input("C (Parâmetro de regulação)", 0.01, 10.0, step=0.01, key="C")
        max_iter = st.sidebar.slider("Máximo de interações", 100, 500, key="max iter")
        metrics = st.sidebar.multiselect("Qual métrica usar?", ("Confusion Matrix", "ROC Curve", "Precision-Recall Curve"))
        st.set_option("deprecation.showPyplotGlobalUse", False)

        if st.sidebar.button("Classify", key="classify"):
            st.subheader("Logistic Regression -> resultados:")
            model = LogisticRegression(C=c, max_iter=max_iter)
            model.fit(Xtrain, ytrain)
            accuracy = model.score(Xtest, ytest)
            ypred = model.predict(Xtest)

            st.write("Accuracy: ", accuracy.round(2))
            st.write("Precision: ", precision_score(ytest, ypred, labels=class_names).round(2))
            st.write("Recall: ", recall_score(ytest, ypred, labels=class_names).round(2))
            plotmetrics(metrics, model, Xtest, ytest)

    
    if class_model == "Random Forest":
        st.sidebar.subheader("Hyperparâmetros")
        n_estimators = st.sidebar.number_input("Número de árvores", 100, 5000, step=10, key="n_estimators")
        max_depth = st.sidebar.number_input("Profundidade", 1, 20, step=1, key="max_depth")
        bootstrap = st.sidebar.radio("Amostras (bootstrap)", ("True", "False"), key="bootstrap")
        metrics = st.sidebar.multiselect("Qual métrica usar?", ("Confusion Matrix", "ROC Curve", "Precision-Recall Curve"))
        st.set_option("deprecation.showPyplotGlobalUse", False)

        if st.sidebar.button("Classify", key="classify"):
            st.subheader("Random Forest -> resultados:")
            model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, bootstrap=bootstrap, n_jobs=-1)
            model.fit(Xtrain, ytrain)
            accuracy = model.score(Xtest, ytest)
            ypred = model.predict(Xtest)

            st.write("Accuracy: ", accuracy.round(2))
            st.write("Precision: ", precision_score(ytest, ypred, labels=class_names).round(2))
            st.write("Recall: ", recall_score(ytest, ypred, labels=class_names).round(2))
            plotmetrics(metrics, model, Xtest, ytest)