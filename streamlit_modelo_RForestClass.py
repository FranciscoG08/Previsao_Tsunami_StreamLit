import streamlit as st
import pandas as pd
import joblib

# Carregar modelo pipeline (árvores não precisam de escalonamento)
modelo = joblib.load("models/modelo_tsunami_nao_normalizado.pkl")  # salva previamente

st.title("Previsão de Tsunami (Modelo Não Normalizado com RandomForestClassifier)")

# Entradas do utilizador (mesmas colunas)
magnitude = st.number_input("Magnitude", min_value=0.0, max_value=10.0, value=6.5)
cdi       = st.number_input("CDI", min_value=0, max_value=10, value=5)
mmi       = st.number_input("MMI", min_value=0, max_value=10, value=5)
sig       = st.number_input("Sig", min_value=0, max_value=2000, value=500)
nst       = st.number_input("NST", min_value=0, max_value=1000, value=500)
dmin      = st.number_input("Dmin", min_value=0.0, max_value=50.0, value=1.0)
gap       = st.number_input("Gap", min_value=0.0, max_value=50.0, value=10.0)
depth     = st.number_input("Depth", min_value=0.0, max_value=700.0, value=10.0)
latitude  = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=0.0)
longitude = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=0.0)

entrada = pd.DataFrame([[magnitude,cdi,mmi,sig,nst,dmin,gap,depth,latitude,longitude]],
                       columns=['magnitude','cdi','mmi','sig','nst','dmin','gap','depth','latitude','longitude'])

if st.button("Prever"):
    pred = modelo.predict(entrada)
    st.write("Previsão de Tsunami:", "Sim" if pred[0]==1 else "Não")