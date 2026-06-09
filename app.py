import streamlit as st
import pandas as pd
import os
import json
from datetime import date

# ==========================================
# CONFIGURACIÓN MODO EXPERTO
# ==========================================
st.set_page_config(layout="wide", page_title="Quiniela Blindamos 2026", page_icon="🛡️")

st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a !important; color: #ffffff !important; }
    h1, h2, h3, h4, h5, h6 { color: #f39c12 !important; }
    [data-testid="stSidebar"] { background-color: #111111 !important; }
    div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input { 
        background-color: #222222 !important; color: white !important; border: 1px solid #444444 !important; 
    }
    .stTabs [data-baseweb="tab"] { color: white; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #f39c12 !important; color: black !important; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# FUNCIONES BASE Y BANDERAS
# ==========================================
ARCHIVO_DB = "db_blindamos.csv"

def cargar_db():
    if os.path.exists(ARCHIVO_DB): return pd.read_csv(ARCHIVO_DB)
    return pd.DataFrame(columns=["Jugador", "PIN", "Puntos", "Predicciones"])

def guardar_db(db_to_save): 
    db_to_save.to_csv(ARCHIVO_DB, index=False)

def es_equipo_tbd(n): 
    return any(p in str(n).upper() for p in ["TBD", "TDB", "WINNER", "GANADOR"]) or (len(str(n)) <= 3 and any(c.isdigit() for c in str(n)))

BANDERAS = {"USA": "🇺🇸", "MEXICO": "🇲🇽", "CANADA": "🇨🇦", "ARGENTINA": "🇦🇷", "BRAZIL": "🇧🇷", "BRASIL": "🇧🇷", "FRANCE": "🇫🇷", "SPAIN": "🇪🇸", "ESPAÑA": "🇪🇸", "GERMANY": "🇩🇪", "ITALY": "🇮🇹", "ENGLAND": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "URUGUAY": "🇺🇾", "COLOMBIA": "🇨🇴", "VENEZUELA": "🇻🇪", "CHILE": "🇨🇱", "PERU": "🇵🇪", "PERÚ": "🇵🇪", "ECUADOR": "🇪🇨", "PARAGUAY": "🇵🇾", "BOLIVIA": "🇧🇴", "NETHERLANDS": "🇳🇱", "PAISES BAJOS": "🇳🇱", "PORTUGAL": "🇵🇹", "BELGIUM": "🇧🇪", "BÉLGICA": "🇧🇪", "CROATIA": "🇭🇷", "CROACIA": "🇭🇷", "GREECE": "🇬🇷", "GRECIA": "🇬🇷"}

def obtener_bandera(pais): return BANDERAS.get(str(pais).strip().upper(), "🏳️") if pd.notna(pais) else "🏳️"

@st.cache_resource
def cargar_excel(): return pd.ExcelFile("excel-mundial-2026-multiideasweb.xlsx")

if "logged_in" not in st.session_state: st.session_state.update({"logged_in": False, "usuario": "", "preds": {}})

# ==========================================
# SIDEBAR (LOGO Y LOGIN MÓVIL)
# ==========================================
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("### TALLERES BLINDAMOS")
        
    st.subheader("Login / Registro")
    usuario_input = st.text_input("👤 Tu Nombre").strip().upper()
    pin_input = st.text_input("🔑 PIN (4+ dígitos)", type="password").strip()
    
    if st.button("Entrar / Registrarse"):
        if len(usuario_input) > 1 and len(pin_input) >= 4:
            db = cargar_db()
            if usuario_input in db["Jugador"].values:
                if str(db[db["Jugador"] == usuario_input].iloc[0]["PIN"]) == pin_input:
                    preds_str = db[db["Jugador"] == usuario_input].iloc[0]["Predicciones"]
                    st.session_state.update({"logged_in": True, "usuario": usuario_input, "preds": json.loads(preds_str) if pd.notna(preds_str) else {}})
                    st.success(f"Bienvenido, {usuario_input}")
                else: st.error("❌ Nombre ya tomado o PIN incorrecto.")
            else:
                db = pd.concat([db, pd.DataFrame([{"Jugador": usuario_input, "PIN": pin_input, "Puntos": 0, "Predicciones": "{}"}])], ignore_index=True)
                guardar_db(db)
                st.session_state.update({"logged_in": True, "usuario": usuario_input, "preds": {}})
                st.success(f"✅ Registrado como {usuario_input}")
        else: st.error("❌ Datos incompletos.")

# ==========================================
# MOTOR PRINCIPAL
# ==========================================
try:
    xls = cargar_excel()
    pestanas_ocultas = ["SETTINGS", "PRINT", "POOL", "PREDICTOR", "SCORES", "HOME", "FIXTURE"]
    standings_bloqueados = ["ROUND 32", "ROUND 16", "QUARTER", "SEMI", "FINAL"]
    tabs_finales = ["🏠 INICIO", "🏆 RANKING OFICIAL", "FIXTURE"] + [h for h in xls.sheet_names if str(h).strip().upper() not in pestanas_ocultas]
    tabs = st.tabs(tabs_finales)
    
    for idx, nombre_hoja in enumerate(tabs_finales):
        with tabs[idx]:
            if nombre_hoja == "🏠 INICIO":
                st.markdown("## 🛡️ Centro de Control Blindamos")
                st.markdown("---")
                st.markdown("### Bienvenido al sistema élite de pronósticos.")
                st.markdown("**Instrucciones:**\n1. Toca la flecha **>** (arriba a la izquierda) en tu móvil para abrir el menú.\n2. Ingresa tu Nombre y PIN.\n3. Ve a **FIXTURE** para cargar predicciones.\n4. Guarda antes de salir. Los partidos se bloquean al iniciar.")
                st.info("⚡ Alta Seguridad. Cifrado activo.")
                
            elif nombre_hoja == "🏆 RANKING OFICIAL":
                db = cargar_db()
                if not db.empty:
                    st.dataframe(db[["Jugador", "Puntos"]].sort_values(by="Puntos", ascending=False), use_container_width=True, hide_index=True)
                else: st.warning("Aún no hay jugadores registrados.")
            
            elif str(nombre_hoja).strip().upper() == "FIXTURE":
                df_fix = pd.read_excel(xls, sheet_name=nombre_hoja, skiprows=1).dropna(subset=['HOME TEAM', 'AWAY TEAM'])
                with st.form("f"):
                    st.write("---")
                    bloqueo_date = date(2026, 6, 27)
                    
                    for i, r in df_fix.iterrows():
                        if es_equipo_tbd(r['HOME TEAM']) or es_equipo_tbd(r['AWAY TEAM']): continue
                        try: match_date = pd.to_datetime(r['DATE']).date()
                        except: match_date = None
                        
                        locked = True if match_date and match_date >= bloqueo_date else False
                        
                        c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 3])
                        c1.markdown(f"#### {obtener_bandera(r['HOME TEAM'])} {r['HOME TEAM']}")
                        
                        if locked:
                            c2.write("🚫 Lock")
                            c3.markdown("## VS")
                            c4.write("🚫 Lock")
                        else:
                            h_pred = st.session_state["preds"].get(f"h_{i}", 0)
                            a_pred = st.session_state["preds"].get(f"a_{i}", 0)
                            c2.number_input("", key=f"h_{i}", label_visibility="collapsed", min_value=0, step=1, value=int(h_pred))
                            c3.markdown("## VS")
                            c4.number_input("", key=f"a_{i}", label_visibility="collapsed", min_value=0, step=1, value=int(a_pred))
                        
                        c5.markdown(f"#### {r['AWAY TEAM']} {obtener_bandera(r['AWAY TEAM'])}")
                        st.write("---")
                    
                    if st.form_submit_button("Guardar Predicciones"):
                        if st.session_state["logged_in"]:
                            for key in st.session_state.keys():
                                if key.startswith("h_") or key.startswith("a_"):
                                    st.session_state["preds"][key] = st.session_state[key]
                            
                            db = cargar_db()
                            idx_user = db[db["Jugador"] == st.session_state["usuario"]].index[0]
                            db.at[idx_user, "Predicciones"] = json.dumps(st.session_state["preds"])
                            guardar_db(db)
                            st.success("✅ Guardado.")
                        else: st.error("❌ Loguéate primero.")
            
            elif "GROUP" in str(nombre_hoja).upper() or str(nombre_hoja).upper() in standings_bloqueados:
                st.subheader(f"📊 {nombre_hoja}")
                if str(nombre_hoja).upper() in standings_bloqueados:
                    st.warning("🚫 Fase bloqueada. Se activa en eliminatorias.")
                else:
                    st.dataframe(pd.read_excel(xls, sheet_name=nombre_hoja, skiprows=1).dropna(how='all'), use_container_width=True, hide_index=True)
            else:
                st.dataframe(pd.read_excel(xls, sheet_name=nombre_hoja).dropna(how='all'), use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Asegúrate de tener el archivo Excel en la misma carpeta.")
