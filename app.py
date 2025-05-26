import streamlit as st
import pandas as pd
import plotly.express as px

# Carrega o CSV corretamente
df = pd.read_csv("Lojas-Campanhas-01_04_2025-24_05_2025.csv", sep=",", encoding="utf-8")

# Conversão das datas para o formato datetime (caso necessário)
df["Início dos relatórios"] = pd.to_datetime(df["Início dos relatórios"], errors='coerce')
df["Fim dos relatórios"] = pd.to_datetime(df["Fim dos relatórios"], errors='coerce')

# Título do Dashboard
st.title("📈 Dashboard de Campanhas - Facebook Ads")

# MULTI-SELEÇÃO de campanhas
campanhas = df["Nome da campanha"].dropna().unique()
campanhas_escolhidas = st.multiselect("Selecione campanhas para comparar", campanhas, default=campanhas[:2])

df_filtrado = df[df["Nome da campanha"].isin(campanhas_escolhidas)]

# KPIs agrupados
st.subheader("📊 Indicadores Gerais das Campanhas Selecionadas")

for campanha in campanhas_escolhidas:
    dados = df[df["Nome da campanha"] == campanha]
    st.markdown(f"**Campanha:** {campanha}")
    col1, col2, col3 = st.columns(3)
    col1.metric("💸 Valor Gasto (R$)", round(dados["Montante gasto (BRL)"].sum(), 2))
    col2.metric("👁️ Alcance", int(dados["Alcance"].sum()))
    col3.metric("🔗 Cliques no link", int(dados["Cliques na ligação"].sum()))
    st.markdown("---")

# 📈 Gráfico comparativo de CPC ao longo do tempo
st.subheader("📉 Comparativo: CPC por campanha")

# Criar uma coluna com a média entre Início e Fim para representar a campanha no tempo
df_filtrado["Data da Campanha"] = df_filtrado[["Início dos relatórios", "Fim dos relatórios"]].mean(axis=1)

fig_cpc = px.line(
    df_filtrado,
    x="Data da Campanha",
    y="CPC (Custo por clique na ligação) (BRL)",
    color="Nome da campanha",
    markers=True,
    title="💹 CPC por Campanha ao Longo do Tempo"
)
fig_cpc.update_layout(xaxis_title="Data", yaxis_title="CPC (R$)", hovermode="x unified")
st.plotly_chart(fig_cpc, use_container_width=True)

# 📋 Tabela final para conferência
st.subheader("📂 Tabela com dados filtrados")
st.dataframe(df_filtrado.reset_index(drop=True))
