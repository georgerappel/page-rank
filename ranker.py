import numpy as np

HOME_URL = "http://dcc.ufrj.br/"
FILE_PATH = "ufrj_scraper/links_dcc_copia.csv"
D_TYPE = float

class Page:
    url = ""
    links = []

    def __init__(self, url = ""):
        self.url = url
        self.links = []

    def add_url(self, url):
        self.links.append(url)

    def print(self):
        print("\n======")
        print("URL: ", self.url)
        for link in self.links:
            print(".......", link)
        print("====== total: ", len(self.links))
        print("\n")


def csv_to_pages():
    pages_array = []
    with open(FILE_PATH, "r") as links_file:
        url_from = 0
        url_to = 1

        csv_header = next(links_file)
        headers = csv_header.split(",")

        # Switch columns in case the file is in a different pattern
        if headers[0] == "url_to":
            url_to = 0
            url_from = 1

        page = Page()
        for line in links_file:
            line_fields = line.split(",")
            current_url = line_fields[url_from].rstrip()
            if page.url != current_url:

                current_index = -1
                previous_index = -1
                for i in range(len(pages_array)):
                    if pages_array[i].url == current_url:
                        current_index = i
                    if pages_array[i].url == page.url:
                        previous_index = i

                if page.url is not "" and previous_index == -1:
                    pages_array.append(page)
                elif previous_index != -1:
                    pages_array[previous_index] = page

                if current_index == -1:
                    page = Page(current_url)
                else:
                    page = pages_array[i]

            page.add_url(line_fields[url_to].rstrip())

        # Append last page element to the array
        previous_index = -1
        for i in range(len(pages_array)):
            if pages_array[i].url == page.url:
                previous_index = i

        if previous_index == -1:
            pages_array.append(page)
        elif previous_index != -1:
            pages_array[previous_index] = page

    return pages_array


def get_unique_links(pages):
    urls = []
    for page in pages:
        if page.url not in urls:
            urls.append(page.url)
        for link in page.links:
            if link not in urls:
                urls.append(link)
    return urls

def rank(a_matrix):
    maxIterations = 5
    matrix_size = len(a_matrix[0])

    # p = 0.05 >> 0.380 / 0.133 / 0.289 / 0.196
    # p = 0.15 >> 0.368 / 0.141 / 0.288 / 0.202 (ideal acording to the author)
    # p = 0.50 >> 0.320 / 0.178 / 0.278 / 0.223
    p = 0.15

    v = np.full([matrix_size, 1], 1/matrix_size, D_TYPE)
    print("V: ", 1/matrix_size)

    B = (1 / matrix_size) * np.ones([matrix_size, matrix_size], D_TYPE)

    # pageRankM = a_matrix
    pageRankM = (1 - p) * a_matrix + p * B

    pageRank = pageRankM @ v
    for i in range(maxIterations):
        pageRank = pageRankM @ pageRank
        print("Soma dos rankings ", i, ": ", np.sum(pageRank), end='')
        print("  prm ", np.sum(pageRankM))

    #print(pageRank)
    print("Soma dos rankings: ", np.sum(pageRank))
    return pageRank


pages_array = csv_to_pages()
unique_links = get_unique_links(pages_array)
for u_link in unique_links:
    found = False
    for page in pages_array:
        if page.url == u_link:
            found = True
            break

    if not found:
        new_page = Page(u_link)
        new_page.add_url(HOME_URL)
        pages_array.append(new_page)

transition_matrix = np.zeros([len(unique_links), len(unique_links)], D_TYPE)

print("Creating adjacency matrix")
for page in pages_array:
    column = unique_links.index(page.url)
    for link in page.links:
        transition_matrix[unique_links.index(link), column] = 1/len(page.links)
print("Created adjacency matrix")
np.savetxt('transicao', transition_matrix)

count_urls = 0
for page in pages_array:
    count_urls = count_urls + len(page.links)

page_rank = rank(transition_matrix)
coluna_urls = np.matrix(unique_links).transpose()
rank_and_url = np.hstack((page_rank, coluna_urls))

with open('ranks.txt', 'w') as outfile:
    for i in range(rank_and_url.shape[0]):
        outfile.write(rank_and_url[i, 0] + "\t" + rank_and_url[i, 1] + "\n")

print("\n\nTotal pages: ", len(pages_array))
print("Total links: ", count_urls)
print("Unique links: ", len(unique_links))

