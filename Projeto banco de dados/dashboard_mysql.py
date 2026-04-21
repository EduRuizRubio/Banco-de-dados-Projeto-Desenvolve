import streamlit as st
import pandas as pd
import mysql.connector

# ── README ────────────────────────────────────────────────────────────────────
# Esse código usa o banco de dados ecom_data diretamente de um servidor local no MySQL
# Rode no terminal ambos abaixo:
#   cd "Projeto banco de dados"
#   python -m streamlit run dashboard_mysql.py

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard E-commerce | MySQL",
    page_icon="🗄️",
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

# ── Conexão ───────────────────────────────────────────────────────────────────
@st.cache_resource
def get_conexao():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="bAtata2212!",
        database="ecom_data",
        charset="utf8mb4",
        collation="utf8mb4_unicode_ci",
    )

try:
    conexao = get_conexao()
except Exception as e:
    st.error(f"❌ Não foi possível conectar ao MySQL: {e}")
    st.info("Certifique-se de que o servidor MySQL está rodando e as credenciais estão corretas.")
    st.stop()

# ── KPIs globais (uma única query) ────────────────────────────────────────────
@st.cache_data(ttl=300)
def kpis_globais():
    q = """
    SELECT
        SUM(valor_total)              AS faturamento_total,
        COUNT(DISTINCT order_id)      AS total_pedidos,
        AVG(valor_total)              AS ticket_medio,
        COUNT(DISTINCT customer_id)   AS total_clientes
    FROM ecom_data
    """
    return pd.read_sql(q, conexao).iloc[0]

kpi = kpis_globais()

# ── Cabeçalho ─────────────────────────────────────────────────────────────────
col_titulo, col_badge = st.columns([4, 1])
with col_titulo:
    st.markdown("## 🗄️ Dashboard E-commerce")
with col_badge:
    st.markdown(
        "<div style='text-align:right;padding-top:10px'>"
        "<span style='background:rgba(248,150,30,0.12);color:#F8961E;"
        "border:1px solid rgba(248,150,30,0.3);border-radius:20px;"
        "padding:5px 14px;font-size:0.78rem;font-weight:600;'>🗄️ MySQL</span>"
        "</div>",
        unsafe_allow_html=True,
    )

k1, k2, k3, k4 = st.columns(4)
k1.metric("💰 Faturamento Total", f"R$ {kpi['faturamento_total']:,.0f}")
k2.metric("📦 Total de Pedidos",  f"{int(kpi['total_pedidos']):,}")
k3.metric("🎫 Compra média",       f"R$ {kpi['ticket_medio']:,.2f}")
k4.metric("👥 Clientes Únicos",   f"{int(kpi['total_clientes']):,}")

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
    df = pd.read_sql("""
        SELECT
            cidade,
            COUNT(order_id)  AS total_pedidos,
            SUM(valor_total) AS faturamento_total,
            AVG(valor_total) AS ticket_medio
        FROM ecom_data
        GROUP BY cidade
        ORDER BY faturamento_total DESC
    """, conexao)

    st.subheader("📍 Faturamento por Cidade")
    m1, m2, m3 = st.columns(3)
    m1.metric("🏙️ Cidade Líder",    df.iloc[0]["cidade"])
    m2.metric("💰 Maior Faturamento", f"R$ {df.iloc[0]['faturamento_total']:,.0f}")
    m3.metric("🎫 Melhor Ticket",
              f"R$ {df.sort_values('ticket_medio', ascending=False).iloc[0]['ticket_medio']:,.2f}")
    st.bar_chart(df.set_index("cidade")["faturamento_total"])
    with st.expander("📋 Ver tabela completa"):
        st.dataframe(df, use_container_width=True)

elif opcao == "📦 Categoria":
    df = pd.read_sql("""
        SELECT
            categoria,
            subcategoria,
            SUM(valor_total) AS faturamento
        FROM ecom_data
        GROUP BY categoria, subcategoria
        ORDER BY faturamento DESC
    """, conexao)
    cat_total = df.groupby("categoria")["faturamento"].sum().reset_index()

    st.subheader("📦 Faturamento por Categoria")
    m1, m2, m3 = st.columns(3)
    top_cat = cat_total.sort_values("faturamento", ascending=False)
    m1.metric("🥇 Top Categoria",    top_cat.iloc[0]["categoria"])
    m2.metric("📦 Nº de Categorias", len(cat_total))
    m3.metric("🧩 Subcategorias",    df["subcategoria"].nunique())
    st.bar_chart(df.set_index("categoria")["faturamento"])
    with st.expander("📋 Ver tabela"):
        st.dataframe(df, use_container_width=True)

