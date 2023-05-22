# -*- coding: utf-8 -*-

import csv


def get_cell_value_from_csv(filename, row_index, column_index):
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i + 1 == row_index:
                if len(row) >= column_index:
                    return row[column_index - 1]
                else:
                    return None
    return None

def write_data_to_csv(filename, row_index, column_index, data):
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    if row_index <= len(rows):
        if column_index <= len(rows[row_index - 1]):
            rows[row_index - 1][column_index - 1] = data

    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

csv_file = input("Введите название файла\n") + ".csv"
while True:
    choice = input("Нажмите 1 чтобы записать значение ячейки D3 в текстовый файл и очистить ячейку\nНажмите 2 чтобы восстановить значение ячейки D3 из текстового файла\n")

    if choice == '1':
        data = get_cell_value_from_csv(csv_file, 3, 4)

        txt_file = "D3.txt"

        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(str(data))

        write_data_to_csv(csv_file, 3, 4, '')

        print("Ячейка D3 записана в ", txt_file, "\nДанные в ячейке D3 удалены.")

    elif choice == '2':
        txt_file = "D3.txt"

        with open(txt_file, 'r', encoding='utf-8') as f:
            data = f.read()

        write_data_to_csv(csv_file, 3, 4, data)

        print("Ячейка D3 восстановлена из файла ", txt_file)

    else:
        print("Ошибка.")