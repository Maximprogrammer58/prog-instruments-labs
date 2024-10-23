import csv


def write_csv(file_name: str, parser_data: list, row: list) -> None:
    """Writing data after parsing to a csv file
       Args:
         file_name: the name of the file to be recorded
         parser_data: data after parsing
         row: сolumn headers of the csv file
    """
    with open(f'{file_name}.csv', 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(row)
        csv_writer.writerows(parser_data)


def read_logs(path: str) -> str:
    """Reading logs from a text file
       Args:
         path: the path to the log file
       Returns:
         logs
    """
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()

