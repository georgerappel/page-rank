import numpy as np

FILE_PATH = "ufrj_scraper/links.csv"
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
            if page.url != line_fields[url_from].rstrip():
                if page.url is not "":
                    pages_array.append(page)
                # page.print()
                page = Page(line_fields[url_from].rstrip())

            page.add_url(line_fields[url_to].rstrip())
        # Append last page element to the array
        pages_array.append(page)
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
    maxIterations = 10
    matrix_size = len(transition_matrix[0])

    # p = 0.05 >> 0.380 / 0.133 / 0.289 / 0.196
    # p = 0.15 >> 0.368 / 0.141 / 0.288 / 0.202 (ideal acording to the author)
    # p = 0.50 >> 0.320 / 0.178 / 0.278 / 0.223
    p = 0.15

    v = np.full([matrix_size, 1], 1/matrix_size, D_TYPE)
    print("V: ", v)

    B = (1 / matrix_size) * np.ones([matrix_size, matrix_size], D_TYPE)

    #pageRankM = a_matrix
    pageRankM = (1 - p) * a_matrix + p * B

    pageRank = pageRankM @ v
    for i in range(maxIterations):
        pageRank = pageRankM @ pageRank

    print(pageRank)
    print("Soma dos rankings: ", np.sum(pageRank))


pages_array = csv_to_pages()
unique_links = get_unique_links(pages_array)
transition_matrix = np.zeros([len(unique_links), len(unique_links)], D_TYPE)

print("Creating adjacency matrix")
for page in pages_array:
    column = unique_links.index(page.url)
    for link in page.links:
        transition_matrix[unique_links.index(link), column] = 1/len(page.links)
print("Created adjacency matrix")

count_urls = 0
for page in pages_array:
    count_urls = count_urls + len(page.links)

# test output
# for i in range(0, 10):
#     for j in range(0, 10):
#         print(transition_matrix[i,j], " ", end="")
#     print(unique_links[i], end="\n")

#TODO it's not working :(
rank(transition_matrix)

print("\n\nTotal pages: ", len(pages_array))
print("Total links: ", count_urls)
print("Unique links: ", len(unique_links))

