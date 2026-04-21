import streamlit as st
import pandas as pd

# ── README ────────────────────────────────────────────────────────────────────
# Esse código usa o arquivo ecom_data.csv para gerar gráficos e tabelas da dashboard
# Rode no terminal ambos abaixo:
#   cd "Projeto banco de dados"
#   python -m streamlit run dashboard_csv.py

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard E-commerce | CSV",
    page_icon="📊",
    layout="wide"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 1rem; }

section[data-testid="stSidebar"] > div:first-child {
    background: #111122;
    border-right: 1px solid #2e2e4d;
}
div[data-testid="metric-container"] {
    background: #1a1a2e;
    border: 1px solid #2e2e4d;
    border-radius: 10px;
    padding: 16px 20px;
}
</style>
""", unsafe_allow_html=True)

# ── Dados ─────────────────────────────────────────────────────────────────────
@st.cache_data
def carregar_dados():
    df = pd.read_csv("ecom_data.csv", parse_dates=["data_pedido"])
    return df

df = carregar_dados()

# ── Cabeçalho ─────────────────────────────────────────────────────────────────
col_titulo, col_badge = st.columns([4, 1])
with col_titulo:
    st.markdown("## 📊 Dashboard E-commerce")
with col_badge:
    st.markdown(
        "<div style='text-align:right;padding-top:10px'>"
        "<span style='background:rgba(67,170,139,0.12);color:#43AA8B;"
        "border:1px solid rgba(67,170,139,0.3);border-radius:20px;"
        "padding:5px 14px;font-size:0.78rem;font-weight:600;'>📁 CSV Local</span>"
        "</div>",
        unsafe_allow_html=True,
    )

# KPIs globais
k1, k2, k3, k4 = st.columns(4)
k1.metric("💰 Faturamento Total", f"R$ {df['valor_total'].sum():,.0f}")
k2.metric("📦 Total de Pedidos",  f"{df['order_id'].nunique():,}")
k3.metric("🎫 Compra média",      f"R$ {df['valor_total'].mean():,.2f}")
k4.metric("👥 Clientes Únicos",   f"{df['customer_id'].nunique():,}")

st.divider()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📋 Análises")
    opcao = st.radio(
        "Escolha a análise",
        [
            "📍 Cidade",
            "📦 Categoria",
            "🏆 Ranking Clientes",
            "📊 Percentual por Pedido",
            "📈 Média Móvel",
            "📊 Acima da Média",
            "🎯 Descontos",
        ],
        label_visibility="collapsed",
    )

# ── Análises ──────────────────────────────────────────────────────────────────

if opcao == "📍 Cidade":
    resultado = (
        df.groupby("cidade")
        .agg(
            total_pedidos=("order_id", "count"),
            faturamento_total=("valor_total", "sum"),
            ticket_medio=("valor_total", "mean"),
        )
        .sort_values("faturamento_total", ascending=False)
        .reset_index()
    )

    st.subheader("📍 Faturamento por Cidade")
    m1, m2, m3 = st.columns(3)
    m1.metric("🏙️ Cidade Líder",    resultado.iloc[0]["cidade"])
    m2.metric("💰 Maior Faturamento", f"R$ {resultado.iloc[0]['faturamento_total']:,.0f}")
    m3.metric("🎫 Melhor Ticket",
              f"R$ {resultado.sort_values('ticket_medio', ascending=False).iloc[0]['ticket_medio']:,.2f}")
    st.bar_chart(resultado.set_index("cidade")["faturamento_total"])
    with st.expander("📋 Ver tabela completa"):
        st.dataframe(resultado, use_container_width=True)

elif opcao == "📦 Categoria":
    resultado = (
        df.groupby(["categoria", "subcategoria"])
        .agg(faturamento=("valor_total", "sum"))
        .sort_values("faturamento", ascending=False)
        .reset_index()
    )
    cat_total = df.groupby("categoria")["valor_total"].sum().reset_index()

    st.subheader("📦 Faturamento por Categoria")
    m1, m2, m3 = st.columns(3)
    top_cat = cat_total.sort_values("valor_total", ascending=False)
    m1.metric("🥇 Top Categoria",    top_cat.iloc[0]["categoria"])
    m2.metric("📦 Nº de Categorias", len(cat_total))
    m3.metric("🧩 Subcategorias",    resultado["subcategoria"].nunique())
    st.bar_chart(resultado.set_index("categoria")["faturamento"])
    with st.expander("📋 Ver tabela"):
        st.dataframe(resultado, use_container_width=True)

elif opcao == "🏆 Ranking Clientes":
    resultado = (
        df.groupby("customer_id")
        .agg(total_gasto=("valor_total", "sum"), total_pedidos=("order_id", "count"))
        .sort_values("total_gasto", ascending=False)
        .reset_index()
    )
    resultado.insert(0, "ranking", range(1, len(resultado) + 1))

    st.subheader("🏆 Ranking de Clientes")
    m1, m2, m3 = st.columns(3)
    m1.metric("🥇 Top Cliente",    resultado.iloc[0]["customer_id"])
    m2.metric("💰 Maior Gasto",    f"R$ {resultado.iloc[0]['total_gasto']:,.0f}")
    m3.metric("📦 Pedidos do Top", int(resultado.iloc[0]["total_pedidos"]))
    st.bar_chart(resultado.set_index("customer_id")["total_gasto"].head(20))
    with st.expander("📋 Ver ranking completo"):
        st.dataframe(resultado, use_container_width=True)

elif opcao == "📊 Percentual por Pedido":
    total_geral = df["valor_total"].sum()
    resultado = df[["order_id", "valor_total"]].copy()
    resultado["total_geral"] = total_geral
    resultado["percentual"] = resultado["valor_total"] / total_geral * 100
    resultado = resultado.sort_values("percentual", ascending=False).reset_index(drop=True)

    st.subheader("📊 Percentual dos Pedidos")
    m1, m2, m3 = st.columns(3)
    m1.metric("💰 Total Geral",   f"R$ {total_geral:,.0f}")
    m2.metric("📋 Maior Pedido",  f"R$ {resultado['valor_total'].max():,.2f}")
    m3.metric("📊 % Máximo",      f"{resultado['percentual'].max():.4f}%")
    with st.expander("📋 Ver tabela completa"):
        st.dataframe(resultado, use_container_width=True)

elif opcao == "📈 Média Móvel":
    resultado = (
        df[["data_pedido", "valor_total"]]
        .sort_values("data_pedido")
        .copy()
    )
    resultado["media_movel"] = (
        resultado["valor_total"].rolling(window=3, min_periods=1).mean()
    )

    st.subheader("📈 Média Móvel (janela de 3 registros)")
    m1, m2, m3 = st.columns(3)
    m1.metric("📅 Início",   resultado["data_pedido"].min().strftime("%d/%m/%Y"))
    m2.metric("📈 Pico",     f"R$ {resultado['valor_total'].max():,.2f}")
    m3.metric("📉 Mínimo",   f"R$ {resultado['valor_total'].min():,.2f}")
    st.line_chart(resultado.set_index("data_pedido")[["valor_total", "media_movel"]])
    with st.expander("📋 Ver tabela"):
        st.dataframe(resultado, use_container_width=True)

elif opcao == "📊 Acima da Média":
    media = df["valor_total"].mean()
    resultado = df[df["valor_total"] > media].copy()
    pct = len(resultado) / len(df) * 100

    st.subheader(f"📊 Pedidos Acima da Média (média: R$ {media:.2f})")
    m1, m2, m3 = st.columns(3)
    m1.metric("📊 Média Geral",   f"R$ {media:,.2f}")
    m2.metric("📋 Pedidos Acima", len(resultado))
    m3.metric("📈 % do Total",    f"{pct:.1f}%")
    with st.expander("📋 Ver pedidos acima da média"):
        st.dataframe(resultado, use_container_width=True)

elif opcao == "🎯 Descontos":
    resultado = (
        df.groupby("categoria")
        .agg(desconto_medio=("desconto_pct", "mean"))
        .reset_index()
        .sort_values("desconto_medio", ascending=False)
    )

    st.subheader("🎯 Desconto Médio por Categoria")
    m1, m2, m3 = st.columns(3)
    m1.metric("🎯 Maior Desconto", resultado.iloc[0]["categoria"])
    m2.metric("📉 % Máximo",       f"{resultado['desconto_medio'].max():.1f}%")
    m3.metric("📊 Desconto Geral", f"{df['desconto_pct'].mean():.1f}%")
    st.bar_chart(resultado.set_index("categoria"))
    with st.expander("📋 Ver tabela"):
        st.dataframe(resultado, use_container_width=True)
