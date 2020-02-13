import csv
from typing import Dict


class CSVCustom:

    def __init__(self, file_path: str, fieldnames: list = None):
        self.file_path = file_path
        self.file = None
        self.fieldnames = fieldnames

    def __enter__(self):
        try:
            self.file = csv.DictReader(open(self.file_path))
        except FileNotFoundError:
            self.file = csv.DictWriter(open(self.file_path, 'w'), fieldnames=self.fieldnames)
            self.file.writeheader()
        finally:
            if not self.file:
                raise
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def read_row(self) -> Dict[str, str]:
        if isinstance(self.file, csv.DictWriter):
            raise RuntimeError('Can read while file is open as write mode.')
        yield from self.file

    def write_row(self, row: Dict[str, str]):
        if isinstance(self.file, csv.DictReader):
            raise RuntimeError('Can write while file is open as read mode.')
        self.file.writerow(row)
