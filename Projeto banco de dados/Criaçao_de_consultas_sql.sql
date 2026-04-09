USE ecom_data;

-- Cidade
CREATE OR REPLACE VIEW vw_cidade AS
SELECT 
    cidade,
    COUNT(order_id) AS total_pedidos,
    SUM(valor_total) AS faturamento_total,
    AVG(valor_total) AS ticket_medio
FROM ecom_data
GROUP BY cidade;

-- Categoria
CREATE OR REPLACE VIEW vw_categoria AS
SELECT 
    categoria,
    subcategoria,
    SUM(valor_total) AS faturamento
FROM ecom_data
GROUP BY categoria, subcategoria;

-- Ranking Clientes
CREATE OR REPLACE VIEW vw_ranking_clientes AS
SELECT 
    customer_id,
    SUM(valor_total) AS total_gasto,
    RANK() OVER (ORDER BY SUM(valor_total) DESC) AS ranking
FROM ecom_data
GROUP BY customer_id;

-- Percentual Pedidos
CREATE OR REPLACE VIEW vw_percentual_pedidos AS
SELECT 
    order_id,
    valor_total,
    SUM(valor_total) OVER () AS total_geral,
    valor_total / SUM(valor_total) OVER () * 100 AS percentual
FROM ecom_data;

-- Média Móvel de 3 dias
CREATE OR REPLACE VIEW vw_media_movel AS
SELECT 
    data_pedido,
    valor_total,
    AVG(valor_total) OVER (
        ORDER BY data_pedido 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS media_movel
FROM ecom_data;

-- Vendas acima da Média
CREATE OR REPLACE VIEW vw_acima_media AS
SELECT *
FROM ecom_data
WHERE valor_total > (
    SELECT AVG(valor_total) FROM ecom_data
);

-- Descontos
CREATE OR REPLACE VIEW vw_descontos AS
SELECT 
    categoria,
    AVG(desconto_pct) AS desconto_medio
FROM ecom_data
GROUP BY categoria;