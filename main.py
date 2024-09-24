import utils
utils.process_all_months(start_year = 2017, link = 'https://camaragoiania.centi.com.br/servidor/remuneracao')

#Concatenando os arquivos baixados e adicionando colunas Ano Mes AnoMes Cidade Estado Pais
arquivos = utils.carregar_arquivos()
utils.concatenar_arquivos(arquivos = arquivos, cidade = "Goiânia", estado = "Goiás" )