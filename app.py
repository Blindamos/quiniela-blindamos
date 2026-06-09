import streamlit as st
import pandas as pd
import random
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
    [data-testid="stSidebar"] { background-color: #111111 !important; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    div[data-testid="stTextInput"] input { background-color: #222222 !important; color: #ffffff !important; border: 1px solid #444444 !important; }
    #MainMenu, header, footer, .stDeployButton, [data-testid="stAppDeployButton"], [data-testid="manage-app-button"], div[class*="viewerBadge"], div[class*="profileContainer"], a.header-anchor, .st-emotion-cache-10trblm, [data-testid="stHeaderActionElements"], [data-testid="stElementToolbar"] {display: none !important;}
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #2b2b2b; color: white; border-radius: 6px 6px 0px 0px; padding: 12px 24px; font-weight: bold; border: 1px solid #333; border-bottom: none; }
    .stTabs [aria-selected="true"] { background-color: #f39c12 !important; color: black !important; }
    .card-sabias { background-color: #262626; border-left: 5px solid #f39c12; padding: 15px; border-radius: 4px; margin-bottom: 15px; color: #ffffff; }
    .player-card { background-color: #222222; border: 1px solid #333333; padding: 15px; border-radius: 8px; text-align: center; color: #ffffff; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. BASE DE DATOS Y ESTADO DE SESIÓN
# ==========================================
ARCHIVO_DB = "db_blindamos.csv"

def cargar_db():
    if os.path.exists(ARCHIVO_DB): return pd.read_csv(ARCHIVO_DB)
    return pd.DataFrame(columns=["Jugador", "PIN", "Puntos", "Predicciones"])

if "logged_in" not in st.session_state:
    st.session_state.update({"logged_in": False, "usuario": "", "preds": {}})

# ==========================================
# 3. DICCIONARIOS Y LÓGICA DE BLOQUEO
# ==========================================
BANDERAS = {
    "USA": "🇺🇸", "MEXICO": "🇲🇽", "CANADA": "🇨🇦", "ARGENTINA": "🇦🇷", "BRAZIL": "🇧🇷", "BRASIL": "🇧🇷",
    "FRANCE": "🇫🇷", "SPAIN": "🇪🇸", "ESPAÑA": "🇪🇸", "GERMANY": "🇩🇪", "ITALY": "🇮🇹", "ENGLAND": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "URUGUAY": "🇺🇾", "COLOMBIA": "🇨🇴", "VENEZUELA": "🇻🇪", "CHILE": "🇨🇱", "PERU": "🇵🇪", "PERÚ": "🇵🇪",
    "ECUADOR": "🇪🇨", "PARAGUAY": "🇵🇾", "BOLIVIA": "🇧🇴", "NETHERLANDS": "🇳🇱", "PAISES BAJOS": "🇳🇱",
    "PORTUGAL": "🇵🇹", "BELGIUM": "🇧🇪", "BÉLGICA": "🇧🇪", "CROATIA": "🇭🇷", "CROACIA": "🇭🇷",
    "JAPAN": "🇯🇵", "JAPON": "🇯🇵", "SOUTH KOREA": "🇰🇷", "COREA DEL SUR": "🇰🇷", "GREECE": "🇬🇷", "GRECIA": "🇬🇷"
}

def obtener_bandera(pais): return BANDERAS.get(str(pais).strip().upper(), "🏳️") if pd.notna(pais) else "🏳️"

def es_equipo_tbd(nombre):
    if pd.isna(nombre): return True
    n = str(nombre).strip().upper()
    return any(p in n for p in ["TBD", "TDB", "WINNER", "GANADOR"]) or (len(n) <= 3 and any(c.isdigit() for c in n))

@st.cache_resource
def cargar_excel():
    import warnings; warnings.filterwarnings('ignore')
    return pd.ExcelFile("excel-mundial-2026-multiideasweb.xlsx")

# ==========================================
# 4. SIDEBAR: ACCESO DE JUGADORES
# ==========================================
with st.sidebar:
    try: st.image("logo.png", use_container_width=True)
    except: st.markdown("### 🛡️ TALLERES BLINDAMOS")
    st.markdown("---")
    st.markdown("### 🔐 Acceso de Jugador")
    usuario_input, pin_input = st.text_input("👤 Tu Nombre").strip().upper(), st.text_input("🔑 PIN (4+ dígitos)", type="password").strip()
    
    if st.button("Entrar / Registrarse"):
        if len(usuario_input) > 1 and len(pin_input) >= 4:
            db = cargar_db()
            if usuario_input in db["Jugador"].values:
                if str(db[db["Jugador"] == usuario_input].iloc[0]["PIN"]) == pin_input:
                    st.session_state.update({"logged_in": True, "usuario": usuario_input, "preds": json.loads(db[db["Jugador"] == usuario_input].iloc[0]["Predicciones"]) if pd.notna(db[db["Jugador"] == usuario_input].iloc[0]["Predicciones"]) else {}})
                    st.success("¡Acceso concedido!")
                else: st.error("PIN incorrecto.")
            else:
                db = pd.concat([db, pd.DataFrame([{"Jugador": usuario_input, "PIN": pin_input, "Puntos": 0, "Predicciones": "{}"}])], ignore_index=True)
                db.to_csv(ARCHIVO_DB, index=False)
                st.session_state.update({"logged_in": True, "usuario": usuario_input, "preds": {}})
                st.success("¡Registrado con éxito!")
        else: st.error("Ingresa nombre y PIN válido.")
    if st.session_state["logged_in"]: st.info(f"✅ Conectado: **{st.session_state['usuario']}**")

# ==========================================
# 5. MOTOR PRINCIPAL
# ==========================================
try:
    xls = cargar_excel()
    # 🔥 FILTRO DESTRUCTOR: Ignora espacios y obliga a mayúsculas
    pestanas_ocultas = ["SETTINGS", "PRINT", "POOL", "PREDICTOR", "SCORES", "HOME"]
    pestanas_excel = [h for h in xls.sheet_names if str(h).strip().upper() not in pestanas_ocultas]
    
    tabs_finales = ["🏠 INICIO", "🏆 RANKING OFICIAL"] + pestanas_excel
    tabs = st.tabs(tabs_finales)
    
    for idx, nombre_hoja in enumerate(tabs_finales):
        with tabs[idx]:
            if nombre_hoja == "🏠 INICIO":
                st.title("🛡️ Centro de Control Quiniela 2026")
                st.markdown("---")
                c1, c2 = st.columns([2, 1])
                c1.markdown("### Bienvenido al sistema élite de pronósticos.\n**Instrucciones:**\n1. Ingresa tu Nombre y PIN en el menú lateral 👈.\n2. Ve a **FIXTURE** para cargar predicciones.\n3. Guarda antes de salir. Los partidos se bloquean al iniciar.")
                c2.info("⚡ Alta Seguridad. Cifrado activo.")
                
            elif nombre_hoja == "🏆 RANKING OFICIAL":
                st.subheader("🏆 Clasificación General")
                db = cargar_db()
                st.dataframe(db[["Jugador", "Puntos"]].sort_values(by="Puntos", ascending=False), use_container_width=True, hide_index=True) if not db.empty else st.info("Aún no hay jugadores registrados.")

            elif str(nombre_hoja).strip().upper() == "FIXTURE":
                st.subheader("⚽ Central de Predicciones")
                if not st.session_state["logged_in"]: st.warning("⚠️ Debes Entrar/Registrarte para habilitar pronósticos.")
                hora_actual = datetime.utcnow() - timedelta(hours=4)
                df_fix = pd.read_excel(xls, sheet_name=nombre_hoja, skiprows=1).dropna(subset=['HOME TEAM', 'AWAY TEAM'])
                
                with st.form("form_pronosticos"):
                    for index, row in df_fix.iterrows():
                        eh, ea = row['HOME TEAM'], row['AWAY TEAM']
                        candado = es_equipo_tbd(eh) or es_equipo_tbd(ea)
                        try:
                            if pd.notna(row['DATE']) and pd.notna(row['TIME']):
                                fs = row['DATE'].strftime('%Y-%m-%d') if hasattr(row['DATE'], 'strftime') else str(row['DATE']).split(' ')[0]
                                hs = ":".join(str(row['TIME']).strip().split(':')[:2])
                                if hora_actual >= datetime.strptime(f"{fs} {hs}", "%Y-%m-%d %H:%M"): candado = True
                        except: pass
                        
                        vh, va = st.session_state["preds"].get(f"h_{index}", None if candado else 0), st.session_state["preds"].get(f"a_{index}", None if candado else 0)
                        ct, txt = ("#ff4b4b", "<br><span style='font-size:12px;'>🔒 AGOTADO</span>") if candado and not es_equipo_tbd(eh) else ("#888", "<br><span style='font-size:12px;'>⏳ TBD</span>") if candado else ("#fff", "")
                        
                        c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 3])
                        c1.markdown(f"<h4 style='text-align:right; color:{ct};'>{obtener_bandera(eh)} {eh} {txt}</h4>", unsafe_allow_html=True)
                        c2.number_input("", min_value=0, step=1, value=vh, disabled=candado, key=f"h_{index}", label_visibility="collapsed")
                        c3.markdown("<h4 style='text-align:center; color:#f39c12;'>VS</h4>", unsafe_allow_html=True)
                        c4.number_input("", min_value=0, step=1, value=va, disabled=candado, key=f"a_{index}", label_visibility="collapsed")
                        c5.markdown(f"<h4 style='text-align:left; color:{ct};'>{ea} {obtener_bandera(ea)} {txt}</h4>", unsafe_allow_html=True)
                        st.markdown("---")
                        
                    if st.form_submit_button("Guardar Pronósticos 🏆"):
                        if st.session_state["logged_in"]:
                            np = {f"{t}_{i}": st.session_state[f"{t}_{i}"] for i, r in df_fix.iterrows() for t in ["h", "a"] if not (es_equipo_tbd(r['HOME TEAM']) or es_equipo_tbd(r['AWAY TEAM']))}
                            pf = st.session_state["preds"].copy(); pf.update(np)
                            db = cargar_db(); db.loc[db["Jugador"] == st.session_state["usuario"], "Predicciones"] = json.dumps(pf); db.to_csv(ARCHIVO_DB, index=False)
                            st.session_state["preds"] = pf
                            st.success("¡Guardados y blindados!")
                        else: st.error("⚠️ Identifícate primero.")

            elif "GROUP" in str(nombre_hoja).upper() or "GRUPO" in str(nombre_hoja).upper():
                st.subheader("📊 Fase de Grupos Oficial")
                dg = pd.read_excel(xls, sheet_name=nombre_hoja, header=None)
                gd = [(str(dg.iloc[r, c]).strip(), dg.iloc[r+1:r+6, c:c+10].rename(columns=dg.iloc[r+1:r+6, c:c+10].iloc[0]).drop(dg.iloc[r+1:r+6, c:c+10].index[0])) for r in range(dg.shape[0]) for c in range(dg.shape[1]) if "GROUP" in str(dg.iloc[r, c]).upper() and "⚽" in str(dg.iloc[r, c])]
                for i in range(0, len(gd), 2):
                    c1, c2 = st.columns(2)
                    c1.markdown(f"#### {gd[i][0]}"); c1.dataframe(gd[i][1], hide_index=True, use_container_width=True)
                    if i+1 < len(gd): c2.markdown(f"#### {gd[i+1][0]}"); c2.dataframe(gd[i+1][1], hide_index=True, use_container_width=True)

            elif str(nombre_hoja).strip().upper() in ["PLAYERS", "JUGADORES"]:
                st.subheader("🔟 Los Números 10 del Mundial")
                dp = pd.read_excel(xls, sheet_name=nombre_hoja, skiprows=1).dropna(subset=['TEAM', 'PLAYER'])
                cols = st.columns(3)
                for i, (_, r) in enumerate(dp.iterrows()):
                    cols[i % 3].markdown(f"<div class='player-card'><h3>{obtener_bandera(r['TEAM'])} {r['TEAM']}</h3><p style='font-size: 24px; margin: 0;'>👤 <b>{r['PLAYER']}</b></p></div><br>", unsafe_allow_html=True)
            else:
                st.subheader(f"📊 {nombre_hoja}")
                st.dataframe(pd.read_excel(xls, sheet_name=nombre_hoja, skiprows=1).dropna(how='all'), use_container_width=True, hide_index=True)

except Exception as e: st.error(f"⚠️ Error Maestro: {e}")
