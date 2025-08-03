
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

    # Exibir tabela resumida
    st.subheader("📊 Visualização da base")
    st.dataframe(df.head(10))

    # ---- CONSULTA GPT ----
    st.subheader("💬 Pergunte algo sobre os dados")
    user_input = st.text_area("Exemplo: 'Quais os departamentos com maior margem em 2025?'", height=100)

    if st.button("Enviar pergunta ao GPT") and user_input:
        # Cria um prompt básico
        prompt = f"""Você é um analista comercial especialista em supermercados.
Abaixo está um resumo da base de dados carregada:

{df.head(5).to_markdown(index=False)}

Com base nisso, responda à pergunta:
'{user_input}'"""

        # Chamada à API OpenAI
        with st.spinner("Consultando GPT..."):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=800
            )
            resposta = response.choices[0].message["content"]
            st.markdown("### 🧠 Resposta do GPT")
            st.write(resposta)
else:
    st.info("Faça upload da sua planilha para começar.")

# ---- RODAPÉ ----
st.markdown("---")
st.caption("Desenvolvido com ❤️ usando Streamlit + OpenAI")
