import streamlit as st
import pandas as pd
import random
import os
import json
from datetime import datetime, timedelta

# ==========================================
# 1. CONFIGURACIÓN MODO DIOS & WHITE-LABELING
# ==========================================
st.set_page_config(page_title="Quiniela Blindamos 2026", page_icon="🛡️", layout="wide")

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

def obtener_bandera(pais):
    if pd.isna(pais): return "🏳️"
    return BANDERAS.get(str(pais).strip().upper(), "🏳️")

def es_equipo_tbd(nombre):
    if pd.isna(nombre): return True
    n = str(nombre).strip().upper()
    if any(palabra in n for palabra in ["TBD", "TDB", "WINNER", "GANADOR"]): return True
    if len(n) <= 3 and any(c.isdigit() for c in n): return True
    return False

@st.cache_resource
def cargar_excel():
    return pd.ExcelFile("excel-mundial-2026-multiideasweb.xlsx")

# ==========================================
# 4. SIDEBAR: ACCESO DE JUGADORES
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
                user_row = db[db["Jugador"] == usuario_input].iloc[0]
                if str(user_row["PIN"]) == pin_input:
                    st.session_state["logged_in"] = True
                    st.session_state["usuario"] = usuario_input
                    st.session_state["preds"] = json.loads(user_row["Predicciones"]) if pd.notna(user_row["Predicciones"]) else {}
                    st.success("¡Acceso concedido!")
                else:
                    st.error("PIN incorrecto. Trata de nuevo.")
            else:
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

