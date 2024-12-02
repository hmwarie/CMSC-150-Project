import numpy as np
from .simplex_method_util import simplex_method

def find_identity(array):
    if 1 in array:
        instance_of_1 = [i for i, value in enumerate(array) if value == 1]
        return instance_of_1[0]
    return None
    
def is_identity(array, index):
    for i in range(len(array)):
        if i == index:
            continue
        if array[i] != 0:
            return False
    return True

def generate_solution_array(matrix):

    return matrix[-1,:]

def generate_slack_variables(matrix, foods):
    num_of_foods = len(foods)
    num_of_slack_variables = matrix.shape[1] - num_of_foods - 2
    slack_variables = []
    for i in range(num_of_slack_variables):
        slack_variables.append(f"s{i+1}")
    
    return slack_variables

def generate_solution_dictionary(foods):
    if foods == []:
        print("System: No Food Selected!")
        return (None, None)

    simplex_matrix, simplex_iteration = simplex_method(foods)

    if simplex_matrix is None:
        return (None, None)

    simplex_iteration = simplex_method(foods)[1]

    solution_array = simplex_matrix[-1,:-2]
    solution_array = np.append(solution_array, simplex_matrix[-1, -1:])

    solution_dictionary_keys = generate_slack_variables(simplex_matrix, foods)
    solution_dictionary_keys.extend(foods)
    solution_dictionary_keys.append("Total Cost")

    solution_dictionary = dict(zip(solution_dictionary_keys, solution_array))
    
    return (solution_dictionary, simplex_iteration)

