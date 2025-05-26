# modules/empresa.py
import streamlit as st
from datetime import date

def run():
    st.title("🏢 Empresa – Dados")

    with st.form("form_empresa"):
        st.subheader("📇 Identificação da Empresa")
        col1, col2 = st.columns(2)
        with col1:
            nome_empresa = st.text_input("Nome da Empresa")
            nipc = st.text_input("NIPC", max_chars=9)
        with col2:
            nif_empresa = st.text_input("NIF da Empresa", max_chars=9)
            data_inicio = st.date_input("Data de Início de Atividade", min_value=date(1900, 1, 1))

        st.subheader("📌 Dados Operacionais")
        fornecedores = ["Rimamundo", "Auto Leandro", "Stand Exemplo"]
        fornecedor = st.selectbox("Fornecedor", fornecedores)

        col_a1, col_a2, col_a3 = st.columns(3)
        with col_a1:
            certidao_com = st.text_input("Código Certidão Comercial (####-####-####)", placeholder="2825-2885-5475")
        with col_a2:
            rcbe = st.text_input("Código RCBE (8-4-4-12)", placeholder="936c9921-498f-4f88-9df5-c50d264e2fa0")
        with col_a3:
            iban = st.text_input("IBAN (PT50 + 21 dígitos)", placeholder="PT50XXXXXXXXXXXXXXX")

        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1:
            morada = st.text_input("Morada")
        with col_b2:
            porta = st.text_input("Porta")
        with col_b3:
            andar = st.text_input("Andar")

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            codigo_postal = st.text_input("Código Postal", placeholder="0000-000")
        with col_c2:
            localidade = st.text_input("Localidade")

        st.subheader("📎 Checklist Documental (Empresa)")
        docs_empresa = [
            "Cartão de Identificação de Pessoa Coletiva",
            "Código de acesso à Certidão Permanente",
            "Último balancete e certidões de não dívida",
            "Último IRC",
            "Último IES",
            "Último RCBE",
            "Comprovativo de IBAN",
            "Comprovativo de morada empresa",
            "Sócios CC",
            "Sócios Comprovativo morada"
        ]

        checklist = []
        for doc in docs_empresa:
            col1, col2 = st.columns([1, 2])
            with col1:
                estado = st.selectbox(f"{doc}", ["OK", "FALTA"], key=f"empresa_{doc}")
            with col2:
                obs = st.text_input(f"Observações {doc}", key=f"empresa_{doc}_obs")
            checklist.append({"Documento": doc, "Estado": estado, "Observacoes": obs})

        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            gravar = st.form_submit_button("💾 Gravar")
        with col_btn2:
            editar = st.form_submit_button("✏️ Editar")
        with col_btn3:
            gerar_pdf = st.form_submit_button("🧾 Exportar PDF Documentos em Falta")

    if gravar:
        if not nome_empresa or not nipc or not nif_empresa:
            st.warning("Por favor, preencha Nome da Empresa, NIPC e NIF.")
        else:
            st.success("✅ Empresa gravada com sucesso.")

    if gerar_pdf:
        st.info("Exportação de PDF ainda não implementada.")