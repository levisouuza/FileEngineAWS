CREATE SCHEMA lake;
-----------------------------------------------------------------------------------------------------
DROP SEQUENCE IF EXISTS lake.id_verifica_carga;
CREATE SEQUENCE lake.id_verifica_carga
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 9999 
    START 1 
    CACHE 1;

DROP TABLE IF EXISTS lake.verifica_carga;
CREATE TABLE IF NOT EXISTS lake.verifica_carga(
        id_verifica_carga int not null default nextval('lake.id_verifica_carga'::regclass) primary key,
        diretorio_raiz varchar(20) not null,
        pasta_origem varchar(15) not null,
        sn_carga_historica char(1) not null,
        data_atualizacao_diretorio timestamp
        );
        


INSERT INTO lake.verifica_carga(diretorio_raiz, pasta_origem, sn_carga_historica)
VALUES
('/home/ubuntu/lake','sales','S'),
('/home/ubuntu/lake','laws','S'),
('/home/ubuntu/lake','public_account','S'),
('/home/ubuntu/lake','crm','S');

-----------------------------------------------------------------------------------------------------

DROP SEQUENCE lake.id_meta_arquivo;
CREATE SEQUENCE lake.id_meta_arquivo
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 9999
    START 1 
    CACHE 1;
    
DROP TABLE IF EXISTS lake.meta_arquivo;
CREATE TABLE IF NOT EXISTS lake.meta_arquivo(
                id_meta_arquivo int not null default  nextval ('lake.id_meta_arquivo') primary key,
                id_verifica_carga int not null,
                arquivo_base varchar(50) not null,
                ultimo_arquivo varchar(50) ,
                data_atualizacao_arquivo timestamp,
                data_insercao_arquivo timestamp,
                FOREIGN KEY (id_verifica_carga) REFERENCES lake.verifica_carga (id_verifica_carga) 
);

INSERT INTO  lake.meta_arquivo(id_verifica_carga,arquivo_base)
VALUES
(1,'Vendas_Internacional.csv'),
(1,'Vendas_Nacional.csv'),
(2,'AWS_Well_Architected_Framework.pdf'),
(3,'municipios_receitas.csv'),
(4,'clientes.csv');
-----------------------------------------------------------------------------------------------------

DROP SEQUENCE lake.id_log_inserts_file;
CREATE SEQUENCE lake.id_log_inserts_file
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 999999999999
    START 1
    CACHE 1;

DROP TABLE IF EXISTS lake.log_inserts_file;
CREATE TABLE IF NOT EXISTS lake.log_inserts_file(
                    id_log_inserts_file int not null default nextval ('lake.id_log_inserts_file') primary key,
                    id_verifica_carga int not null,
                    id_meta_arquivo int not null,
                    arquivo_name varchar(50) not null,
                    data_inclusao_arquivo timestamp not null,
                    FOREIGN KEY (id_verifica_carga) REFERENCES lake.verifica_carga(id_verifica_carga),
                    FOREIGN KEY (id_meta_arquivo) REFERENCES lake.meta_arquivo(id_meta_arquivo)
);
