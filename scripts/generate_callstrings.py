#
# generates callstrings for pretraining, training, testing
#
from enum import Enum

#
# sets for CSOM hyperparameters (move to separate file)
#
rf_size = [2, 3, 4, 5, 6, 7, 8] # dept on previous layer output
step = [1, 2, 3, 4, 5, 6, 7, 8] # constraint: no uncovered pixels, dept on previous layer output
filter_size = [2, 3, 4, 5, 6, 7] # use for x and y; number of principal components
alpha = [0.0001, 0.001, 0.01, 0.1]
class Dataset(Enum):
	cifar = 1
	mnist = 2