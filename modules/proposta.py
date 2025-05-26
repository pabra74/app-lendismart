# modules/proposta.py
import streamlit as st
from datetime import date
import pandas as pd
from fpdf import FPDF

# Função para carregar clientes
def carregar_clientes():
    return pd.DataFrame({
        "NIF": ["123456789", "987654321", "654987321"],
        "Nome": ["Paulo Abrantes", "Joana Sousa", "Carlos Silva"]
    })

# Função para gerar identificador
def gerar_identificador(nif, nome):
    hoje = date.today().strftime("%d%m%Y")
    primeiro_nome = nome.split()[0] if nome else "Nome"
    return f"{nif}_{primeiro_nome}_{hoje}"

# Função para gerar PDF de documentos em falta
def gerar_pdf_documentos(nome, checklist):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font("DejaVu", size=12)
    pdf.cell(200, 10, f"Documentos em falta – {nome}", ln=True, align="L")
    pdf.ln(5)
    for doc in checklist:
        if doc["Estado"] == "FALTA":
            linha = f"{doc['Documento']}: FALTA – {doc['Observacoes']}"
            pdf.set_text_color(255, 0, 0)
            pdf.cell(200, 10, linha, ln=True, align="L")
    file_path = f"documentos_faltam_{nome.replace(' ', '_')}.pdf"
    pdf.output(file_path)
    return file_path

