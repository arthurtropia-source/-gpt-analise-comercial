
import streamlit as st
import openai
import pandas as pd

# ---- CONFIGURAÇÃO ----
st.set_page_config(page_title="GPT Analista Comercial", layout="wide")
st.title("🧠 GPT Analista Comercial – Supermercados Feira Nova")

openai.api_key = st.secrets["OPENAI_API_KEY"]

# ---- CARREGAR INSTRUÇÕES GPT ----
with open("instrucoes_gpt_analista.txt", "r", encoding="utf-8") as f:
    instrucoes_gpt = f.read()

# ---- UPLOAD DE PLANILHA ----
st.sidebar.header("📁 Carregar Planilha (opcional)")
uploaded_file = st.sidebar.file_uploader("Selecione uma planilha (.xlsx)", type="xlsx")

# ---- CARREGAR BASE PADRÃO ----
if uploaded_file:
    df = pd.read_excel(uploaded_file, header=0)
    st.success("Planilha enviada foi carregada.")
else:
    df = pd.read_excel("base_comercial_gpt 2.xlsx", header=0)
    st.info("Usando a base padrão integrada no app.")

# ---- VISUALIZAÇÃO ----
st.subheader("📊 Visualização (Top 10 linhas)")
st.dataframe(df.head(10))

# ---- PRÉ-TRATAMENTO ----
categorias_excluidas = [
    "ativo imobilizado", "uso e consumo", "refeitório", "avarias",
    "consumo", "encartes", "telefonia", "entregas"
]
if "Dpto" in df.columns:
    df = df[~df["Dpto"].str.lower().isin([x.lower() for x in categorias_excluidas])]

if all(col in df.columns for col in ["Dpto", "Venda", "Lucro", "Custo"]):
    df["Margem (%)"] = ((df["Venda"] - df["Custo"]) / df["Venda"]) * 100
    resumo = df.groupby("Dpto")[["Venda", "Lucro", "Margem (%)"]].sum().reset_index()
    resumo = resumo.sort_values("Venda", ascending=False)
    st.subheader("📦 Dados agregados por departamento")
    st.dataframe(resumo)

    # ---- PERGUNTA ----
    st.subheader("💬 Pergunte algo sobre os dados")
    user_input = st.text_area("Exemplo: 'Quais os departamentos com maior margem em 2025?'")

    if st.button("Enviar ao GPT") and user_input:
        resumo_markdown = resumo.to_markdown(index=False)
        prompt = f"{instrucoes_gpt}\n\nBase de dados resumida por departamento:\n\n{resumo_markdown}\n\nPergunta:\n{user_input}"
        with st.spinner("Consultando GPT..."):
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1500
            )
            resposta = response.choices[0].message.content
            st.markdown("### 📈 Resposta do GPT")
            st.write(resposta)
else:
    st.error("A planilha precisa conter as colunas: Dpto, Venda, Lucro e Custo.")
