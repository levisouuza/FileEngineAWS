"""
Purpose:
    Capture engine to search files to insert in S3 buckets
"""

from support.credentials import Host, Database, User
from Database.DbConnection import DbConnection
from datetime import datetime
from time import sleep
import os
import re

print("\n")
print("*************************************************************")
print("** Iniciando Tranferencia de arquivos para o Lake (AWS S3) **")
print("*************************************************************")
print("\n")

print("********************************************************************************")
print("* {} - Conectando ao Banco de dados para verificacao   *".format(datetime.now()))
print("*                                                                              *\n")
print("* Parametros de acesso:                                                        *")
print("* Host................:{}   *".format(Host))
print("* Database............:{}                                            *".format(Database))
print("* User................:{}                                                   *".format(User))
print("********************************************************************************")
print("\n")

sleep(0.3)


class FileSearch:

    def __init__(self):

        self.connect = DbConnection()
        self.cursor = self.connect.db_cursor()
        self.file_upload = list()

        self.query = open(r'/home/ubuntu/app/support/tableInput.sql')
        self.query_string = self.query.read()

    def file_search(self):

        global last_file, last_update, file_standard, last_file_update

        last_file = ''
        last_update = datetime.fromtimestamp(00000000000.00)

        print("{} - Executando a query de verificacao".format(datetime.now()))
        print("\n")
        self.cursor.execute(self.query_string)

        for iterator in self.cursor.fetchall():
            row = list(iterator)
            department = row[2]
            file_path = row[1] + "/" + department
            historical_charge = row[3]
            id_verifica_carga = row[0]
            id_meta_arquivo = row[4]
            arquivo_base = row[5]
            data_atualizacao_arquivo = row[6]

            last_file = ''
            last_update = datetime.fromtimestamp(00000000000.00)
            file_standard = ''

            print("===============================================================")
            print("{} - Verificando atualizacao pasta {}".format(datetime.now(), id_verifica_carga))
            print("Departamento.............:{}".format(department))
            print("Diretorio................:{}".format(file_path))
            print("Arquivo base.............:{}".format(arquivo_base))
            print("Data atualizacao arquivo.:{}".format(data_atualizacao_arquivo))
            print("===============================================================")
            print("\n")
            sleep(0.5)

            # block for historical load
            if historical_charge in 'Ss':

                print("{} - Processo de carga historica".format(datetime.now()))

                sleep(0.3)

                for file_input in os.listdir(file_path):

                    file = file_path + "/" + file_input

                    if ("".join(re.findall("\d+", file_input))).isdigit() and arquivo_base[:-4] in file_input:
                        self.file_upload.append(str(file))

                        # log insert

                        self.connect.insert_log(id_verifica_carga, id_meta_arquivo, file_input, datetime.now())

                        sleep(0.3)

                        print("{} - Inserindo arquivo {} na fila de transferencia.".format(datetime.now(), file_input))

                        if datetime.fromtimestamp(os.path.getmtime(file)) > last_update:
                            last_update = datetime.fromtimestamp(os.path.getmtime(file))
                            last_file = file_input

                print("\n")
                print("{} - Atualizando de monitoramento de cargas".format(datetime.now()))
                self.connect.update_meta_file(last_file, last_update, id_meta_arquivo, datetime.now())
                sleep(0.2)

                print("{} - Atualizando campo de carga historica.".format(datetime.now()))
                self.connect.update_sn_hist(id_verifica_carga)
                sleep(0.2)

                print("{} - Atualizando campo de atualizacao do diretorio".format(datetime.now()))
                self.connect.update_datetime(id_verifica_carga, datetime.now())
                sleep(0.2)

            # Block for update folders
            if historical_charge in 'Nn':

                print("{} - Processo de atualizacao de carga".format(datetime.now()))

                sleep(0.1)

                id_meta_arquivo_anterior = 0
                last_file_update = datetime.fromtimestamp(00000000000.00)

                for file_input in os.listdir(file_path):

                    file = file_path + "/" + file_input

                    if ("".join(re.findall("\d+", file_input))).isdigit() \
                            and datetime.fromtimestamp(os.path.getmtime(file)) > list(iterator)[6] \
                            and arquivo_base[:-4] in file_input:
                        self.file_upload.append(str(file))

                        # log insert
                        self.connect.insert_log(id_verifica_carga, id_meta_arquivo, file_input, datetime.now())

                        sleep(0.3)

                        print("{} - Inserindo arquivo {} na fila de transferencia.".format(datetime.now(), file_input))

                        last_update = datetime.fromtimestamp(os.path.getmtime(file))

                        if len(self.file_upload) > 0:

                            if id_meta_arquivo_anterior == 0:
                                id_meta_arquivo_anterior = id_meta_arquivo
                                last_file = file_input
                                last_file_update = last_update
                            else:
                                if last_file_update < last_update:
                                    last_file = file_input
                                    last_file_update = last_update

                                    print("\n")
                                    print("{} - Atualizando de monitoramento de cargas".format(datetime.now()))
                                    self.connect.update_meta_file(last_file, last_update, id_meta_arquivo,
                                                                  datetime.now())
                                    sleep(0.2)

                                    print("{} - Atualizando campo de atualizacao do diretorio".format(datetime.now()))
                                    self.connect.update_datetime(id_verifica_carga, datetime.now())

        return self.file_upload
