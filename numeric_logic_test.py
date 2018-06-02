import numpy as np



maxIterations = 10

nPages = 4

# p = 0.05 >> 0.380 / 0.133 / 0.289 / 0.196
# p = 0.15 >> 0.368 / 0.141 / 0.288 / 0.202 (ideal acording to the author)
# p = 0.50 >> 0.320 / 0.178 / 0.278 / 0.223
p = 0.05

v = np.matrix([[1 / 4], [1 / 4], [1 / 4], [1 / 4]])

A = np.matrix([[0, 0, 1, 1 / 2],
               [1 / 3, 0, 0, 0],
               [1 / 3, 1 / 2, 0, 1 / 2],
               [1 / 3, 1 / 2, 0, 0]])

B = (1 / nPages) * np.ones([4, 4])

pageRankM = (1 - p) * A + p * B

print(pageRankM)

pageRank = pageRankM @ v
for i in range(maxIterations):
    pageRank = pageRankM @ pageRank

print(pageRank)