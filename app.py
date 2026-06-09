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
    h1, h2, h3, h4 { color: #f39c12 !important; }
    /*Sidebar siempre visible */
    [data-testid="stSidebar"] { background-color: #111111 !important; display: block !important; min-width: 300px !important; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    /* Aniquilación robot/corona */
    #MainMenu, header, footer, .stDeployButton, [data-testid="stAppDeployButton"], 
    [data-testid="manage-app-button"], div[class*="viewerBadge"], .stStatusWidget { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. FUNCIONES Y BANDERAS (RESTAURADAS)
# ==========================================
BANDERAS = {"USA": "🇺🇸", "MEXICO": "🇲🇽", "CANADA": "🇨🇦", "ARGENTINA": "🇦🇷", "BRAZIL": "🇧🇷", "BRASIL": "🇧🇷", "FRANCE": "🇫🇷", "SPAIN": "🇪🇸", "ESPAÑA": "🇪🇸", "GERMANY": "🇩🇪", "ITALY": "🇮🇹", "ENGLAND": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "URUGUAY": "🇺🇾", "COLOMBIA": "🇨🇴", "VENEZUELA": "🇻🇪", "CHILE": "🇨🇱", "PERU": "🇵🇪", "PERÚ": "🇵🇪", "ECUADOR": "🇪🇨", "PARAGUAY": "🇵🇾", "BOLIVIA": "🇧🇴", "NETHERLANDS": "🇳🇱", "PAISES BAJOS": "🇳🇱", "PORTUGAL": "🇵🇹", "BELGIUM": "🇧🇪", "BÉLGICA": "🇧🇪", "CROATIA": "🇭🇷", "CROACIA": "🇭🇷", "GREECE": "🇬🇷", "GRECIA": "🇬🇷"}

def obtener_bandera(pais): return BANDERAS.get(str(pais).strip().upper(), "🏳️") if pd.notna(pais) else "🏳️"
def es_equipo_tbd(n): return any(p in str(n).upper() for p in ["TBD", "TDB", "WINNER", "GANADOR"])

@st.cache_resource
def cargar_excel(): return pd.ExcelFile("excel-mundial-2026-multiideasweb.xlsx")

# ==========================================
# 3. SIDEBAR (SIEMPRE VISIBLE)
# ==========================================
with st.sidebar:
    st.markdown("### 🛡️ TALLERES BLINDAMOS")
    usuario_input = st.text_input("👤 Nombre").strip().upper()
    pin_input = st.text_input("🔑 PIN (4+ dígitos)", type="password").strip()
    if st.button("Entrar"):
        # (Lógica de acceso)
        st.session_state["logged_in"] = True
        st.session_state["usuario"] = usuario_input

# ==========================================
# 4. MOTOR PRINCIPAL
# ==========================================
xls = cargar_excel()
pestanas = ["🏠 INICIO", "🏆 RANKING OFICIAL", "FIXTURE"] + [h for h in xls.sheet_names if h not in ["SETTINGS", "PRINT", "POOL", "PREDICTOR", "SCORES", "HOME", "FIXTURE"]]
tabs = st.tabs(pestanas)

for idx, nombre_hoja in enumerate(pestanas):
    with tabs[idx]:
        if nombre_hoja == "🏠 INICIO":
            st.markdown("## 🛡️ Centro de Control Quiniela 2026")
            st.markdown("Instrucciones: Ingresa tu Nombre y PIN en el panel lateral.")
        elif nombre_hoja == "FIXTURE":
            df_fix = pd.read_excel(xls, sheet_name=nombre_hoja, skiprows=1).dropna(subset=['HOME TEAM', 'AWAY TEAM'])
            for i, r in df_fix.iterrows():
                c1, c2, c3, c4, c5 = st.columns([3,1,1,1,3])
                c1.markdown(f"#### {obtener_bandera(r['HOME TEAM'])} {r['HOME TEAM']}")
                c2.number_input("", key=f"h_{i}", label_visibility="collapsed")
                c3.write("VS")
                c4.number_input("", key=f"a_{i}", label_visibility="collapsed")
                c5.markdown(f"#### {r['AWAY TEAM']} {obtener_bandera(r['AWAY TEAM'])}")
        elif "GROUP" in str(nombre_hoja).upper():
            dg = pd.read_excel(xls, sheet_name=nombre_hoja, header=None)
            st.dataframe(dg.dropna(how='all'), use_container_width=True, hide_index=True)
