import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

n = 1000

# Categorias e subcategorias
subcategorias_map = {
    'Eletrônicos':    ['Celular', 'Câmera', 'Relógio'],
    'Roupas':         ['Blusa', 'Short', 'Calça'],
    'Casa & Jardim':  ['Sofá', 'Vaso', 'Luminária'],
    'Esportes':       ['Tênis', 'Bicicleta', 'Haltere'],
    'Livros':         ['Romance', 'Técnico', 'Infantil'],
}

# Preço fixo por subcategoria
preco_por_subcategoria = {
    'Celular': 1200.00,
    'Câmera': 800.00,
    'Relógio': 350.00,
    'Blusa': 80.00,
    'Short': 60.00,
    'Calça': 120.00,
    'Sofá': 900.00,
    'Vaso': 70.00,
    'Luminária': 150.00,
    'Tênis': 250.00,
    'Bicicleta': 1500.00,
    'Haltere': 200.00,
    'Romance': 40.00,
    'Técnico': 120.00,
    'Infantil': 30.00,
}

status      = ['Entregue', 'Pendente', 'Cancelado', 'Em trânsito']
cidades     = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Curitiba', 'Porto Alegre']
categorias  = list(subcategorias_map.keys())

# Gerar categoria e subcategoria juntas
cat_subcat = [
    (cat := random.choice(categorias), random.choice(subcategorias_map[cat]))
    for _ in range(n)
]
cats, subcats = zip(*cat_subcat)

data_inicio = datetime(2023, 1, 1)
datas = [data_inicio + timedelta(days=random.randint(0, 364)) for _ in range(n)]

# Criar DataFrame (sem avaliação ainda)
df = pd.DataFrame({
    'order_id':       range(1001, 1001 + n),
    'customer_id':    np.random.randint(1, 301, n),
    'data_pedido':    datas,
    'categoria':      cats,
    'subcategoria':   subcats,
    'preco_unitario': [preco_por_subcategoria[sub] for sub in subcats],
    'quantidade':     np.random.randint(1, 6, n),
    'desconto_pct':   np.random.choice([0, 5, 10, 15, 20], n),
    'status_pedido':  np.random.choice(status, n, p=[0.7, 0.15, 0.1, 0.05]),
    'cidade':         np.random.choice(cidades, n),
})

# Avaliação apenas para pedidos entregues
df['avaliacao'] = np.where(
    df['status_pedido'] == 'Entregue',
    np.random.choice([1, 2, 3, 4, 5], size=n, p=[0.05, 0.1, 0.2, 0.35, 0.3]),
    np.nan
)

# Valor total
df['valor_total'] = np.round(
    df['preco_unitario'] * df['quantidade'] * (1 - df['desconto_pct'] / 100), 2
)

df.to_csv('ecom_data.csv', index=False)

print(df.head(10).to_string())
print(f"\nShape: {df.shape}")

print("\nDistribuição categoria/subcategoria:")
print(df.groupby(['categoria', 'subcategoria']).size().to_string())