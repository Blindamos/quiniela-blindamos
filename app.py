import streamlit as st
import pandas as pd
import os
import json
from datetime import date

# ==========================================
# CONFIGURACIÓN MODO DIOS DE LA PROGRAMACIÓN
# ==========================================
st.set_page_config(layout="wide", page_title="Quiniela Blindamos 2026", page_icon="🛡️")

# Estilos visuales Dark Mode profesionales
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
# BASE DE DATOS Y LOGÍSITICA DE BANDERAS
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
    "HAITÍ": "🇭🇹", "HAITI": "🇭🇹", "ESCOCIA": "🏴%f3%a0%81%a7%f3%a0%81%a3%f3%a0%81%b3%f3%a0%81%b4%f3%a0%81%b3%f3%a0%81%b7", "SCOTLAND": "🏴%f3%a0%81%a7%f3%a0%81%a3%f3%a0%81%b3%f3%a0%81%b4%f3%a0%81%b3%f3%a0%81%b7",
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
    "PORTUGAL": "🇵🇹", "RD CONGO": "🇨🇩", "CONGO": "🇨🇩", "INGLATERRA": "🏴%f3%a0%81%a7%f3%a0%81%a2%f3%a0%81%b5%f3%a0%81%b4%f3%a0%81%b4%f3%a0%81%b7", "ENGLAND": "🏴%f3%a0%81%a7%f3%a0%81%a2%f3%a0%81%b5%f3%a0%81%b4%f3%a0%81%b4%f3%a0%81%b7",
    "CROACIA": "🇭🇷", "CROATIA": "🇭🇷", "GHANA": "🇬🇭", "PANAMÁ": "🇵🇦", "PANAMA": "🇵🇦",
    "UZBEKISTÁN": "🇺🇿", "UZBEKISTAN": "🇺🇿", "COLOMBIA": "🇨🇴", "VENEZUELA": "🇻🇪", "VEN": "🇻🇪"
}

def obtener_bandera(pais):
    if pd.isna(pais): return "🏳️"
    return BANDERAS.get(str(pais).strip().upper(), "🏳️")

