from urllib.request import urlopen
from bs4 import BeautifulSoup
import random
import mysql.connector
import re

dados__conexao = {'user': 'root', 'password': '1234', 'host': '127.0.0.1', 'database': 'scraping', 'charset': 'utf-8'}
conexao = mysql.connector.connect(**dados__conexao)
cursor = conexao.cursor()


def gravar_dados(titulo, url, conteudo):
    cursor.execute('INSERT INTO PAGINAS VALUES(%s, %s, %s)', (titulo, url, conteudo))
    conexao.commit()


# Implementando o método para retornar os links da página
def getLinks(urlArtigo):
    url = 'http://pt.wikipedia.org' + urlArtigo
    html = urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')
    titulo = bs.find('h1').get_text()
    conteudo = bs.find('div', {'id': 'mw-content-text'}).find('p').get_text()
    gravar_dados(titulo, url, conteudo)
    # Localizando e retornando todos os links que estejam na página
    # Pegaremos na página do Wikipedia (/wiki/), todos os caracteres com exceção dos ':'
    # (?!:): Afirmação negativa para ele não pegar o ':'
    # ^: Indica o início da string
    # $: Indica o fim da string
    # .: Qualquer caractere
    # *: Qualquer quantidade
    return bs.find('div', {'id': 'bodyContent'}).find_all('a', href=re.compile('^(/wiki/) ((?!:).)*$'))


links = getLinks('/wiki/Copa_do_Mundo_FIFA_de_2026')

try:
    contador = 1
    # Enquanto houver links
    # Limitado para apenas 10 vezes (contador <= 10)
    while len(links) > 0 and contador <= 10:
        # Pegando um artigo aleatório da página e retornando o atributo 'href'
        novoArtigo = links[random.randint(0, len(links) - 1)].attrs['href']
        print(f'{str(contador)} -> {novoArtigo}')
        # Começamos de novo com o artigo que selecionamos acima
        links = getLinks(novoArtigo)
        contador += 1
finally:
    cursor.close()
    conexao.close()
