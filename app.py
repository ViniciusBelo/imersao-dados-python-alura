import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard de Salários — Área de Dados",
    layout="wide",
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* Fundo branco geral */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {
    background-color: #f8fafc !important;
}

/* Animações */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}

.main .block-container {
    animation: fadeInUp 0.5s ease both;
    padding-top: 1.5rem;
}

/* Header */
.dash-header {
    background: #ffffff;
    border-radius: 12px;
    padding: 1.8rem 2.2rem;
    margin-bottom: 2rem;
    border-left: 5px solid #2563eb;
    box-shadow: 0 2px 16px rgba(0, 0, 0, 0.06);
    animation: fadeInUp 0.45s ease both;
}
.dash-header h1 {
    color: #0f172a;
    font-size: 1.75rem;
    font-weight: 700;
    margin: 0 0 0.4rem 0;
    letter-spacing: -0.025em;
}
.dash-header p {
    color: #64748b;
    font-size: 0.88rem;
    margin: 0;
    line-height: 1.65;
}

/* Labels de seção */
.sec-label {
    font-size: 0.68rem;
    font-weight: 700;
    color: #2563eb;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: 0 0 0.2rem 0;
}
.sec-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 1rem 0;
}

/* Divisor */
.dash-divider {
    height: 2px;
    background: linear-gradient(to right, #2563eb 0%, #93c5fd 50%, transparent 90%);
    border: none;
    margin: 2rem 0;
    border-radius: 2px;
}

/* KPI Cards */
[data-testid="metric-container"] {
    background: #ffffff !important;
    border-radius: 12px !important;
    padding: 1.2rem 1.4rem !important;
    border: 1px solid #e2e8f0 !important;
    border-top: 3px solid #2563eb !important;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06) !important;
    transition: transform 0.22s ease, box-shadow 0.22s ease !important;
    animation: slideUp 0.6s ease both !important;
}
[data-testid="metric-container"]:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 10px 30px rgba(37, 99, 235, 0.12) !important;
}
[data-testid="stMetricLabel"] p {
    color: #64748b !important;
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.09em !important;
}
[data-testid="stMetricValue"] {
    color: #0f172a !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #f1f5f9 !important;
    border-right: 1px solid #e2e8f0 !important;
}
[data-testid="stSidebar"] label {
    color: #475569 !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

/* Gráficos */
[data-testid="stPlotlyChart"] > div {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid #e2e8f0 !important;
    transition: box-shadow 0.22s ease !important;
    background: #ffffff !important;
}
[data-testid="stPlotlyChart"] > div:hover {
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.09) !important;
}

/* Botão de download */
[data-testid="stDownloadButton"] > button {
    background: #2563eb !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 0.84rem !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 2px 10px rgba(37, 99, 235, 0.3) !important;
    transition: background 0.2s ease, transform 0.2s ease !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: #1d4ed8 !important;
    transform: translateY(-2px) !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid #e2e8f0 !important;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ── Template de layout para gráficos ─────────────────────────────────────────
def layout_padrao(**kwargs):
    base = dict(
        template="plotly_white",
        font=dict(family="Inter, sans-serif", color="#334155"),
        title_font=dict(size=14, color="#0f172a", family="Inter, sans-serif"),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        margin=dict(l=10, r=20, t=50, b=40),
    )
    base.update(kwargs)
    return base


# ── Dados ─────────────────────────────────────────────────────────────────────
DATA_URL = "https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv"


@st.cache_data
def carregar_dados():
    return pd.read_csv(DATA_URL)


df = carregar_dados()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<p style="color:#2563eb;font-size:0.68rem;font-weight:700;'
        'letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.3rem;">'
        'Painel de Controle</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#0f172a;font-size:1.05rem;font-weight:700;margin-bottom:1.5rem;">'
        'Filtros</p>',
        unsafe_allow_html=True,
    )
    anos_selecionados = st.multiselect(
        "Ano", sorted(df["ano"].unique()), default=sorted(df["ano"].unique())
    )
    senioridades_selecionadas = st.multiselect(
        "Senioridade", sorted(df["senioridade"].unique()), default=sorted(df["senioridade"].unique())
    )
    contratos_selecionados = st.multiselect(
        "Tipo de Contrato", sorted(df["contrato"].unique()), default=sorted(df["contrato"].unique())
    )
    tamanhos_selecionados = st.multiselect(
        "Tamanho da Empresa", sorted(df["tamanho_empresa"].unique()), default=sorted(df["tamanho_empresa"].unique())
    )

# ── Filtragem ─────────────────────────────────────────────────────────────────
df_filtrado = df[
    (df["ano"].isin(anos_selecionados))
    & (df["senioridade"].isin(senioridades_selecionadas))
    & (df["contrato"].isin(contratos_selecionados))
    & (df["tamanho_empresa"].isin(tamanhos_selecionados))
]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="dash-header">
        <h1>Dashboard de Salários — Área de Dados</h1>
        <p>
            Explore tendências salariais no mercado global de dados.
            Utilize os filtros à esquerda para segmentar os resultados
            por ano, senioridade, tipo de contrato e porte da empresa.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── KPIs ──────────────────────────────────────────────────────────────────────
st.markdown('<p class="sec-label">Visão Geral</p>', unsafe_allow_html=True)
st.markdown('<p class="sec-title">Indicadores — Salário Anual em USD</p>', unsafe_allow_html=True)

