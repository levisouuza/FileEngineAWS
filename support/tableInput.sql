/*
Query utilizada para retornar informações dos arquivos cadastrados para que o robô 
procure os novos arquivos inseridos no servidor inicial
*/

select
     verif.id_verifica_carga
    ,verif.diretorio_raiz
    ,verif.pasta_origem
    ,verif.sn_carga_historica
    ,id_meta_arquivo
    ,meta.arquivo_base
    ,meta.data_atualizacao_arquivo
from lake.verifica_carga verif
    left join lake.meta_arquivo meta
    on verif.id_verifica_carga
    = meta.id_verifica_carga
order by verif.id_verifica_carga,
        meta.arquivo_base;
