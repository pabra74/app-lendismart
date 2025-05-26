# modules/propostas_gravadas.py
import streamlit as st
import pandas as pd
from gsheets_utils import ler_propostas_antigas

def run():
    st.title("📦 Propostas Gravadas")

    df = ler_propostas_antigas()
    if not df.empty:
        st.dataframe(df)
    else:
        st.warning("⚠️ Nenhuma proposta antiga encontrada.")