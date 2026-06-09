import streamlit as st
import pandas as pd
import random
import os
import json

# ==========================================
# 1. CONFIGURACIÓN MODO DIOS & WHITE-LABELING
# ==========================================
st.set_page_config(page_title="Quiniela Blindamos 2026", page_icon="🛡️", layout="wide")

# CSS para ocultar logos, menú de Streamlit y darle estilo premium
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #1a1a1a; color: #ffffff; }
    h1, h2, h3, h4 { color: #f39c12 !important; font-family: 'Helvetica Neue', sans-serif; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #2b2b2b; color: white; border-radius: 6px 6px 0px 0px; padding: 12px 24px; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #f39c12 !important; color: black !important; }
    .card-sabias { background-color: #262626; border-left: 5px solid #f39c12; padding: 15px; border-radius: 4px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. BASE DE DATOS Y ESTADO DE SESIÓN
# ==========================================
ARCHIVO_DB = "db_blindamos.csv"

def cargar_db():
    if os.path.exists(ARCHIVO_DB):
        return pd.read_csv(ARCHIVO_DB)
    return pd.DataFrame(columns=["Jugador", "PIN", "Puntos", "Predicciones"])

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["usuario"] = ""
    st.session_state["preds"] = {}

# ==========================================
# 3. DICCIONARIOS Y BANDERAS
# ==========================================
BANDERAS = {
    "USA": "🇺🇸", "MEXICO": "🇲🇽", "CANADA": "🇨🇦", "ARGENTINA": "🇦🇷", "BRAZIL": "🇧🇷", "BRASIL": "🇧🇷",
    "FRANCE": "🇫🇷", "SPAIN": "🇪🇸", "ESPAÑA": "🇪🇸", "GERMANY": "🇩🇪", "ITALY": "🇮🇹", "ENGLAND": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "URUGUAY": "🇺🇾", "COLOMBIA": "🇨🇴", "VENEZUELA": "🇻🇪", "CHILE": "🇨🇱", "PERU": "🇵🇪", "PERÚ": "🇵🇪",
    "ECUADOR": "🇪🇨", "PARAGUAY": "🇵🇾", "BOLIVIA": "🇧🇴", "NETHERLANDS": "🇳🇱", "PAISES BAJOS": "🇳🇱",
    "PORTUGAL": "🇵🇹", "BELGIUM": "🇧🇪", "BÉLGICA": "🇧🇪", "CROATIA": "🇭🇷", "CROACIA": "🇭🇷",
    "JAPAN": "🇯🇵", "JAPON": "🇯🇵", "SOUTH KOREA": "🇰🇷", "COREA DEL SUR": "🇰🇷"
}

def obtener_bandera(pais):
    if pd.isna(pais): return "🏳️"
    return BANDERAS.get(str(pais).strip().upper(), "🏳️")

@st.cache_resource
def cargar_excel():
    return pd.ExcelFile("excel-mundial-2026-multiideasweb.xlsx")

# ==========================================
# 4. SIDEBAR: SISTEMA DE LOGIN Y PIN
# ==========================================
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("### 🛡️ TALLERES BLINDAMOS")
    
    st.markdown("---")
    st.markdown("### 🔐 Acceso de Jugador")
    
    usuario_input = st.text_input("👤 Tu Nombre").strip().upper()
    pin_input = st.text_input("🔑 PIN Secreto (4 dígitos)", type="password").strip()
    
    if st.button("Entrar / Registrarse"):
        if len(usuario_input) > 1 and len(pin_input) >= 4:
            db = cargar_db()
            if usuario_input in db["Jugador"].values:
                # Usuario existe, validar PIN
                user_row = db[db["Jugador"] == usuario_input].iloc[0]
                if str(user_row["PIN"]) == pin_input:
                    st.session_state["logged_in"] = True
                    st.session_state["usuario"] = usuario_input
                    st.session_state["preds"] = json.loads(user_row["Predicciones"]) if pd.notna(user_row["Predicciones"]) else {}
                    st.success("¡Acceso concedido!")
                else:
                    st.error("PIN incorrecto.")
            else:
                # Usuario nuevo, registrar
                nueva_fila = pd.DataFrame([{"Jugador": usuario_input, "PIN": pin_input, "Puntos": 0, "Predicciones": "{}"}])
                db = pd.concat([db, nueva_fila], ignore_index=True)
                db.to_csv(ARCHIVO_DB, index=False)
                st.session_state["logged_in"] = True
                st.session_state["usuario"] = usuario_input
                st.session_state["preds"] = {}
                st.success("¡Registrado con éxito!")
        else:
            st.error("Ingresa un nombre y un PIN de al menos 4 números.")
            
    if st.session_state["logged_in"]:
        st.info(f"✅ Conectado como: **{st.session_state['usuario']}**")
    
    st.markdown("---")
    st.markdown("⚡ *Modo Dios Configurado por Wanda*")

# ==========================================
# 5. MOTOR PRINCIPAL Y PESTAÑAS
# ==========================================
try:
    xls = cargar_excel()
    pestanas_ocultas = ["SETTINGS", "PRINT", "POOL", "PREDICTOR"]
    pestanas_visibles = [h for h in xls.sheet_names if h not in pestanas_ocultas]
    pestanas_visibles.insert(1, "🏆 RANKING OFICIAL")
    
    tabs = st.tabs(pestanas_visibles)
    
    for idx, nombre_hoja in enumerate(pestanas_visibles):
        with tabs[idx]:
            
            # --- RANKING ---
            if nombre_hoja == "🏆 RANKING OFICIAL":
                st.subheader("🏆 Clasificación General Blindamos")
                db = cargar_db()
                if not db.empty:
                    df_ranking = db[["Jugador", "Puntos"]].sort_values(by="Puntos", ascending=False)
                    st.dataframe(df_ranking, use_container_width=True, hide_index=True)
                else:
                    st.info("Aún no hay jugadores registrados.")

            # --- FIXTURE (CON MEMORIA) ---
            elif nombre_hoja == "FIXTURE":
                st.subheader("⚽ Central de Predicciones")
                if not st.session_state["logged_in"]:
                    st.warning("⚠️ Debes Entrar/Registrarte en el menú lateral para habilitar tus pronósticos.")
                
                df_fix = pd.read_excel(xls, sheet_name="FIXTURE", skiprows=1).dropna(subset=['HOME TEAM', 'AWAY TEAM'])
                
                with st.form("form_pronosticos"):
                    for index, row in df_fix.iterrows():
                        # Cargar valor previo si existe, si no 0
                        val_h = st.session_state["preds"].get(f"h_{index}", 0)
                        val_a = st.session_state["preds"].get(f"a_{index}", 0)
                        
                        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 3])
                        col1.markdown(f"<h4 style='text-align: right;'>{obtener_bandera(row['HOME TEAM'])} {row['HOME TEAM']}</h4>", unsafe_allow_html=True)
                        col2.number_input("", min_value=0, step=1, value=int(val_h), key=f"h_{index}", label_visibility="collapsed")
                        col3.markdown("<h4 style='text-align: center; color: #f39c12;'>VS</h4>", unsafe_allow_html=True)
                        col4.number_input("", min_value=0, step=1, value=int(val_a), key=f"a_{index}", label_visibility="collapsed")
                        col5.markdown(f"<h4 style='text-align: left;'>{row['AWAY TEAM']} {obtener_bandera(row['AWAY TEAM'])}</h4>", unsafe_allow_html=True)
                        st.markdown("---")
                        
                    guardar = st.form_submit_button("Guardar Mis Pronósticos 🏆")
                    
                    if guardar:
                        if st.session_state["logged_in"]:
                            nuevas_preds = {}
                            for idx_f in df_fix.index:
                                nuevas_preds[f"h_{idx_f}"] = st.session_state[f"h_{idx_f}"]
                                nuevas_preds[f"a_{idx_f}"] = st.session_state[f"a_{idx_f}"]
                            
                            db = cargar_db()
                            db.loc[db["Jugador"] == st.session_state["usuario"], "Predicciones"] = json.dumps(nuevas_preds)
                            db.to_csv(ARCHIVO_DB, index=False)
                            st.session_state["preds"] = nuevas_preds
                            st.success("¡Pronósticos guardados en la bóveda!")
                        else:
                            st.error("⚠️ Identifícate primero en el menú lateral.")

            # --- HOME / PLAYERS / ETC ---
            elif nombre_hoja == "HOME":
                st.subheader("🏁 Centro de Control Blindamos")
                st.markdown("Navega por las pestañas para registrar pronósticos y ver el ranking.")
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
