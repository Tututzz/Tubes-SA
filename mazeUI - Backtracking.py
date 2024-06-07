import tkinter as tk
from tkinter import messagebox
import time

def buatmatrix():
    rows = int(rows_entry.get())
    cols = int(cols_entry.get())
    return [[0 for x in range(cols)] for x in range(rows)]

def update_matrix():
    for i, row in enumerate(matrix_entries):
        for j, entry in enumerate(row):
            matrix[i][j] = int(entry.get())
            color_path([i,j],"white")

def print_matrix():
    for row in matrix:
        print(' '.join(str(element) for element in row))

def kiri(lokasi):
    return [lokasi[0], lokasi[1] - 1]

def kanan(lokasi):
    return [lokasi[0], lokasi[1] + 1]

def atas(lokasi):
    return [lokasi[0] - 1, lokasi[1]]

def bawah(lokasi):
    return [lokasi[0] + 1, lokasi[1]]

def lokasivalid(lokasi, matrix):
    if lokasi[0] < 0 or lokasi[0] >= len(matrix):
        return False
    if lokasi[1] < 0 or lokasi[1] >= len(matrix[0]):
        return False
    if matrix[lokasi[0]][lokasi[1]] != 1:
        return False
    return True

def solve_labyrinth():
    global lokasi, matrix
    update_matrix()
    lokasi = [int(start_row_entry.get()), int(start_col_entry.get())]
    awal = lokasi
    akhir = [int(end_row_entry.get()), int(end_col_entry.get())]
    gerakan = []
    stack = [(lokasi, [])]
    visited = set()
    backtracking_tree = []  # Simpen Node Backtrack
    
    #menghitung running time
    start_time = time.time()


    while stack:
        lokasi, path = stack.pop()
        if tuple(lokasi) in visited:
            continue
        visited.add(tuple(lokasi))

        if lokasi == akhir:
            gerakan = path
            break

        if not lokasivalid(lokasi, matrix):
            continue
        
        adajalan = 0
        for direction, name in [(kiri, "kiri"), (atas, "atas"), (kanan, "kanan"), (bawah, "bawah")]:
            new_lokasi = direction(lokasi)
            if lokasivalid(new_lokasi, matrix) and tuple(new_lokasi) not in visited:
                stack.append((new_lokasi, path + [name]))
                adajalan=+1
        if adajalan ==0:
            path.append("INVALID")
            backtracking_tree.append((lokasi, path))
        else:
            backtracking_tree.append((lokasi, path))



    if lokasi == akhir:
        backtracking_tree.append((lokasi, path))
        movements_label.config(text="Gerakan: " + ', '.join(gerakan))
        # Buat Ngewarnain
        lokasi = awal
        for step in gerakan:
            color_path(lokasi, "yellow")
            lokasi = eval(step)(lokasi)
        color_path(lokasi, "yellow")
    else:
        messagebox.showinfo("Info", "Buntu.")
        
    print("--- %s seconds ---" % (time.time() - start_time))

    display_backtracking_tree(backtracking_tree)

def color_path(lokasi, color):
    matrix_entries[lokasi[0]][lokasi[1]].config(bg=color)

def display_backtracking_tree(tree):
    # Bersihkan tree
    for widget in tree_frame.winfo_children():
        widget.destroy()

    # Display tree
    for i, (node, path) in enumerate(tree):
        tk.Label(tree_frame, text=f"{node} -> {path}", bg="lightblue").pack(anchor="w")

# GUI Setup
root = tk.Tk()
root.title("Maze Code (BackTrack)")
root.configure(bg="lightblue")

# Matrix input
tk.Label(root, text="Rows:", bg="lightblue").grid(row=0, column=0, padx=5, pady=5)
rows_entry = tk.Entry(root, width=5)
rows_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Columns:", bg="lightblue").grid(row=1, column=0, padx=5, pady=5)
cols_entry = tk.Entry(root, width=5)
cols_entry.grid(row=1, column=1, padx=5, pady=5)

def create_matrix_entries():
    global matrix, matrix_entries
    # Buat ngosongin entri
    for widget in matrix_frame.winfo_children():
        widget.destroy()
    matrix = buatmatrix()
    matrix_entries = []
    for i in range(len(matrix)):
        row_entries = []
        for j in range(len(matrix[0])):
            entry = tk.Entry(matrix_frame, width=3)
            entry.grid(row=i, column=j, padx=1, pady=1)
            row_entries.append(entry)
        matrix_entries.append(row_entries)

# Frame matriks
matrix_frame = tk.Frame(root, bg="lightblue")
matrix_frame.grid(row=3, column=0, columnspan=5, padx=5, pady=5)

# Tombol matrix
create_matrix_button = tk.Button(root, text="Create Matrix", command=create_matrix_entries, bg="lightgreen")
create_matrix_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# input titik akhir dan awal
tk.Label(root, text="Start (row, col):", bg="lightblue").grid(row=0, column=2, padx=5, pady=5)
start_row_entry = tk.Entry(root, width=5)
start_row_entry.grid(row=0, column=3, padx=5, pady=5)
start_col_entry = tk.Entry(root, width=5)
start_col_entry.grid(row=0, column=4, padx=5, pady=5)

tk.Label(root, text="End (row, col):", bg="lightblue").grid(row=1, column=2, padx=5, pady=5)
end_row_entry = tk.Entry(root, width=5)
end_row_entry.grid(row=1, column=3, padx=5, pady=5)
end_col_entry = tk.Entry(root, width=5)
end_col_entry.grid(row=1, column=4, padx=5, pady=5)

# Solve button
solve_button = tk.Button(root, text="Solve", command=solve_labyrinth, bg="lightgreen")
solve_button.grid(row=2, column=2, columnspan=3, padx=5, pady=5)

# Label gerakan
movements_label = tk.Label(root, text="Gerakan: ", bg="lightblue")
movements_label.grid(row=4, column=0, columnspan=5, padx=5, pady=5)

# Frame backtracking tree
tree_frame = tk.Frame(root, bg="lightblue")
tree_frame.grid(row=5, column=0, columnspan=5, padx=5, pady=5)

root.mainloop()
