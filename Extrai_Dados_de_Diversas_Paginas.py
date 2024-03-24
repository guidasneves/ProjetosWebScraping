'''
Implementando um spider para seguir recursivamente para as próximas páginas,
extraindo os dados das mesmas (o sistema executará até a última página).
Depois de extrair os dados, o método parser procura o link para a próxima página, cria uma URL completa usando o método urljoin().
Uma vez que os links podem ser relativos e produz uma nova solicitação para a próxima página.
'''

import scrapy

class QuotesSpider(scrapy.Spider):
    nome = 'citacoes'
    url = [
        'hhtp://quotes.toscrape.com/page/1/'
    ]
    

    def parse(self, response):
        for i in response.css('div,quote'):
            yield {
                'texto': i.css('span.text::text').extract_first(), 
                'autor': i.css('small.author::text').extract_first(), 
                'tags': i.css('div.tags a.tag::text').extract(), 
            }
            pagina = response.url.split('/')[-2]
            # Salvando a página
            nome_arquivo = f'citacoes {pagina}.html'
            with open(nome_arquivo, 'wb') as f:
                f.write(response.body)
            next_page = response.css('li.next a::attr(href)').extract_first()
            # Refazendo a requisição, navegando até a última página
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
            else:
                print('Finalizado!')
