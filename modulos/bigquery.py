def salvar_gbq(df, dataset, nome_tabela, json_key, id_projeto):
    import pandas_gbq
    from google.oauth2 import service_account

    credenciais = service_account.Credentials.from_service_account_file(json_key) #configura as credencias do google para acessar os recursos
    
    # Faz o upload dos dados para o bigquery. OBS: parametro if_exists esta como replace, pois, quando a função for executada, ira sobrescreber a tabela no Bigquery, se ela existir.
    pandas_gbq.to_gbq(dataframe = df,
    destination_table = f'{dataset}.{nome_tabela}',
    project_id = id_projeto,
    credentials = credenciais,
    if_exists = 'replace')