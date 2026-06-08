
import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Quiniela Blindamos", page_icon="🛡️", layout="centered")

# 2. Estilos corporativos de Blindamos
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; color: #ffffff; }
    h1, h2, h3 { color: #f39c12 !important; font-family: 'Helvetica Neue', sans-serif; }
    div.stButton > button:first-child { background-color: #f39c12 !important; color: black !important; font-weight: bold; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ Quiniela Blindamos")
st.subheader("Ingresa tus pronósticos")

# 3. Leer el archivo con todos los partidos automáticamente
@st.cache_data
def cargar_partidos():
    # Lee tu archivo de GitHub detectando automáticamente si usa comas o puntos y comas
    return pd.read_csv("resultados_quiniela.csv", sep=None, engine="python")

try:
    df = cargar_partidos()
    
    # 4. Crear las pestañas (labels de arriba) basadas en las Fases del Excel
    fases = df['Fase'].unique()
    tabs = st.tabs([str(f) for f in fases])
    
    # 5. Organizar los partidos automáticamente dentro de cada pestaña
    for i, fase in enumerate(fases):
        with tabs[i]:
            st.write(f"### Partidos de {fase}")
            partidos_fase = df[df['Fase'] == fase]
            
            for index, row in partidos_fase.iterrows():
                col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 3])
                
                with col1:
                    st.markdown(f"<p style='text-align: right; font-size: 18px; margin-top: 10px;'><b>{row['Local']}</b></p>", unsafe_allow_html=True)
                with col2:
                    st.number_input("", min_value=0, step=1, key=f"loc_{row['ID']}", label_visibility="collapsed")
                with col3:
                    st.markdown("<p style='text-align: center; font-size: 18px; color: #f39c12; margin-top: 10px;'><b>VS</b></p>", unsafe_allow_html=True)
                with col4:
                    st.number_input("", min_value=0, step=1, key=f"vis_{row['ID']}", label_visibility="collapsed")
                with col5:
                    st.markdown(f"<p style='text-align: left; font-size: 18px; margin-top: 10px;'><b>{row['Visitante']}</b></p>", unsafe_allow_html=True)
                
                st.markdown("---")
                
    # 6. Botón para guardar
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Guardar Mis Pronósticos 🏆"):
        st.success("¡Excelente PELE! Tus pronósticos fueron guardados en el sistema de Blindamos. ¡Mucha suerte!")
        
except Exception as e:
    st.error("No se pudo cargar el archivo resultados_quiniela.csv. Por favor verifica que esté guardado en GitHub.")
