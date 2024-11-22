import random
import time
import tkinter as tk
from tkinter import messagebox

def print_grid(grid):
    for row in grid:
        print(" ".join(str(num) if num != 0 else '.' for num in row))

def is_safe(grid, row, col, num):
    for x in range(6):
        if grid[row][x] == num or grid[x][col] == num:
            return False

    start_row, start_col = 2 * (row // 2), 3 * (col // 3)
    for i in range(2):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False
    return True

def solve_sudoku(grid):
    empty = find_empty_location(grid)
    if not empty:
        return True

    row, col = empty
    for num in range(1, 7):
        if is_safe(grid, row, col, num):
            grid[row][col] = num
            if solve_sudoku(grid):
                return True
            grid[row][col] = 0
    return False

def find_empty_location(grid):
    for i in range(6):
        for j in range(6):
            if grid[i][j] == 0:
                return (i, j)
    return None

def generate_sudoku(num_empty_cells=10):
    grid = [[0 for _ in range(6)] for _ in range(6)]
    
 
    for i in range(6):
        for j in range(6):
            attempts = 0
            num = random.randint(1, 6)
            while not is_safe(grid, i, j, num) and attempts < 10:
                num = random.randint(1, 6)
                attempts += 1
            if attempts < 10:
                grid[i][j] = num
                if not solve_sudoku(grid):
                    grid[i][j] = 0
                    break

    empty_cells_count = 0
    while empty_cells_count < num_empty_cells:
        row, col = random.randint(0, 5), random.randint(0, 5)
        if grid[row][col] != 0:
            grid[row][col] = 0
            empty_cells_count += 1

    return grid

class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku 6x6")
        self.grid = generate_sudoku(10)
        self.entries = []
        self.start_time = None 

        self.create_grid()
        self.create_buttons()

    def create_grid(self):
        for row in range(6):
            row_entries = []
            for col in range(6):
                value = self.grid[row][col]
                entry = tk.Entry(self.root, width=3, font=("Arial", 18), justify="center")
                entry.grid(row=row, column=col, padx=5, pady=5)
                if value != 0:
                    entry.insert(0, str(value))
                    entry.config(state="disabled")
                row_entries.append(entry)
            self.entries.append(row_entries)

    def create_buttons(self):
     
        solve_button = tk.Button(self.root, text="Resolver", command=self.solve_sudoku_gui)
        solve_button.grid(row=7, column=0, columnspan=2, pady=10)

        # Botón para reiniciar
        reset_button = tk.Button(self.root, text="Reiniciar", command=self.reset_grid)
        reset_button.grid(row=7, column=2, columnspan=2, pady=10)

    
        new_game_button = tk.Button(self.root, text="Otro Juego", command=self.new_game)
        new_game_button.grid(row=7, column=4, columnspan=2, pady=10)

        self.timer_label = tk.Label(self.root, text="Tiempo: 0 s", font=("Arial", 14))
        self.timer_label.grid(row=8, column=0, columnspan=6, pady=5)
        self.start_timer()

    def start_timer(self):
        self.start_time = time.time()  
        self.update_timer()

    def update_timer(self):
        if self.start_time:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Tiempo: {elapsed_time} s")
            self.root.after(1000, self.update_timer)

    def solve_sudoku_gui(self):
   
        for row in range(6):
            for col in range(6):
                try:
                    value = int(self.entries[row][col].get())
                except ValueError:
                    value = 0
                self.grid[row][col] = value

        if solve_sudoku(self.grid):
            for row in range(6):
                for col in range(6):
                    self.entries[row][col].delete(0, tk.END)
                    self.entries[row][col].insert(0, str(self.grid[row][col]))
                    self.entries[row][col].config(state="disabled")
            elapsed_time = int(time.time() - self.start_time)
            messagebox.showinfo("¡Felicidades!", f"¡El Sudoku fue resuelto correctamente!\nTiempo total: {elapsed_time} segundos")
            self.start_time = None  
        else:
            messagebox.showerror("¡Incorrecto!", "Revisa bien el ejercicio")

    def reset_grid(self):
        for row in range(6):
            for col in range(6):
                entry = self.entries[row][col]
                if entry["state"] == "normal":
                    entry.delete(0, tk.END)
        self.start_timer() 

    def new_game(self):

        self.grid = generate_sudoku(10)

    
        for row in range(6):
            for col in range(6):
                entry = self.entries[row][col]
                entry.delete(0, tk.END)  
                value = self.grid[row][col]

                if value != 0:
                    entry.insert(0, str(value))  
                    entry.config(state="disabled") 
                else:
                    entry.config(state="normal")  
        self.start_timer()  


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
