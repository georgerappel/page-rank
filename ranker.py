class Page:
    url = ""
    links = []

    def __init__(self, url = ""):
        self.url = url
        self.links = []

    def addUrl(self, url):
        self.links.append(url)

    def print(self):
        print("\n======")
        print("URL: ", self.url)
        for link in self.links:
            print(".......", link)
        print("====== total: ", len(self.links))
        print("\n")

pages_array = []
with open("ufrj_scraper/links.csv", "r") as links_file:
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
            pages_array.append(page)
            page.print()
            page = Page(line_fields[url_from].rstrip())

        page.addUrl(line_fields[url_to].rstrip())
    # Append last page element to the array
    pages_array.append(page)

count_urls = 0
for page in pages_array:
    count_urls = count_urls + len(page.links)

print("Total pages: ", len(pages_array))
print("Total links: ", count_urls)


