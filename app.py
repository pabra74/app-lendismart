# app.py
import streamlit as st
from modules.titular import run as proposta_titular
from modules.empresa import run as proposta_empresa
from modules.bem import run as proposta_bem
from modules.simulador import run as simulador_financiamento
from modules.proposta import run as criar_proposta
from modules.propostas_gravadas import run as ver_propostas_gravadas

st.set_page_config(page_title="Lendismart App", layout="wide")

st.sidebar.title("📄 Lendismart App")
modulo = st.sidebar.radio(
    "Selecione o módulo",
    [
        "Titular Individual",
        "Empresa",
        "Bem",
        "Simulador de Financiamento",
        "Criar Proposta",
        "Propostas Gravadas"
    ]
)

if modulo == "Titular Individual":
    proposta_titular(tipo_titular="Titular Individual")
elif modulo == "Empresa":
    proposta_empresa()
elif modulo == "Bem":
    proposta_bem()
elif modulo == "Simulador de Financiamento":
    simulador_financiamento()
elif modulo == "Criar Proposta":
    criar_proposta()
elif modulo == "Propostas Gravadas":
    ver_propostas_gravadas()