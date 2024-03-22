import scrapy
import requests
import pyodbc
import os
import logging

class Conexao():
    server = '127.0.0.1'
    database = 'basetelelista'
    username = 'sa'
    password = 'senha'
    conexao = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password + ';MARS_Connection=Yes')

conexao = Conexao()
cursor = conexao.conexao.cursor()
cursor_cidade = conexao.conexao.cursor()

class SpiderTelelista(scrapy.Spider):
    try:
        name = "telelista4"

        def __init__(self, url='', *args, **kwargs):
            super(SpiderTelelista, self).__init__(*args, **kwargs)

            url_desmontada = url.split("/")
            self.uf_pesquisa = url_desmontada[3]
            self.id_ramo_atividade = pegar_ramo_atividade(url_desmontada[5])
            self.url = url

        def start_requests(self):
            yield scrapy.Request(url=self.url, callback=self.parse)

        def parse(self, response):
            if response.url.count("/") == 5:
                link_desmontado = response.url.split("/")
                uf_busca = link_desmontado[3]
                cidade_busca = link_desmontado[4]
                cidade_busca = cidade_busca.replace("+", " ")
                proxima_pagina = response.xpath('//link[contains(@rel, "next")]/@href').extract_first()
                page = response.url
                link_estabelecimentos = response.xpath('//td[@class="nome_resultado_ag"]//a/@href').extract()
                for link in link_estabelecimentos:
                    yield response.follow(link, callback=self.parse)

                if proxima_pagina:
                    yield response.follow(proxima_pagina, callback=self.parse)
            else:
                #pagina individual
                link_desmontado = response.url.split("/")
                uf_busca = link_desmontado[4]
                cidade_busca = link_desmontado[5]
                cidade_busca = cidade_busca.replace("+", " ")
                nome = response.xpath('//h1[contains(@class,"nome_anun")]/text()').extract()
                telefones = response.xpath('//div[@id="telInfo"]//span/text()').extract()
                imagens = response.xpath('//div[@id="telInfo"]//span//img/@src').extract()
                endereco = response.xpath('//input[contains(@id,"enderecoreg")]/@value').extract()
                endereco_completo = response.xpath('//div[contains(text(),"' + endereco[0] + '")]/text()').extract()
                endereco_final = None
                for endereco in endereco_completo:
                    if endereco_final:
                        endereco_final = endereco_final + " - " + endereco
                    else:
                        endereco_final = endereco

                if len(telefones)>0:
                    id_cliente = gravar_cliente(uf_busca, cidade_busca, nome[0], endereco_final, self.id_ramo_atividade)
                    x = 0

                    for telefone in telefones:
                        id_telefone = gravar_telefone(str(id_cliente), telefone)
                        imagem = requests.get(imagens[x])
                        nome_arquivo_imagem = gerar_nome_imagem(uf_busca, id_telefone)
                        with open(nome_arquivo_imagem, 'wb') as f:
                            f.write(imagem.content)
                        gravar_imagem(id_telefone, nome_arquivo_imagem)
                        x += 1
    except:
        logging.info("Erro na funcao principal")

def limpar_telefone(telefone):
    if telefone:
        if "Tel:" in telefone:
            telefone = telefone.split("Tel:")
            telefone = telefone[1]
        elif "PABX:" in telefone:
            telefone = telefone.split("PABX:")
            telefone = telefone[1]
        elif "Cel:" in telefone:
            telefone = telefone.split("Cel:")
            telefone = telefone[1]
        elif "Fax:" in telefone:
            telefone = telefone.split("Fax:")
            telefone = telefone[1]

        return telefone

def limpar_campo(campo):
    campo = campo.replace("'", "").replace(",", "").replace("%20", " ").strip().strip("\n\r")
    campo = campo.replace('\n', ' ').replace('\r', '')
    return campo

def gerar_nome_imagem(uf_busca, id_cliente):
    if not os.path.exists('C:\\imagens\\' + uf_busca):
        os.mkdir('C:\\imagens\\' + uf_busca)
    return 'C:\\imagens\\' + uf_busca + "\\" + str(id_cliente) + ".jpg"

def gravar_cliente(uf_busca, cidade_busca, nome_cliente, endereco, ramo_atividade):
    cidade_busca = limpar_campo(cidade_busca)
    nome_cliente = limpar_campo(nome_cliente)
    #endereco = limpar_campo(endereco)
    sql = ("insert into LOJAS (UF, CIDADE, NOME, ENDERECO, ID_RAMO) values (" +
           "'" + uf_busca + "','" + cidade_busca + "','" + nome_cliente + "','" + endereco +"'," + str(ramo_atividade) + ")")

    logging.info("SQL gravar_cliente: " + sql)
    cursor.execute(sql)
    conexao.conexao.commit()
    sql = "SELECT MAX(ID) FROM LOJAS"
    with cursor.execute(sql):
        row = cursor.fetchone()
        while row:
            id_cliente = row[0]
            row = cursor.fetchone()
    return id_cliente

def gravar_telefone(id_cliente, telefone):
    telefone = limpar_telefone(telefone)
    sql = ("insert into TELEFONES (ID_LOJA, NUMERO) values (" +
           id_cliente +", '"+ telefone + "')")

    logging.info("SQL gravar_telefone: " + sql)
    cursor.execute(sql)
    conexao.conexao.commit()
    sql = "SELECT MAX(ID) FROM TELEFONES"
    with cursor.execute(sql):
        row = cursor.fetchone()
        while row:
            id_telefone = row[0]
            row = cursor.fetchone()
    return id_telefone

def gravar_imagem(id_telefone, imagem):
    sql = ("UPDATE TELEFONES SET CAMINHO_IMAGEM='" + imagem + "' WHERE ID = " + str(id_telefone))

    logging.info("SQL gravar_imagem: " + sql)
    cursor.execute(sql)
    conexao.conexao.commit()

def pegar_ramo_atividade(ramo):
    try:
        ramo = ramo.replace('+', ' ').lower()
        sql = "select ID from RAMO_ATIVIDADE where NOME='" + ramo + "'"
        cursor.execute(sql)
        row = cursor.fetchone()
    except:
        logging.info("Erro na funcao pegar_ramo_atividade")

    return row[0]
