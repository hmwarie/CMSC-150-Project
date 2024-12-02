import tkinter as tk
from tkinter import *
import ttkbootstrap as ttk

from .optimized_solution import OptimizedSolution

from util.food_data_util import foods, food_data, food_cost, food_serving, nutrients
from util.generate_solution_util import generate_solution_dictionary

from texts import *

class DietOptimizerPage(ttk.Frame):
    def __init__(self, root, send_to, main_frame):
        super().__init__(root)
        self.root = root
        self.send_to = send_to
        self.main_frame = main_frame

        self.searched_food = StringVar()

        self.food_cost = food_cost
        self.food_serving = food_serving
        self.food_data = food_data
        self.nutrients = nutrients

        self.foods = foods
        self.selected_foods = []

        self.initialize_frames()

    def initialize_frames(self):
        self.diet_optimizer_detail_frame = ttk.Frame(self)
        self.diet_optimizer_detail_frame.pack(side="top", padx=10, fill="x")

        self.checkbox_parent_frame = ttk.Frame(self)
        self.checkbox_parent_frame.pack(pady=10)

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=10, fill="x")

        self.generate_diet_optimizer_details()
        self.generate_food_checkbox()
        self.generate_buttons()


    def generate_diet_optimizer_details(self):
        diet_optimizer_title_label = ttk.Label(self.diet_optimizer_detail_frame, text="Diet Optimizer", font=("Arial Black", 28))
        diet_optimizer_title_label.pack(pady=15, anchor="w")

        self.generate_food_search()

    def generate_food_search(self):
        food_search_label = ttk.Label(self.diet_optimizer_detail_frame, text=food_search_description, font=("Bahnschrift Light", 10))
        food_search_label.pack(anchor="w")

        self.food_search_entry = ttk.Entry(self.diet_optimizer_detail_frame, textvariable=self.searched_food, width=40, foreground="grey", style="secondary.TEntry")
        self.food_search_entry.insert(0, "Search desired foods")
        self.food_search_entry.pack(side="left", anchor="w", pady=10)
        
        self.food_search_entry.bind('<FocusIn>', lambda event: self.on_entry_click())
        self.food_search_entry.bind('<FocusOut>', lambda event: self.on_entry_leave())

        self.add_food_button = ttk.Button(self.diet_optimizer_detail_frame, text="Add", bootstyle="light-outline", command=self.add_food)
        self.add_food_button.pack(side="left", anchor="w", padx=10, pady=10)

        self.success_promt = ttk.Label(self.diet_optimizer_detail_frame, text="")
        self.success_promt.pack(side="left", anchor="w", padx=10, pady=10)

    def generate_success_prompt(self):
        entered_food = self.food_search_entry.get()
        
        if entered_food in self.foods and entered_food not in self.selected_foods:
            self.success_promt.config(text=f"Succesfully added {self.food_search_entry.get()}", bootstyle="success")
            self.selected_foods.append(entered_food)

        elif entered_food in self.selected_foods:
            self.success_promt.config(text=f"{entered_food} is already selected", bootstyle="danger")
        elif entered_food == "Select desired food":
            self.success_promt.config(text="")
        else:
            self.success_promt.config(text=f"Food not in list of food selection", bootstyle="danger")

    def generate_food_checkbox(self):
        checkbox_frame = ttk.Frame(self.checkbox_parent_frame)
        checkbox_frame.pack(side="left", padx=5, pady=5)

        for i, food in enumerate(self.foods):

            checkbox_var = tk.BooleanVar(value=False)
            food_checkbox = ttk.Checkbutton(checkbox_frame, text=food, variable=checkbox_var, onvalue=True, offvalue=False, command=lambda f=food, var=checkbox_var: self.toggle_selection(f, var))
            food_checkbox.pack(side="top", pady=5, anchor="nw")

            if (i + 1) % 13 == 0:
                checkbox_frame = ttk.Frame(self.checkbox_parent_frame)
                checkbox_frame.pack(side="left", anchor="nw", padx=5, pady=5)

    def generate_buttons(self):
        back_button = ttk.Button(self.button_frame, text="Back", bootstyle="light-outline", command=lambda: self.send_to(self.main_frame))
        back_button.pack(side="left", anchor="w", padx=5)

        nutrient_table_button = ttk.Button(self.button_frame, text="See Nutrients Table", bootstyle="light-outline", command=self.genetate_nutrient_table)
        nutrient_table_button.pack(side="left", anchor="w", padx=5)


        select_all_button = ttk.Button(self.button_frame, text="Select All", bootstyle="light-outline", command=self.select_all_foods)
        select_all_button.pack(side="left", anchor="w", padx=5)

        generate_button = ttk.Button(self.button_frame, text="Generate", bootstyle="primary", command=self.generate_optimal_solution)
        generate_button.pack(side="left", anchor="w", padx=5)

        clear_button = ttk.Button(self.button_frame, text="Clear Selection", bootstyle="danger", command=self.clear_selection)
        clear_button.pack(side="left", anchor="w", padx=5)

    def genetate_nutrient_table(self):
        nutrient_table = ttk.Toplevel(self.root)
        nutrient_table.title("Nutrient Table")
        nutrient_table.geometry("720x400")

        nutrient_table_frame = ttk.Frame(nutrient_table)
        nutrient_table_frame.pack(padx=80, pady=50)

        food_search_label = ttk.Label(nutrient_table_frame, text="Below is the list of foods and its corresponding cost and nutritional value per serving", font=("Bahnschrift Light", 10))
        food_search_label.pack(pady=10, anchor="w")

        column_names = ["Foods", "Costs", "Serving"]
        column_names.extend(self.nutrients)

        simplex_iteration_y_scrollbar = ttk.Scrollbar(nutrient_table_frame, bootstyle="dark-round")
        simplex_iteration_y_scrollbar.pack(side="right", fill="y")

        simplex_iteration_x_scrollbar = ttk.Scrollbar(nutrient_table_frame, orient="horizontal", bootstyle="dark-round")
        simplex_iteration_x_scrollbar.pack(side="bottom", fill="x")

        nutrient_treeview = ttk.Treeview(nutrient_table_frame, columns=column_names, show="headings",  yscrollcommand=simplex_iteration_y_scrollbar.set, xscrollcommand=simplex_iteration_x_scrollbar.set, height=15, bootstyle="dark")
        
        for column_name in column_names:
            nutrient_treeview.heading(column_name, text=column_name, anchor="w")
            nutrient_treeview.column(column_name, width=100)


        for foods, nutrients in self.food_data.items():
            content = [foods, self.food_cost[foods], self.food_serving[foods]]
            content.extend(nutrients)
            row_values = tuple(content)
            nutrient_treeview.insert("", "end", values=row_values)

        simplex_iteration_y_scrollbar.config(command=nutrient_treeview.yview)
        simplex_iteration_x_scrollbar.config(command=nutrient_treeview.xview)

        nutrient_treeview.pack()

    def generate_optimal_solution(self):
        self.optimized_solution_frame = OptimizedSolution(self.root, self, self.selected_foods)
        self.optimized_solution_frame.pack()
        self.pack_forget()

    def on_entry_click(self):
        self.food_search_entry.delete(0, tk.END)

    def on_entry_leave(self):
        default_text = "Search desired food"
        entered_food = self.food_search_entry.get()

        if not entered_food or entered_food not in self.foods:
            self.food_search_entry.delete(0, tk.END)
            self.food_search_entry.insert(0, default_text)
            self.food_search_entry.config(foreground="grey")

    def add_food(self):
        for frame in self.checkbox_parent_frame.winfo_children():
            if isinstance(frame, ttk.Frame):
                for checkbox in frame.winfo_children():
                    if isinstance(checkbox, ttk.Checkbutton) and checkbox.cget("text") == self.food_search_entry.get():
                        checkbox.state(['selected'])

        self.generate_success_prompt()

    def toggle_selection(self, food, checkbox_var):
        selected = checkbox_var.get()

        if selected:
            self.selected_foods.append(food)
        else:
            self.selected_foods.remove(food)

    def select_all_foods(self):
        for frame in self.checkbox_parent_frame.winfo_children():
            if isinstance(frame, ttk.Frame):
                for checkbox in frame.winfo_children():
                    if isinstance(checkbox, ttk.Checkbutton):
                        checkbox.state(['selected'])
                
        self.selected_foods.clear()
        for food in self.foods:
            self.selected_foods.append(food)

    def clear_selection(self):
        for frame in self.checkbox_parent_frame.winfo_children():
            if isinstance(frame, ttk.Frame):
                for checkbox in frame.winfo_children():
                    if isinstance(checkbox, ttk.Checkbutton):
                        checkbox.state(['!selected'])
                
        self.selected_foods.clear()
        self.success_promt.config(text="")
    
    def send_to_optimized_solution_frame(self):
        self.optimized_solution_frame.pack()
        self.pack_forget()
        