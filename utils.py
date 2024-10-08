from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime
import time
import pandas as pd

def setup_browser(download_dir):
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def get_filename(ano, mes):
    return f"{ano}_{mes:02d}.csv"

def process_month( wait, ano, mes, download_dir):
    # Selecionando o ano e mes
    ano_dropdown = Select(wait.until(EC.element_to_be_clickable((By.ID, 'ano'))))
    ano_dropdown.select_by_value(ano)

    mes_dropdown = Select(wait.until(EC.element_to_be_clickable((By.ID, 'mes'))))
    mes_dropdown.select_by_value(mes)

    # Clicando no botão "Pesquisar"
    pesquisar_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Pesquisar']")))
    pesquisar_button.click()
    time.sleep(5)

    # Clicando no botão de exportar
    export_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'open-exportar')]")))
    export_button.click()

    # Esperar o modal de exportação aparecer
    modal = wait.until(EC.visibility_of_element_located((By.ID, 'exportar')))
    assert modal.is_displayed(), "O modal de exportação não está visível."

    # Selecionando o formato CSV via o input radio usando o ID
    # csv_radio = wait.until(EC.element_to_be_clickable((By.ID, 'exp1')))
    # csv_radio.click()

    # Clicando no botão "Exportar" no modal
    export_final_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@onclick='exportarTabela()']")))
    export_final_button.click()
    time.sleep(5) 

    # Renomear o arquivo
    rename_recent_file(download_dir, ano, mes)


def process_all_months(start_year, link):
    # Configuração do diretório de downloads
    download_dir = os.path.join(os.getcwd(), "downloads")
    
    # Abrindo o navegador
    driver = setup_browser(download_dir)
    driver.get(link)
    
    # Esperando a página carregar
    wait = WebDriverWait(driver, 20)
    
    # Calculando o mês atual e o mês anterior
    hoje = datetime.now()
    ano_atual = hoje.year
    mes_atual = hoje.month
    mes_anterior = mes_atual - 1
    if mes_anterior == 0:
        mes_anterior = 12
        ano_maximo = ano_atual - 1
    else:
        ano_maximo = ano_atual  
    mes_maximo = 12
    # Iterando sobre os anos e meses
    for ano in range(start_year, ano_maximo + 1):
        mes = 1
        if ano == ano_maximo:
            mes_maximo = mes_anterior
        while mes <= mes_maximo :
            print(f"Processando {ano}-{mes:02d}")
            process_month(wait, str(ano), str(mes), download_dir)
            mes += 1
    
    # Fechar o navegador
    driver.quit()

def rename_recent_file(download_dir, year, month):
    # Encontrar o arquivo mais recente que não começa com o ano esperado
    files = os.listdir(download_dir)
    files = [f for f in files if f.endswith(".txt")] 
    
    if not files:
        print("Nenhum arquivo .txt encontrado para renomear.")
        return
    
    # Ordenar arquivos por data de modificação
    files.sort(key=lambda f: os.path.getmtime(os.path.join(download_dir, f)), reverse=True)
    
    recent_file = files[0]
    if recent_file.startswith(f"{year}_"):
        print(f"O arquivo {recent_file} já está com o nome correto.")
        return
    
    # Renomear o arquivo
    old_file_path = os.path.join(download_dir, recent_file)
    new_file_name = f"{year}_{month.zfill(2)}.txt"
    new_file_path = os.path.join(download_dir, new_file_name)
    
    os.rename(old_file_path, new_file_path)
    print(f"Arquivo renomeado para: {new_file_name}")

# Função para carregar os arquivos da pasta
def carregar_arquivos(directory = ""):
    if directory :
        directory = directory
    elif directory == "":
        directory = os.path.join(os.getcwd(), "downloads")
    arquivos = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            arquivos.append(os.path.join(directory, filename))
    return arquivos

# Função para extrair ano e mês do nome do arquivo
def extrair_ano_mes(nome_arquivo):
    base_name = os.path.basename(nome_arquivo)
    ano_mes = base_name.split('.')[0]
    ano, mes = ano_mes.split('_')
    return f"{ano}/{mes}", ano, mes

# Função para concatenar os arquivos txt em um csv
def concatenar_arquivos(arquivos, cidade, estado):
    tabela_completa = []
    for nome_arquivo in arquivos:
        df = pd.read_csv(nome_arquivo, sep=';', encoding='utf-8')

        ano_mes, ano, mes = extrair_ano_mes(nome_arquivo)
        df['Ano/Mes'] = ano_mes
        df['Ano'] = ano
        df['Mes'] = mes
        df['Cidade'] = cidade
        df['Estado'] = estado
        df['Pais'] = "Brasil"
        df.rename(columns={'Mes': 'Mês', 'Pais': 'País', 'Ano/Mes':'Ano/Mês'}, inplace=True) 
        tabela_completa.append(df)

    # Concatenar todos os DataFrames em uma única tabela
    tabela_final = pd.concat(tabela_completa, ignore_index=True)
    print(tabela_final.head())

    # Salvar a tabela final em um arquivo CSV
    output_path = "folha_salario_completa.csv"  
    tabela_final.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Arquivo salvo em: {output_path}")