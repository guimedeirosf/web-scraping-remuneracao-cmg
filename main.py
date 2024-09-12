from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import os
import time

# Configuração do Chrome para baixar arquivos automaticamente
download_dir = os.path.join(os.getcwd(), "downloads")  

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,  
    "download.prompt_for_download": False,       
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

#Abrindo a pagina
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get('https://camaragoiania.centi.com.br/servidor/remuneracao')
wait = WebDriverWait(driver, 20)  # Aumenta o tempo de espera para 20 segundos

# Selecionando o ano e mes
ano = '2024'
mes = '1'

# Selecionando o dropdown de ano e mes
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

# # Selecionando o formato CSV via o input radio usando o ID
# csv_radio = wait.until(EC.element_to_be_clickable((By.ID, 'exp1')))
# csv_radio.click()

# Clicando no botão "Exportar" no modal
export_final_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@onclick='exportarTabela()']")))
export_final_button.click()

# Esperar o download ser concluído
time.sleep(15) 

# Fechar o navegador
driver.quit()