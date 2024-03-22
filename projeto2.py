from lxml import etree as et
import locale as lc


def carrega():
    deputado = {}
    bd = et.parse('Ano-2017.xml')
    despesas = bd.findall('DESPESAS')
    for i in despesas:
        for informacao in i:
            propriedades = informacao.getchildren()
            if propriedades[18].tag == 'vlrLiquido':
                nome = propriedades[0].text
                despesa = propriedades[8].text
                valor = propriedades[18].text
                if ',' not in valor:
                    valor += ',00'
                valor = float(valor.replace(',', '.'))
                if nome in deputado:
                    dicionario = deputado[nome]
                    if despesa in dicionario:
                        dicionario[despesa] += valor
                    else:
                        dicionario[despesa] = valor
                    deputado[nome] = dicionario
                else:
                    dic = {}
                    dic[despesa] = valor
                    deputado[nome] = dic
    return deputado


def formata(valor):
    lc.setlocale(lc.LC_ALL, 'pt_br.UTF-8')
    valor = lc.currency(valor, grouping=True, symbol=None)
    lc.setlocale(lc.LC_ALL, 'pt_br.UTF-8')


if __name__ == '__main__':
    dicionario = carrega()
    while True:
        total = 0
        nome = input('Informe o nome do deputado (Ou 0 (zero) para sair): ').upper()
        if nome == '0':
            break
        elif nome in dicionario:
            for chave, valor in dicionario[nome].items():
                total += valor
                valor = formata(valor)
                print(f'Chave: {chave} - Valor: {valor}')
        else:
            input('Deputado não localizado! Pressione qualquer tecla para ver a lista de deputados: ')
            for nome in dicionario.keys():
                print(nome)
            continue
        total = formata(total)
        print(f'Total das despesas: {total}')
