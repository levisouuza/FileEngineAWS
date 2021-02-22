
"""
Purpose:
    Script to use in basic operations on PostgreSQL created in AWS RDS.
"""

from support.credentials import Host, Database, User, Password
import psycopg2 as pg


class DbConnection:

    def __init__(self):
        """
        self.connection: connection in Postgresql database
        """
        self.connection = pg.connect(
                host=Host,
                database=Database,
                user=User,
                password=Password
        )

    def db_cursor(self):
        """
        :return: return in database cursor
        """
        return self.connection.cursor()

    def update_sn_hist(self, id_verificacao):
        """
        Function to realize update in field sn_carga_historica.
        :param id_verificacao: field to filter the folder updated
        """
        cursor = self.connection.cursor()
        cursor.execute('''update lake.verifica_carga set sn_carga_historica='N' where id_verifica_carga = %s''',
                       (id_verificacao,))

        self.connection.commit()

    def update_datetime(self, id_verificacao, last_update):
        """
        Function to realize update in datetime field to show last update folder
        :param id_verificacao: field to filter the folder updated
        :param last_update: datetime field
        """
        cursor = self.connection.cursor()
        cursor.execute('''update lake.verifica_carga set data_atualizacao_diretorio = %s where id_verifica_carga = %s''',
                       (last_update, id_verificacao))

        self.connection.commit()

    def update_meta_file(self, files, last_update_file, id_meta_arquivo, last_update):
        """
        :param files: name last file updated
        :param last_update_file: last datetime file updated (creation date or updated date)
        :param id_meta_arquivo: field to filter the folder updated
        :param last_update:  datetime field
        """
        cursor = self.connection.cursor()
        cursor.execute(''' update lake.meta_arquivo set ultimo_arquivo = %s, data_atualizacao_arquivo= %s, data_insercao_arquivo = %s 
                        where id_meta_arquivo = %s''', (files, last_update_file, last_update, id_meta_arquivo,))

        self.connection.commit()

    def insert_log(self, id_verificacao, id_meta_arquivo, file, insert_date):
        """
        :param id_verificacao: last file name updated
        :param id_meta_arquivo: field to filter the folder updated
        :param file: file transfered for S3 bucket
        :param insert_date: datetime insert transfer queue
        """
        cursor = self.connection.cursor()
        cursor.execute('''insert into lake.log_inserts_file (id_verifica_carga, id_meta_arquivo, arquivo_name, data_inclusao_arquivo) values (%s, %s, %s, %s)''',
                       (id_verificacao, id_meta_arquivo, file, insert_date))

        self.connection.commit()