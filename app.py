import streamlit as st
import plotly.express as px
import pandas as pd
from src.data_loader import carregar_dados
from src.stats import calcular_estatisticas

# Configuração da página
st.set_page_config(
    page_title="IBGE - Alfabetização por Sexo e Raça",
    page_icon="📊",
    layout="wide"
)

# Estilização CSS adicional
st.markdown("""
    <style>
    .stMetric {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }
    </style>
""", unsafe_allow_html=True)

# Título do Projeto Integrador
st.title("📊 Indicadores de Alfabetização por Sexo e Raça (IBGE)")
st.caption("Projeto Integrador: Números que Falam — Tema 2 | Matemática & Python")

# Carga de dados
df_raw = carregar_dados()

# Sidebar: Filtros de Seleção (Escopo Técnico Tópico 9)
st.sidebar.header("🔍 Filtros de Análise")

regioes = ["Todas"] + sorted(df_raw["Regiao"].unique().tolist())
regiao_sel = st.sidebar.selectbox("Região:", regioes)

racas = ["Todas"] + sorted(df_raw["Raca_Cor"].unique().tolist())
raca_sel = st.sidebar.selectbox("Cor/Raça:", racas)

sexos = ["Todos"] + sorted(df_raw["Sexo"].unique().tolist())
sexo_sel = st.sidebar.selectbox("Sexo:", sexos)

# Filtragem do DataFrame
df_filtered = df_raw.copy()
if regiao_sel != "Todas":
    df_filtered = df_filtered[df_filtered["Regiao"] == regiao_sel]
if raca_sel != "Todas":
    df_filtered = df_filtered[df_filtered["Raca_Cor"] == raca_sel]
if sexo_sel != "Todos":
    df_filtered = df_filtered[df_filtered["Sexo"] == sexo_sel]

# Cálculo das Estatísticas Descritivas
stats = calcular_estatisticas(df_filtered["Taxa_Alfabetizacao"])

# --- SEÇÃO 1: CARDS COM MEDIDAS DE TENDÊNCIA CENTRAL E DISPERSÃO ---
st.subheader("📌 Medidas Estatísticas")
c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric("Média", f"{stats['media']:.2f}%")
c2.metric("Mediana (Q2)", f"{stats['mediana']:.2f}%")
c3.metric("IQR (Q3 - Q1)", f"{stats['iqr']:.2f}%")
c4.metric("Desvio Padrão", f"{stats['desvio_padrao']:.2f}%")
c5.metric("Amplitude", f"{stats['amplitude']:.2f}%")
c6.metric("Outliers Detectados", f"{len(stats['outliers'])}")

st.markdown("---")

# --- SEÇÃO 2: GRÁFICOS VISUAIS ---
g1, g2 = st.columns([1, 1])

with g1:
    st.subheader("📈 Distribuição e Identificação de Outliers (Boxplot)")
    fig_box = px.box(
        df_filtered,
        y="Taxa_Alfabetizacao",
        x="Regiao" if regiao_sel == "Todas" else "Raca_Cor",
        points="all",
        hover_data=["UF", "Sexo", "Raca_Cor"],
        title="Dispersão da Taxa de Alfabetização (%)",
        labels={"Taxa_Alfabetizacao": "Taxa de Alfabetização (%)"}
    )
    st.plotly_chart(fig_box, use_container_width=True)

with g2:
    st.subheader("📊 Comparativo por Cor/Raça")
    df_raca = df_filtered.groupby("Raca_Cor")["Taxa_Alfabetizacao"].mean().reset_index()
    fig_bar = px.bar(
        df_raca,
        x="Raca_Cor",
        y="Taxa_Alfabetizacao",
        color="Raca_Cor",
        text_auto=".2f",
        title="Média da Taxa de Alfabetização por Etnia",
        labels={"Taxa_Alfabetizacao": "Média (%)", "Raca_Cor": "Raça / Cor"}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Ranking por UF
st.subheader("🗺️ Ranking Territorial por Unidade da Federação")
df_uf = df_filtered.groupby(["UF", "Regiao"])["Taxa_Alfabetizacao"].mean().reset_index()
df_uf = df_uf.sort_values(by="Taxa_Alfabetizacao", ascending=False)

fig_rank = px.bar(
    df_uf,
    x="UF",
    y="Taxa_Alfabetizacao",
    color="Regiao",
    title="Taxa de Alfabetização Médias por Estado (UF)",
    labels={"Taxa_Alfabetizacao": "Taxa (%)", "UF": "Estado"}
)
st.plotly_chart(fig_rank, use_container_width=True)

st.markdown("---")

# --- SEÇÃO 3: INTERPRETAÇÃO EBNCC E ANÁLISE CRÍTICA ---
st.subheader("🧠 Interpretação Estatística & Leitura Crítica (BNCC)")

col_mat, col_soc = st.columns(2)

with col_mat:
    st.markdown("### 📐 Análise Matemática (EM13MAT316 / EM13MAT104)")
    st.write(f"""
    - **Sensibilidade da Média vs. Mediana:** A média observada é de **{stats['media']:.2f}%**, enquanto a mediana se fixa em **{stats['mediana']:.2f}%**.
    - **Efeito de Assimetria:** Quando a média se desvia da mediana ou quando há presença de outliers (*{len(stats['outliers'])} ponto(s) atípico(s)*), a **mediana se mostra uma medida de tendência central mais robusta**.
    - **Dispersão (IQR e Desvio Padrão):** O Intervalo Interquartil (IQR) de **{stats['iqr']:.2f}%** reflete a variabilidade dos 50% centrais dos dados, enquanto o desvio padrão de **{stats['desvio_padrao']:.2f}%** mensura o afastamento geral das UFs em relação à média.
    """)

with col_soc:
    st.markdown("### 🌍 Análise Socioeconômica (EM13CHS402)")
    st.write("""
    - **Desigualdade Racial e Regional:** Os dados evidenciam disparidades históricas. As populações pretas, pardas e indígenas frequentemente apresentam taxas de alfabetização inferiores às populações branca e amarela nas mesmas regiões.
    - **Disparidade Territorial:** Observa-se que regiões como Sul e Sudeste mantêm médias de alfabetização mais elevadas em comparação a estados do Norte e Nordeste, ressaltando a necessidade de políticas públicas focalizadas.
    """)