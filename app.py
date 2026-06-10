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
# BASE DE DATOS Y LOGÍSITICA
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
    {"DATE": "Sábado, 27 de junio 2026", "TIME": "17:00", "HOME TEAM": "PANAMÁ", "AWAY TEAM": "INGL
