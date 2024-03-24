from lxml import etree
import locale


def despesas(nome):
    nomes = set()
    categoria = {}
    total = 0
    bd = etree.parse('Ano-2017.xml')
    despesas = bd.findall('DEPUTADOS')
    if len(nomes) == 0:
        for i in despesas:
            for a in i:
                filho = a.getchildren()
                deputado = filho[0].text
                if deputado not in nomes:
                    nomes.add(deputado)
    if nome in nomes:
        if filho[8].text == 'vlrLiquido':
            despesa = filho[8].text
            valor = filho[18].text
            if ',' not in valor:
                valor += ',00'
            valor = float(valor.replace(',', '.'))
            if despesa in categoria:
                categoria[despesa] = float(categoria[despesa]) + valor
            else:
                categoria[despesa] = valor
    for chave, valor in categoria.items():
        total += valor
        # Mudando a moeda para PT-BR
        locale.setlocale(locale.LC_ALL, 'pt_br.UTF-8')
        # Formatando a variável valor para moeda, sem símbolos e colocando delimitador para milhar
        valor = locale.currency(valor, grouping=True, symbol=None)
        # Retornando a configuração padrão do sistema
        locale.setlocale(locale.LC_ALL, '')
        print(f'Categoria: {chave} - Valor: {valor}')
    locale.setlocale(locale.LC_ALL, 'pt_bt.UTF-8')
    total = locale.currency(total, grouping=True, symbol=None)
    locale.setlocale(locale.LC_ALL, '')
    print(f'Total de despesas: {total}')


if __name__ == '__main__':
    while True:
        deputado = input('Digite o nome de um deputado (Ou (0) zero para sair): ')
        if deputado == '0':
            break
        else:
            despesas(deputado)
        '''elif deputado not in nomes:
            nao_encontrado = input('Aperte qualquer tecla para ver os deputados disponíveis: ')
            for i in nomes:
                print(nomes)
            continue'''
