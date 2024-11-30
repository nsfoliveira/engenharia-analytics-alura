import boto3

# Cliente do AWS Glue
glue_client = boto3.client('glue')

# Criação do crawler
response = glue_client.create_crawler(
    Name='crawler-projetos-eng-analytics',
    Role='AWSGlueServiceRole-zoop',
    DatabaseName='db-glue-zoop',
    Description='Ler e catalogar dados para o projeto zoop da formação de eng de analytics da Alura',
    Targets={
        'S3Targets': [
            {
                'Path': 's3://projetos-eng-analytics-zoop/bronze/',
                'Exclusions': []  # Use para excluir padrões, se necessário
            },
            {
                'Path': 's3://projetos-eng-analytics-zoop/silver/',
                'Exclusions': []
            }
        ]
    },
    TablePrefix='zoop-glue-',  # Prefixo para as tabelas criadas
    RecrawlPolicy={
        'RecrawlBehavior': 'CRAWL_EVERYTHING'  # Recrawl all
    },
    Schedule='',  # "On demand" significa sem agendamento
    SchemaChangePolicy={
        'UpdateBehavior': 'UPDATE_IN_DATABASE',
        'DeleteBehavior': 'LOG'
    }
)

print("Crawler criado com sucesso:", response)
