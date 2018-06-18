# This is the Ranked file working with the Google Colaboratory
# https://colab.research.google.com/

# The file must be uploaded to google drive, and
# # the file_id should be placed in the correct variable
# CSV file pattern, just like the file example_urls.csv:
# 2 columns - Headers "url_to" and "url_from" - comma separated

import io
import pandas as pd
import numpy as np

from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google.colab import files

debug = True

# configurações para baixar o arquivo do drive com as URLs
drive_service = build('drive', 'v3')
file_id = '1rXIBofE7-rmYDHN0P36fbyYTsTz7GTEx'
# file_id = '1wB1VXNATEfLtCjMnyJcP2xnfDNr5wMyJ' # Arquivo pequeno para teste
request = drive_service.files().get_media(fileId=file_id)
downloaded = io.BytesIO()
downloader = MediaIoBaseDownload(downloaded, request)

done = False
if debug:
    print("Baixando arquivo com links")
while done is False:
    # _ is a placeholder for a progress object that we ignore.
    # (Our file is small, so we skip reporting progress.)
    _, done = downloader.next_chunk()
if debug:
    print("Baixado arquivo com sucesso")

# passa o arquivo baixado do drive para CSV do pandas
downloaded.seek(0)
csv_file = pd.read_csv(downloaded, sep=',')

# Usado para redirecionar os nós finais que não tem links de saída
HOME_URL = "http://dcc.ufrj.br/"

D_TYPE = np.float128


def csv_to_transition_matrix():
    if debug:
        print("Montando matriz de transição")

    unique_links = get_unique_links(csv_file.values)

    transition_matrix = np.zeros([len(unique_links), len(unique_links)], D_TYPE)

    url_from = 0
    url_to = 1

    # trocar as colunas caso estejam na ordem invertida
    for i in range(len(csv_file.columns)):
        if csv_file.columns[i] == "url_to":
            url_to = i
            url_from = 1 - i

    for line_fields in csv_file.values:
        current_to = line_fields[url_to].rstrip()
        current_from = line_fields[url_from].rstrip()

        if current_to == current_from:
            # Discard loops
            continue

        column = unique_links.index(current_from)
        row = unique_links.index(current_to)

        transition_matrix[row, column] = 1.0

    home_row = unique_links.index(HOME_URL)
    sum_columns = np.sum(transition_matrix, axis=0)

    for i in range(len(unique_links)):
        if sum_columns[i] == 0.0:
            transition_matrix[home_row, i] = 1.0

    sum_columns = np.sum(transition_matrix, axis=0)

    for i in range(len(unique_links)):
        n_elementos = sum_columns.item(i)
        for j in range(len(unique_links)):
            if transition_matrix[j, i] == 1:
                transition_matrix[j, i] = 1.0 / n_elementos
    # np.savetxt('transicao2.txt', transition_matrix)

    if debug:
        print("Montada matriz de transição")

    return transition_matrix


# recebe uma matriz do pandas com os links de origem e chegada entre as páginas
# e retorna um array com os links únicos encontrados
def get_unique_links(links_matrix):
    unique_links = []
    for row in links_matrix:
        if row[0].rstrip() not in unique_links:
            unique_links.append(row[0].rstrip())
        if row[1].rstrip() not in unique_links:
            unique_links.append(row[1].rstrip())

    return unique_links


# faz o ranking, dada uma matriz A de transição
def rank(a_matrix):
    if debug:
        print("Iniciando rankeamento")
    maxIterations = 100
    matrix_size = len(a_matrix[0])

    # p = 0.05 >> 0.380 / 0.133 / 0.289 / 0.196
    # p = 0.15 >> 0.368 / 0.141 / 0.288 / 0.202 (padrão)
    # p = 0.50 >> 0.320 / 0.178 / 0.278 / 0.223
    p = 0.05

    v = np.full([matrix_size, 1], 1 / float(matrix_size), D_TYPE)

    B = (1.0 / float(matrix_size)) * np.ones([matrix_size, matrix_size], D_TYPE)

    # parte do algoritmo de Page e Brin. Dá uma probabilidade p de iniciar em
    # qualquer uma das páginas
    pageRankM = (1.0 - p) * a_matrix + p * B

    previous_sum = 0
    pageRank = pageRankM @ v
    for i in range(maxIterations):
        pageRank = pageRankM @ pageRank
        if debug:
            print("Soma na iteração ", i, ": ", np.sum(pageRank))
        if abs(previous_sum - np.sum(pageRank)) < 0.000000000000000019:
            break
        else:
            previous_sum = np.sum(pageRank)

    print("Soma final convergida: ", np.sum(pageRank))

    return pageRank


unique_links = get_unique_links(csv_file.values)
transition = csv_to_transition_matrix()

page_rank = rank(transition)

print("\n\nTotal pages: ", len(transition[0]))
print("Total links: ", len(csv_file.values))
print("\n")

links_column = np.transpose(np.array([unique_links]))
rank_per_page = np.append(page_rank, links_column, axis=1)

# cria a 'tabela' com a matriz do pagerank
pandas_rank = pd.DataFrame(rank_per_page)

# renomeia as colunas para exibição
pandas_rank.columns = ["Page Rank", "URL"]

# para resolver alguns problemas com a formatação/ordenação da coluna do pagerank
pandas_rank['Page Rank'] = pandas_rank['Page Rank'].astype(D_TYPE)

# exibe N valores ordenados do maior para o menor pagerank
print("Exibindo os 30 melhores Page Ranks:")
pandas_rank.sort_values("Page Rank", ascending=False).head(30)