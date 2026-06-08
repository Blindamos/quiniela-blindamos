import streamlit as st
import pandas as pd
import random

# ==========================================
# 1. CONFIGURACIÓN MODO DIOS & ESTILOS
# ==========================================
st.set_page_config(page_title="Quiniela Blindamos 2026", page_icon="🛡️", layout="wide")

# Estilos premium negro y dorado Blindamos
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; color: #ffffff; }
    h1, h2, h3, h4 { color: #f39c12 !important; font-family: 'Helvetica Neue', sans-serif; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #2b2b2b; color: white; border-radius: 6px 6px 0px 0px; padding: 12px 24px; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #f39c12 !important; color: black !important; }
    .card-sabias { background-color: #262626; border-left: 5px solid #f39c12; padding: 15px; border-radius: 4px; margin-bottom: 15px; }
    .player-card { background-color: #222222; border: 1px solid #333333; padding: 15px; border-radius: 8px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DICCIONARIO MAESTRO DE BANDERAS (i18n robusto)
# ==========================================
BANDERAS = {
    "USA": "🇺🇸", "ESTADOS UNIDOS": "🇺🇸", "UNITED STATES": "🇺🇸",
    "MEXICO": "🇲🇽", "MÉXICO": "🇲🇽",
    "CANADA": "🇨🇦", "CANADÁ": "🇨🇦",
    "ARGENTINA": "🇦🇷", "BRAZIL": "🇧🇷", "BRASIL": "🇧🇷",
    "FRANCE": "🇫🇷", "FRANCIA": "🇫🇷", "SPAIN": "🇪🇸", "ESPAÑA": "🇪🇸",
    "GERMANY": "🇩🇪", "ALEMANIA": "🇩🇪", "ITALY": "🇮🇹", "ITALIA": "🇮🇹",
    "ENGLAND": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "INGLATERRA": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
}

def obtener_bandera(pais):
    if pd.isna(pais):
        return "🏳️"
    nombre_limpio = str(pais).strip().upper()
    return BANDERAS.get(nombre_limpio, "🏳️")

# ==========================================
# 3. BASE DE DATOS DE TRIVIA "¿SABÍAS QUÉ?"
# ==========================================
TRIVIAS = [
    "¡El Mundial 2026 será el primero en la historia con 48 equipos participantes en lugar de 32!",
    "Talleres Blindamos protege tu pasión: Este será el primer mundial organizado estratégicamente por tres países simultáneamente (USA, México y Canadá).",
    "El Estadio Azteca de México se convertirá en el primer estadio del mundo en albergar tres partidos de inauguración de la Copa del Mundo.",
    "La gran final del Mundial 2026 se jugará en el imponente MetLife Stadium en East Rutherford, Nueva Jersey.",
    "Se recorrerán más de 4,000 kilómetros entre las sedes más extremas del torneo, un reto logístico sin precedentes."
]

# ==========================================
# 4. CARGA CENTRAL DE DATOS (EXCEL)
# ==========================================
@st.cache_data
def cargar_base_datos():
    archivo_maestro = "excel-mundial-2026-multiideasweb.xlsx"
    return pd.ExcelFile(archivo_maestro)

# Sidebar corporativo permanente
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("### 🛡️ TALLERES BLINDAMOS")
    
    st.markdown("---")
    st.markdown("### 💡 ¿Sabías qué? Mundial 2026")
    st.markdown(f"<div class='card-sabias'>{random.choice(TRIVIAS)}</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("⚡ *Modo Dios Configurado por Wanda*")

# Control de ejecución principal
try:
    xls = cargar_base_datos()
    pestanas_excel = xls.sheet_names
    
    # Generación de la barra de navegación superior exacta a las etiquetas del Excel
    tabs = st.tabs(pestanas_excel)
    
    for idx, nombre_hoja in enumerate(pestanas_excel):
        with tabs[idx]:
            
            # --- HOJA HOME ---
            if nombre_hoja == "HOME":
                st.subheader("🏁 Bienvenido al Centro de Control de la Quiniela Mundialista")
                st.markdown("""
                ¡Todo listo para arrancar la competición interna en Blindamos! 
                Este sistema lee en tiempo real la configuración completa de tu libro de análisis. Navega por las pestañas de arriba para evaluar clasificaciones, plantillas y registrar scores.
                """)
                
            # --- HOJA FIXTURE (Central Operativa de Marcadores) ---
            elif nombre_hoja == "FIXTURE":
                st.subheader("⚽ Predicciones Oficiales del Torneo")
                df_fix = pd.read_excel(xls, sheet_name=nombre_hoja, skiprows=1)
                
                # Filtrar filas vacías para evitar errores de renderizado
                if 'HOME TEAM' in df_fix.columns and 'AWAY TEAM' in df_fix.columns:
                    df_fix = df_fix.dropna(subset=['HOME TEAM', 'AWAY TEAM'])
                    
                    for index, row in df_fix.iterrows():
                        flag_home = obtener_bandera(row['HOME TEAM'])
                        flag_away = obtener_bandera(row['AWAY TEAM'])
                        
                        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 3])
                        
                        with col1:
                            st.markdown(f"<h4 style='text-align: right;'>{flag_home} {row['HOME TEAM']}</h4>", unsafe_allow_html=True)
                        with col2:
                            st.number_input("", min_value=0, step=1, key=f"home_score_{index}", label_visibility="collapsed")
                        with col3:
                            st.markdown("<h4 style='text-align: center; color: #f39c12;'>VS</h4>", unsafe_allow_html=True)
                        with col4:
                            st.number_input("", min_value=0, step=1, key=f"away_score_{index}", label_visibility="collapsed")
                        with col5:
                            st.markdown(f"<h4 style='text-align: left;'>{row['AWAY TEAM']} {flag_away}</h4>", unsafe_allow_html=True)
                        st.markdown("---")
                        
                    if st.button("Guardar Mis Pronósticos Oficiales 🏆"):
                        st.success("¡Excelente PELE! Tus pronósticos blindados fueron procesados con éxito.")
                else:
                    st.warning("Estructura de columnas de FIXTURE no reconocida. Mostrando datos planos.")
                    st.dataframe(pd.read_excel(xls, sheet_name=nombre_hoja))

            # --- HOJA PLAYERS / NUMEROS 10 ---
            elif nombre_hoja in ["PLAYERS", "JUGADORES"]:
                st.subheader("🔟 Galería Estratégica: Los Números 10 del Mundial")
                df_players = pd.read_excel(xls, sheet_name=nombre_hoja, skiprows=1).dropna(subset=['TEAM', 'PLAYER'])
                
                cols = st.columns(3)
                for i, row in enumerate(df_players.iterrows()):
                    datos = row[1]
                    flag = obtener_bandera(datos['TEAM'])
                    with cols[i % 3]:
                        st.markdown(f"""
                        <div class='player-card'>
                            <h3>{flag} {datos['TEAM']}</h3>
                            <p style='font-size: 24px; margin: 0;'>👤 <b>{datos['PLAYER']}</b></p>
                            <p style='color: #f39c12; font-weight: bold; margin-top: 5px;'>Camiseta: N° 10</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)

            # --- TRATAMIENTO AUTOMÁTICO PARA TODAS LAS DEMÁS PESTAÑAS ---
            else:
                st.subheader(f"📊 Datos del Tablero: {nombre_hoja}")
                # Lee saltando los encabezados típicos estéticos del formato Excel
                df_generico = pd.read_excel(xls, sheet_name=nombre_hoja, skiprows=3).dropna(how='all')
                st.dataframe(df_generico, use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"⚠️ Alerta del Sistema: Asegúrate de que el archivo maestro 'excel-mundial-2026-multiideasweb.xlsx' esté subido en la raíz de tu GitHub junto a este script. Detalles: {e}")
