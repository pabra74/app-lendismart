# gsheets_utils.py
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

def conectar_google_sheets():
    scope = [
        "https://spreadsheets.google.com/feeds ",
        "https://www.googleapis.com/auth/drive "
    ]
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        return client
    except FileNotFoundError:
        st.error("⚠️ Arquivo credentials.json não encontrado. Coloque-o na raiz do projeto.")
    except Exception as e:
        st.error(f"❌ Erro ao conectar ao Google Sheets: {e}")
    return None

def ler_leads():
    try:
        client = conectar_google_sheets()
        sheet = client.open("LendismartDB")
        worksheet = sheet.worksheet("Leads")
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"Erro ao ler Leads: {e}")
        return pd.DataFrame()

def ler_propostas_antigas():
    try:
        client = conectar_google_sheets()
        sheet = client.open("LendismartDB")
        worksheet = sheet.worksheet("Propostas_old")
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"Erro ao ler propostas antigas: {e}")
        return pd.DataFrame()

def gravar_cliente(dados_cliente):
    try:
        client = conectar_google_sheets()
        if not client:
            st.warning("🚫 Não foi possível conectar ao Google Sheets.")
            return

        sheet = client.open("LendismartDB")
        worksheet = sheet.worksheet("Clientes")

        linha = [
            dados_cliente.get("NIF", ""),
            dados_cliente.get("Tipo de Identificação", ""),
            dados_cliente.get("Nº Identificação", ""),
            dados_cliente.get("Data de Validade", ""),
            dados_cliente.get("Entidade Emitente", ""),
            dados_cliente.get("País de Emissão", ""),
            dados_cliente.get("Nº Segurança Social", ""),
            dados_cliente.get("Nome Completo", ""),
            dados_cliente.get("Género", ""),
            dados_cliente.get("Data de Nascimento", ""),
            dados_cliente.get("Nacionalidade", ""),
            dados_cliente.get("Outras Nacionalidades", ""),
            dados_cliente.get("Naturalidade", ""),
            dados_cliente.get("Estado Civil", ""),
            dados_cliente.get("Número de Dependentes", 0),
            dados_cliente.get("Habilitações", ""),
            dados_cliente.get("Código Postal", ""),
            dados_cliente.get("Morada", ""),
            dados_cliente.get("Porta", ""),
            dados_cliente.get("Andar", ""),
            dados_cliente.get("Localidade", ""),
            dados_cliente.get("Morada igual à fiscal?", ""),
            dados_cliente.get("Tipo Habitação", ""),
            dados_cliente.get("Telefone Fixo", ""),
            dados_cliente.get("Telemóvel", ""),
            dados_cliente.get("Email", ""),
            dados_cliente.get("Profissão", ""),
            dados_cliente.get("Antiguidade", ""),
            dados_cliente.get("Contrato de Trabalho", ""),
            dados_cliente.get("NIPC", ""),
            dados_cliente.get("Nome da Empresa", ""),
            dados_cliente.get("Telefone da Empresa", ""),
            dados_cliente.get("CAE do Empregador", ""),
            dados_cliente.get("Atividade do Empregador", ""),
            dados_cliente.get("Duodécimos", ""),
            dados_cliente.get("Recibo mês -1", ""),
            dados_cliente.get("Recibo mês -2", ""),
            dados_cliente.get("Recibo mês -3", ""),
            dados_cliente.get("Subsídio mês -1", ""),
            dados_cliente.get("Subsídio mês -2", ""),
            dados_cliente.get("Subsídio mês -3", ""),
            dados_cliente.get("Vencimento Líquido A (€)", ""),
            dados_cliente.get("Vencimento Líquido B (€)", "")
        ]

        worksheet.append_row(linha)
        st.success("Cliente gravado com sucesso.")
    except Exception as e:
        st.error(f"Erro ao gravar cliente: {e}")