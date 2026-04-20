
  PROJETO: DASHBOARD ANALÍTICO DE E-COMMERCE
===========================

Projeto desenvolvido como parte do Projeto Desenvolve, com foco
em análise de dados de uma loja virtual usando Python, MySQL e
Streamlit.

-------------------------------------------------------------
DESCRIÇÃO
-------------------------------------------------------------

Este projeto simula uma base de dados de pedidos de e-commerce,
aplica consultas SQL analíticas e exibe os resultados em um
dashboard interativo construído com Streamlit.

O objetivo é praticar conceitos de:
  - Geração e modelagem de dados sintéticos
  - Conexão Python <-> MySQL
  - Consultas SQL intermediárias e avançadas (GROUP BY, Window
    Functions, Subqueries, JOINs)
  - Criação de Views no banco de dados
  - Visualização de dados com Streamlit

-------------------------------------------------------------
ESTRUTURA DO PROJETO
-------------------------------------------------------------

  gerador_dataset.py        → Gera o dataset sintético de 1000
                              pedidos e exporta para ecom_data.csv

  ecom_data.csv             → Dataset com os dados dos pedidos
                              gerado pelo script acima

  puxando_banco.py          → Conecta ao MySQL e executa as
                              consultas SQL de análise

  Criacao_de_consultas_sql.sql → Script SQL com a criação das 
                                 Views analíticas no banco

  dashboard.py              → Dashboard interativo com Streamlit
                              que exibe os gráficos e tabelas

  README.txt                → Este arquivo

-------------------------------------------------------------
DATASET - COLUNAS
-------------------------------------------------------------

  order_id         → Identificador único do pedido
  
  customer_id      → Identificador do cliente (1 a 300)
  
  data_pedido      → Data do pedido (entre 01/01/2023 e 31/12/2023)
  
  categoria        → Categoria do produto
  
  subcategoria     → Subcategoria do produto
  
  preco_unitario   → Preço fixo por subcategoria
  
  quantidade       → Quantidade de itens (1 a 5)
  
  desconto_pct     → Desconto aplicado (0%, 5%, 10%, 15% ou 20%)
  
  status_pedido    → Status: Entregue, Pendente, Cancelado, Em trânsito
  
  cidade           → Cidade do pedido (5 capitais brasileiras)
  
  avaliacao        → Nota do cliente de 1 a 5 (somente pedidos Entregues)
  
  valor_total      → Valor calculado: preço × quantidade × (1 - desconto)

  Obs: algumas vezes o MySQL gerou o banco de dados com a coluna "order_id" como "ï»¿order_id", é necessário renomear a coluna para "order_id" no MySQL.

-------------------------------------------------------------
CATEGORIAS E SUBCATEGORIAS
-------------------------------------------------------------

  Eletrônicos   → Celular (R$1200), Câmera (R$800), Relógio (R$350)
  
  Roupas        → Blusa (R$80), Short (R$60), Calça (R$120)
  
  Casa & Jardim → Sofá (R$900), Vaso (R$70), Luminária (R$150)
  
  Esportes      → Tênis (R$250), Bicicleta (R$1500), Haltere (R$200)
  
  Livros        → Romance (R$40), Técnico (R$120), Infantil (R$30)

-------------------------------------------------------------
ANÁLISES DISPONÍVEIS NO DASHBOARD
-------------------------------------------------------------

  📍 Cidade            → Faturamento total, número de pedidos e
                          ticket médio por cidade

  📦 Categoria         → Faturamento por categoria e subcategoria

  🏆 Ranking Clientes  → Clientes ranqueados pelo total gasto
                          (Window Function: RANK)

  📊 Percentual por Pedido → Participação percentual de cada pedido
                              no faturamento total (Window Function: SUM OVER)

  📈 Média Móvel       → Média móvel de 3 dias do valor dos pedidos
                          (Window Function: AVG OVER ROWS)

  📊 Acima da Média    → Pedidos com valor acima da média geral
                          (Subquery)

  🎯 Descontos         → Desconto médio por categoria

