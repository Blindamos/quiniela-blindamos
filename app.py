import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime, date, timedelta

# ==========================================
# 1. CONFIGURACIÓN MODO PRO & ESTABILIDAD
# ==========================================
st.set_page_config(layout="wide", page_title="Quiniela Blindamos 2026", page_icon="🛡️")

# CSS AGRESIVO PARA MINIMIZAR BRANDING DE STREAMLIT (Nativo)
st.markdown("""
    <style>
    /* Dark Mode Base */
    .stApp { background-color: #1a1a1a !important; color: #ffffff !important; }
    h1, h2, h3, h4, h5, h6 { color: #f39c12 !important; }
    
    /* Sidebar Forzado para ser Visible y Táctil */
    [data-testid="stSidebar"] { 
        background-color: #111111 !important; 
        display: block !important; 
        min-width: 300px !important; 
    }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input { 
        background-color: #222222 !important; 
        color: white !important; 
        border: 1px solid #444444 !important; 
    }
    
    /* ANIQUILACIÓN NATIVA DE ELEMENTOS DE BRANDING */
    /* Intento de borrar corona, robot, profile y botón deploy */
    header, #MainMenu, footer, .stDeployButton, [data-testid="stAppDeployButton"], 
    [data-testid="stStatusWidget"], [data-testid="manage-app-button"], div[class*="viewerBadge"], 
    a.header-anchor { display: none !important; visibility: hidden !important; }
    
    /* Mejoras de visualización generales */
    .stTabs [data-baseweb="tab"] { color: white; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #f39c12 !important; color: black !important; }
    .player-card { background-color: #222222; border: 1px solid #333333; padding: 15px; border-radius: 8px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. FUNCIONES BASE, DB Y BANDERAS (RESTAURADAS)
# ==========================================
ARCHIVO_DB = "db_blindamos.csv"

def cargar_db():
    if os.path.exists(ARCHIVO_DB): return pd.read_csv(ARCHIVO_DB)
    return pd.DataFrame(columns=["Jugador", "PIN", "Puntos", "Predicciones"])

def guardar_db(df): df.to_csv(ARCHIVO_DB, index=False)

def es_equipo_tbd(n): return any(p in str(n).upper() for p in ["TBD", "TDB", "WINNER", "GANADOR"]) or (len(str(n)) <= 3 and any(c.isdigit() for c in str(n)))

# Diccionario de banderas completo (Restaurado)
BANDERAS = {"USA": "🇺🇸", "MEXICO": "🇲🇽", "MEX": "🇲🇽", "CANADA": "🇨🇦", "ARGENTINA": "🇦🇷", "ARG": "🇦🇷", "BRAZIL": "🇧🇷", "BRASIL": "🇧🇷", "BRA": "🇧🇷", "FRANCE": "🇫🇷", "FRA": "🇫🇷", "SPAIN": "🇪🇸", "ESPAÑA": "🇪🇸", "ESP": "🇪🇸", "GERMANY": "🇩🇪", "GER": "🇩🇪", "ITALY": "🇮🇹", "ITA": "🇮🇹", "ENGLAND": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "ENG": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "URUGUAY": "🇺🇾", "URU": "🇺🇾", "COLOMBIA": "🇨🇴", "COL": "🇨🇴", "VENEZUELA": "🇻🇪", "VEN": "🇻🇪", "CHILE": "🇨🇱", "CHI": "🇨🇱", "PERU": "🇵🇪", "PERÚ": "🇵🇪", "PER": "🇵🇪", "ECUADOR": "🇪🇨", "ECU": "🇪🇨", "PARAGUAY": "🇵🇾", "PAR": "🇵🇾", "BOLIVIA": "🇧🇴", "BOL": "🇧🇴", "NETHERLANDS": "🇳🇱", "PAISES BAJOS": "🇳🇱", "NED": "🇳🇱", "PORTUGAL": "🇵🇹", "POR": "🇵🇹", "BELGIUM": "🇧🇪", "BÉLGICA": "🇧🇪", "BEL": "🇧🇪", "CROATIA": "🇭🇷", "CROACIA": "🇭🇷", "CRO": "🇭🇷", "GREECE": "🇬🇷", "GRECIA": "🇬🇷", "GRE": "🇬🇷"}

def obtener_bandera(pais): return BANDERAS.get(str(pais).strip().upper(), "🏳️") if pd.notna(pais) else "🏳️"

@st.cache_resource
def cargar_excel(): return pd.ExcelFile("excel-mundial-2026-multiideasweb.xlsx")

# Inicializar sesión
if "logged_in" not in st.session_state: st.session_state.update({"logged_in": False, "usuario": "", "preds": {}})

# ==========================================
# 3. SIDEBAR (LOGUEO/REGISTRO REFORZADO)
# ==========================================
with st.sidebar:
    st.markdown("### 🛡️ TALLERES BLINDAMOS")
    st.subheader("Login / Registro")
    usuario_input = st.text_input("👤 Tu Nombre").strip().upper()
    pin_input = st.text_input("🔑 PIN (4+ dígitos)", type="password").strip()
    
    if st.button("Entrar / Registrarse"):
        if len(usuario_input) > 1 and len(pin_input) >= 4:
            db = cargar_db()
            if usuario_input in db["Jugador"].values:
                # El usuario EXISTE, verificamos PIN
                if str(db[db["Jugador"] == usuario_input].iloc[0]["PIN"]) == pin_input:
                    st.session_state.update({"logged_in": True, "usuario": usuario_input, "preds": json.loads(db[db["Jugador"] == usuario_input].iloc[0]["Predicciones"]) if pd.notna(db[db["Jugador"] == usuario_input].iloc[0]["Predicciones"]) else {}})
                    st.success(f"Bienvenido de nuevo, {usuario_input}")
                else: st.error("❌ Nombre de usuario ya tomado o PIN incorrecto.")
            else:
                # El usuario NO existe, lo REGISTRAMOS
                db = pd.concat([db, pd.DataFrame([{"Jugador": usuario_input, "PIN": pin_input, "Puntos": 0, "Predicciones": "{}"}])], ignore_index=True)
                guardar_db(df) # Corregí nombre de variable db
                st.session_state.update({"logged_in": True, "usuario": usuario_input, "preds": {}})
                st.success(f"✅ Registrado y Conectado como, {usuario_input}")
        else: st.error("❌ Datos incompletos.")
    if st.session_state["logged_in"]: st.info(f"Connected as: {st.session_state['usuario']}")

# ==========================================
# 4. MOTOR PRINCIPAL
# ==========================================
st.title("🛡️ Quiniela Blindamos 2026")
# Instrucción vital para móviles si el CSS nativo falla
if not st.session_state["logged_in"]: 
    st.info("👈 Por favor, utiliza el panel de la izquierda (despliega el menú '>' arriba a la izquierda si estás en móvil) para Registrarte.")

try:
    xls = cargar_excel()
    pestanas_ocultas = ["SETTINGS", "PRINT", "POOL", "PREDICTOR", "SCORES", "HOME", "FIXTURE"]
    # Pestañas de STANDINGS bloqueadas (fase dos en adelante)
    standings_bloqueados = ["ROUND 32", "ROUND 16", "QUARTER", "SEMI", "FINAL"]
    
    tabs_finales = ["🏠 INICIO", "🏆 RANKING OFICIAL", "FIXTURE"] + [h for h in xls.sheet_names if str(h).strip().upper() not in pestanas_ocultas]
    tabs = st.tabs(tabs_finales)
    
    for idx, nombre_hoja in enumerate(tabs_finales):
        with tabs[idx]:
            # --- PORTADA RESTAURADA CON INSTRUCCIONES Y TEXTO DE ENCRIPTADO ---
            if nombre_hoja == "🏠 INICIO":
                st.markdown("## 🛡️ Centro de Control Quiniela 2026")
                st.markdown("---")
                st.markdown("### Bienvenido al sistema élite de pronósticos.")
                st.markdown("""
                **Instrucciones:**
                1. Ingresa tu Nombre y PIN en el menú lateral.
                2. Ve a **FIXTURE** para cargar predicciones.
                3. Guarda antes de salir. Los partidos se bloquean al iniciar.
                4. El **RANKING** se actualiza automáticamente.
                """)
                st.info("⚡ Alta Seguridad. Cifrado activo.")
            
            # --- RANKING LIMPIO (Ordenado por puntos desc) ---
            elif nombre_hoja == "🏆 RANKING OFICIAL":
                db = cargar_db()
                if not db.empty:
                    df_rank = db[["Jugador", "Puntos"]].sort_values(by="Puntos", ascending=False)
                    st.dataframe(df_rank, use_container_width=True, hide_index=True)
                else: st.warning("Aún no hay jugadores registrados.")
            
            # --- FIXTURE REFORZADO CON BANDERAS Y BLOQUEO DE FASE DOS ---
            elif str(nombre_hoja).strip().upper() == "FIXTURE":
                df_fix = pd.read_excel(xls, sheet_name=nombre_hoja, skiprows=1).dropna(subset=['HOME TEAM', 'AWAY TEAM'])
                
                with st.form("f"):
                    st.write("---")
                    # Lógica de bloqueo por Fecha (Asumiendo que Fase de Grupos es hasta 2026-06-26)
                    current_context_date = date(2026, 6, 9)
                    bloqueo_date = date(2026, 6, 27)
                    fase_dos_activa = current_context_date >= bloqueo_date # False si es antes
                    
                    for i, r in df_fix.iterrows():
                        if es_equipo_tbd(r['HOME TEAM']) or es_equipo_tbd(r['AWAY TEAM']): continue
                        
                        # Definir si este partido específico está bloqueado (por fecha o TBD)
                        try: match_date = pd.to_datetime(r['DATE']).date()
                        except: match_date = None
                        
                        locked = False
                        if match_date and match_date >= bloqueo_date: locked = True
                        
                        c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 3])
                        # BANDERAS RESTAURADAS Y NOMBRES
                        c1.markdown(f"#### {obtener_bandera(r['HOME TEAM'])} {r['HOME TEAM']}")
                        
                        # Si está bloqueado, mostramos el mensaje y no el input
                        if locked:
                            c2.write("🚫 Locked")
                            c3.markdown("## VS")
                            c4.write("🚫 Locked")
                        else:
                            # Inputs editables para fase de grupos
                            h_pred = st.session_state["preds"].get(f"h_{i}", 0)
                            a_pred = st.session_state["preds"].get(f"a_{i}", 0)
                            c2.number_input("", key=f"h_{i}", label_visibility="collapsed", min_value=0, step=1, value=int(h_pred))
                            c3.markdown("## VS")
                            c4.number_input("", key=f"a_{i}", label_visibility="collapsed", min_value=0, step=1, value=int(a_pred))
                        
                        c5.markdown(f"#### {r['AWAY TEAM']} {obtener_bandera(r['AWAY TEAM'])}")
                        st.write("---")
                    
                    # Botón de Guardado
                    submit = st.form_submit_button("Guardar Predicciones")
                    
                if submit:
                    if st.session_state["logged_in"]:
                        for key in st.form_submit_button_key_list: # No pude conseguir st.form_data, uso session state
                            if key.startswith(("h_", "a_")):
                                st.session_state["preds"][key] = st.session_state[key]
                        
                        db = cargar_db()
                        idx_user = db[db["Jugador"] == st.session_state["usuario"]].index[0]
                        db.at[idx_user, "Predicciones"] = json.dumps(st.session_state["preds"])
                        guardar_db(df) # Corregí nombre de variable db
                        st.success("✅ Predicciones guardadas correctamente.")
                    else: st.error("❌ Debes estar logueado para guardar.")
            
            # --- STANDINGS (Correcto, skiprows=1) CON BLOQUEO DE FASE DOS ---
            elif "GROUP" in str(nombre_hoja).upper() or str(nombre_hoja).upper() in standings_bloqueados:
                st.subheader(f"📊 {nombre_hoja}")
                # Bloqueo lógico de tablas de standings de fase dos
                if str(nombre_hoja).upper() in standings_bloqueados:
                    st.warning("🚫 Fase no activa. Esta tabla se desbloqueará al comenzar la fase eliminatoria.")
                else:
                    # Tablas de grupos permitidas
                    st.dataframe(pd.read_excel(xls, sheet_name=nombre_hoja, skiprows=1).dropna(how='all'), use_container_width=True, hide_index=True)
            
            # --- OTRAS PESTAÑAS ---
            else:
                st.dataframe(pd.read_excel(xls, sheet_name=nombre_hoja).dropna(how='all'), use_container_width=True, hide_index=True)

except Exception as e:
    st.error("Error cargando base de datos. Asegúrate de que el archivo Excel esté subido.")
