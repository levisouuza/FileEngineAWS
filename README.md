# FileEngineAWS

Podemos definir um data pipeline como uma série de estágios de processamento de dados. Basicamente, para termos um pipeline de dados é necessários termos os seguintes agentes:

 - Fonte de dados
 - Engine de Processamento, realizando a atividade de ETL ou ELT.
 - Destino do dados

O projeto FileEngineAWS apresenta um pipeline de dados que extrai arquivos, com uma engine construída em python, de diversos business alocados em um servidor EC2 e são persistidos em um S3 Bucket, considerado como Raw Layer. Os dados das extrações são persistidos em um postgreSQL, criado pelo Amazon RDS e o monitoramento/análise das cargas é realizado por um dashboard no Microsoft PowerBI.