-------------------------------------------------------------
VIEWS SQL CRIADAS
-------------------------------------------------------------

  vw_cidade             → Análise por cidade
  
  vw_categoria          → Análise por categoria/subcategoria
  
  vw_ranking_clientes   → Ranking de clientes por total gasto
  
  vw_percentual_pedidos → Percentual por pedido
  
  vw_media_movel        → Média móvel de faturamento
  
  vw_acima_media        → Pedidos acima da média
  
  vw_descontos          → Desconto médio por categoria

-------------------------------------------------------------
COMO OBTER O PROJETO
-------------------------------------------------------------

  Clone o repositório para sua máquina local usando o Git:

    git clone https://github.com/seu-usuario/nome-do-repositorio.git

  Em seguida, acesse a pasta do projeto:

    cd nome-do-repositorio

  Obs.: Substitua "seu-usuario" e "nome-do-repositorio" pelo
  endereço real do repositório no GitHub.

-------------------------------------------------------------
REQUISITOS
-------------------------------------------------------------

  Python 3.8+
  MySQL Server (rodando localmente)
  
  Bibliotecas Python:
    pip install streamlit pandas mysql-connector-python numpy

-------------------------------------------------------------
CONFIGURAÇÃO DO BANCO DE DADOS (com MySQL)
-------------------------------------------------------------

  1. Instale o MySQL Community Server e o MySQL Workbench:
       https://dev.mysql.com/downloads/

  2. Configure um servidor local no MySQL Workbench:
       - Abra o MySQL Workbench e crie uma nova conexão
         com host "localhost", porta 3306 e usuário "root".
       - Teste a conexão e salve.

  3. Crie o Schema ecom_data:
       - No MySQL Workbench, clique com o botão direito em
         "Schemas" no painel esquerdo e selecione
         "Create Schema...".
       - Nomeie o schema como: ecom_data
       - Clique em "Apply" para confirmar.

  4. Importe o CSV usando o Table Data Import Wizard:
       - Clique com o botão direito sobre o schema ecom_data
         e selecione "Table Data Import Wizard".
       - Selecione o arquivo ecom_data.csv do projeto.
       - Siga os passos do assistente: escolha criar uma nova
         tabela chamada "ecom_data", confirme os tipos de
         coluna detectados automaticamente e clique em "Next"
         até finalizar a importação.
       - Lembre-se de checar se as colunas foram importadas corretamente, pois o MySQL pode gerar o banco de dados com a coluna "order_id" como "ï»¿order_id", é necessário renomear a coluna para "order_id" no MySQL.

  5. Ajuste as credenciais de acesso nos arquivos
     puxando_banco.py e dashboard.py:

       host     = "localhost"

       user     = "root"
       
       password = "sua_senha"
       
       database = "ecom_data"

  6. Execute o script de views SQL (opcional):
       Criacao_de_consultas_sql.sql

-------------------------------------------------------------
COMO EXECUTAR (com MySQL)
-------------------------------------------------------------

  1. Gere o dataset (caso necessário):
       python gerador_dataset.py

  2. Execute as consultas de análise:
       python puxando_banco.py

  3. Inicie o dashboard:
       python -m streamlit run dashboard_mysql.py

     O dashboard abrirá automaticamente no navegador em:
       http://localhost:8501

-------------------------------------------------------------
COMO EXECUTAR (direto do CSV, sem MySQL)
-------------------------------------------------------------

  Essa versão não exige instalação do MySQL. Basta ter o
  arquivo ecom_data.csv na mesma pasta e rodar:

  1. Instale apenas as dependências necessárias:
       pip install streamlit pandas

  2. Acesse a pasta do projeto:
       cd "Projeto banco de dados"

  3. Inicie o dashboard:
       python -m streamlit run dashboard_csv.py

     O dashboard abrirá automaticamente no navegador em:
       http://localhost:8501

  Obs.: Todas as análises são equivalentes à versão com MySQL,
  mas os dados são lidos diretamente do arquivo ecom_data.csv
  usando a biblioteca pandas.

-------------------------------------------------------------
AUTOR
-------------------------------------------------------------

  Autor: Eduardo Ruiz Rubio
  
  Projeto desenvolvido como parte do Projeto Desenvolve da cidade de Itabira.

