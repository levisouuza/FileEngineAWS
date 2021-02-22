# FileEngineAWS

Podemos definir um data pipeline como uma série de estágios de processamento de dados. Basicamente, para termos um pipeline de dados, é necessário termos os seguintes agentes:

 - Fonte de dados
 - Engine de Processamento, realizando a atividade de ETL ou ELT.
 - Destino do dados

O projeto FileEngineAWS apresenta um data pipeline que extrai arquivos, com uma engine construída em python, de diversos business, alocados no EC2 e persistidos em um S3 Bucket (Raw Layer). Os dados das extrações são persistidos em um postgreSQL, criado pelo Amazon RDS e o monitoramento/análise das cargas é realizado por um dashboard no PowerBI.

![pipeline](https://github.com/levisouuza/FileEngineAWS/blob/master/images/AWSpipeline.png)

#### Algumas pontos importantes para execução do projeto: 

* **Bibliotecas utilizadas:** boto3 (SDK dos serviços da AWS) e psycopg2 (lib para instânciar o banco de dados).
* **Conectividade e segurança:** Na AWS, é importante que, para desenvolvimento, dentro do Security Group da VPC default, em regras de entrada (Inbound Rules) seja inserido o seu IP e o IP da servidor EC2 aberta na porta 5432, para que ocorra a comunicação entre o EC2 e o RDS (PostgreSQL). Além disso, foi necessário criar um Security Group com a regra de entrada específica do tipo SSH com o IP da máquina local para acessar via Putty e, realizar as devidas alterações no server.

Com a execução do Script, podemos verificar resultado no S3 bucket na imagem abaixo:

![s3bucket](https://github.com/levisouuza/FileEngineAWS/blob/master/images/AWSs3.png)

É possível monitorar o resultado das cargas pelo Dashboard abaixo:

![dash](https://github.com/levisouuza/FileEngineAWS/blob/master/images/MonitorAWS.png)
