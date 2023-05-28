import csv
import json
import os
import re
import tkinter as tk
from tkinter import filedialog


def get_cell_values_from_csv(filename, symbols_count_threshold):
    cell_data = {}
    with open(filename, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            for j, cell in enumerate(row):
                if len(cell) > symbols_count_threshold:
                    cell_name = get_cell_name(j, i + 1)
                    cell_data[cell_name] = cell
                    row[j] = ''
    return cell_data


def write_data_to_csv(filename, cell_data):
    with open(filename, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        rows = list(reader)

    for cell_name, cell_value in cell_data.items():
        column_index, row_index = get_cell_indices(cell_name)
        if row_index < len(rows):
            if column_index < len(rows[row_index]):
                rows[row_index][column_index] = cell_value
            else:
                rows[row_index].extend([""] * (column_index - len(rows[row_index]) + 1))
                rows[row_index][column_index] = cell_value
        else:
            empty_row = [""] * (column_index + 1)
            empty_row[column_index] = cell_value
            rows.extend([empty_row] * (row_index - len(rows) + 1))

    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def delete_cells_from_csv(filename, cell_data):
    with open(filename, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        rows = list(reader)

    for cell_name in cell_data:
        column_index, row_index = get_cell_indices(cell_name)
        if row_index < len(rows) and column_index < len(rows[row_index]):
            rows[row_index][column_index] = ''

    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def get_cell_name(column_index, row_index):
    dividend = column_index + 1
    cell_name = ''
    while dividend > 0:
        modulo = (dividend - 1) % 26
        cell_name = chr(65 + modulo) + cell_name
        dividend = (dividend - modulo) // 26
    return cell_name + str(row_index)


def get_cell_indices(cell_name):
    match = re.match(r'([A-Z]+)(\d+)', cell_name)
    column_name = match.group(1)
    row_index = int(match.group(2))
    column_index = 0
    for i, char in enumerate(column_name):
        column_index += (ord(char) - 65 + 1) * (26 ** (len(column_name) - i - 1))
    return column_index - 1, row_index - 1


def browse_csv_file():
    filename = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
    csv_file_entry.delete(0, tk.END)
    csv_file_entry.insert(0, filename)


def save_cells_to_json():
    csv_file = csv_file_entry.get()
    symbols_count_threshold = int(symbols_count_entry.get())
    json_file = os.path.splitext(csv_file)[0] + ".json"

    cell_data = get_cell_values_from_csv(csv_file, symbols_count_threshold)

    if cell_data:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(cell_data, f, ensure_ascii=False, indent=4)

        delete_cells_from_csv(csv_file, cell_data)

        status_label.config(text=f"Cells saved to {json_file}. Corresponding cells in the CSV file cleared.")
    else:
        status_label.config(text=f"No cells found with symbols count exceeding {symbols_count_threshold}.")


def restore_cells_from_json():
    csv_file = csv_file_entry.get()
    json_file = os.path.splitext(csv_file)[0] + ".json"

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            cell_data = json.load(f)
    except FileNotFoundError:
        status_label.config(text=f"File {json_file} not found.")
        return
    except json.JSONDecodeError:
        status_label.config(text=f"Invalid JSON format in {json_file}.")
        return

    write_data_to_csv(csv_file, cell_data)

    status_label.config(text=f"Cell values restored from {json_file}.")


root = tk.Tk()
root.title("CSV Cell Manager")
# root.iconbitmap('icon.ico')
root.iconphoto(False, tk.PhotoImage(file="icon.png"))

# CSV file selection
csv_file_label = tk.Label(root, text="CSV File:")
csv_file_label.grid(row=0, column=0, sticky="e")

csv_file_entry = tk.Entry(root, width=40)
csv_file_entry.grid(row=0, column=1)

csv_file_browse_button = tk.Button(root, text="Browse", command=browse_csv_file)
csv_file_browse_button.grid(row=0, column=2)

# Symbols count threshold
symbols_count_label = tk.Label(root, text="Symbols Count Threshold:")
symbols_count_label.grid(row=1, column=0, sticky="e")

symbols_count_entry = tk.Entry(root, width=10)
symbols_count_entry.grid(row=1, column=1)
symbols_count_entry.insert(0, "32767")

# Save and Restore buttons
save_button = tk.Button(root, text="Save to JSON", command=save_cells_to_json)
save_button.grid(row=2, column=0)

restore_button = tk.Button(root, text="Restore from JSON", command=restore_cells_from_json)
restore_button.grid(row=2, column=1)

# Status label
status_label = tk.Label(root, text="")
status_label.grid(row=3, columnspan=3)

root.mainloop()