if not df_filtrado.empty:
    salario_medio   = df_filtrado["usd"].mean()
    salario_mediano = df_filtrado["usd"].median()
    salario_maximo  = df_filtrado["usd"].max()
    total_registros = df_filtrado.shape[0]
    cargo_frequente = df_filtrado["cargo"].mode()[0]
else:
    salario_medio = salario_mediano = salario_maximo = 0
    total_registros = 0
    cargo_frequente = "—"

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Salário Médio",        f"${salario_medio:,.0f}")
c2.metric("Salário Mediano",      f"${salario_mediano:,.0f}")
c3.metric("Salário Máximo",       f"${salario_maximo:,.0f}")
c4.metric("Total de Registros",   f"{total_registros:,}")
c5.metric("Cargo mais Frequente", cargo_frequente)

st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

# ── Gráficos ──────────────────────────────────────────────────────────────────
st.markdown('<p class="sec-label">Análise Visual</p>', unsafe_allow_html=True)
st.markdown('<p class="sec-title">Distribuição e Comparativos</p>', unsafe_allow_html=True)

col_g1, col_g2 = st.columns(2)

with col_g1:
    if not df_filtrado.empty:
        top_cargos = (
            df_filtrado.groupby("cargo")["usd"]
            .mean()
            .nlargest(10)
            .sort_values(ascending=True)
            .reset_index()
        )
        fig1 = px.bar(
            top_cargos,
            x="usd",
            y="cargo",
            orientation="h",
            title="Top 10 Cargos por Salário Médio",
            labels={"usd": "Salário médio anual (USD)", "cargo": ""},
            color="usd",
            color_continuous_scale=[[0, "#93c5fd"], [1, "#1d4ed8"]],
        )
        fig1.update_traces(
            hovertemplate="<b>%{y}</b><br>Salário médio: $%{x:,.0f}<extra></extra>",
        )
        fig1.update_coloraxes(showscale=False)
        fig1.update_layout(
            **layout_padrao(yaxis={"categoryorder": "total ascending"})
        )
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível com os filtros selecionados.")

with col_g2:
    if not df_filtrado.empty:
        fig2 = px.histogram(
            df_filtrado,
            x="usd",
            nbins=30,
            title="Distribuição de Salários Anuais",
            labels={"usd": "Faixa salarial (USD)", "count": "Quantidade"},
            color_discrete_sequence=["#2563eb"],
        )
        fig2.update_traces(
            hovertemplate="Faixa: $%{x:,.0f}<br>Quantidade: %{y}<extra></extra>",
            marker_line_width=0,
            opacity=0.85,
        )
        fig2.update_layout(
            **layout_padrao(
                bargap=0.04,
                xaxis_title="Faixa salarial (USD)",
                yaxis_title="Quantidade",
            )
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível com os filtros selecionados.")

col_g3, col_g4 = st.columns(2)

with col_g3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado["remoto"].value_counts().reset_index()
        remoto_contagem.columns = ["tipo_trabalho", "quantidade"]
        fig3 = px.pie(
            remoto_contagem,
            names="tipo_trabalho",
            values="quantidade",
            title="Modalidade de Trabalho",
            hole=0.55,
            color_discrete_sequence=["#2563eb", "#60a5fa", "#93c5fd", "#bfdbfe"],
        )
        fig3.update_traces(
            textinfo="percent+label",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Quantidade: %{value:,}<br>"
                "Percentual: %{percent}<extra></extra>"
            ),
            textfont_size=12,
        )
        fig3.update_layout(
            **layout_padrao(
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
            )
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível com os filtros selecionados.")

with col_g4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado["cargo"] == "Data Scientist"]
        if not df_ds.empty:
            media_ds_pais = df_ds.groupby("residencia_iso3")["usd"].mean().reset_index()
            fig4 = px.choropleth(
                media_ds_pais,
                locations="residencia_iso3",
                color="usd",
                color_continuous_scale="rdylgn",
                title="Salário Médio de Cientista de Dados por País",
                labels={"usd": "Salário médio (USD)", "residencia_iso3": "País"},
            )
            fig4.update_layout(
                **layout_padrao(
                    geo=dict(showframe=False, showcoastlines=True, coastlinecolor="#e2e8f0"),
                    coloraxis_colorbar=dict(
                        title=dict(text="USD"),
                        tickformat="$,.0f",
                        tickfont=dict(size=10, color="#64748b"),
                    ),
                    margin=dict(l=0, r=0, t=50, b=0),
                    xaxis=dict(visible=False),
                    yaxis=dict(visible=False),
                )
            )
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("Nenhum registro de Cientista de Dados para os filtros selecionados.")
    else:
        st.warning("Nenhum dado disponível com os filtros selecionados.")

# ── Tabela ────────────────────────────────────────────────────────────────────
st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)
st.markdown('<p class="sec-label">Explorar</p>', unsafe_allow_html=True)
st.markdown('<p class="sec-title">Dados Detalhados</p>', unsafe_allow_html=True)

col_btn, _ = st.columns([1, 4])
with col_btn:
    csv_export = df_filtrado.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Baixar dados filtrados (.csv)",
        data=csv_export,
        file_name="salarios_filtrados.csv",
        mime="text/csv",
    )

st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
