import numpy as np
import pandas as pd

#####################
#   CONFIGURATION   #
#####################
debug = True
HOME_URL = "http://dcc.ufrj.br/"
FILE_PATH = "example_urls.csv"
D_TYPE = np.float128

csv_file = pd.read_csv(FILE_PATH, sep=',')

##################
# Transforms the csv_file into a matrix
def csv_to_transition_matrix():
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

    return transition_matrix


# Receives a pandas matrix from the CSV file
# Returns an array of each unique link found, either scraped our outgoing
def get_unique_links(links_matrix):
    unique_links = []
    for row in links_matrix:
        if row[0].rstrip() not in unique_links:
            unique_links.append(row[0].rstrip())
        if row[1].rstrip() not in unique_links:
            unique_links.append(row[1].rstrip())

    return unique_links


# Ranks the transition matrix A
def rank(a_matrix):
    if debug:
        print("Begin ranking")

    maxIterations = 100
    p = 0.05
    matrix_size = len(a_matrix[0])

    v = np.full([matrix_size, 1], 1 / float(matrix_size), D_TYPE)

    B = (1.0 / float(matrix_size)) * np.ones([matrix_size, matrix_size], D_TYPE)

    # Page and Brin algorithm
    pageRankM = (1.0 - p) * a_matrix + p * B

    previous_sum = 0
    pageRank = pageRankM @ v
    for i in range(maxIterations):
        pageRank = pageRankM @ pageRank

        if debug:
            print("Rank sum at iteration ", i, ": ", np.sum(pageRank))

        if abs(previous_sum - np.sum(pageRank)) < 0.000000000000000019:
            break
        else:
            previous_sum = np.sum(pageRank)

    print("Final converged sum (must be very close to one): ", np.sum(pageRank))

    return pageRank


#####################
#   Start ranking   #
#####################
unique_links = get_unique_links(csv_file.values)
transition = csv_to_transition_matrix()
page_rank = rank(transition)

if debug:
    print("\n\nTotal unique pages: ", len(transition[0]))
    print("Total links: ", len(csv_file.values))
    print("\n")

# Append links to its ranks (already in the right order)
links_column = np.transpose(np.array([unique_links]))
rank_per_page = np.append(page_rank, links_column, axis=1)

# Create pandas dataframe from rank matrix
pandas_rank = pd.DataFrame(rank_per_page)

# Rename columns for exhibition
pandas_rank.columns = ["Page Rank", "URL"]

# Solve formating for page rank value
pandas_rank['Page Rank'] = pandas_rank['Page Rank'].astype(D_TYPE)

# Show best N pages ranked
print(pandas_rank.sort_values("Page Rank", ascending=False).head(30))

# Exports the rank-url matrix to a txt file
pandas_rank.to_csv('ranks.txt', index=False)


