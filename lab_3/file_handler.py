import csv


def write_csv(file_name: str, parser_data: list, row: list) -> None:
    with open(f'{file_name}.csv', 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(row)
        csv_writer.writerows(parser_data)


def read_logs(path: str):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()

