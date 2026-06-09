import streamlit as st
import pandas as pd
import random
import os

# ==========================================
# 1. CONFIGURACIÓN MODO DIOS
# ==========================================
st.set_page_config(page_title="Quiniela Blindamos 2026", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; color: #ffffff; }
    h1, h2, h3, h4 { color: #f39c12 !important; font-family: 'Helvetica Neue', sans-serif; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #2b2b2b; color: white; border-radius: 6px 6px 0px 0px; padding: 12px 24px; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #f39c12 !important; color: black !important; }
    .card-sabias { background-color: #262626; border-left: 5px solid #f39c12; padding: 15px; border-radius: 4px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. BANDERAS & TRIVIAS
# ==========================================
BANDERAS = {
    "USA": "🇺🇸", "MEXICO": "🇲🇽", "CANADA": "🇨🇦", "ARGENTINA": "🇦🇷", "BRAZIL": "🇧🇷", "BRASIL": "🇧🇷",
    "FRANCE": "🇫🇷", "SPAIN": "🇪🇸", "ESPAÑA": "🇪🇸", "GERMANY": "🇩🇪", "ITALY": "🇮🇹", "ENGLAND": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "URUGUAY": "🇺🇾", "COLOMBIA": "🇨🇴", "VENEZUELA": "🇻🇪", "CHILE": "🇨🇱", "PERU": "🇵🇪", "PERÚ": "🇵🇪",
    "ECUADOR": "🇪🇨", "PARAGUAY": "🇵🇾", "BOLIVIA": "🇧🇴", "NETHERLANDS": "🇳🇱", "PAISES BAJOS": "🇳🇱",
    "PORTUGAL": "🇵🇹", "BELGIUM": "🇧🇪", "BÉLGICA": "🇧🇪", "CROATIA": "🇭🇷", "CROACIA": "🇭🇷",
    "JAPAN": "🇯🇵", "JAPON": "🇯🇵", "SOUTH KOREA": "🇰🇷", "COREA DEL SUR": "🇰🇷", "MOROCCO": "🇲🇦", 
    "SENEGAL": "🇸🇳", "SAUDI ARABIA": "🇸🇦", "AUSTRALIA": "🇦🇺", "SWITZERLAND": "🇨🇭", "SUIZA": "🇨🇭"
}

def obtener_bandera(pais):
    if pd.isna(pais): return "🏳️"
    return BANDERAS.get(str(pais).strip().upper(), "🏳️")

TRIVIAS = [
    "¡El Mundial 2026 será el primero con 48 equipos!",
    "Talleres Blindamos protege tu pasión: Primer mundial en 3 países (USA, México y Canadá).",
    "El Estadio Azteca albergará su tercer partido inaugural.",
    "La gran final será en el MetLife Stadium de Nueva Jersey."
]

# ==========================================
# 3. CARGA DE DATOS & SIDEBAR
# ==========================================
@st.cache_resource
def cargar_base_datos():
    return pd.ExcelFile("excel-mundial-2026-multiideasweb.xlsx")

with st.sidebar:
    # 🔥 Logo recuperado
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("### 🛡️ TALLERES BLINDAMOS EN EL MUNDIAL 2026")
    
    st.markdown("---")
    usuario_actual = st.text_input("👤 Tu Nombre (Ej: Alvaro Giménez)", placeholder="Ingresa tu nombre para jugar")
    st.markdown("---")
    
    # 🔥 Trivias recuperadas
    st.markdown("### 💡 ¿Sabías qué? Mundial 2026")
    st.markdown(f"<div class='card-sabias'>{random.choice(TRIVIAS)}</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("⚡ *Configurado por Blindamos IT*")

# ==========================================
# 4. MOTOR PRINCIPAL
# ==========================================
try:
    xls = cargar_base_datos()
    
    pestanas_ocultas = ["SETTINGS", "PRINT", "POOL", "PREDICTOR"]
    pestanas_visibles = [h for h in xls.sheet_names if h not in pestanas_ocultas]
    pestanas_visibles.insert(1, "🏆 POSICIONES (RANKING)")
    
    tabs = st.tabs(pestanas_visibles)
    
    for idx, nombre_hoja in enumerate(pestanas_visibles):
        with tabs[idx]:
            if nombre_hoja == "🏆 POSICIONES (RANKING)":
                st.subheader("🏆 Ranking Oficial Blindamos")
                if os.path.exists("puntajes.csv"):
                    df_puntajes = pd.read_csv("puntajes.csv")
                    st.dataframe(df_puntajes.sort_values(by="Puntos", ascending=False), use_container_width=True, hide_index=True)
                else:
                    st.info("La tabla está limpia. ¡Registra tus pronósticos para ser el primero en liderar!")

            elif nombre_hoja == "FIXTURE":
                st.subheader("⚽ Central de Predicciones")
                df_fix = pd.read_excel(xls, sheet_name="FIXTURE", skiprows=1).dropna(subset=['HOME TEAM', 'AWAY TEAM'])
                
                for index, row in df_fix.iterrows():
                    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 3])
                    col1.markdown(f"<h4 style='text-align: right;'>{obtener_bandera(row['HOME TEAM'])} {row['HOME TEAM']}</h4>", unsafe_allow_html=True)
                    col2.number_input("", min_value=0, step=1, key=f"h_{index}", label_visibility="collapsed")
                    col3.markdown("<h4 style='text-align: center; color: #f39c12;'>VS</h4>", unsafe_allow_html=True)
                    col4.number_input("", min_value=0, step=1, key=f"a_{index}", label_visibility="collapsed")
                    col5.markdown(f"<h4 style='text-align: left;'>{row['AWAY TEAM']} {obtener_bandera(row['AWAY TEAM'])}</h4>", unsafe_allow_html=True)
                    st.markdown("---")
                    
                if st.button("Guardar Mis Pronósticos Oficiales 🏆"):
                    if not usuario_actual:
                        st.error("⚠️ Identifícate: Ingresa tu nombre en el menú lateral antes de guardar.")
                    else:
                        nuevo_registro = {"Jugador": usuario_actual, "Puntos": 0}
                        if os.path.exists("puntajes.csv"):
                            df_p = pd.read_csv("puntajes.csv")
                            if usuario_actual not in df_p["Jugador"].values:
                                df_p = pd.concat([df_p, pd.DataFrame([nuevo_registro])], ignore_index=True)
                                df_p.to_csv("puntajes.csv", index=False)
                        else:
                            pd.DataFrame([nuevo_registro]).to_csv("puntajes.csv", index=False)
                        st.success(f"¡Atención equipo! Pronósticos de {usuario_actual} guardados y encriptados.")

            elif nombre_hoja == "HOME":
                st.subheader("🏁 Centro de Control Blindamos")
                st.markdown("Navega por las pestañas superiores para registrar tus pronósticos y ver tu posición en la tabla.")
            
            elif nombre_hoja in ["PLAYERS", "JUGADORES"]:
                st.subheader("🔟 Los Números 10 del Mundial")
                df_players = pd.read_excel(xls, sheet_name=nombre_hoja, skiprows=1).dropna(subset=['TEAM', 'PLAYER'])
                cols = st.columns(3)
                for i, row in enumerate(df_players.iterrows()):
                    with cols[i % 3]:
                        st.markdown(f"<div style='background-color:#222; padding:15px; border-radius:8px; text-align:center;'><h3>{obtener_bandera(row[1]['TEAM'])} {row[1]['TEAM']}</h3><p style='font-size: 24px; margin: 0;'>👤 <b>{row[1]['PLAYER']}</b></p></div><br>", unsafe_allow_html=True)
            
            else:
                st.subheader(f"📊 {nombre_hoja}")
                st.dataframe(pd.read_excel(xls, sheet_name=nombre_hoja, skiprows=3).dropna(how='all'), use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"⚠️ Error: {e}")
