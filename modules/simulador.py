# modules/simulador.py
import streamlit as st
from datetime import date

def run():
    st.title("📈 Simulador de Financiamento")

    with st.form("form_simulador"):

        st.subheader("🗓 Dados do Financiamento")
        col1, col2 = st.columns(2)
        with col1:
            data_matricula = st.date_input("Data Matrícula", value=date.today(), min_value=date(1970, 1, 1), max_value=date.today())
        with col2:
            categoria = st.selectbox("Categoria", [
                "Ligeiros de passageiros", "Todo o terreno", "Caravanas",
                "Comerciais ligeiros", "Tratores agrícolas", "Máquinas industriais",
                "Motos", "Pessoal"
            ])

        col3, col4 = st.columns(2)
        with col3:
            valor_pvp = st.number_input("Valor PVP (€)", min_value=0.0, step=100.0, format="%.2f")
        with col4:
            entrada = st.number_input("Valor Entrada (€)", min_value=0.0, step=100.0, format="%.2f")

        subvencao = st.number_input("Valor Subvenção (€)", min_value=0.0, step=100.0, format="%.2f")

        valor_financiar = float(valor_pvp - entrada + subvencao)
        st.markdown("### 💸 Valor a Financiar")
        st.markdown(f"<h2 style='color:red;'>{valor_financiar:.2f} €</h2>", unsafe_allow_html=True)

        st.subheader("📉 Taxas e Comissões")
        comissao_pv_pct = st.number_input("Comissão PV (%)", min_value=0.0, step=0.01, format="%.2f")
        t_stand_pct = st.number_input("T (para Stand) (%)", min_value=0.0, step=0.01, format="%.2f")

        seguro_opcional = st.selectbox("Seguro proteção ao crédito", ["Sem seguro", "Vida", "Vida+", "+65"])
        valor_seguros = 0.0015 * valor_financiar if seguro_opcional != "Sem seguro" else 0

        margem_broker_pct = comissao_pv_pct - t_stand_pct
        margem_broker = margem_broker_pct * valor_financiar / 100

        if margem_broker_pct <= 3.5:
            comissao_comercial_pct = margem_broker_pct * (1.5 / 3.5)
        else:
            comissao_comercial_pct = 1.5 + ((margem_broker_pct - 3.5) / 0.5) * 0.25

        if valor_seguros > 0:
            comissao_comercial_pct += 0.15

        comissao_comercial = comissao_comercial_pct * valor_financiar / 100

        colc1, colc2 = st.columns(2)
        with colc1:
            st.number_input("Margem Broker (%)", value=float(margem_broker_pct), format="%.2f", disabled=True)
        with colc2:
            st.number_input("Margem Broker (€)", value=float(margem_broker), format="%.2f", disabled=True)

        colc3, colc4 = st.columns(2)
        with colc3:
            st.number_input("Valor Seguros (€)", value=float(valor_seguros), format="%.2f", disabled=True)
        with colc4:
            st.number_input("Comissão Comercial (%)", value=float(comissao_comercial_pct), format="%.2f", disabled=True)

        st.number_input("Comissão Comercial (€)", value=float(comissao_comercial), format="%.2f", disabled=True)

        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            gravar = st.form_submit_button("💾 Gravar")
        with col_btn2:
            editar = st.form_submit_button("✏️ Editar")
        with col_btn3:
            exportar = st.form_submit_button("🔁 Exportar para Proposta")

    if exportar and valor_financiar > 0:
        st.session_state.simulacao = {
            "data": str(data_matricula),
            "categoria": categoria,
            "pvp": f"{valor_pvp:.2f}",
            "entrada": f"{entrada:.2f}",
            "subvencao": f"{subvencao:.2f}",
            "valor_financiado": f"{valor_financiar:.2f}",
            "comissao_comercial_pct": f"{comissao_comercial_pct:.2f}",
            "comissao_comercial_eur": f"{comissao_comercial:.2f}"
        }
        st.success("🔁 Simulação exportada para Proposta.")