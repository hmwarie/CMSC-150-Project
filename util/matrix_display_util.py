import numpy as np
from tkinter import *
import ttkbootstrap as ttk

class MatrixDisplay(ttk.Frame):
    def __init__(self, root, matrix, selected_foods, is_last_iteration):
        """
        Initializes the MatrixDisplay frame with the given parameters.
        """
        super().__init__(root)
        self.selected_foods = selected_foods
        self.matrix = matrix
        self.final_solution = is_last_iteration
        self.initialize_frame()

    def initialize_frame(self):
        """
        Initializes the frame by generating column names and adding necessary subframes.
        """
        self.generate_column_names()
        self.generate_simplex_iteration_frame()
        self.generate_simplex_basic_solution_frame()

    def generate_column_names(self):
        """
        Generates the column names for the simplex matrix, including slack variables, food variables, and other necessary columns.
        """
        self.columns_names = [f"S{i+1}" for i in range(self.matrix.shape[1] - len(self.selected_foods) - 2)]
        self.columns_names.extend([f"x{i+1}" for i in range(len(self.selected_foods))])
        self.columns_names.extend(["z", "RHS"])

    def generate_simplex_iteration_frame(self):
        """
        Generates and displays the frame for the simplex iteration matrix, including scrollbars for navigation.
        """
        simplex_iteration_frame = ttk.Frame(self)
        simplex_iteration_frame.pack(padx=130, pady=10)

        simplex_iteration_y_scrollbar = ttk.Scrollbar(simplex_iteration_frame, bootstyle="dark-round")
        simplex_iteration_y_scrollbar.pack(side="right", fill="y")

        simplex_iteration_x_scrollbar = ttk.Scrollbar(simplex_iteration_frame, orient="horizontal", bootstyle="dark-round")
        simplex_iteration_x_scrollbar.pack(side="bottom", fill="x")

        simplex_iteration_treeview = ttk.Treeview(simplex_iteration_frame, columns=self.columns_names, show="headings",  yscrollcommand=simplex_iteration_y_scrollbar.set, xscrollcommand=simplex_iteration_x_scrollbar.set, height=15, bootstyle="dark")
        
        for column_name in self.columns_names:
            simplex_iteration_treeview.heading(column_name, text=column_name, anchor="w")
            simplex_iteration_treeview.column(column_name, width=50)

        for i in range(self.matrix.shape[0]):
            row_values = tuple(np.round(self.matrix[i, :], decimals=2))
            simplex_iteration_treeview.insert("", "end", values=row_values)

        simplex_iteration_y_scrollbar.config(command=simplex_iteration_treeview.yview)
        simplex_iteration_x_scrollbar.config(command=simplex_iteration_treeview.xview)

        simplex_iteration_treeview.pack()

    def generate_simplex_basic_solution_frame(self):
        """
        Generates and displays the frame for the basic solution in the simplex method, showing either the final or current solution.
        """
        simplex_basic_solution_frame = ttk.Frame(self)
        simplex_basic_solution_frame.pack(padx=130, pady=20)

        simplex_basic_solution_x_scrollbar = ttk.Scrollbar(simplex_basic_solution_frame, orient="horizontal", bootstyle="dark-round")
        simplex_basic_solution_x_scrollbar.pack(side="bottom", fill="x")

        simplex_iteration_treeview = ttk.Treeview(simplex_basic_solution_frame, columns=self.columns_names, show="headings", xscrollcommand=simplex_basic_solution_x_scrollbar.set, height=1, bootstyle="dark")
        
        for column_name in self.columns_names[:-1]:
            simplex_iteration_treeview.heading(column_name, text=column_name, anchor="w")
            simplex_iteration_treeview.column(column_name, width=50)

        if self.final_solution:
            simplex_iteration_treeview.insert("", "end", values=tuple(np.round(np.append(self.matrix[-1,:-2],self.matrix[-1,-1]), decimals=2)))
        else:
            simplex_iteration_treeview.insert("", "end", values=tuple(np.round(self.get_solution(self.matrix), decimals=2)))

        simplex_basic_solution_x_scrollbar.config(command=simplex_iteration_treeview.xview)

        simplex_iteration_treeview.pack()        

    def find_identity(self, array):
        """
        Finds the index of the identity (value '1') in the given array, if it exists.
        """
        if 1 in array:
            instance_of_1 = np.where(array == 1)[0]
            if instance_of_1.size == 1:
                return instance_of_1.item()
            return instance_of_1[0].item()
        return None
    
    def is_identity(self, array, index):
        """
        Checks if the given index in the array corresponds to an identity column (only 1 at that index, 0 elsewhere).
        """
        for i in range(len(array)):
            if i == index:
                continue
            if array[i] != 0:
                return False
        return True

    def get_solution(self, matrix):
        """
        Extracts the solution vector from the simplex matrix by identifying basic variables.
        """
        num_variables = matrix.shape[1] - 1
        solution = np.empty(num_variables)
        for i in range(num_variables):
            solution_index = self.find_identity(matrix[:, i])        
            if solution_index is not None and self.is_identity(matrix[:, i], solution_index):
                solution[i] = matrix[solution_index, -1]
            else:
                solution[i] = 0
        return solution
