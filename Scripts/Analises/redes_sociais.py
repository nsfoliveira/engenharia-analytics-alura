"""" As avaliações e os comentários nas redes sociais impactam diretamente as vendas dos produtos?"""

SELECT 
    v.produto,
    rs.Avaliacao,
    SUM(v.Quantidade) AS total_vendas
FROM 
    "zoop-glue-redes_sociais_zoop_silver" rs
JOIN
    "zoop-glue-vendas_zoop_silver" v ON rs.Nome_produto = v.Produto
GROUP BY 
    v.produto, rs.Avaliacao
ORDER BY 
    rs.Avaliacao DESC;


redes_sociais_zoop_silver_dyf = glueContext.create_dynamic_frame.from_catalog(
    database='db-glue-zoop', 
    table_name='zoop-glue-redes_sociais_zoop_silver')
redes_sociais_zoop_silver_dyf.printSchema()

redes_sociais_zoop_silver_df = redes_sociais_zoop_silver_dyf.toDF().toPandas()
redes_sociais_zoop_silver_df

import pandas as pd

# Unir os dados de redes sociais e vendas para análise

social_vendas = pd.merge(redes_sociais_zoop_silver_df, vendas_zoop_silver_df, left_on='Nome_produto', right_on='Produto')

print(social_vendas.columns)

Index(['ID_social', 'Data_x', 'Influencia_autor', 'Plataforma', 'Nome_produto',
       'Categoria_produto_x', 'Avaliacao_x', 'Comentario', 'ID_venda',
       'Data_y', 'Horario', 'Canal_venda', 'Origem_venda', 'ID_produto',
       'Produto', 'Categoria_produto_y', 'Preco_unitario', 'Quantidade',
       'Metodo_pagamento', 'ID_cliente', 'Nome_cliente', 'Genero_cliente',
       'Idade_cliente', 'Cidade_cliente', 'UF_cliente', 'Regiao_cliente',
       'Avaliacao_y'],
      dtype='object')

# Agrupar por produto e avaliação, somando as vendas

social_vendas_agrupadas = social_vendas.groupby(['Nome_produto', 'Avaliacao_x'])['Quantidade'].sum().reset_index()

print(social_vendas_agrupadas)

# Plotar gráfico de vendas por avaliação nas redes sociais

plt.figure(figsize=(12, 6))
sns.barplot(data=social_vendas_agrupadas, x='Avaliacao_x', y='Quantidade',errorbar=None)
plt.title('Impacto das Avaliações nas Vendas por Produto')
plt.xlabel('Avaliação nas Redes Sociais')
plt.ylabel('Total de Vendas')

%matplot plt