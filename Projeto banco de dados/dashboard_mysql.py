import streamlit as st
import pandas as pd
import mysql.connector


# - - - - - - README - - - - - -

# Esse código usa o banco de dados ecom_data diretamente de um servidor local no Mysql

#Rode o código abaixo no terminal:

#python -m streamlit run dashboard.py


# Conexão
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bAtata2212!",
    database="ecom_data",
    charset='utf8mb4',
    collation="utf8mb4_unicode_ci"  
)

# Configuração da página

st.set_page_config(page_title="Dashboard E-commerce", layout="wide")
st.title("📊 Dashboard E-commerce")

# Menu lateral para separar as tabelas e gráficos
opcao = st.sidebar.selectbox(
    "Escolha a análise",
    [
        "📍 Cidade",
        "📦 Categoria",
        "🏆 Ranking Clientes",
        "📊 Percentual por Pedido",
        "📈 Média Móvel",
        "📊 Acima da Média",
        "🎯 Descontos",
    ]
)


# Faturamento por cidade

if opcao == "📍 Cidade":
    query = """
    SELECT 
        cidade,
        COUNT(order_id) AS total_pedidos,
        SUM(valor_total) AS faturamento_total,
        AVG(valor_total) AS ticket_medio
    FROM ecom_data
    GROUP BY cidade
    ORDER BY faturamento_total DESC
    """
    df = pd.read_sql(query, conexao)

    st.subheader("Faturamento por Cidade")
    st.dataframe(df)
    st.bar_chart(df.set_index("cidade")["faturamento_total"])

# Faturamento por categoria
elif opcao == "📦 Categoria":
    query = """
    SELECT 
        categoria,
        subcategoria,
        SUM(valor_total) AS faturamento
    FROM ecom_data
    GROUP BY categoria, subcategoria
    ORDER BY faturamento DESC
    """
    df = pd.read_sql(query, conexao)

    st.subheader("Faturamento por Categoria")
    st.dataframe(df)
    st.bar_chart(df.set_index("categoria")["faturamento"])

# ranking dos clientes
elif opcao == "🏆 Ranking Clientes":
    query = """
    SELECT 
        customer_id,
        SUM(valor_total) AS total_gasto,
        RANK() OVER (ORDER BY SUM(valor_total) DESC) AS ranking
    FROM ecom_data
    GROUP BY customer_id
    """
    df = pd.read_sql(query, conexao)

    st.subheader("Ranking de Clientes")
    st.dataframe(df)

# Percentual por pedido
elif opcao == "📊 Percentual por Pedido":
    query = """
    SELECT 
        order_id,
        valor_total,
        SUM(valor_total) OVER () AS total_geral,
        valor_total / SUM(valor_total) OVER () * 100 AS percentual
    FROM ecom_data
    """
    df = pd.read_sql(query, conexao)

    st.subheader("Percentual dos Pedidos")
    st.dataframe(df)


# 📈 MÉDIA MÓVEL
elif opcao == "📈 Média Móvel":
    query = """
    SELECT 
        data_pedido,
        valor_total,
        AVG(valor_total) OVER (
            ORDER BY data_pedido 
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) AS media_movel
    FROM ecom_data
    """
    df = pd.read_sql(query, conexao)

    st.subheader("Média Móvel")
    st.line_chart(df.set_index("data_pedido")[["valor_total", "media_movel"]])


# -----------------------------
# 📊 ACIMA DA MÉDIA
# -----------------------------
elif opcao == "📊 Acima da Média":
    query = """
    SELECT *
    FROM ecom_data
    WHERE valor_total > (
        SELECT AVG(valor_total) FROM ecom_data
    )
    """
    df = pd.read_sql(query, conexao)

    st.subheader("Pedidos Acima da Média")
    st.dataframe(df)

# -----------------------------
# 🎯 DESCONTOS
# -----------------------------
elif opcao == "🎯 Descontos":
    query = """
    SELECT 
        categoria,
        AVG(desconto_pct) AS desconto_medio
    FROM ecom_data
    GROUP BY categoria
    """
    df = pd.read_sql(query, conexao)

    st.subheader("Desconto Médio por Categoria")
    st.dataframe(df)
    st.bar_chart(df.set_index("categoria"))