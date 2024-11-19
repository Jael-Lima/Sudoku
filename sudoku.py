import random

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
    
    # Llena la cuadrícula de manera aleatoria asegurando que sea solucionable
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
    
    # Ahora eliminará celdas para crear un Sudoku con celdas vacías
    empty_cells_count = 0
    while empty_cells_count < num_empty_cells:
        row, col = random.randint(0, 5), random.randint(0, 5)
        if grid[row][col] != 0:
            grid[row][col] = 0
            empty_cells_count += 1
    
    return grid

def user_solve_sudoku(grid):
    print("Por favor, introduce los números en las posiciones vacías.")
    print("Para cada celda vacía, introduce el número en el formato: fila columna valor (ej: 1 2 4 para poner el 4 en la fila 1 columna 2)")
    while find_empty_location(grid):
        print_grid(grid)
        try:
            input_data = input("Introduce tu jugada: ")
            row, col, num = map(int, input_data.split())
            if is_safe(grid, row - 1, col - 1, num):
                grid[row - 1][col - 1] = num
            else:
                print("Número no válido para esta posición. Intenta de nuevo.")
        except ValueError:
            print("Entrada no válida. Asegúrate de usar el formato correcto.")
    
    print("\nSudoku 6x6 resuelto manualmente:")
    print_grid(grid)

if __name__ == "__main__":
    random_sudoku = generate_sudoku(num_empty_cells=10)
    print("Tablero de Sudoku 6x6 generado con celdas vacías:")
    print_grid(random_sudoku)

    user_solve_sudoku(random_sudoku)
