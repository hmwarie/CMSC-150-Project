import numpy as np
from .food_data_util import food_data, upper_limit, lower_limit, food_cost

def get_variables(foods):
    """
    Generates a list of variable names for the optimization problem.
    """
    variables = []
    for i in range(len(foods)):
        variables.append(f"x{i+1}")
    for i in range(22 + len(foods)):
        variables.append(f"s{i+1}")
    variables.append("z")
    return variables

def generate_maximum_constraints(foods):
    """
    Generates the matrix for upper-bound constraints in the optimization problem.
    """
    matrix_coefficients = []
    for i in range(11):
        upper_constraints_coefficients = []
        for food in foods:
            upper_constraints_coefficients.append(-1*food_data[food][i])
        upper_constraints_coefficients.append(-1*upper_limit[i])
        matrix_coefficients.append(upper_constraints_coefficients)
    return np.array(matrix_coefficients)

def generate_minimum_constraints(foods):
    """
    Generates the matrix for lower-bound constraints in the optimization problem.
    """
    matrix_coefficients = []
    for i in range(11):
        lower_constraints_coefficients = []
        for food in foods:
            lower_constraints_coefficients.append(food_data[food][i])
        lower_constraints_coefficients.append(lower_limit[i])
        matrix_coefficients.append(lower_constraints_coefficients)
    return np.array(matrix_coefficients)

def generate_serving_constraints(foods):
    """
    Generates the matrix for serving constraints (e.g., serving size constraints) in the optimization problem.
    """
    matrix_coefficients = []
    for i in range(len(foods)):
        serving_coefficient = []
        for j in range(len(foods)):
            if i == j:
                serving_coefficient.append(-1)
            else:
                serving_coefficient.append(0)
        serving_coefficient.append(-10)
        matrix_coefficients.append(serving_coefficient)
    return np.array(matrix_coefficients)

def generate_constraints_matrix(foods):
    """
    Generates the complete matrix of constraints, combining upper, lower, and serving constraints.
    """
    upper_constraints = generate_maximum_constraints(foods)
    lower_constraints = generate_minimum_constraints(foods)
    serving_constraints = generate_serving_constraints(foods)
    constraints_matrix = np.vstack((upper_constraints, lower_constraints, serving_constraints))
    return constraints_matrix

def generate_objective_matrix(foods):
    """
    Generates the objective function's coefficient matrix, which corresponds to the food costs.
    """
    objective_coefficients = []
    for food in foods:
        objective_coefficients.append(food_cost[food])
    objective_coefficients.extend([0])
    return np.array(objective_coefficients)

def generate_augmented_matrix(foods):
    """
    Generates the augmented matrix combining constraints and objective function.
    """
    constraints_matrix = generate_constraints_matrix(foods)
    objective_matrix = generate_objective_matrix(foods)
    return np.vstack((constraints_matrix, objective_matrix))
