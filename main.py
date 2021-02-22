from SearchEngine.FileSearch import FileSearch
from awsS3.S3management import S3transfer
from datetime import datetime
from time import sleep

start = datetime.now()

bucket = 'bucket-name'

print("{} - Bucket Selecionado: {}".format(datetime.now(), bucket))
print("\n")

file_upload = FileSearch().file_search()

print("\n")
print("{} - REALIZANDO TRANSFERENCIA PARA O BUCKET".format(datetime.now()))
print('\n')

for file in file_upload:
    folder_out = file.split('/')[4]
    file_out = file.split('/')[5]
    object_out = folder_out + '/' + file_out

    print("{} - Transferindo arquivo {}".format(datetime.now(), object_out))
    S3transfer().s3_upload(file, bucket, object_out)

    sleep(0.5)

end = datetime.now()
print("\n")
print("Tempo de processo: Inicio: {} | Fim: {}".format(start, end))
print("\n")
print("*************************************************************")
print("**    Finalizando Tranferencia de arquivos para o Lake     **")
print("*************************************************************")
print("\n")


