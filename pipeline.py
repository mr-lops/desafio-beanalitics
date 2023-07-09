import os
from dotenv import load_dotenv
from modulos.scraping import scrapy
from modulos.bigquery import salvar_gbq

print('carregando variaveis de ambiente...\n')

load_dotenv()

print('Realizando captura dos dados...\n')
#Realiza a captura dos dados, a função recebe o site
dataframe = scrapy('https://steamdb.info/sales/')

print('Realizando upload dos dados para o Bigquery...\n')

# Realiza o upload dos dados para o big query, a funcão recebe: Dataframe Pandas, Nome Dataset_Bigquery, Nome Tablela_Bigquery, Caminho das credencias do google em json, Id do projeto
salvar_gbq(dataframe,'steam','descontos_steam',os.environ.get('GOOGLE_CLOUD_CREDENCIAIS'),os.environ.get('ID_PROJETO'))

print('Scraping realizado com sucesso!')