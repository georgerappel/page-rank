#########################################################################
# Numeric example implementation of the Page and Brin Page Rank Algorithm
#

import numpy as np

maxIterations = 10000

# Algo source: http://pi.math.cornell.edu/~mec/Winter2009/RalucaRemus/Lecture3/lecture3.html
# p = 0.05 >> 0.380 / 0.133 / 0.289 / 0.196
# p = 0.15 >> 0.368 / 0.141 / 0.288 / 0.202 (ideal acording to the author)
# p = 0.50 >> 0.320 / 0.178 / 0.278 / 0.223
p = 0.05

v = np.matrix([[1 / 4], [1 / 4], [1 / 4], [1 / 4]])
A = np.matrix([[0, 0, 1, 1 / 2],
               [1 / 3, 0, 0, 0],
               [1 / 3, 1 / 2, 0, 1 / 2],
               [1 / 3, 1 / 2, 0, 0]])

nPages = len(v)
B = (1 / nPages) * np.ones([nPages, nPages])

pageRankM = (1 - p) * A + p * B

print(pageRankM)

pageRank = pageRankM @ v
for i in range(maxIterations):
    pageRank = pageRankM @ pageRank

print(pageRank)
print("total somado: ", np.sum(pageRank))