# Função principal da aplicação para propostas
def run():
    st.title("📄 Proposta Resumo")

    # Carregar dados dos clientes
    df_clientes = carregar_clientes()
    lista_nomes = df_clientes["Nome"].tolist()
    financeiras = ["Credibom", "Cetelem", "321 Crédito", "Cofidis", "Primus", "Montepio", "BBVA", "CA Bank"]

    with st.form("form_proposta"):
        # Intervenientes
        st.subheader("👥 Intervenientes")
        col1, col2, col3 = st.columns(3)
        with col1:
            titular1 = st.selectbox("1º Titular", lista_nomes, key="titular1")
        with col2:
            titular2 = st.selectbox("2º Titular (se aplicável)", [""] + lista_nomes, key="titular2")
        with col3:
            avalista = st.selectbox("Avalista (se aplicável)", [""] + lista_nomes, key="avalista")

        empresa = st.selectbox("Empresa (se aplicável)", ["", "BIZAN CONSTRUÇÕES, UNIPESSOAL LDA"], key="empresa")

        # Identificador da proposta
        st.subheader("📌 Identificador da Proposta")
        dados_titular = st.session_state.get("titular", {})
        if isinstance(dados_titular, str):  # Correção para evitar erro de tipo
            try:
                import json
                dados_titular = json.loads(dados_titular)
            except Exception:
                dados_titular = {}
        if dados_titular:
            identificador = gerar_identificador(
                dados_titular.get("NIF", ""), dados_titular.get("Nome", "")
            )
            st.text_input("Identificador Interno", value=identificador, disabled=True)
        else:
            st.info("⚠️ Nenhum titular selecionado. Vá ao separador Titular.")

        # Dados bancários
        st.subheader("🏦 IBAN")
        iban = st.text_input("IBAN", placeholder="PT50XXXXXXXXXXXXXXX", key="iban")

        # Stand e Simulação
        st.subheader("🏢 Stand e Simulação")
        col4, col5 = st.columns(2)
        with col4:
            stand = st.selectbox("Stand", ["Rimamundo", "Auto Leandro"], key="stand")
        with col5:
            simulacao_selecionada = st.selectbox("Simulação (por data)", ["Simulação 2025-05-18", "Simulação 2025-04-10"], key="simulacao")

        # Dados da Simulação (preenchidos)
        st.markdown("### 🔄 Dados da Simulação (preenchidos)")
        dados_simulacao = st.session_state.get("simulacao", {})
        if isinstance(dados_simulacao, str):  # Correção para evitar erro de tipo
            try:
                import json
                dados_simulacao = json.loads(dados_simulacao)
            except Exception:
                dados_simulacao = {}
        if not dados_simulacao:
            st.info("⚠️ Nenhuma simulação foi exportada ainda.")
        else:
            st.text_input("Data Matrícula", value=dados_simulacao.get("data", ""), disabled=True)
            st.text_input("Categoria", value=dados_simulacao.get("categoria", ""), disabled=True)

            col6, col7, col8 = st.columns(3)
            with col6:
                st.text_input("Valor PVP (€)", value=dados_simulacao.get("pvp", ""), disabled=True)
            with col7:
                st.text_input("Valor Entrada (€)", value=dados_simulacao.get("entrada", ""), disabled=True)
            with col8:
                st.text_input("Subvenção (€)", value=dados_simulacao.get("subvencao", ""), disabled=True)

            st.text_input("Valor a Financiar (€)", value=dados_simulacao.get("valor_financiado", ""), disabled=True)

        # Dados da Viatura
        st.markdown("### 🚗 Dados da Viatura (preenchidos)")
        marca = st.text_input("Marca", key="viat_marca")
        modelo = st.text_input("Modelo", key="viat_modelo")
        versao = st.text_input("Versão", key="viat_versao")
        matricula = st.text_input("Matrícula", key="viat_matricula")
        chassis = st.text_input("Nº Chassis", max_chars=17, key="viat_chassis")

        # Financeiras
        st.markdown("### 🏛 Financeiras")
        for financeira in financeiras:
            st.markdown(f"**{financeira}**")
            colf1, colf2, colf3 = st.columns(3)
            with colf1:
                numero_proposta = st.text_input(f"Nº Proposta {financeira}", key=f"{financeira}_num")
            with colf2:
                data_proposta = st.date_input(f"Data {financeira}", key=f"{financeira}_data")
            with colf3:
                decisao = st.selectbox(
                    f"Decisão {financeira}",
                    ["Aguarda", "Aprovada", "Recusada", "Reanálise", "Arquivada", "Financiada"],
                    key=f"{financeira}_decisao"
                )
            observacao = st.text_area(f"Observações {financeira}", key=f"{financeira}_obs")

        # Checklists
        st.markdown("### 📎 Checklists")
        docs_financiamento = [
            "MUA Venda", "MUA Compra", "DAV", "DUA",
            "Leitura DUAapp", "DVI", "Contrato assinatura manual",
            "Envio documentos originais financeira"
        ]
        checklist = []
        for doc in docs_financiamento:
            col1, col2 = st.columns([1, 2])
            with col1:
                estado = st.selectbox(doc, ["OK", "FALTA"], key=f'proposta_{doc}')
            with col2:
                obs = st.text_input(f"Observações {doc}", key=f'proposta_{doc}_obs')
            checklist.append({"Documento": doc, "Estado": estado, "Observacoes": obs})

        # Botões de ação
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            gravar = st.form_submit_button("💾 Gravar")
        with col_btn2:
            editar = st.form_submit_button("✏️ Editar")

    if gravar:
        st.success("✅ Proposta gravada com sucesso.")

    if st.button("📥 Exportar Proposta", key="export_geral"):
        st.info("Exportação não implementada ainda.")

    for financeira in financeiras:
        if st.button(f"📤 Exportar dados {financeira}", key=f"export_{financeira}_btn"):
            st.info(f"Exportando dados para {financeira}")

    # Geração de PDF
    if st.button("🧾 Gerar PDF Documentos em Falta", key="gerar_pdf"):
        if not checklist:
            st.warning("⚠️ Nenhum documento foi marcado como 'FALTA'.")
        else:
            caminho_pdf = gerar_pdf_documentos(titular1, checklist)
            st.success(f"PDF gerado com sucesso.")
            st.markdown(f"[📄 Abrir PDF]({caminho_pdf})")