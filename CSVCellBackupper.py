import csv
import json
import os
import re
import tkinter as tk
from tkinter import filedialog


class CSVCellBackupper:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        self.root.title("CSV Cell Backupper")
        self.root.configure(bg="#212121")

        self.csv_file_label = tk.Label(self.root, text="CSV File:", fg="white", bg="#212121")
        self.csv_file_label.grid(row=0, column=0)

        self.csv_file_entry = tk.Entry(self.root, width=40, fg="white", bg="#212121")
        self.csv_file_entry.grid(row=0, column=1)

        self.csv_file_browse_button = tk.Button(self.root, text="Browse", command=self.browse_csv_file, fg="white", bg="#212121")
        self.csv_file_browse_button.grid(row=0, column=2)

        self.symbols_count_label = tk.Label(self.root, text="Symbols Count Threshold:", fg="white", bg="#212121")
        self.symbols_count_label.grid(row=1, column=1)

        self.symbols_count_entry = tk.Entry(self.root, width=10, fg="white", bg="#212121")
        self.symbols_count_entry.grid(row=1, column=2)
        self.symbols_count_entry.insert(0, "32767")

        self.status_label = tk.Label(self.root, text="", fg="white", bg="#212121")
        self.status_label.grid(row=2, columnspan=3)
        self.root.rowconfigure(1, minsize=50)
        self.root.rowconfigure(3, minsize=50)

        self.save_button = tk.Button(self.root, text="Save to JSON", command=self.save_cells_to_json, fg="white", bg="#212121")
        self.save_button.grid(row=3, column=0)

        self.restore_button = tk.Button(self.root, text="Restore from JSON", command=self.restore_cells_from_json, fg="white", bg="#212121")
        self.restore_button.grid(row=3, column=1)

        self.remove_button = tk.Button(self.root, text="Remove JSON", command=self.remove_json, fg="white", bg="#6c0f0f")
        self.remove_button.grid(row=3, column=2)

        self.root.configure(pady=10, padx=10)

    def browse_csv_file(self):
        filename = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
        self.csv_file_entry.delete(0, tk.END)
        self.csv_file_entry.insert(0, filename)

    def get_cell_values_from_csv(self, filename, symbols_count_threshold):
        cell_data = {}
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                for j, cell in enumerate(row):
                    if len(cell) > symbols_count_threshold:
                        cell_name = self.get_cell_name(j, i + 1)
                        cell_data[cell_name] = cell
                        row[j] = ''
        return cell_data

    def write_data_to_csv(self, filename, cell_data):
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        for cell_name, cell_value in cell_data.items():
            column_index, row_index = self.get_cell_indices(cell_name)
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

        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    def delete_cells_from_csv(self, filename, cell_data):
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        for cell_name in cell_data:
            column_index, row_index = self.get_cell_indices(cell_name)
            if row_index < len(rows) and column_index < len(rows[row_index]):
                rows[row_index][column_index] = ''

        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    def get_cell_name(self, column_index, row_index):
        dividend = column_index + 1
        cell_name = ''
        while dividend > 0:
            modulo = (dividend - 1) % 26
            cell_name = chr(65 + modulo) + cell_name
            dividend = (dividend - modulo) // 26
        return cell_name + str(row_index)

    def get_cell_indices(self, cell_name):
        match = re.match(r'([A-Z]+)(\d+)', cell_name)
        column_name = match.group(1)
        row_index = int(match.group(2))
        column_index = 0
        for i, char in enumerate(column_name):
            column_index += (ord(char) - 65 + 1) * (26 ** (len(column_name) - i - 1))
        return column_index - 1, row_index - 1

    def remove_json(self):
        csv_file = self.csv_file_entry.get()
        json_file = os.path.splitext(csv_file)[0] + ".json"
        if os.path.exists(json_file):
            os.remove(json_file)
            self.status_label.config(text=f"JSON file '{json_file}' removed.")
        else:
            self.status_label.config(text=f"JSON file '{json_file}' does not exist.")

    def save_cells_to_json(self):
        csv_file = self.csv_file_entry.get()
        symbols_count_threshold = int(self.symbols_count_entry.get())
        json_file = os.path.splitext(csv_file)[0] + ".json"

        cell_data = self.get_cell_values_from_csv(csv_file, symbols_count_threshold)

        if cell_data:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(cell_data, f, ensure_ascii=False, indent=4)

            self.delete_cells_from_csv(csv_file, cell_data)

            self.status_label.config(text=f"Cells saved to {json_file}. Corresponding cells in the CSV file cleared.")
        else:
            self.status_label.config(text=f"No cells found with symbols count exceeding {symbols_count_threshold}.")

    def restore_cells_from_json(self):
        csv_file = self.csv_file_entry.get()
        json_file = os.path.splitext(csv_file)[0] + ".json"

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                cell_data = json.load(f)
        except FileNotFoundError:
            self.status_label.config(text=f"File {json_file} not found.")
            return
        except json.JSONDecodeError:
            self.status_label.config(text=f"Invalid JSON format in {json_file}.")
            return

        self.write_data_to_csv(csv_file, cell_data)

        self.status_label.config(text=f"Cell values restored from {json_file}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVCellBackupper(root)
    root.mainloop()
