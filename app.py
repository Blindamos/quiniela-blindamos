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

# Calendario formateado para evitar cortes de línea en el editor
JUEGOS_FIXTURE = [
    {"DATE": "11 de junio", "TIME": "15:00", "HOME TEAM": "MÉXICO", "AWAY TEAM": "SUDÁFRICA"},
    {"DATE": "11 de junio", "TIME": "22:00", "HOME TEAM": "REPÚBLICA DE COREA", "AWAY TEAM": "REPÚBLICA CHECA"},
    {"DATE": "12 de junio", "TIME": "15:00", "HOME TEAM": "CANADÁ", "AWAY TEAM": "BOSNIA Y HERZEGOVINA"},
    {"DATE": "12 de junio", "TIME": "21:00", "HOME TEAM": "ESTADOS UNIDOS", "AWAY TEAM": "PARAGUAY"},
    {"DATE": "13 de junio", "TIME": "15:00", "HOME TEAM": "CATAR", "AWAY TEAM": "SUIZA"},
    {"DATE": "13 de junio", "TIME": "18:00", "HOME TEAM": "BRASIL", "AWAY TEAM": "MARRUECOS"},
    {"DATE": "13 de junio", "TIME": "21:00", "HOME TEAM": "HAITÍ", "AWAY TEAM": "ESCOCIA"},
    {"DATE": "13 de junio", "TIME": "00:00", "HOME TEAM": "AUSTRALIA", "AWAY TEAM": "TURQUÍA"},
    {"DATE": "14 de junio", "TIME": "13:00", "HOME TEAM": "ALEMANIA", "AWAY TEAM": "CURAZAO"},
    {"DATE": "14 de junio", "TIME": "16:00", "HOME TEAM": "PAÍSES BAJOS", "AWAY TEAM": "JAPÓN"},
    {"DATE": "14 de junio", "TIME": "19:00", "HOME TEAM": "COSTA DE MARFIL", "AWAY TEAM": "ECUADOR"},
    {"DATE": "14 de junio", "TIME": "22:00", "HOME TEAM": "SUECIA", "AWAY TEAM": "TÚNEZ"},
    {"DATE": "15 de junio", "TIME": "12:00", "HOME TEAM": "ESPAÑA", "AWAY TEAM": "CABO VERDE"},
    {"DATE": "15 de junio", "TIME": "15:00", "HOME TEAM": "BÉLGICA", "AWAY TEAM": "EGIPTO"},
    {"DATE": "15 de junio", "TIME": "18:00", "HOME TEAM": "ARABIA SAUDÍ", "AWAY TEAM": "URUGUAY"},
    {"DATE": "15 de junio", "TIME": "21:00", "HOME TEAM": "RI DE IRÁN", "AWAY TEAM": "NUEVA ZELANDA"},
    {"DATE": "16 de junio", "TIME": "15:00", "HOME TEAM": "FRANCIA", "AWAY TEAM": "SENEGAL"},
    {"DATE": "16 de junio", "TIME": "18:00", "HOME TEAM": "IRAK", "AWAY TEAM": "NORUEGA"},
    {"DATE": "16 de junio", "TIME": "21:00", "HOME TEAM": "ARGENTINA", "AWAY TEAM": "ARGELIA"},
    {"DATE": "16 de junio", "TIME": "00:00", "HOME TEAM": "AUSTRIA", "AWAY TEAM": "JORDANIA"},
    {"DATE": "17 de junio", "TIME": "13:00", "HOME TEAM": "PORTUGAL", "AWAY TEAM": "RD CONGO"},
    {"DATE": "17 de junio", "TIME": "16:00", "HOME TEAM": "INGLATERRA", "AWAY TEAM": "CROACIA"},
    {"DATE": "17 de junio", "TIME": "19:00", "HOME TEAM": "GHANA", "AWAY TEAM": "PANAMÁ"},
    {"DATE": "17 de junio", "TIME": "22:00", "HOME TEAM": "UZBEKISTÁN", "AWAY TEAM": "COLOMBIA"},
    {"DATE": "18 de junio", "TIME": "12:00", "HOME TEAM": "REPÚBLICA CHECA", "AWAY TEAM": "SUDÁFRICA"},
    {"DATE": "18 de junio", "TIME": "15:00", "HOME TEAM": "SUIZA", "AWAY TEAM": "BOSNIA Y HERZEGOVINA"},
    {"DATE": "18 de junio", "TIME": "18:00", "HOME TEAM": "CANADÁ", "AWAY TEAM": "CATAR"},
    {"DATE": "18 de junio", "TIME": "21:00", "HOME TEAM": "MÉXICO", "AWAY TEAM": "REPÚBLICA DE COREA"},
    {"DATE": "19 de junio", "TIME": "15:00", "HOME TEAM": "ESTADOS UNIDOS", "AWAY TEAM": "AUSTRALIA"},
    {"DATE": "19 de junio", "TIME": "18:00", "HOME TEAM": "ESCOCIA", "AWAY TEAM": "MARRUECOS"},
    {"DATE": "19 de junio", "TIME": "21:00", "HOME TEAM": "BRASIL", "AWAY TEAM": "HAITÍ"},
    {"DATE": "19 de junio", "TIME": "00:00", "HOME TEAM": "TURQUÍA", "AWAY TEAM": "PARAGUAY"},
    {"DATE": "20 de junio", "TIME": "13:00", "HOME TEAM": "PAÍSES BAJOS", "AWAY TEAM": "SUECIA"},
    {"DATE": "20 de junio", "TIME": "16:00", "HOME TEAM": "ALEMANIA", "AWAY TEAM": "COSTA DE MARFIL"},
    {"DATE": "20 de junio", "TIME": "22:00", "HOME TEAM": "ECUADOR", "AWAY TEAM": "CURAZAO"},
    {"DATE": "20 de junio", "TIME": "00:00", "HOME TEAM": "TÚNEZ", "AWAY TEAM": "JAPÓN"},
    {"DATE": "21 de junio", "TIME": "12:00", "HOME TEAM": "ESPAÑA", "AWAY TEAM": "ARABIA SAUDÍ"},
    {"DATE": "21 de junio", "TIME": "15:00", "HOME TEAM": "BÉLGICA", "AWAY TEAM": "IRÁN"},
    {"DATE": "21 de junio", "TIME": "18:00", "HOME TEAM": "URUGUAY", "AWAY TEAM": "CABO VERDE"},
    {"DATE": "21 de junio", "TIME": "21:00", "HOME TEAM": "NUEVA ZELANDA", "AWAY TEAM": "EGIPTO"},
    {"DATE": "22 de junio", "TIME": "13:00", "HOME TEAM": "ARGENTINA", "AWAY TEAM": "AUSTRIA"},
    {"DATE": "22 de junio", "TIME": "17:00", "HOME TEAM": "FRANCIA", "AWAY TEAM": "IRAK"},
    {"DATE": "22 de junio", "TIME": "20:00", "HOME TEAM": "NORUEGA", "AWAY TEAM": "SENEGAL"},
    {"DATE": "22 de junio", "TIME": "23:00", "HOME TEAM": "JORDANIA", "AWAY TEAM": "ARGELIA"},
    {"DATE": "23 de junio", "TIME": "13:00", "HOME TEAM": "PORTUGAL", "AWAY TEAM": "UZBEKISTÁN"},
    {"DATE": "23 de junio", "TIME": "16:00", "HOME TEAM": "INGLATERRA", "AWAY TEAM": "GHANA"},
    {"DATE": "23 de junio", "TIME": "19:00", "HOME TEAM": "PANAMÁ", "AWAY TEAM": "CROACIA"},
    {"DATE": "23 de junio", "TIME": "22:00", "HOME TEAM": "COLOMBIA", "AWAY TEAM": "RD CONGO"},
    {"DATE": "24 de junio", "TIME": "15:00", "HOME TEAM": "SUIZA", "AWAY TEAM": "CANADÁ"},
    {"DATE": "24 de junio", "TIME": "15:00", "HOME TEAM": "BOSNIA Y HERZEGOVINA", "AWAY TEAM": "CATAR"},
    {"DATE": "24 de junio", "TIME": "18:00", "HOME TEAM": "ESCOCIA", "AWAY TEAM": "BRASIL"},
    {"DATE": "24 de junio
