# Irá receber a URL inicial
# Vai encontrar um link com algumas das palavras definidas na expressão regular
# Guardando esse link no set paginas
# Caso der erro, irá guardar em paginas_invalidas
# Caso não der erro, chamará a função recursivamente e abrirá a página do link encontrado
# Começando tudo de novo
def get_links(url):
    global paginas # Definindo a variável paginas como global
    global paginas_invalidas
    # Tratamento de Exceção
    try:
        if url not in paginas_invalidas:
            html = urlopen(url)
            objeto = BeautifulSoup(html, 'html.parser')
            # Criando uma expressão regular que irá procurar a palavra definida
            # Podendo estar no meio de qualquer outra palavra
            serie_a_g6_2027 = ('.corinthians.|.santos.|.palmeiras.|.flamengo.|.cruzeiro.')

            # Procuramos a tag 'a', com o atributo href
            for link in objeto.find_all('a', href=re.compile(serie_a_g6_2027)):
                # Validando se algum dos atributos do link é href
                if 'href' in link.attrs:
                    if link.attrs['href'] not in paginas and link.attrs['href'] not in paginas_invalidas:
                        nova_pagina = link.attrs['href']
                        print(nova_pagina)
                        # Adicionamos no set paginas
                        paginas.add(nova_pagina)
                        # Chamamos novamente a função, recursivamente
                        get_links(nova_pagina)
    except:
        # Caso der erro na hora de abrir a página, adicionamos ao set paginas_invalidas
        paginas_invalidas.add(nova_pagina)

get_links('http://globoesporte.globo.com')
