"""Quais produtos apresentam a maior necessidade de reposição, considerando a quantidade vendida em relação à quantidade remanescente no estoque?"""

# Consulta inicial em SQL
SELECT 
    produto,
    SUM(Quantidade_vendida) AS total_vendida,
    (SUM(Quantidade_em_estoque) - SUM(Quantidade_vendida)) AS estoque_restante
FROM zoop-glue-estoques_zoop_silver
GROUP produto
ORDER BY estoque_restante ASC;

estoque_zoop_silver_dyf = glueContext.create_dynamic_frame.from_catalog(
    database='db-glue-zoop',
    table_name='zoop-glue-estoques_zoop_silver'
)
estoque_zoop_silver_dyf.printSchema()

estoque_zoop_silver_df = estoque_zoop_silver_dyf.toDF().toPandas()
estoque_zoop_silver_df

# Agrupando por Produto e calculando total vendida e estoque restante
df_agrupado = estoque_zoop_silver_df.groupby('Produto').agg(
    total_vendida=('Quantidade_vendida', 'sum'),
    total_novos=('Quantidade_novos_produtos', 'sum')
).reset_index()

df_agrupado['estoque_restante'] = df_agrupado['total_novos'] - df_agrupado['total_vendida']

df_agrupado.head()

df_menores_estoques_restantes = df_agrupado.sort_values(by='estoque_restante').head(10)
print(df_menores_estoques_restantes)

fig, ax = plt.subplots(figsize=(10, 6))
plt.barh(df_menores_estoques_restantes['Produto'], df_menores_estoques_restantes['estoque_restante'], color='skyblue')
plt.xlabel('Menores Estoques Restante')
plt.ylabel('Produto')
plt.title('Produtos com menor estoque restante')
ax.set_frame_on(False)

%matplot plt