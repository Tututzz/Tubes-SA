import tkinter as tk
from tkinter import messagebox
from itertools import product
import time

def printmatrix(matrix):
    for row in matrix:
        for elem in row:
            print(elem, end=' ')
        print()

def buatmatrix():
    rows = int(rows_entry.get())
    cols = int(cols_entry.get())
    return [[0 for x in range(cols)] for x in range(rows)]

def update_matrix():
    for i, row in enumerate(matrix_entries):
        for j, entry in enumerate(row):
            matrix[i][j] = int(entry.get())
            color_path([i, j], "white")

def buatmatrixstring():
    rows = int(rows_entry.get())
    cols = int(cols_entry.get())
    return [['0' for x in range(cols)] for x in range(rows)]

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

def diam(lokasi):
    return lokasi

def lokasivalid(lokasi, matrix):
    if lokasi[0] < 0 or lokasi[0] >= len(matrix):
        return False
    if lokasi[1] < 0 or lokasi[1] >= len(matrix[0]):
        return False
    if matrix[lokasi[0]][lokasi[1]] != 1:
        return False
    return True

def cekmatriksjalan(matrixjalan, matrix):
    lokasi = [int(start_row_entry.get()), int(start_col_entry.get())]
    akhir = [int(end_row_entry.get()), int(end_col_entry.get())]

    gerakan = []
    visited = set()

    while lokasi != akhir:
        if tuple(lokasi) in visited:
            break
        visited.add(tuple(lokasi))

        arah = matrixjalan[lokasi[0]][lokasi[1]]
        gerakan.append(arah)
        lokasi = eval(arah)(lokasi)
        if not lokasivalid(lokasi, matrix):
            break

    if lokasi == akhir:
        return (True, gerakan, lokasi)
    else:
        return (False, gerakan, lokasi)

def solve_labyrinth():
    global lokasi, matrix
    update_matrix()
    lokasi = [int(start_row_entry.get()), int(start_col_entry.get())]
    awal = lokasi
    akhir = [int(end_row_entry.get()), int(end_col_entry.get())]
    jalan = []

    #menghitung running time
    start_time = time.time()

    matrixjalan = buatmatrixstring()
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:
                jalan.append((i, j))
    # membuat matriks
    possibleJalan = list(product(['kiri', 'kanan', 'atas', 'bawah'], repeat=len(jalan)))
    print(len(possibleJalan))
    found_solution = False
    for kombinasi in possibleJalan:
        matrixjalan_temp = [row[:] for row in matrixjalan]  # membuat salinan matrixjalan
        for idx, elm in enumerate(jalan):
            matrixjalan_temp[elm[0]][elm[1]] = kombinasi[idx]  # mengganti elemen dengan arah dari kombinasi
        matrixjalan_temp[akhir[0]][akhir[1]] = 'diam'
        benar, gerakan, lokasi = cekmatriksjalan(matrixjalan_temp, matrix)
        if benar:
            found_solution = True
            break

    if found_solution:
        print("BERHASIL")
        print(gerakan)
        movements_label.config(text="Gerakan: " + ', '.join(gerakan))
        kombinasi_label.config(text="Jalur yang mungkin: "+str(len(possibleJalan)))
        lokasi = awal
        for step in gerakan:
            color_path(lokasi, "yellow")
            lokasi = eval(step)(lokasi)
        color_path(lokasi, "yellow")
    else:
        messagebox.showinfo("Info", "Buntu.")

    print("--- %s seconds ---" % (time.time() - start_time))


def color_path(lokasi, color):
    matrix_entries[lokasi[0]][lokasi[1]].config(bg=color)

# GUI Setup
root = tk.Tk()
root.title("Maze Code (Exhaustive)")
root.configure(bg="lightblue")

# input ukuran matriks
tk.Label(root, text="Rows:", bg="lightblue").grid(row=0, column=0, padx=5, pady=5)
rows_entry = tk.Entry(root, width=5)
rows_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Columns:", bg="lightblue").grid(row=1, column=0, padx=5, pady=5)
cols_entry = tk.Entry(root, width=5)
cols_entry.grid(row=1, column=1, padx=5, pady=5)

def create_matrix_entries():
    global matrix, matrix_entries
    # Bersihin entri
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

# Frame matrix entries
matrix_frame = tk.Frame(root, bg="lightblue")
matrix_frame.grid(row=3, column=0, columnspan=5, padx=5, pady=5)

# Matrixs button
create_matrix_button = tk.Button(root, text="Create Matrix", command=create_matrix_entries, bg="lightgreen")
create_matrix_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Input titik awal akhir
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

#kombinasi label
kombinasi_label = tk.Label(root, text="Jumlah Jalur Yang Mungkin: ", bg="lightblue")
kombinasi_label.grid(row=5, column=0, columnspan=5, padx=5, pady=5)



root.mainloop()
