import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
  
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
dyf = glueContext.create_dynamic_frame.from_catalog(database='db-glue-zoop', 
table_name='zoop-glue-redes_sociais_zoop_bronze_parquet')
dyf.printSchema()
df = dyf.toDF()
df.show(5, truncate=False) # mostrar apenas as 5 primeiras linhas e o truncate = false para que ele mostre 
# todos os valores das linhas

from pyspark.sql.functions import regexp_extract, regexp_replace 
# primeira função é para extração e a segunda para substituição de valores
# Criando uma coluna chamada avaliação onde conterá apenas o valor número da Nota atribuída ao produto 
# na variável comentário
df = df.withColumn('Avaliacao', regexp_extract('Comentario', r'Nota (\d)', 1))
df.show(5, truncate=False) # mostrar apenas as 5 primeiras linhas e o truncate = false para que ele mostre 
# todos os valores das linhas
# Tratando a coluna comentário para substituir Nota 'valor' por nada, assim a variável fica apenas com os 
# comentários
df = df.withColumn('Comentario', regexp_replace('Comentario', r'Nota \d', ''))
df.show(5, truncate=False) # mostrar apenas as 5 primeiras linhas e o truncate = false para que ele mostre 
# todos os valores das linhas
df.printSchema()
from awsglue.dynamicframe import DynamicFrame

redes_sociais_dyf = DynamicFrame.fromDF(df, glueContext)
# Mapeando as variáveis e aplicando transformações (renomeando variáveis e convertendo tipo de dados)

redes_sociais_dyf = redes_sociais_dyf.apply_mapping(
    mappings=[
        ("ID_social", "long", "id_estoque", "long"),
        ("Data", "string", "data", "date"),
        ("Influencia_autor", "long", "influencia_autor", "int"),
        ("Plataforma", "string", "plataforma", "string"),
        ("Nome_produto", "string", "produto", "string"),
        ("Categoria_produto", "string", "categoria_produto", "string"),
        ("Avaliacao", "string", "avaliacao", "int"),
        ("Comentario", "string", "comentario", "string")        
    ]
)

redes_sociais_dyf.printSchema()
s3output = glueContext.getSink(
  path="s3://projetos-eng-analytics-zoop/silver/sot-redes-sociais",
  connection_type="s3",
  updateBehavior="UPDATE_IN_DATABASE",
  partitionKeys=[],
  compression="snappy",
  enableUpdateCatalog=True,
  transformation_ctx="s3output",
)
s3output.setCatalogInfo(
  catalogDatabase="db-glue-zoop", catalogTableName="zoop-glue-redes_sociais_zoop_silver"
)
s3output.setFormat("glueparquet")
s3output.writeFrame(redes_sociais_dyf)
job.commit()