# Função que faz a transformação dos dados
def tranformacao(pagina):
    texto = pagina.replace("®", "")
    texto = texto.replace("™", "")
    
    tex = texto.splitlines()
    tex = tex[(tex.index('Highlighted Deal')-1):-2]
    
    tex = [item for item in tex if item not in ['Highlighted Deal','new historical low','Top Seller']]
    tex = [item for item in tex if not item.startswith('all-time low')]
    
    allw = [i.split() for i in tex[1::2]]
    
    nomes = tex[::2]
    
    descB = [i[0] for i in allw]
    desconto = list(map(lambda x: int(''.join(i for i in x if i.isnumeric())), descB)) 
    
    lancamento = [i[-2]+'/'+i[-1] for i in allw]
    
    aprovacao = [float(i[3].strip('%')) for i in allw]
    
    val_desconto = [float(i[2].replace(',','.')) for i in allw]
    
    data = {'nome_jogo':nomes, 'data_lancamento':lancamento, 'aprovacao_pub':aprovacao, 'desconto':desconto, 'valor_c_des':val_desconto}
    
    return data

# Função que tranforma os dados em um dataset e realiza mais transformações
def to_dataframe(dados):
    import pandas as pd
    
    df = pd.DataFrame(dados)
    
    df['nome_jogo'] =  df['nome_jogo'].apply(lambda x: x)
    df['nome_jogo'] =  df['nome_jogo'].apply(lambda x: x.replace(' V',' 5').replace(' IV',' 4').replace(' III',' 3').replace(' II',' 2').title())
    df['valor_ori'] = round((df['valor_c_des'] / (1 - df['desconto'] / 100)), 2)
    
    return df

# Função que realiza a raspagem dos dados do site
def scrapy(site):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    import undetected_chromedriver as uc

    #define parametros para evitar que o site detecte que o que esta acessando o site é um bot
    options = uc.ChromeOptions()

    options.add_argument('headless')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")


    navegador = uc.Chrome(
        options=options)

    # Tenta realizar requisições na pagina 3 vezes, caso tenha sucesso sai do loop
    for _ in range(3):
        try:
            navegador.get(site)

            # Expera por 60 segundos ate o site carregar o componente 'js-app' que é onde contem a primeira lista de jogos
            element = WebDriverWait(navegador, 60).until(
                EC.presence_of_element_located((By.ID, "js-app"))
            )

            site = str(element.text)
            
            ex = tranformacao(site)
            dados = to_dataframe(ex)
            
            return dados
        except:
            print('erro ao realizar requisição. Tentando novamente...\n')
    