# ==========================================
# BASE DE DATOS FIJA INCORPORADA (CALENDARIO OFICIAL)
# ==========================================
JUEGOS_FIXTURE = [
    {"DATE": "Jueves, 11 de junio 2026", "TIME": "15:00", "HOME TEAM": "MÉXICO", "AWAY TEAM": "SUDÁFRICA", "STAGE": "Grupo A"},
    {"DATE": "Jueves, 11 de junio 2026", "TIME": "22:00", "HOME TEAM": "REPÚBLICA DE COREA", "AWAY TEAM": "REPÚBLICA CHECA", "STAGE": "Grupo A"},
    {"DATE": "Viernes, 12 de junio 2026", "TIME": "15:00", "HOME TEAM": "CANADÁ", "AWAY TEAM": "BOSNIA Y HERZEGOVINA", "STAGE": "Grupo B"},
    {"DATE": "Viernes, 12 de junio 2026", "TIME": "21:00", "HOME TEAM": "ESTADOS UNIDOS", "AWAY TEAM": "PARAGUAY", "STAGE": "Grupo D"},
    {"DATE": "Sábado, 13 de junio 2026", "TIME": "15:00", "HOME TEAM": "CATAR", "AWAY TEAM": "SUIZA", "STAGE": "Grupo B"},
    {"DATE": "Sábado, 13 de junio 2026", "TIME": "18:00", "HOME TEAM": "BRASIL", "AWAY TEAM": "MARRUECOS", "STAGE": "Grupo C"},
    {"DATE": "Sábado, 13 de junio 2026", "TIME": "21:00", "HOME TEAM": "HAITÍ", "AWAY TEAM": "ESCOCIA", "STAGE": "Grupo C"},
    {"DATE": "Sábado, 13 de junio 2026", "TIME": "00:00", "HOME TEAM": "AUSTRALIA", "AWAY TEAM": "TURQUÍA", "STAGE": "Grupo D"},
    {"DATE": "Domingo, 14 de junio 2026", "TIME": "13:00", "HOME TEAM": "ALEMANIA", "AWAY TEAM": "CURAZAO", "STAGE": "Grupo E"},
    {"DATE": "Domingo, 14 de junio 2026", "TIME": "16:00", "HOME TEAM": "PAÍSES BAJOS", "AWAY TEAM": "JAPÓN", "STAGE": "Grupo F"},
    {"DATE": "Domingo, 14 de junio 2026", "TIME": "19:00", "HOME TEAM": "COSTA DE MARFIL", "AWAY TEAM": "ECUADOR", "STAGE": "Grupo E"},
    {"DATE": "Domingo, 14 de junio 2026", "TIME": "22:00", "HOME TEAM": "SUECIA", "AWAY TEAM": "TÚNEZ", "STAGE": "Grupo F"},
    {"DATE": "Lunes, 15 de junio 2026", "TIME": "12:00", "HOME TEAM": "ESPAÑA", "AWAY TEAM": "CABO VERDE", "STAGE": "Grupo H"},
    {"DATE": "Lunes, 15 de junio 2026", "TIME": "15:00", "HOME TEAM": "BÉLGICA", "AWAY TEAM": "EGIPTO", "STAGE": "Grupo G"},
    {"DATE": "Lunes, 15 de junio 2026", "TIME": "18:00", "HOME TEAM": "ARABIA SAUDÍ", "AWAY TEAM": "URUGUAY", "STAGE": "Grupo H"},
    {"DATE": "Lunes, 15 de junio 2026", "TIME": "21:00", "HOME TEAM": "RI DE IRÁN", "AWAY TEAM": "NUEVA ZELANDA", "STAGE": "Grupo G"},
    {"DATE": "Martes, 16 de junio 2026", "TIME": "15:00", "HOME TEAM": "FRANCIA", "AWAY TEAM": "SENEGAL", "STAGE": "Grupo I"},
    {"DATE": "Martes, 16 de junio 2026", "TIME": "18:00", "HOME TEAM": "IRAK", "AWAY TEAM": "NORUEGA", "STAGE": "Grupo I"},
    {"DATE": "Martes, 16 de junio 2026", "TIME": "21:00", "HOME TEAM": "ARGENTINA", "AWAY TEAM": "ARGELIA", "STAGE": "Grupo J"},
    {"DATE": "Martes, 16 de junio 2026", "TIME": "00:00", "HOME TEAM": "AUSTRIA", "AWAY TEAM": "JORDANIA", "STAGE": "Grupo J"},
    {"DATE": "Miércoles, 17 de junio 2026", "TIME": "13:00", "HOME TEAM": "PORTUGAL", "AWAY TEAM": "RD CONGO", "STAGE": "Grupo K"},
    {"DATE": "Miércoles, 17 de junio 2026", "TIME": "16:00", "HOME TEAM": "INGLATERRA", "AWAY TEAM": "CROACIA", "STAGE": "Grupo L"},
    {"DATE": "Miércoles, 17 de junio 2026", "TIME": "19:00", "HOME TEAM": "GHANA", "AWAY TEAM": "PANAMÁ", "STAGE": "Grupo L"},
    {"DATE": "Miércoles, 17 de junio 2026", "TIME": "22:00", "HOME TEAM": "UZBEKISTÁN", "AWAY TEAM": "COLOMBIA", "STAGE": "Grupo K"},
    {"DATE": "Jueves, 18 de junio 2026", "TIME": "12:00", "HOME TEAM": "REPÚBLICA CHECA", "AWAY TEAM": "SUDÁFRICA", "STAGE": "Grupo A"},
    {"DATE": "Jueves, 18 de junio 2026", "TIME": "15:00", "HOME TEAM": "SUIZA", "AWAY TEAM": "BOSNIA Y HERZEGOVINA", "STAGE": "Grupo B"},
    {"DATE": "Jueves, 18 de junio 2026", "TIME": "18:00", "HOME TEAM": "CANADÁ", "AWAY TEAM": "CATAR", "STAGE": "Grupo B"},
    {"DATE": "Jueves, 18 de junio 2026", "TIME": "21:00", "HOME TEAM": "MÉXICO", "AWAY TEAM": "REPÚBLICA DE COREA", "STAGE": "Grupo A"},
    {"DATE": "Viernes, 19 de junio 2026", "TIME": "15:00", "HOME TEAM": "ESTADOS UNIDOS", "AWAY TEAM": "AUSTRALIA", "STAGE": "Grupo D"},
    {"DATE": "Viernes, 19 de junio 2026", "TIME": "18:00", "HOME TEAM": "ESCOCIA", "AWAY TEAM": "MARRUECOS", "STAGE": "Grupo C"},
    {"DATE": "Viernes, 19 de junio 2026", "TIME": "21:00", "HOME TEAM": "BRASIL", "AWAY TEAM": "HAITÍ", "STAGE": "Grupo C"},
    {"DATE": "Viernes, 19 de junio 2026", "TIME": "00:00", "HOME TEAM": "TURQUÍA", "AWAY TEAM": "PARAGUAY", "STAGE": "Grupo D"},
    {"DATE": "Sábado, 20 de junio 2026", "TIME": "13:00", "HOME TEAM": "PAÍSES BAJOS", "AWAY TEAM": "SUECIA", "STAGE": "Grupo F"},
    {"DATE": "Sábado, 20 de junio 2026", "TIME": "16:00", "HOME TEAM": "ALEMANIA", "AWAY TEAM": "COSTA DE MARFIL", "STAGE": "Grupo E"},
    {"DATE": "Sábado, 20 de junio 2026", "TIME": "22:00", "HOME TEAM": "ECUADOR", "AWAY TEAM": "CURAZAO", "STAGE": "Grupo E"},
    {"DATE": "Sábado, 20 de junio 2026", "TIME": "00:00", "HOME TEAM": "TÚNEZ", "AWAY TEAM": "JAPÓN", "STAGE": "Grupo F"},
    {"DATE": "Domingo, 21 de junio 2026", "TIME": "12:00", "HOME TEAM": "ESPAÑA", "AWAY TEAM": "ARABIA SAUDÍ", "STAGE": "Grupo H"},
    {"DATE": "Domingo, 21 de junio 2026", "TIME": "15:00", "HOME TEAM": "BÉLGICA", "AWAY TEAM": "IRÁN", "STAGE": "Grupo G"},
    {"DATE": "Domingo, 21 de junio 2026", "TIME": "18:00", "HOME TEAM": "URUGUAY", "AWAY TEAM": "CABO VERDE", "STAGE": "Grupo H"},
    {"DATE": "Domingo, 21 de junio 2026", "TIME": "21:00", "HOME TEAM": "NUEVA ZELANDA", "AWAY TEAM": "EGIPTO", "STAGE": "Grupo G"},
    {"DATE": "Lunes, 22 de junio 2026", "TIME": "13:00", "HOME TEAM": "ARGENTINA", "AWAY TEAM": "AUSTRIA", "STAGE": "Grupo J"},
    {"DATE": "Lunes, 22 de junio 2026", "TIME": "17:00", "HOME TEAM": "FRANCIA", "AWAY TEAM": "IRAK", "STAGE": "Grupo I"},
    {"DATE": "Lunes, 22 de junio 2026", "TIME": "20:00", "HOME TEAM": "NORUEGA", "AWAY TEAM": "SENEGAL", "STAGE": "Grupo I"},
    {"DATE": "Lunes, 22 de junio 2026", "TIME": "23:00", "HOME TEAM": "JORDANIA", "AWAY TEAM": "ARGELIA", "STAGE": "Grupo J"},
    {"DATE": "Martes, 23 de junio 2026", "TIME": "13:00", "HOME TEAM": "PORTUGAL", "AWAY TEAM": "UZBEKISTÁN", "STAGE": "Grupo K"},
    {"DATE": "Martes, 23 de junio 2026", "TIME": "16:00", "HOME TEAM": "INGLATERRA", "AWAY TEAM": "GHANA", "STAGE": "Grupo L"},
    {"DATE": "Martes, 23 de junio 2026", "TIME": "19:00", "HOME TEAM": "PANAMÁ", "AWAY TEAM": "CROACIA", "STAGE": "Grupo L"},
    {"DATE": "Martes, 23 de junio 2026", "TIME": "22:00", "HOME TEAM": "COLOMBIA", "AWAY TEAM": "RD CONGO", "STAGE": "Grupo K"},
    {"DATE": "Miércoles, 24 de junio 2026", "TIME": "15:00", "HOME TEAM": "SUIZA", "AWAY TEAM": "CANADÁ", "STAGE": "Grupo B"},
    {"DATE": "Miércoles, 24 de junio 2026", "TIME": "15:00", "HOME TEAM": "BOSNIA Y HERZEGOVINA", "AWAY TEAM": "CATAR", "STAGE": "Grupo B"},
    {"DATE": "Miércoles, 24 de junio 2026", "TIME": "18:00", "HOME TEAM": "ESCOCIA", "AWAY TEAM": "BRASIL", "STAGE": "Grupo C"},
    {"DATE": "Miércoles, 24 de junio 2026", "TIME": "18:00", "HOME TEAM": "MARRUECOS", "AWAY TEAM": "HAITÍ", "STAGE": "Grupo C"},
    {"DATE": "Miércoles, 24 de junio 2026", "TIME": "21:00", "HOME TEAM": "REPÚBLICA CHECA", "AWAY TEAM": "MÉXICO", "STAGE": "Grupo A"},
    {"DATE": "Miércoles, 24 de junio 2026", "TIME": "21:00", "HOME TEAM": "SUDÁFRICA", "AWAY TEAM": "REPÚBLICA DE COREA", "STAGE": "Grupo A"},
    {"DATE": "Jueves, 25 de junio 2026", "TIME": "16:00", "HOME TEAM": "CURAZAO", "AWAY TEAM": "COSTA DE MARFIL", "STAGE": "Grupo E"},
    {"DATE": "Jueves, 25 de junio 2026", "TIME": "16:00", "HOME TEAM": "ECUADOR", "AWAY TEAM": "ALEMANIA", "STAGE": "Grupo E"},
    {"DATE": "Jueves, 25 de junio 2026", "TIME": "19:00", "HOME TEAM": "JAPÓN", "AWAY TEAM": "SUECIA", "STAGE": "Grupo F"},
    {"DATE": "Jueves, 25 de junio 2026", "TIME": "19:00", "HOME TEAM": "TÚNEZ", "AWAY TEAM": "PAÍSES BAJOS", "STAGE": "Grupo F"},
    {"DATE": "Jueves, 25 de junio 2026", "TIME": "22:00", "HOME TEAM": "TURQUÍA", "AWAY TEAM": "ESTADOS UNIDOS", "STAGE": "Grupo D"},
    {"DATE": "Jueves, 25 de junio 2026", "TIME": "22:00", "HOME TEAM": "PARAGUAY", "AWAY TEAM": "AUSTRALIA", "STAGE": "Grupo D"},
    {"DATE": "Viernes, 26 de junio 2026", "TIME": "15:00", "HOME TEAM": "NORUEGA", "AWAY TEAM": "FRANCIA", "STAGE": "Grupo I"},
    {"DATE": "Viernes, 26 de junio 2026", "TIME": "15:00", "HOME TEAM": "SENEGAL", "AWAY TEAM": "IRAK", "STAGE": "Grupo I"},
    {"DATE": "Viernes, 26 de junio 2026", "TIME": "20:00", "HOME TEAM": "CABO VERDE", "AWAY TEAM": "ARABIA SAUDÍ", "STAGE": "Grupo H"},
    {"DATE": "Viernes, 26 de junio 2026", "TIME": "20:00", "HOME TEAM": "URUGUAY", "AWAY TEAM": "ESPAÑA", "STAGE": "Grupo H"},
    {"DATE": "Viernes, 26 de junio 2026", "TIME": "23:00", "HOME TEAM": "EGIPTO", "AWAY TEAM": "IRÁN", "STAGE": "Grupo G"},
    {"DATE": "Viernes, 26 de junio 2026", "TIME": "23:00", "HOME TEAM": "NUEVA ZELANDA", "AWAY TEAM": "BÉLGICA", "STAGE": "Grupo G"},
    {"DATE": "Sábado, 27 de junio 2026", "TIME": "17:00", "HOME TEAM": "PANAMÁ", "AWAY TEAM": "INGLATERRA", "STAGE": "Grupo L"},
    {"DATE": "Sábado, 27 de junio 2026", "TIME": "17:00", "HOME TEAM": "CROACIA", "AWAY TEAM": "GHANA", "STAGE": "Grupo L"},
    {"DATE": "Sábado, 27 de junio 2026", "TIME": "19:30", "HOME TEAM": "COLOMBIA", "AWAY TEAM": "PORTUGAL", "STAGE": "Grupo K"},
    {"DATE": "Sábado, 27 de junio 2026", "TIME": "19:30", "HOME TEAM": "RD CONGO", "AWAY TEAM": "UZBEKISTÁN", "STAGE": "Grupo K"},
    {"DATE": "Sábado, 27 de junio 2026", "TIME": "22:00", "HOME TEAM": "ARGELIA", "AWAY TEAM": "AUSTRIA", "STAGE": "Grupo J"},
    {"DATE": "Sábado, 27 de junio 2026", "TIME": "22:00", "HOME TEAM": "JORDANIA", "AWAY TEAM": "ARGENTINA", "STAGE": "Grupo J"}
]

@st.cache_resource
def cargar_excel(): return pd.ExcelFile("excel-mundial-2026-multiideasweb.xlsx")

if "logged_in" not in st.session_state: st.session_state.update({"logged_in": False, "usuario": "", "preds": {}})

# ==========================================
# SIDEBAR (CON EJEMPLO DE NOMBRE Y LOGO)
# ==========================================
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("### 🛡️ TALLERES BLINDAMOS")
        
    st.subheader("Login / Registro")
    # REQUISITO EXPLICITO: Ejemplo configurado con Alvaro Giménez
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
try:
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
                    bloqueo_date = date
