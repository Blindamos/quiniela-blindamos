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
# BASE DE DATOS Y BANDERAS
# ==========================================
ARCHIVO_DB = "db_blindamos.csv"

def cargar_db():
    if os.path.exists(ARCHIVO_DB): return pd.read_csv(ARCHIVO_DB)
    return pd.DataFrame(columns=["Jugador", "PIN", "Puntos", "Predicciones"])

def guardar_db(db_to_save): 
    db_to_save.to_csv(ARCHIVO_DB, index=False)

BANDERAS = {
    "MÉXICO": "🇲🇽", "MEXICO": "🇲🇽", "SUDÁFRICA": "🇿🇦", "SOUTH AFRICA": "🇿🇦",
    "REPÚBLICA DE COREA": "🇰🇷", "COREA DEL SUR": "🇰🇷", "SOUTH KOREA": "🇰🇷",
    "REPÚBLICA CHECA": "🇨🇿", "CZECH REPUBLIC": "🇨🇿",
    "CANADÁ": "🇨🇦", "CANADA": "🇨🇦", "BOSNIA Y HERZEGOVINA": "🇧🇦", "BOSNIA": "🇧🇦",
    "ESTADOS UNIDOS": "🇺🇸", "USA": "🇺🇸", "PARAGUAY": "🇵🇾",
    "CATAR": "🇶🇦", "QATAR": "🇶🇦", "SUIZA": "🇨🇭", "SWITZERLAND": "🇨🇭",
    "BRASIL": "🇧🇷", "BRAZIL": "🇧🇷", "MARRUECOS": "🇲🇦", "MOROCCO": "🇲🇦",
    "HAITÍ": "🇭🇹", "HAITI": "🇭🇹", "ESCOCIA": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "SCOTLAND": "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "AUSTRALIA": "🇦🇺", "TURQUÍA": "🇹🇷", "TURKEY": "🇹🇷", "TURQUIA": "🇹🇷",
    "ALEMANIA": "🇩🇪", "GERMANY": "🇩🇪", "CURAZAO": "🇨🇼", "CURACAO": "🇨🇼",
    "PAÍSES BAJOS": "🇳🇱", "PAISES BAJOS": "🇳🇱", "NETHERLANDS": "🇳🇱", "JAPÓN": "🇯🇵", "JAPON": "🇯🇵", "JAPAN": "🇯🇵",
    "COSTA DE MARFIL": "🇨🇮", "IVORY COAST": "🇨🇮", "ECUADOR": "🇪🇨",
    "SUECIA": "🇸🇪", "SWEDEN": "🇸🇪", "TÚNEZ": "🇹🇳", "TUNEZ": "🇹🇳", "TUNISIA": "🇹🇳",
    "ESPAÑA": "🇪🇸", "SPAIN": "🇪🇸", "CABO VERDE": "🇨🇻", "CAPE VERDE": "🇨🇻",
    "BÉLGICA": "🇧🇪", "BELGIUM": "🇧🇪", "EGIPTO": "🇪🇬", "EGYPT": "🇪🇬",
    "ARABIA SAUDÍ": "🇸🇦", "ARABIA SAUDITA": "🇸🇦", "SAUDI ARABIA": "🇸🇦", "URUGUAY": "🇺🇾",
    "RI DE IRÁN": "🇮🇷", "IRÁN": "🇮🇷", "IRAN": "🇮🇷", "NUEVA ZELANDA": "🇳🇿", "NEW ZEALAND": "🇳🇿",
    "FRANCIA": "🇫🇷", "FRANCE": "🇫🇷", "SENEGAL": "🇸🇳", "IRAK": "🇮🇶", "IRAQ": "🇮🇶", "NORUEGA": "🇳🇴", "NORWAY": "🇳🇴",
    "ARGENTINA": "🇦🇷", "ARGELIA": "🇩🇿", "ALGERIA": "🇩🇿", "AUSTRIA": "🇦🇹", "JORDANIA": "🇯🇴", "JORDAN": "🇯🇴",
    "PORTUGAL": "🇵🇹", "RD CONGO": "🇨🇩", "CONGO": "🇨🇩", "INGLATERRA": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "ENGLAND": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "CROACIA": "🇭🇷", "CROATIA": "🇭🇷", "GHANA": "🇬🇭", "PANAMÁ": "🇵🇦", "PANAMA": "🇵🇦",
    "UZBEKISTÁN": "🇺🇿", "UZBEKISTAN": "🇺🇿", "COLOMBIA": "🇨🇴", "VENEZUELA": "🇻🇪", "VEN": "🇻🇪"
}

def obtener_bandera(pais):
    if pd.isna(pais): return "🏳️"
    return BANDERAS.get(str(pais).strip().upper(), "🏳️")

