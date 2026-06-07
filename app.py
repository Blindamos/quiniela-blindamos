import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. CONFIGURACIÓN Y ESTILOS CORPORATIVOS ---
st.set_page_config(page_title="Quiniela Blindamos - Mundial 2026", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; color: #ffffff; }
    h1, h2, h3 { color: #f39c12 !important; font-family: 'Helvetica Neue', sans-serif; }
    .css-1r6slb0, .stForm { background-color: #262626 !important; border: 1px solid #333333; border-radius: 10px; padding: 20px; }
    div.stButton > button:first-child { background-color: #f39c12 !important; color: black !important; font-weight: bold !important; border-radius: 5px; width: 100%; height: 3em; }
    div.stButton > button:first-child:hover { background-color: #e67e22 !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. CABECERA Y LOGO ---
ruta_logo = "logo.png"
if os.path.exists(ruta_logo):
    st.image(ruta_logo, use_container_width=True)
else:
    st.title("🛡️ BLINDAMOS")
st.subheader("🏆 Quiniela Corporativa - Mundial 2026")
st.markdown("---")

# --- 3. DICCIONARIO DE BANDERAS (PREMIUM) ---
banderas = {
    'USA': '🇺🇸', 'Mexico': '🇲🇽', 'Canada': '🇨🇦', 'Uruguay': '🇺🇾', 'Argentina': '🇦🇷', 
    'Brazil': '🇧🇷', 'Ecuador': '🇪🇨', 'Colombia': '🇨🇴', 'Spain': '🇪🇸', 'France': '🇫🇷', 
    'Germany': '🇩🇪', 'England': '🏴󠁧󠁢󠁥󠁮󠁧󠁿', 'Portugal': '🇵🇹', 'Italy': '🇮🇹', 'Netherlands': '🇳🇱', 
    'Belgium': '🇧🇪', 'Croatia': '🇭🇷', 'Denmark': '🇩🇰', 'Switzerland': '🇨🇭', 'Poland': '🇵🇱', 
    'Serbia': '🇷🇸', 'Wales': '🏴󠁧󠁢󠁷󠁬󠁳󠁿', 'Scotland': '🏴󠁧󠁢󠁳󠁣󠁴󠁿', 'Ukraine': '🇺🇦', 'Czech Republic': '🇨🇿', 
    'Austria': '🇦🇹', 'Hungary': '🇭🇺', 'Greece': '🇬🇷', 'Turkey': '🇹🇷', 'Japan': '🇯🇵', 
    'South Korea': '🇰🇷', 'Australia': '🇦🇺', 'Iran': '🇮🇷', 'Saudi Arabia': '🇸🇦', 'Qatar': '🇶🇦', 
    'Senegal': '🇸🇳', 'Morocco': '🇲🇦', 'Cameroon': '🇨🇲', 'Ghana': '🇬🇭', 'Nigeria': '🇳🇬', 
    'Ivory Coast': '🇨🇮', 'South Africa': '🇿🇦', 'Algeria': '🇩🇿', 'Egypt': '🇪🇬', 
    'Costa Rica': '🇨🇷', 'Panama': '🇵🇦', 'Honduras': '🇭🇳', 'Jamaica': '🇯🇲'
}

def obtener_bandera(pais):
    return f"{banderas.get(pais, '🏳️')} {pais}"

# --- 4. CONEXIÓN A TU GOOGLE SHEETS (PANEL DE CONTROL) ---
# Usamos tu enlace y lo convertimos a formato de lectura de datos
sheet_url = "https://docs.google.com/spreadsheets/d/1I7gXA3LsVZ0tmLziT8H3xM0lD_BlvFgpGd4E0tSgrYQ/export?format=csv"

@st.cache_data(ttl=60) # Actualiza los partidos nuevos cada minuto
def cargar_partidos():
    try:
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip() # Limpia espacios en blanco
        return df
    except Exception as e:
        return None

df_partidos = cargar_partidos()

# --- 5. INTERFAZ DEL FORMULARIO ---
with st.form("registro_quiniela"):
    st.markdown("### 📝 Datos del Colaborador")
    # Colocamos un ejemplo corporativo en el cajón de texto
    nombre = st.text_input("Nombre y Apellido:", placeholder="Ej. Alejandro Saravia")
    departamento = st.selectbox("Departamento / Área:", ["Operaciones", "Ventas", "Administración", "Taller de Blindaje", "Dirección", "Otro"])
    
    st.markdown("---")
    st.markdown("### ⚽ Tus Pronósticos")
    
    resultados_usuario = {}
    
    # Verificamos que la hoja de Google Sheets tenga información
    if df_partidos is not None and not df_partidos.empty:
        if set(['ID', 'Local', 'Visitante', 'Fase']).issubset(df_partidos.columns):
            
            for index, row in df_partidos.iterrows():
                p_id = row['ID']
                local = str(row['Local']).strip()
                visitante = str(row['Visitante']).strip()
                fase = str(row['Fase']).strip()
                
                st.markdown(f"**Partido {p_id} | Fase: {fase}**")
                col1, col2, col3 = st.columns([3, 1, 3])
                
                with col1:
                    st.markdown(f"<div style='text-align: right; font-size: 1.1em;'>{obtener_bandera(local)}</div>", unsafe_allow_html=True)
                    goles_l = st.number_input("Goles L.", min_value=0, max_value=15, step=1, key=f"l_{p_id}", label_visibility="collapsed")
                    
                with col2:
                    st.markdown("<h3 style='text-align: center; color: gray; margin-top: -10px;'>VS</h3>", unsafe_allow_html=True)
                    
                with col3:
                    st.markdown(f"<div style='text-align: left; font-size: 1.1em;'>{obtener_bandera(visitante)}</div>", unsafe_allow_html=True)
                    goles_v = st.number_input("Goles V.", min_value=0, max_value=15, step=1, key=f"v_{p_id}", label_visibility="collapsed")
                    
                resultados_usuario[f"P{p_id}_{local}"] = goles_l
                resultados_usuario[f"P{p_id}_{visitante}"] = goles_v
                st.markdown("<hr style='margin: 0.5em 0px; border-top: 1px solid #333;'>", unsafe_allow_html=True)
        else:
            st.error("⚠️ Tu Google Sheets no tiene los títulos correctos. Asegúrate de poner: ID, Local, Visitante, Fase en la primera fila.")
    else:
        st.info("Cargando partidos... (Si no aparecen, asegúrate de haberlos escrito en tu Google Sheets).")

    enviar = st.form_submit_button("Guardar Mis Pronósticos 🏆")
    
    # --- 6. GUARDAR RESULTADOS ---
    if enviar:
        if nombre.strip() == "":
            st.error("❌ Por favor, escribe tu nombre en la parte de arriba.")
        elif df_partidos is None or df_partidos.empty:
             st.error("❌ No hay partidos para guardar. Avisa a administración.")
        else:
            registro = {
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Nombre": nombre,
                "Departamento": departamento
            }
            registro.update(resultados_usuario)
            
            df_nuevo = pd.DataFrame([registro])
            archivo_csv = "resultados_quiniela.csv"
            
            if os.path.exists(archivo_csv):
                df_nuevo.to_csv(archivo_csv, mode='a', header=False, index=False)
            else:
                df_nuevo.to_csv(archivo_csv, mode='w', header=True, index=False)
                
            st.success(f"¡Excelente {nombre}! Tus pronósticos fueron guardados en el sistema de Blindamos. ¡Mucha suerte!")
            st.balloons()
