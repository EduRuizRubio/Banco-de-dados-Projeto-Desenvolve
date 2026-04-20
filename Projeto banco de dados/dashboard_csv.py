import streamlit as st
import pandas as pd

# - - - - - - README - - - - - -

# Esse código usa o arquivo ecom_data.csv para gerar gráficos e tabelas da dashboard

# Rode o código abaixo no terminal:
#   python -m streamlit run dashboard_csv.py

# Carrega o CSV uma única vez (cache para performance)
@st.cache_data
def carregar_dados():
    df = pd.read_csv("ecom_data.csv", parse_dates=["data_pedido"])
    return df

df = carregar_dados()

# Configuração da página
st.set_page_config(page_title="Dashboard E-commerce", layout="wide")
st.title("📊 Dashboard E-commerce")
st.caption("Fonte de dados: ecom_data.csv")

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

    st.subheader("Faturamento por Cidade")
    st.dataframe(resultado)
    st.bar_chart(resultado.set_index("cidade")["faturamento_total"])


# Faturamento por categoria
elif opcao == "📦 Categoria":
    resultado = (
        df.groupby(["categoria", "subcategoria"])
        .agg(faturamento=("valor_total", "sum"))
        .sort_values("faturamento", ascending=False)
        .reset_index()
    )

    st.subheader("Faturamento por Categoria")
    st.dataframe(resultado)
    st.bar_chart(resultado.set_index("categoria")["faturamento"])


# Ranking dos clientes
elif opcao == "🏆 Ranking Clientes":
    resultado = (
        df.groupby("customer_id")
        .agg(total_gasto=("valor_total", "sum"))
        .sort_values("total_gasto", ascending=False)
        .reset_index()
    )
    resultado.insert(0, "ranking", range(1, len(resultado) + 1))

    st.subheader("Ranking de Clientes")
    st.dataframe(resultado)


# Percentual por pedido
elif opcao == "📊 Percentual por Pedido":
    total_geral = df["valor_total"].sum()
    resultado = df[["order_id", "valor_total"]].copy()
    resultado["total_geral"] = total_geral
    resultado["percentual"] = resultado["valor_total"] / total_geral * 100

    st.subheader("Percentual dos Pedidos")
    st.dataframe(resultado)


# Média Móvel
elif opcao == "📈 Média Móvel":
    resultado = (
        df[["data_pedido", "valor_total"]]
        .sort_values("data_pedido")
        .copy()
    )
    resultado["media_movel"] = (
        resultado["valor_total"]
        .rolling(window=3, min_periods=1)
        .mean()
    )

    st.subheader("Média Móvel (janela de 3 registros)")
    st.line_chart(resultado.set_index("data_pedido")[["valor_total", "media_movel"]])


# Acima da Média
elif opcao == "📊 Acima da Média":
    media = df["valor_total"].mean()
    resultado = df[df["valor_total"] > media].copy()

    st.subheader(f"Pedidos Acima da Média (média: R$ {media:.2f})")
    st.dataframe(resultado)


# Descontos
elif opcao == "🎯 Descontos":
    resultado = (
        df.groupby("categoria")
        .agg(desconto_medio=("desconto_pct", "mean"))
        .reset_index()
    )

    st.subheader("Desconto Médio por Categoria")
    st.dataframe(resultado)
    st.bar_chart(resultado.set_index("categoria"))
