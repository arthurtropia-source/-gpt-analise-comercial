
import streamlit as st
import openai
import pandas as pd
import matplotlib.pyplot as plt

# ---- CONFIGURAÇÃO ----
st.set_page_config(page_title="Análise Comercial GPT", layout="wide")
st.title("🧠 GPT Analista Comercial – Supermercados Feira Nova")

# ---- CHAVE DE API ----
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ---- UPLOAD DE DADOS ----
st.sidebar.header("📁 Carregar Planilha Comercial")
uploaded_file = st.sidebar.file_uploader("Escolha um arquivo Excel (.xlsx)", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file, skiprows=1)
    st.success("Base carregada com sucesso!")

    # Exibir visualização da base
    st.subheader("📊 Visualização da base (top 10 linhas)")
    st.dataframe(df.head(10))

    # Pré-agregação para reduzir volume
    if "Dpto" in df.columns and "Venda" in df.columns and "Lucro" in df.columns:
        resumo = df.groupby("Dpto")[["Venda", "Lucro"]].sum().reset_index()
        resumo["Margem (%)"] = (resumo["Lucro"] / resumo["Venda"]) * 100
        resumo = resumo.sort_values("Venda", ascending=False).reset_index(drop=True)
        resumo_markdown = resumo.to_markdown(index=False)

        st.subheader("📦 Dados agregados por departamento")
        st.dataframe(resumo)

        # ---- CONSULTA GPT ----
        st.subheader("💬 Pergunte algo sobre os dados agregados")
        user_input = st.text_area("Exemplo: 'Quais departamentos têm alta venda mas margem baixa?'", height=100)

        if st.button("Enviar pergunta ao GPT") and user_input:
            prompt = f"""Você é um analista comercial especialista em supermercados.
Receba a tabela abaixo com dados agregados por departamento (venda, lucro, margem):

{resumo_markdown}

Com base nela, responda a seguinte pergunta:
'{user_input}'
"""
            with st.spinner("Consultando GPT..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    max_tokens=1000
                )
                resposta = response.choices[0].message["content"]
                st.markdown("### 🧠 Resposta do GPT")
                st.write(resposta)
    else:
        st.warning("A planilha deve conter as colunas: Dpto, Venda, Lucro.")
else:
    st.info("Faça upload da sua planilha para começar.")

# ---- RODAPÉ ----
st.markdown("---")
st.caption("Desenvolvido com ❤️ usando Streamlit + OpenAI")
