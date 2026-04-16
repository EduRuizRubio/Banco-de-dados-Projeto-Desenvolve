import mysql.connector
import pandas as pd

# conexão
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bAtata2212!",
    database="ecom_data",
    charset='utf8mb4'
)

print("Conectado com sucesso!")


# 📊 GROUP BY - cidade
query1 = """
SELECT 
    cidade,
    COUNT(order_id) AS total_pedidos,
    SUM(valor_total) AS faturamento_total,
    AVG(valor_total) AS ticket_medio
FROM ecom_data
GROUP BY cidade
ORDER BY faturamento_total DESC
"""

df_cidade = pd.read_sql(query1, conexao)
print(df_cidade.head())



# 📊 GROUP BY - categoria
query2 = """
SELECT 
    categoria,
    subcategoria,
    SUM(valor_total) AS faturamento
FROM ecom_data
GROUP BY categoria, subcategoria
ORDER BY faturamento DESC
"""

df_categoria = pd.read_sql(query2, conexao)



# 🧠 WINDOW FUNCTION - ranking
query3 = """
SELECT 
    customer_id,
    SUM(valor_total) AS total_gasto,
    RANK() OVER (ORDER BY SUM(valor_total) DESC) AS ranking
FROM ecom_data
GROUP BY customer_id
"""

df_ranking = pd.read_sql(query3, conexao)



# 📊 Percentual do total
query4 = """
SELECT 
    order_id,
    valor_total,
    SUM(valor_total) OVER () AS total_geral,
    valor_total / SUM(valor_total) OVER () * 100 AS percentual
FROM ecom_data
"""

df_percentual = pd.read_sql(query4, conexao)



# 📈 Média móvel
query5 = """
SELECT 
    data_pedido,
    valor_total,
    AVG(valor_total) OVER (
        ORDER BY data_pedido 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS media_movel
FROM ecom_data
"""

df_media_movel = pd.read_sql(query5, conexao)



# 🔗 JOIN com média do cliente
query6 = """
SELECT *
FROM ecom_data e
JOIN (
    SELECT customer_id, AVG(valor_total) AS media_cliente
    FROM ecom_data
    GROUP BY customer_id
) m ON e.customer_id = m.customer_id
WHERE m.media_cliente > 1000
"""

df_clientes_top = pd.read_sql(query6, conexao)



# 📊 Subquery (acima da média)
query7 = """
SELECT *
FROM ecom_data
WHERE valor_total > (
    SELECT AVG(valor_total) FROM ecom_data
)
"""

df_acima_media = pd.read_sql(query7, conexao)



# 🎯 Desconto médio por categoria
query8 = """
SELECT 
    categoria,
    AVG(desconto_pct) AS desconto_medio
FROM ecom_data
GROUP BY categoria
"""

df_desconto = pd.read_sql(query8, conexao)



# 📊 Desconto vs valor
query9 = """
SELECT 
    desconto_pct,
    AVG(valor_total) AS media_valor
FROM ecom_data
GROUP BY desconto_pct
ORDER BY desconto_pct
"""

df_relacao = pd.read_sql(query9, conexao)


print("Tudo executado com sucesso 🚀")