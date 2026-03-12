import streamlit as st
import pandas as pd
import joblib

# Configuração da página (deve ser a primeira instrução Streamlit)
st.set_page_config(page_title="Preditor de Tsunami", page_icon="🌊", layout="wide")

# Estilo CSS personalizado para melhorar a estética
st.markdown("""
    <style>
    .main {
        background-color: #6276b3;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Carregar modelo
@st.cache_resource
def load_model():
    return joblib.load("models/modelo_tsunami_normalizado.pkl")

modelo = load_model()

# Título e Subtítulo
st.title("🌊 Previsão de Tsunami")
st.markdown("Insira os dados geológicos abaixo para prever a probabilidade de ocorrência de um tsunami com base no modelo **SVC**.")

# Organização em Colunas
st.subheader("📍 Parâmetros do Evento")
col1, col2, col3 = st.columns(3)
#Dividir em 3 colunas
with col1:
    magnitude = st.number_input("Magnitude (0-10)", 0.0, 10.0, 6.5, step=0.1)
    cdi = st.slider("CDI (Intensidade)", 0, 10, 5)
    mmi = st.slider("MMI (Intensidade Mercalli)", 0, 10, 5)

with col2:
    sig = st.number_input("Sig (Significância)", 0, 2000, 500)
    nst = st.number_input("NST (Estações)", 0, 1000, 500)
    dmin = st.number_input("Dmin (Distância)", 0.0, 50.0, 1.0)

with col3:
    gap = st.number_input("Gap (Ângulo)", 0.0, 50.0, 10.0)
    depth = st.number_input("Depth (Profundidade km)", 0.0, 700.0, 10.0)

#Expandir Coordenadas
# Coordenadas numa secção separada (ou sidebar)
with st.expander("🌐 Coordenadas Geográficas"):
    c_lat, c_lon = st.columns(2)
    latitude = c_lat.number_input("Latitude", -90.0, 90.0, 0.0)
    longitude = c_lon.number_input("Longitude", -180.0, 180.0, 0.0)

# Preparar dados
entrada = pd.DataFrame([[magnitude, cdi, mmi, sig, nst, dmin, gap, depth, latitude, longitude]],
                       columns=['magnitude', 'cdi', 'mmi', 'sig', 'nst', 'dmin', 'gap', 'depth', 'latitude', 'longitude'])

st.divider()

# Botão de Previsão
if st.button("Executar Análise de Risco"):
    with st.spinner('A processar dados...'):
        pred = modelo.predict(entrada)
        # Probabilidades (se o teu SVC tiver probability=True)
        # prob = modelo.predict_proba(entrada)[0][1] 
        
    st.subheader("Resultado da Previsão:")
    
    if pred[0] == 1:
        st.error("⚠️ **ALERTA: Possibilidade de Tsunami Detetada**")
        st.warning("Recomenda-se a verificação imediata dos protocolos de segurança.")
    else:
        st.success("✅ **SISTEMA ESTÁVEL: Sem evidência de Tsunami**")
        st.info("Os parâmetros analisados não indicam risco iminente.")

# Rodapé simples
st.caption("Nota: Utiliza o modelo SVC e normalização RobustScaler.")

#MELHORADO COM GEMINI