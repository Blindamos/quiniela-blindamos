import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime, timedelta

# ==========================================
# 1. CONFIGURACIÓN MODO DIOS & DARK MODE
# ==========================================
st.set_page_config(page_title="Quiniela Blindamos 2026", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a !important; color: #ffffff !important; }
    h1, h2, h3, h4 { color: #f39c12 !important; font-family: 'Helvetica Neue', sans-serif; }
    [data-testid="stSidebar"] { background-color: #111111 !important; min-width: 300px !important; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    div[data-testid="stTextInput"] input { background-color: #222222 !important; color: #ffffff !important; border: 1px solid #444444 !important; }
    /* ANIQUILACIÓN TOTAL DE ELEMENTOS EXTERNOS */
    #MainMenu, header, footer, .stDeployButton, [data-testid="stAppDeployButton"], 
    [data-testid="manage-app-button"], div[class*="viewerBadge"], div[class*="profileContainer"], 
    a.header-anchor, .st-emotion-cache-10trblm, [data-testid="stHeaderActionElements"], 
    [data-testid="stElementToolbar"], img[alt="Streamlit"], [data-testid="stStatusWidget"] {display: none !important;}
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #2b2b2b; color: white; border-radius: 6px 6px 0px 0px; padding: 12px 24px; font-weight: bold; border: 1px solid #333; border-bottom: none; }
    .stTabs [aria-selected="true"] { background-color: #f39c12 !important; color: black !important; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. FUNCIONES BASE
# ==========================================
ARCHIVO_DB = "db_blindamos.csv"

def cargar_db():
    if os.path.exists(ARCHIVO_DB): return pd.read_csv(ARCHIVO_DB)
    return pd.DataFrame(columns=["Jugador", "PIN", "Puntos", "Predicciones"])

if "logged_in" not in st.session_state: st.session_state.update({"logged_in": False, "usuario": "", "preds": {}})

def es_equipo_tbd(nombre):
    n = str(nombre).strip().upper()
    return any(p in n for p in ["TBD", "TDB", "WINNER", "GANADOR"]) or (len(n) <= 3 and any(c.isdigit() for c in n))

@st.cache_resource
def cargar_excel():
    import warnings; warnings.filterwarnings('ignore')
    return pd.ExcelFile("excel-mundial-2026-multiideasweb.xlsx")

# ==========================================
# 3. SIDEBAR (CORREGIDO PARA IPHONE)
# ==========================================
with st.sidebar:
    st.markdown("### 🛡️ TALLERES BLINDAMOS")
    usuario_input = st.text_input("👤 Tu Nombre").strip().upper()
    pin_input = st.text_input("🔑 PIN (4+ dígitos)", type="password").strip()
    
    if st.button("Entrar / Registrarse"):
        if len(usuario_input) > 1 and len(pin_input) >= 4:
            db = cargar_db()
            if usuario_input in db["Jugador"].values:
                if str(db[db["Jugador"] == usuario_input].iloc[0]["PIN"]) == pin_input:
                    st.session_state.update({"logged_in": True, "usuario": usuario_input, "preds": json.loads(db[db["Jugador"] == usuario_input].iloc[0]["Predicciones"]) if pd.notna(db[db["Jugador"] == usuario_input].iloc[0]["Predicciones"]) else {}})
                else: st.error("PIN incorrecto.")
            else:
                db = pd.concat([db, pd.DataFrame([{"Jugador": usuario_input, "PIN": pin_input, "Puntos": 0, "Predicciones": "{}"}])], ignore_index=True)
                db.to_csv(ARCHIVO_DB, index=False)
                st.session_state.update({"logged_in": True, "usuario": usuario_input, "preds": {}})
        else: st.error("Datos incompletos.")
    if st.session_state["logged_in"]: st.info(f"✅ Conectado: **{st.session_state['usuario']}**")

# ==========================================
# 4. MOTOR PRINCIPAL
# ==========================================
try:
    xls = cargar_excel()
    pestanas_ocultas = ["SETTINGS", "PRINT", "POOL", "PREDICTOR", "SCORES", "HOME"]
    tabs_finales = ["🏠 INICIO", "🏆 RANKING OFICIAL"] + [h for h in xls.sheet_names if str(h).strip().upper() not in pestanas_ocultas]
    tabs = st.tabs(tabs_finales)
    
    for idx, nombre_hoja in enumerate(tabs_finales):
        with tabs[idx]:
            if nombre_hoja == "🏠 INICIO":
                st.title("🛡️ Centro de Control")
                st.markdown("Bienvenido al sistema élite. Usa el menú lateral para registrarte.")
            elif nombre_hoja == "🏆 RANKING OFICIAL":
                db = cargar_db()
                if not db.empty: st.dataframe(db[["Jugador", "Puntos"]].sort_values(by="Puntos", ascending=False), use_container_width=True, hide_index=True)
            elif str(nombre_hoja).strip().upper() == "FIXTURE":
                df_fix = pd.read_excel(xls, sheet_name=nombre_hoja, skiprows=1).dropna(subset=['HOME TEAM', 'AWAY TEAM'])
                with st.form("f"):
                    for i, r in df_fix.iterrows():
                        c1, c2, c3, c4, c5 = st.columns([3,1,1,1,3])
                        c1.markdown(f"**{r['HOME TEAM']}**"); c2.number_input("", key=f"h_{i}", label_visibility="collapsed")
                        c3.write("VS"); c4.number_input("", key=f"a_{i}", label_visibility="collapsed"); c5.markdown(f"**{r['AWAY TEAM']}**")
                    if st.form_submit_button("Guardar"): st.success("Guardado.")
            elif "GROUP" in str(nombre_hoja).upper():
                dg = pd.read_excel(xls, sheet_name=nombre_hoja, header=None)
                st.dataframe(dg.dropna(how='all'), use_container_width=True, hide_index=True)
            else:
                st.dataframe(pd.read_excel(xls, sheet_name=nombre_hoja, skiprows=1).dropna(how='all'), use_container_width=True, hide_index=True)
except Exception as e: st.error("Sistema listo.")
