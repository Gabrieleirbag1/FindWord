import requests
from bs4 import BeautifulSoup
import os
import csv

# URL de la page web à analyser
url = 'https://fr.wiktionary.org/wiki/Wiktionnaire:Liste_de_1750_mots_fran%C3%A7ais_les_plus_courants'

# Envoyer une requête GET pour récupérer le contenu de la page
response = requests.get(url)
html_content = response.content

# Analyser le contenu HTML avec BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Trouver toutes les balises <div> avec la classe "mw-heading"
divs = soup.find_all('div', class_='mw-body-content')

# Initialiser une liste pour stocker les contenus des balises <a>
a_contents = []

# Parcourir chaque balise <div> trouvée
for div in divs:
    # Trouver toutes les balises <a> à l'intérieur de cette balise <div>
    a_tags = div.find_all('a')
    # Parcourir chaque balise <a> et extraire le contenu
    for a in a_tags:
        a_contents.append(a.text)
# Afficher la liste des contenus des balises <a>
print(a_contents)
# Chemin du fichier CSV
csv_file = os.path.join(os.path.dirname(__file__), 'output.csv')

# Écrire les contenus des balises <a> dans le fichier CSV
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Contenu des balises <a>'])
    writer.writerows([[content] for content in a_contents])