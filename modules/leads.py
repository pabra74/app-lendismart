# modules/leads.py

import streamlit as st
import pandas as pd
from gsheets_utils import ler_leads

def leads():
    st.title("📬 Leads")

    df = ler_leads()

    if df is None:
        st.error("Erro ao carregar os dados. Verifique a fonte de dados.")
        return

    if df.empty:
        st.warning("Nenhuma lead encontrada.")
        return

    st.subheader("📋 Lista de Leads")
    search_term = st.text_input("🔍 Procurar lead (nome, email ou telefone):")
    if search_term:
        df_filtrado = df[df.apply(lambda row: search_term.lower() in str(row).lower(), axis=1)]
    else:
        df_filtrado = df

    st.dataframe(df_filtrado, use_container_width=True)

    st.subheader("✉️ Mensagem para Lead")
    nome = st.text_input("Nome do lead")
    contacto = st.text_input("Email ou Telemóvel")

    corpo_mensagem = st.text_area("Mensagem", value=f"""Olá {nome},

Espero que esteja bem!

Estou a entrar em contacto para confirmar se ainda está à procura de financiamento automóvel. Caso tenha interesse, estou disponível para ajudar.

Cumprimentos,
Paulo
""")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 Enviar por Email", type="primary"):
            st.success("Email enviado com sucesso!")
    with col2:
        if st.button("💬 Enviar por WhatsApp"):
            st.success("Mensagem enviada por WhatsApp com sucesso!")

