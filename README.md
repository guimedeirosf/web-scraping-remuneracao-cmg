# Projeto: Web Scraping e Consolidação de Dados de Folha de Pagamento

## Descrição
Este projeto realiza o **web scraping** de dados de folha de pagamento de uma instituição pública, utilizando **Selenium** para automatizar a navegação e extração de arquivos no formato `.txt`. O projeto também inclui a consolidação desses dados em uma tabela única no formato **CSV**.

A aplicação foi desenvolvida em **Python** e organiza os dados por ano, mês, cidade, estado e país, com suporte a múltiplos meses. A renomeação automática dos arquivos e a concatenação dos arquivos de texto em um único **CSV** final também são feitas de forma automatizada.

## Funcionalidades
- **Automação de navegação e download**: O Selenium automatiza a seleção de ano e mês, faz o download dos arquivos de pagamento no formato `.txt` e renomeia-os para um formato padrão `YYYY_MM.txt`.
- **Concatenação de arquivos**: Após o download, os arquivos `.txt` são processados e concatenados em um único arquivo **CSV**.
- **Organização dos dados**: Inclui as colunas de ano, mês, cidade, estado e país no arquivo final.
- **Renomeação automática**: Arquivos de pagamento baixados são automaticamente renomeados para garantir consistência.

## Estrutura do Projeto
- `setup_browser()`: Configura o navegador Chrome para automatizar os downloads.
- `process_month()`: Processa o download para um mês específico.
- `process_all_months()`: Itera sobre os meses e anos, fazendo o download de cada mês.
- `rename_recent_file()`: Renomeia o arquivo `.txt` mais recente baixado.
- `carregar_arquivos()`: Carrega todos os arquivos `.txt` de um diretório.
- `extrair_ano_mes()`: Extrai o ano e o mês do nome do arquivo.
- `concatenar_arquivos()`: Concatena os arquivos `.txt` em um arquivo **CSV** final, adicionando colunas de localidade e data.

## Pré-requisitos
- **Python 3.8+**
- **Selenium** 
- **ChromeDriver** e **webdriver-manager**
- **pandas** para manipulação de dados.

### Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/guimedeirosf/web-scraping-remuneracao-cmg.git
