import streamlit as st
import os
import pandas as pd
from datetime import datetime

# 1. Configuración y Estilos (Igual que antes)
st.set_page_config(page_title="Quiniela Blindamos", page_icon="⚽", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; color: #ffffff; }
    h1, h2, h3 { color: #f39c12 !important; font-family: 'Helvetica Neue', sans-serif; }
    .css-1r6slb0, .stForm { background-color: #262626 !important; border: 1px solid #333333; border-radius: 10px; padding: 20px; }
    div.stButton > button:first-child { background-color: #f39c12 !important; color: black !important; font-weight: bold !important; border-radius: 5px; width: 100%; height: 3em; }
    div.stButton > button:first-child:hover { background-color: #e67e22 !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# 2. Cabecera y Logo
ruta_logo = "logo.png"
if os.path.exists(ruta_logo):
    st.image(ruta_logo, use_container_width=True)
else:
    st.title("🛡️ BLINDAMOS")

st.subheader("🏆 Quiniela Corporativa - Mundial 2026")
st.write("¡Bienvenido al torneo de la oficina! Registra tus pronósticos.")
st.markdown("---")

# 3. Lista de partidos (Puedes agregar todos los que quieras aquí)
partidos = [
    {"id": 1, "local": "México", "visitante": "Sudáfrica"},
    {"id": 2, "local": "Estados Unidos", "visitante": "Gales"},
    {"id": 3, "local": "Canadá", "visitante": "Irlanda"}
]

# 4. Formulario principal
with st.form("registro_quiniela"):
    st.markdown("### 📝 Datos del Colaborador")
    nombre = st.text_input("Nombre y Apellido:", placeholder="Ej. Juan Pérez")
    departamento = st.selectbox("Departamento / Área:", ["Operaciones", "Ventas", "Administración", "Taller de Blindaje", "Dirección", "Otro"])
    
    st.markdown("---")
    st.markdown("### ⚽ Tus Pronósticos")
    st.caption("Ingresa los goles para cada equipo.")
    
    # Diccionario para guardar lo que escriba el usuario
    resultados_usuario = {}
    
    for p in partidos:
        st.markdown(f"**Partido {p['id']}: {p['local']} vs {p['visitante']}**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            goles_l = st.number_input(f"{p['local']}", min_value=0, max_value=15, step=1, key=f"l_{p['id']}")
        with col2:
            st.markdown("<h3 style='text-align: center; color: gray;'>VS</h3>", unsafe_allow_html=True)
        with col3:
            goles_v = st.number_input(f"{p['visitante']}", min_value=0, max_value=15, step=1, key=f"v_{p['id']}")
            
        # Guardamos el pronóstico temporalmente
        resultados_usuario[f"P{p['id']}_{p['local']}"] = goles_l
        resultados_usuario[f"P{p['id']}_{p['visitante']}"] = goles_v
        
        st.markdown("<hr style='margin: 0.5em 0px; border-top: 1px solid #333;'>", unsafe_allow_html=True)

    enviar = st.form_submit_button("Guardar Mis Pronósticos 🏆")
    
    # 5. Lógica al presionar el botón
    if enviar:
        if nombre.strip() == "":
            st.error("❌ Por favor, escribe tu nombre en la parte de arriba.")
        else:
            # Crear un registro con la fecha, nombre y los pronósticos
            registro = {
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Nombre": nombre,
                "Departamento": departamento
            }
            # Unimos los datos personales con los pronósticos
            registro.update(resultados_usuario)
            
            # Convertimos a formato de tabla (Pandas DataFrame)
            df_nuevo = pd.DataFrame([registro])
            
            # Archivo donde se guardará todo
            archivo_csv = "resultados_quiniela.csv"
            
            # Si el archivo ya existe, lo añadimos; si no, lo creamos
            if os.path.exists(archivo_csv):
                df_nuevo.to_csv(archivo_csv, mode='a', header=False, index=False)
            else:
                df_nuevo.to_csv(archivo_csv, mode='w', header=True, index=False)
                
            st.success(f"¡Excelente {nombre}! Tus pronósticos fueron guardados con éxito. ¡Mucha suerte!")
            st.balloons() # ¡Un pequeño efecto de celebración en la pantalla!