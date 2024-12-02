import numpy as np
from .augmented_matrix_util import generate_augmented_matrix

def has_negative(array):
    for coefficient in array:
        if coefficient < 0:
            return True
    return False

def find_pivot_column(array):
    negative_indices = np.where(array < 0)[0]
    if negative_indices.size > 0:
        pivot_col = negative_indices[np.argmax(np.abs(array[negative_indices]))]
        return pivot_col
    return None

def get_test_ratio(array, solution_column):
    test_ratio = np.empty(len(array))
    for i in range(len(array)):
        if array[i] == 0:
            test_ratio[i] = None
        else:
            test_ratio[i] = solution_column[i]/array[i]
    return test_ratio

def find_pivot_row_index(array, solution_column):
    test_ratio = get_test_ratio(array, solution_column)

    try:
        min_positive_value = np.min(test_ratio[test_ratio > 0])
    except Exception as e:
        return None

    min_positive_index = np.where(test_ratio == min_positive_value)[0]
    return min_positive_index[0]

def simplex_method(constraints):
    matrix = generate_augmented_matrix(constraints)
    matrix = matrix.transpose()

    matrix[-1,:-1] *= -1

    num_rows = matrix.shape[0]
    identity_matrix = np.eye(num_rows)

    matrix = np.insert(matrix, -1, identity_matrix, axis=1)

    iteration_count = 0
    last_row = matrix[-1,:-1]

    simplex_iteration = []
    simplex_iteration.append(np.copy(matrix))

    while has_negative(last_row):
    
        if iteration_count == 1000:
            print(f"Simplex Iteration: {iteration_count}")  
            print("System: No Feasible Solution!")
            return (None, None)

        last_row = matrix[-1,:-1]

        solution_column = matrix[:,-1]

        pivot_column_index = find_pivot_column(last_row)
        pivot_column = matrix[:, pivot_column_index]
    
        pivot_row_index = find_pivot_row_index(pivot_column, solution_column)

        if pivot_row_index is None:
            print(f"Simplex Iteration: {iteration_count}")  
            print("System: No Feasible Solution!")
            return (None, None)

        matrix[pivot_row_index,:] /= matrix[pivot_row_index, pivot_column_index]

        number_of_rows = matrix.shape[0]
        for i in range(number_of_rows):
            if i == pivot_row_index:
                continue
            normalized_row = matrix[i, pivot_column_index]*matrix[pivot_row_index,:]
            matrix[i,:] -= normalized_row

        simplex_iteration.append(np.copy(matrix))
        iteration_count += 1

    return (matrix, simplex_iteration)

