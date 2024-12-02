from tkinter import *
import ttkbootstrap as ttk

from .simplex_iteration import SimplexIteration
from util.generate_solution_util import generate_solution_dictionary

from util.food_data_util import foods, food_cost

from texts import *

class OptimizedSolution(ttk.Frame):
    def __init__(self, root, diet_optimizer, selected_foods):
        super().__init__(root)
        self.root = root
        self.diet_optimizer = diet_optimizer
        self.searched_food = StringVar()

        self.foods = foods
        self.food_cost = food_cost
        self.selected_foods = selected_foods

        self.initialize_frames()

    def initialize_frames(self):
        self.optimized_solution_detail_frame = ttk.Frame(self)
        self.optimized_solution_detail_frame.pack(side="top", pady=10)

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=10, anchor="w")

        self.solution_frame = ttk.Frame(self)
        self.solution_frame.pack(anchor="w", pady=10)

        self.generate_diet_optimizer_details()
        self.generate_buttons()
        self.generate_optimal_solution()
        self.display_solution()

        self.disable_simplex_iterations()

    def generate_diet_optimizer_details(self):
        optimized_solution_title_label = ttk.Label(self.optimized_solution_detail_frame, text="Optimized Food Combination", font=("Arial Black", 28))
        optimized_solution_title_label.pack(pady=15, anchor="w")

        self.optimized_solution_description_label = ttk.Label(self.optimized_solution_detail_frame, text=optimized_solution_text, font=("Bahnschrift Light", 10), wraplength=800, justify="left")
        self.optimized_solution_description_label.pack(pady=5, anchor="w")

        self.warning_prompt = ttk.Label(self.optimized_solution_detail_frame, text="", font=("Bahnschrift Light", 10), wraplength=800, justify="left", bootstyle="danger")
        self.warning_prompt.pack(pady=5, anchor="w")

    def generate_buttons(self):
        back_button = ttk.Button(self.button_frame, text="Back", bootstyle="light-outline", command=lambda: self.send_to_diet_optimizer())
        back_button.pack(side="left", anchor="w", padx=5)

        self.simplex_iterations_button = ttk.Button(self.button_frame, text="See Simplex Iterations", bootstyle="light-outline", command= self.generate_simplex_iteration_frame)
        self.simplex_iterations_button.pack(side="left", anchor="w", padx=5)

    def disable_simplex_iterations(self):
        if self.selected_foods == []:
            self.warning_prompt.config(text="Warning: No Food Selected")
            self.simplex_iterations_button.config(state="disabled")
        elif self.simplex_iteration is None:
            self.simplex_iterations_button.config(state="disabled")
        else:
            self.warning_prompt.config(text="")
            self.simplex_iterations_button.config(state="normal")

    def generate_optimal_solution(self):
        self.solution_dictionary, self.simplex_iteration = generate_solution_dictionary(self.selected_foods)
            
    def generate_simplex_iteration_frame(self):
        if self.simplex_iteration != []:
            self.simplex_iteration_frame = SimplexIteration(self.root, self.simplex_iteration, self.selected_foods, self)
                
        self.send_to_simplex_iteration_frame()

    def display_solution(self):
        if self.solution_dictionary is None:
            self.optimized_solution_description_label.config(text=no_optimized_solution_text, font=("Bahnschrift Light", 10), wraplength=800, justify="left")
            return

        food_frame = ttk.Frame(self.solution_frame)
        food_frame.pack(side="left", padx=5)

        serving_frame = ttk.Frame(self.solution_frame)
        serving_frame.pack(side="left", padx=5)

        cost_frame = ttk.Frame(self.solution_frame)
        cost_frame.pack(side="left", padx=5)


        food_heading_label = ttk.Label(food_frame, text="Food", font=("Bahnschrift SemiBold", 10))
        food_heading_label.pack(anchor="w", pady=5)

        serving_heading_label = ttk.Label(serving_frame, text="Serving", font=("Bahnschrift SemiBold", 10))
        serving_heading_label.pack(anchor="w", pady=5)

        cost_heading_label = ttk.Label(cost_frame, text="Cost", font=("Bahnschrift SemiBold", 10))
        cost_heading_label.pack(anchor="w", pady=5)

        for food, serving in self.solution_dictionary.items():    
            if food in self.foods and serving != 0:
                food_label = ttk.Label(food_frame, text=food, font=("Bahnschrift Light", 10),)
                food_label.pack(anchor="w", pady=5)

                serving_label = ttk.Label(serving_frame, text=f"{format(serving, ".2f")}", font=("Bahnschrift Light", 10))
                serving_label.pack(anchor="w", pady=5)

                serving_label = ttk.Label(cost_frame, text=f"$ {format(self.food_cost[food]*serving, ".2f")}", font=("Bahnschrift Light", 10))
                serving_label.pack(anchor="w", pady=5)

        total_food_label = ttk.Label(food_frame, text="Total Cost", font=("Bahnschrift Light", 10))
        total_food_label.pack(anchor="w", pady=5)

        total_serving_label = ttk.Label(serving_frame, text="   ~   ", font=("Bahnschrift Light", 10))
        total_serving_label.pack(anchor="w", pady=5)

        total_cost_label = ttk.Label(cost_frame, text=f"$ {format(self.solution_dictionary["Total Cost"], ".2f")}", font=("Bahnschrift Light", 10))
        total_cost_label.pack(anchor="w", pady=5)

    def send_to_diet_optimizer(self):
        self.diet_optimizer.pack()
        self.pack_forget()

    def send_to_simplex_iteration_frame(self):
        self.simplex_iteration_frame.pack(fill="both", expand=True)
        self.pack_forget()