# ==========================================
# 5. MOTOR PRINCIPAL
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

            # --- FIXTURE (BLOQUEO TBD + CANDADO DE TIEMPO) ---
            elif nombre_hoja == "FIXTURE":
                st.subheader("⚽ Central de Predicciones")
                if not st.session_state["logged_in"]:
                    st.warning("⚠️ Debes Entrar/Registrarte en el menú lateral para habilitar tus pronósticos.")
                
                # Reloj maestro ajustado
                hora_actual = datetime.utcnow() - timedelta(hours=4)
                
                df_fix = pd.read_excel(xls, sheet_name="FIXTURE", skiprows=1).dropna(subset=['HOME TEAM', 'AWAY TEAM'])
                
                with st.form("form_pronosticos"):
                    for index, row in df_fix.iterrows():
                        equipo_h = row['HOME TEAM']
                        equipo_a = row['AWAY TEAM']
                        
                        partido_bloqueado = es_equipo_tbd(equipo_h) or es_equipo_tbd(equipo_a)
                        candado_tiempo = False
                        
                        # Evaluación del Tiempo
                        try:
                            if pd.notna(row['DATE']) and pd.notna(row['TIME']):
                                fecha_str = row['DATE'].strftime('%Y-%m-%d') if hasattr(row['DATE'], 'strftime') else str(row['DATE']).split(' ')[0]
                                hora_str = str(row['TIME']).strip()
                                # Limpieza por si hay segundos en la hora
                                if len(hora_str.split(':')) == 3:
                                    hora_str = ":".join(hora_str.split(':')[:2])
                                
                                fecha_hora_partido = datetime.strptime(f"{fecha_str} {hora_str}", "%Y-%m-%d %H:%M")
                                if hora_actual >= fecha_hora_partido:
                                    candado_tiempo = True
                        except Exception:
                            pass
                            
                        bloqueo_total = partido_bloqueado or candado_tiempo
                        
                        # Diseño visual según el bloqueo
                        texto_alerta = ""
                        color_t = "#fff"
                        if candado_tiempo:
                            texto_alerta = "<br><span style='color:#ff4b4b; font-size:12px;'>🔒 TIEMPO AGOTADO</span>"
                            color_t = "#ff4b4b"
                        elif partido_bloqueado:
                            texto_alerta = "<br><span style='color:#555; font-size:12px;'>⏳ POR DEFINIR</span>"
                            color_t = "#555"

                        val_h = st.session_state["preds"].get(f"h_{index}", None if bloqueo_total else 0)
                        val_a = st.session_state["preds"].get(f"a_{index}", None if bloqueo_total else 0)
                        
                        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 3])
                        col1.markdown(f"<h4 style='text-align: right; color: {color_t};'>{obtener_bandera(equipo_h)} {equipo_h} {texto_alerta}</h4>", unsafe_allow_html=True)
                        col2.number_input("", min_value=0, step=1, value=val_h, disabled=bloqueo_total, key=f"h_{index}", label_visibility="collapsed")
                        col3.markdown("<h4 style='text-align: center; color: #f39c12;'>VS</h4>", unsafe_allow_html=True)
                        col4.number_input("", min_value=0, step=1, value=val_a, disabled=bloqueo_total, key=f"a_{index}", label_visibility="collapsed")
                        col5.markdown(f"<h4 style='text-align: left; color: {color_t};'>{equipo_a} {obtener_bandera(equipo_a)} {texto_alerta}</h4>", unsafe_allow_html=True)
                        st.markdown("---")
                        
                    guardar = st.form_submit_button("Guardar Mis Pronósticos 🏆")
                    
                    if guardar:
                        if st.session_state["logged_in"]:
                            nuevas_preds = {}
                            for idx_f, row_f in df_fix.iterrows():
                                # Verificamos candado de tiempo al guardar por seguridad extra
                                candado_seguridad = False
                                try:
                                    if pd.notna(row_f['DATE']) and pd.notna(row_f['TIME']):
                                        fs = row_f['DATE'].strftime('%Y-%m-%d') if hasattr(row_f['DATE'], 'strftime') else str(row_f['DATE']).split(' ')[0]
                                        hs = ":".join(str(row_f['TIME']).strip().split(':')[:2])
                                        if hora_actual >= datetime.strptime(f"{fs} {hs}", "%Y-%m-%d %H:%M"):
                                            candado_seguridad = True
                                except: pass

                                if not (es_equipo_tbd(row_f['HOME TEAM']) or es_equipo_tbd(row_f['AWAY TEAM']) or candado_seguridad):
                                    nuevas_preds[f"h_{idx_f}"] = st.session_state[f"h_{idx_f}"]
                                    nuevas_preds[f"a_{idx_f}"] = st.session_state[f"a_{idx_f}"]
                            
                            # Fusionar con los previos (para no borrar los bloqueados que ya habían guardado)
                            preds_finales = st.session_state["preds"].copy()
                            preds_finales.update(nuevas_preds)
                            
                            db = cargar_db()
                            db.loc[db["Jugador"] == st.session_state["usuario"], "Predicciones"] = json.dumps(preds_finales)
                            db.to_csv(ARCHIVO_DB, index=False)
                            st.session_state["preds"] = preds_finales
                            st.success("¡Pronósticos guardados y blindados!")
                        else:
                            st.error("⚠️ Identifícate primero en el menú lateral.")

            # --- REDISEÑO VERTICAL DE LOS GRUPOS ---
            elif "GROUP" in nombre_hoja.upper() or "GRUPO" in nombre_hoja.upper():
                st.subheader("📊 Fase de Grupos Oficial")
                df_groups_raw = pd.read_excel(xls, sheet_name=nombre_hoja, header=None)
                
                grupos_data = []
                for r in range(df_groups_raw.shape[0]):
                    for c in range(df_groups_raw.shape[1]):
                        val = str(df_groups_raw.iloc[r, c]).strip().upper()
                        if "GROUP" in val and "⚽" in val:
                            nombre_grupo = str(df_groups_raw.iloc[r, c]).strip()
                            df_g = df_groups_raw.iloc[r+1:r+6, c:c+10].copy()
                            df_g.columns = df_g.iloc[0]
                            df_g = df_g[1:]
                            grupos_data.append((nombre_grupo, df_g))
                
                # Renderizar los grupos en un formato web impecable
                for i in range(0, len(grupos_data), 2):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"#### {grupos_data[i][0]}")
                        st.dataframe(grupos_data[i][1], hide_index=True, use_container_width=True)
                    if i+1 < len(grupos_data):
                        with c2:
                            st.markdown(f"#### {grupos_data[i+1][0]}")
                            st.dataframe(grupos_data[i+1][1], hide_index=True, use_container_width=True)

            # --- OTRAS PESTAÑAS ---
            else:
                st.subheader(f"📊 {nombre_hoja}")
                st.dataframe(pd.read_excel(xls, sheet_name=nombre_hoja, skiprows=3).dropna(how='all'), use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"⚠️ Error Maestro: {e}")
