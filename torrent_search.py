from urllib.request import Request, urlopen
import re
from googlesearch import search
import time
import os

# Configurações iniciais

provedores = []

provedores.append(["sld", "https://solidtorrents.to/search?q=REPLACEMAIS"])
provedores.append(["tpb", "https://tpb.party/search/REPLACEPORCENTAGEM/1/99/0"])
provedores.append(["tgy", "https://torrentgalaxy.to/torrents.php?search=REPLACEMAIS#results"])

lista_provedores = ["sld", "tpb", "tgy"]
#lista_provedores = ["tpb"]

#Verifica se um link magnet é válido
def verify_magnet_link(magnet_link):
    pattern=re.compile(r"magnet:\?xt=urn:[a-z0-9]+:[a-zA-Z0-9]{32}")
    result = pattern.match(magnet_link)
    return result


# Recebe um termo e um provedor, e devolve o link desse provedor
def get_link(provedor, termo):
    termo_mais = termo.replace(" ", "+")
    termo_porcentagem = termo.replace(" ", "%20")

    for i in provedores:

        if i[0] == provedor:
            devolver = i[1].replace("REPLACEMAIS", termo_mais)
            devolver = devolver.replace("REPLACEPORCENTAGEM", termo_porcentagem)

            return devolver

    return "erro!"


# Recebe um termo e uma lista de provedores, e devolve uma tupla
# [magnet, magnet, rating]
# * significa top n - provável melhor saúde
# # significa bottom n - provável pior saúde
def get_list_of_torrents(provedores, termo):
    lista_magnets_main = []
    lista_magnets_second = []
    lista_magnets_google = []

    for prov in provedores:
        try:
            contador = 0

            link = get_link(prov, termo)

            req = Request(link, headers={'User-Agent': 'Sapo'})
            webpage = urlopen(req).read()

            texto_pagina = webpage.decode('ISO-8859-1')
            lista_split = texto_pagina.split('"')[1:-1]

            for i in (lista_split):
                if "magnet:?" in i:
                    pure = i
                    i = i.replace("&#", "=")
                    i = i.replace("x3D;", "")
                    i = i.replace("amp;", "")

                    if i not in lista_magnets_main and i not in lista_magnets_second and contador <= 4:
                        lista_magnets_main.append([i, i, "M"])
                        contador = contador + 1

                    if i not in lista_magnets_main and i not in lista_magnets_second and contador > 4:
                        lista_magnets_second.append([i, i, "S"])
        except:
            print("Erro no provedor " + prov)

    query = termo + '"magnet"'
    for j in search(query):
        try:
            req = Request(j, headers={'User-Agent': 'Sapo'})
            webpage = urlopen(req).read()

            texto_pagina = webpage.decode('ISO-8859-1')

            lista_split = texto_pagina.split('"')[1:-1]

            for i in (lista_split):
                if "magnet:?" in i:
                    pure = i
                    i = i.replace("&#", "=")
                    i = i.replace("x3D;", "")
                    i = i.replace("amp;", "")

                    if i not in lista_magnets_main and i not in lista_magnets_second and verify_magnet_link(i):
                        lista_magnets_google.append([i, i, "G"])
        except:
            print("Erro na página " + j)
    return lista_magnets_main + lista_magnets_second + lista_magnets_google

# Recebe uma tupla [magnet, magnet, rating] e devolve uma tupla [nome, magnet, rating]
# É uma função de enbelezamento, removendo deixando o nome da tupla amigável
def get_torrent_metadata(lista_magnets):
    lista_metadata = []
    for j in lista_magnets:
        try:
            name = j[0]
            name = name.split('dn=')[1]
            name = name.split('tr=')[0]

            name = name.replace("Bitsearch.to", "")
            name = name.replace("%5D", "")
            name = name.replace("%5B", "")

            name = name.replace("+", " ")
            name = name.replace(".", " ")

            lista_metadata.append([name, j[1], j[2]])

        except:
            lista_metadata.append([j[0], j[1], j[2]])

    return lista_metadata

# Obtém o tamanho da linha para desenhar
def get_size_linha(handlers):
    a = 0
    for i in handlers:
        if a < len(i[0]):
            a = len(i[0])
    return a + 15 # uma aposta generosa de caracteres não contados pelo len() por alguma razão


# Imprime uma linha de pontos do tamanho necessário
def print_linha(size_linha):
    to_print = "+"
    for i in range(size_linha - 2):
        to_print = to_print + "-"
    to_print = to_print + "+"
    print(to_print)


# Imprime uma linha com nome e número do tamanho necessário
def print_linha_nome(nome, num, size_linha):
    offset = size_linha - len(nome) - 7
    offset_num = len(str(num))
    for i in range(offset - offset_num):
        nome = nome + " "
    print("| " + str(num) + " | " + nome + " |")

def listar_torrents(buscar):
    torrents = get_list_of_torrents(lista_provedores, buscar)
    handlers = get_torrent_metadata(torrents)

    counter = 0

    size_linha = get_size_linha(handlers)

    return handlers


    #print_linha(size_linha)
    #for i in range(len(handlers)):
        #current_torrent = handlers[i]

        #current_nome = current_torrent[0]
        #current_magnet = current_torrent[1]
        #current_grade = current_torrent[2]

        #print_linha_nome(current_nome, i, size_linha)
        #print_linha(size_linha)

    #entrada = int(input("Qual valor deseja buscar? "))
    #magnet_ok = handlers[entrada][1]
    #os.startfile(magnet_ok)