# Estructura de tuplas cortas anti-recortes
DATOS_JUEGOS = [
    ("11 de junio", "15:00", "MÉXICO", "SUDÁFRICA"),
    ("11 de junio", "22:00", "REPÚBLICA DE COREA", "REPÚBLICA CHECA"),
    ("12 de junio", "15:00", "CANADÁ", "BOSNIA Y HERZEGOVINA"),
    ("12 de junio", "21:00", "ESTADOS UNIDOS", "PARAGUAY"),
    ("13 de junio", "15:00", "CATAR", "SUIZA"),
    ("13 de junio", "18:00", "BRASIL", "MARRUECOS"),
    ("13 de junio", "21:00", "HAITÍ", "ESCOCIA"),
    ("13 de junio", "00:00", "AUSTRALIA", "TURQUÍA"),
    ("14 de junio", "13:00", "ALEMANIA", "CURAZAO"),
    ("14 de junio", "16:00", "PAÍSES BAJOS", "JAPÓN"),
    ("14 de junio", "19:00", "COSTA DE MARFIL", "ECUADOR"),
    ("14 de junio", "22:00", "SUECIA", "TÚNEZ"),
    ("15 de junio", "12:00", "ESPAÑA", "CABO VERDE"),
    ("15 de junio", "15:00", "BÉLGICA", "EGIPTO"),
    ("15 de junio", "18:00", "ARABIA SAUDÍ", "URUGUAY"),
    ("15 de junio", "21:00", "RI DE IRÁN", "NUEVA ZELANDA"),
    ("16 de junio", "15:00", "FRANCIA", "SENEGAL"),
    ("16 de junio", "18:00", "IRAK", "NORUEGA"),
    ("16 de junio", "21:00", "ARGENTINA", "ARGELIA"),
    ("16 de junio", "00:00", "AUSTRIA", "JORDANIA"),
    ("17 de junio", "13:00", "PORTUGAL", "RD CONGO"),
    ("17 de junio", "16:00", "INGLATERRA", "CROACIA"),
    ("17 de junio", "19:00", "GHANA", "PANAMÁ"),
    ("17 de junio", "22:00", "UZBEKISTÁN", "COLOMBIA"),
    ("18 de junio", "12:00", "REPÚBLICA CHECA", "SUDÁFRICA"),
    ("18 de junio", "15:00", "SUIZA", "BOSNIA Y HERZEGOVINA"),
    ("18 de junio", "18:00", "CANADÁ", "CATAR"),
    ("18 de junio", "21:00", "MÉXICO", "REPÚBLICA DE COREA"),
    ("19 de junio", "15:00", "ESTADOS UNIDOS", "AUSTRALIA"),
    ("19 de junio", "18:00", "ESCOCIA", "MARRUECOS"),
    ("19 de junio", "21:00", "BRASIL", "HAITÍ"),
    ("19 de junio", "00:00", "TURQUÍA", "PARAGUAY"),
    ("20 de junio", "13:00", "PAÍSES BAJOS", "SUECIA"),
    ("20 de junio", "16:00", "ALEMANIA", "COSTA DE MARFIL"),
    ("20 de junio", "22:00", "ECUADOR", "CURAZAO"),
    ("20 de junio", "00:00", "TÚNEZ", "JAPÓN"),
    ("21 de junio", "12:00", "ESPAÑA", "ARABIA SAUDÍ"),
    ("21 de junio", "15:00", "BÉLGICA", "IRÁN"),
    ("21 de junio", "18:00", "URUGUAY", "CABO VERDE"),
    ("21 de junio", "21:00", "NUEVA ZELANDA", "EGIPTO"),
    ("22 de junio", "13:00", "ARGENTINA", "AUSTRIA"),
    ("22 de junio", "17:00", "FRANCIA", "IRAK"),
    ("22 de junio", "20:00", "NORUEGA", "SENEGAL"),
    ("22 de junio", "23:00", "JORDANIA", "ARGELIA"),
    ("23 de junio", "13:00", "PORTUGAL", "UZBEKISTÁN"),
    ("23 de junio", "16:00", "INGLATERRA", "GHANA"),
    ("23 de junio", "19:00", "PANAMÁ", "CROACIA"),
    ("23 de junio", "22:00", "COLOMBIA", "RD CONGO"),
    ("24 de junio", "15:00", "SUIZA", "CANADÁ"),
    ("24 de junio", "15:00", "BOSNIA Y HERZEGOVINA", "CATAR"),
    ("24 de junio", "18:00", "ESCOCIA", "BRASIL"),
    ("24 de junio", "18:00", "MARRUECOS", "HAITÍ"),
    ("24 de junio", "21:00", "REPÚBLICA CHECA", "MÉXICO"),
    ("24 de junio", "21:00", "SUDÁFRICA", "REPÚBLICA DE COREA"),
    ("25 de junio", "16:00", "CURAZAO", "COSTA DE MARFIL"),
    ("25 de junio", "16:00", "ECUADOR", "ALEMANIA"),
    ("25 de junio", "19:00", "JAPÓN", "SUECIA"),
    ("25 de junio", "19:00", "TÚNEZ", "PAÍSES BAJOS"),
    ("25 de junio", "22:00", "TURQUÍA", "ESTADOS UNIDOS"),
    ("25 de junio", "22:00", "PARAGUAY", "AUSTRALIA"),
    ("26 de junio", "15:00", "NORUEGA", "FRANCIA"),
    ("26 de junio", "15:00", "SENEGAL", "IRAK"),
    ("26 de junio", "20:00", "CABO VERDE", "ARABIA SAUDÍ"),
    ("26 de junio", "20:00", "URUGUAY", "ESPAÑA"),
    ("26 de junio", "23:00", "EGIPTO", "IRÁN"),
    ("26 de junio", "23:00", "NUEVA ZELANDA", "BÉLGICA"),
    ("27 de junio", "17:00", "PANAMÁ", "INGLATERRA"),
    ("27 de junio", "17:00", "CROACIA", "GHANA"),
    ("27 de junio", "19:30", "COLOMBIA", "PORTUGAL"),
    ("27 de junio", "19:30", "RD CONGO", "UZBEKISTÁN"),
    ("27 de junio", "22:00", "ARGELIA", "AUSTRIA"),
    ("27 de junio", "22:00", "JORDANIA", "ARGENTINA")
]

