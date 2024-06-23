from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import re

options = webdriver.EdgeOptions()
options.add_argument('--headless')  # Comente esta linha se quiser ver o navegador

driver = webdriver.Edge(options=options)

# Acessar a página
url = str(input('Qual a página a ser analisada? '))
driver.get(url)

title = driver.title

# Obter o conteúdo da página renderizada
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Fechar o navegador
driver.quit()

# Write the HTML content to a file
#with open("output.html", "w", encoding="utf-8") as file:
    #file.write(soup.prettify())

# Encontre a tabela
table = soup.find('table', class_=re.compile(r'Table'))

# Verifique se a tabela foi encontrada
if table is not None:
    # Convertendo a string HTML em um objeto StringIO
    html_string = str(table)
    html_obj = StringIO(html_string)

    # Convertendo o objeto StringIO em um DataFrame
    df = pd.read_html(html_obj)[0]

    # Função para extrair o valor antes do "_"
    def extract_team_name(player):
        return player.split('_')[0]

    # Aplicar a função à coluna "Players" para criar a coluna "Team"
    df['Team'] = df['Player'].apply(lambda x: extract_team_name(x))

    # Função para remover parte do valor na coluna 'Player'
    def remove_team_prefix(player):
        parts = player.split('_')
        return parts[1] if len(parts) > 1 else player

    # Aplicar a função à coluna 'Player'
    df['Player'] = df['Player'].apply(lambda x: remove_team_prefix(x))

    # Exibir o DataFrame atualizado
    #print(df)

    title_id = str(input('Alguma identificação para o título? Pressione Enter Caso Não.'))
    if title_id.strip():
        file_name = re.sub(r'\W+', '', title_id.lower()) + '.csv'
    else:
        # Nome do arquivo CSV com base no título da página
        file_name = re.sub(r'\W+', '', title.lower()) + '.csv'

    print("Nome do arquivo CSV:", file_name)
    df.to_csv(file_name, index=False)
else:
    print("Tabela não encontrada.")
