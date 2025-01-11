""" Consultando os produtos mais vendidos por Região e Canal"""
SELECT 
    Produto,
    Regiao_cliente,
    Canal_venda,
    SUM(Quantidade) AS total_vendas
FROM 
    "zoop-glue-vendas_zoop_silver"
GROUP BY 
    Produto, Regiao_cliente, Canal_venda
ORDER BY 
    total_vendas DESC;

"""Carregando a base de dados de vendas da camada Silver no AWS Glue como um DynamicFrame, 
que permite a manipulação de dados em larga escala. 
O comando printSchema() exibe a estrutura da tabela carregada."""

# Importando a base de dados de vendas no formato DynamicFrame
vendas_zoop_silver_dyf = glueContext.create_dynamic_frame.from_catalog(
    database='db-glue-zoop', 
table_name='zoop-glue-vendas_zoop_silver')
vendas_zoop_silver_dyf.printSchema()

#Convertendo o DynamicFrame de vendas para um spark DataFrame e na sequência para um pandas DataFrame:

vendas_zoop_silver_df = vendas_zoop_silver_dyf.toDF().toPandas()
vendas_zoop_silver_df

#Importando a biblioteca matplotlib

import matplotlib.pyplot as plt

#Instalando a biblioteca seaborn

%pip install seaborn matplotlib

#Importando a biblioteca seaborn

import seaborn as sns

# Agrupar dados por Produto e Região de Cliente

vendas_agrupadas = vendas_zoop_silver_df.groupby(['Produto', 'Regiao_cliente'])['Quantidade'].sum().reset_index()

vendas_agrupadas

# Ordenar produtos pelos mais vendidos

top_5_produtos = vendas_agrupadas.groupby('Produto')['Quantidade'].sum().nlargest(5).index

top_5_produtos

# Filtrar os 5 produtos mais vendidos

vendas_top_5 = vendas_agrupadas[vendas_agrupadas['Produto'].isin(top_5_produtos)]

vendas_top_5

# Plotar o gráfico de vendas dos 5 produtos mais vendidos por região

plt.figure(figsize=(12, 6))
sns.barplot(data=vendas_top_5, x='Produto', y='Quantidade', hue='Regiao_cliente')
plt.legend(bbox_to_anchor=(1,1))
plt.title('Top 5 Produtos Mais Vendidos por Região', fontsize = 14)
plt.xticks(rotation=0)
plt.ylabel('Total de Vendas', fontsize = 12)
plt.xlabel('Produto', fontsize = 12)
sns.despine()

%matplot plt

# Agrupar os dados por Canal de Venda e calcular o total de vendas por canal

vendas_por_canal = vendas_zoop_silver_df.groupby('Canal_venda')['Quantidade'].sum().reset_index()
vendas_por_canal = vendas_por_canal.sort_values('Quantidade',ascending=False) 

# Plotar o gráfico de vendas por canal de venda

plt.figure(figsize=(12, 6))
ax=sns.barplot(data=vendas_por_canal, x='Canal_venda', y='Quantidade')
plt.title('Eficiência dos Canais de Venda', fontsize=14)
plt.ylabel('Total de Vendas', fontsize=12)
plt.xlabel('Canal de Venda', fontsize=12)
sns.despine()

# Adicionando os rótulos às barras

ax.bar_label(ax.containers[0])
%matplot plt