JUEGOS_FIXTURE = [{"DATE": f, "TIME": h, "HOME TEAM": l, "AWAY TEAM": v} for f, h, l, v in DATOS_JUEGOS]

def procesar_fecha(date_str):
    meses = {"junio": 6, "julio": 7}
    try:
        partes = date_str.split(" de ")
        return date(2026, meses[partes[1].lower()], int(partes[0]))
    except:
        return date(2026, 7, 20)

@st.cache_resource
def cargar_excel(): 
    return pd.ExcelFile("excel-mundial-2026-multiideasweb.xlsx")

if "logged_in" not in st.session_state: st.session_state.update({"logged_in": False, "usuario": "", "preds": {}})

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("### 🛡️ TALLERES BLINDAMOS")
        
    st.subheader("Login / Registro")
    usuario_input = st.text_input("👤 Tu Nombre", placeholder="Ej: Alvaro Giménez").strip().upper()
    pin_input = st.text_input("🔑 PIN (4+ dígitos)", type="password").strip()
    
    if st.button("Entrar / Registrarse"):
        if len(usuario_input) > 1 and len(pin_input) >= 4:
            db = cargar_db()
            if usuario_input in db["Jugador"].values:
                if str(db[db["Jugador"] == usuario_input].iloc[0]["PIN"]) == pin_input:
                    preds_str = db[db["Jugador"] == usuario_input].iloc[0]["Predicciones"]
                    st.session_state.update({"logged_in": True, "usuario": usuario_input, "preds": json.loads(preds_str) if pd.notna(preds_str) else {}})
                    st.success(f"Bienvenido, {usuario_input}")
                else: st.error("❌ Nombre de usuario ya tomado o PIN incorrecto.")
            else:
                db = pd.concat([db, pd.DataFrame([{"Jugador": usuario_input, "PIN": pin_input, "Puntos": 0, "Predicciones": "{}"}])], ignore_index=True)
                guardar_db(db)
                st.session_state.update({"logged_in": True, "usuario": usuario_input, "preds": {}})
                st.success(f"✅ Registrado como {usuario_input}")
        else: st.error("❌ Datos incompletos.")
        
    if st.session_state["logged_in"]:
        st.info(f"Conectado: {st.session_state['usuario']}")

# ==========================================
# MOTOR PRINCIPAL
# ==========================================
xls = cargar_excel()
pestanas_ocultas = ["SETTINGS", "PRINT", "POOL", "PREDICTOR", "SCORES", "HOME", "FIXTURE"]
standings_bloqueados = ["ROUND 32", "ROUND 16", "QUARTER", "SEMI", "FINAL"]
tabs_finales = ["🏠 INICIO", "🏆 RANKING OFICIAL", "FIXTURE"] + [h for h in xls.sheet_names if str(h).strip().upper() not in pestanas_ocultas]
tabs = st.tabs(tabs_finales)

for idx, nombre_hoja in enumerate(tabs_finales):
    with tabs[idx]:
        if nombre_hoja == "🏠 INICIO":
            st.markdown("## 🛡️ Centro de Control Quiniela 2026")
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
            df_fix = pd.DataFrame(JUEGOS_FIXTURE)
            with st.form("f"):
                st.write("---")
                bloqueo_date = date(2026, 6, 27)
                
                for i, r in df_fix.iterrows():
                    c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 3])
                    c1.markdown(f"#### {obtener_bandera(r['HOME TEAM'])} {r['HOME TEAM']}")
                    
                    match_date = procesar_fecha(r['DATE'])
                    locked = match_date >= bloqueo_date
                    
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
                        for key in list(st.session_state.keys()):
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