elif opcao == "🏆 Ranking Clientes":
    df = pd.read_sql("""
        SELECT
            customer_id,
            SUM(valor_total)  AS total_gasto,
            COUNT(order_id)   AS total_pedidos,
            RANK() OVER (ORDER BY SUM(valor_total) DESC) AS ranking
        FROM ecom_data
        GROUP BY customer_id
    """, conexao)

    st.subheader("🏆 Ranking de Clientes")
    m1, m2, m3 = st.columns(3)
    m1.metric("🥇 Top Cliente",    df.iloc[0]["customer_id"])
    m2.metric("💰 Maior Gasto",    f"R$ {df.iloc[0]['total_gasto']:,.0f}")
    m3.metric("📦 Pedidos do Top", int(df.iloc[0]["total_pedidos"]))
    st.bar_chart(df.set_index("customer_id")["total_gasto"].head(20))
    with st.expander("📋 Ver ranking completo"):
        st.dataframe(df, use_container_width=True)

elif opcao == "📊 Percentual por Pedido":
    df = pd.read_sql("""
        SELECT
            order_id,
            valor_total,
            SUM(valor_total) OVER ()                          AS total_geral,
            valor_total / SUM(valor_total) OVER () * 100     AS percentual
        FROM ecom_data
        ORDER BY percentual DESC
    """, conexao)

    st.subheader("📊 Percentual dos Pedidos")
    m1, m2, m3 = st.columns(3)
    m1.metric("💰 Total Geral",  f"R$ {df['total_geral'].iloc[0]:,.0f}")
    m2.metric("📋 Maior Pedido", f"R$ {df['valor_total'].max():,.2f}")
    m3.metric("📊 % Máximo",     f"{df['percentual'].max():.4f}%")
    with st.expander("📋 Ver tabela completa"):
        st.dataframe(df, use_container_width=True)

elif opcao == "📈 Média Móvel":
    df = pd.read_sql("""
        SELECT
            data_pedido,
            valor_total,
            AVG(valor_total) OVER (
                ORDER BY data_pedido
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
            ) AS media_movel
        FROM ecom_data
        ORDER BY data_pedido
    """, conexao)
    df["data_pedido"] = pd.to_datetime(df["data_pedido"])

    st.subheader("📈 Média Móvel (janela de 3 registros)")
    m1, m2, m3 = st.columns(3)
    m1.metric("📅 Início",  df["data_pedido"].min().strftime("%d/%m/%Y"))
    m2.metric("📈 Pico",    f"R$ {df['valor_total'].max():,.2f}")
    m3.metric("📉 Mínimo",  f"R$ {df['valor_total'].min():,.2f}")
    st.line_chart(df.set_index("data_pedido")[["valor_total", "media_movel"]])
    with st.expander("📋 Ver tabela"):
        st.dataframe(df, use_container_width=True)

elif opcao == "📊 Acima da Média":
    df = pd.read_sql("""
        SELECT *
        FROM ecom_data
        WHERE valor_total > (SELECT AVG(valor_total) FROM ecom_data)
    """, conexao)
    media = pd.read_sql("SELECT AVG(valor_total) AS media FROM ecom_data", conexao).iloc[0]["media"]
    total = pd.read_sql("SELECT COUNT(*) AS total FROM ecom_data", conexao).iloc[0]["total"]
    pct = len(df) / total * 100

    st.subheader(f"📊 Pedidos Acima da Média (média: R$ {media:.2f})")
    m1, m2, m3 = st.columns(3)
    m1.metric("📊 Média Geral",   f"R$ {media:,.2f}")
    m2.metric("📋 Pedidos Acima", len(df))
    m3.metric("📈 % do Total",    f"{pct:.1f}%")
    with st.expander("📋 Ver pedidos acima da média"):
        st.dataframe(df, use_container_width=True)

elif opcao == "🎯 Descontos":
    df = pd.read_sql("""
        SELECT
            categoria,
            AVG(desconto_pct) AS desconto_medio
        FROM ecom_data
        GROUP BY categoria
        ORDER BY desconto_medio DESC
    """, conexao)
    media_geral = pd.read_sql("SELECT AVG(desconto_pct) AS m FROM ecom_data", conexao).iloc[0]["m"]

    st.subheader("🎯 Desconto Médio por Categoria")
    m1, m2, m3 = st.columns(3)
    m1.metric("🎯 Maior Desconto", df.iloc[0]["categoria"])
    m2.metric("📉 % Máximo",       f"{df['desconto_medio'].max():.1f}%")
    m3.metric("📊 Desconto Geral", f"{media_geral:.1f}%")
    st.bar_chart(df.set_index("categoria"))
    with st.expander("📋 Ver tabela"):
        st.dataframe(df, use_container_width=True)