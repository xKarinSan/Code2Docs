from io import BytesIO
from typing import BinaryIO
from zipfile import ZipFile
from pydantic import BaseModel


class FileItem(BaseModel):
    file_name: str = ""
    contents: bytes = None


class FileReader:
    def __init__(self):
        self.files = {}
        pass

    def unzip_file(self, file: BinaryIO) -> None:
        read_zip_file = ZipFile(BytesIO(file.read()))
        # print("read_zip_file", read_zip_file)
        # print("read_zip_file.namelist", read_zip_file.namelist())
        # items = read_zip_file.extractall("../file_items", read_zip_file.namelist())
        # print("items", items)
        file_list = read_zip_file.namelist()
        for file_name in file_list:
            if ".java" in file_name:
                with read_zip_file.open(file_name) as curr_file:
                    file_lines = []
                    file_contents = curr_file.readlines()
                    for line in file_contents:
                        file_lines.append(line.decode("utf-8").replace("\n", ""))
                        print(line)
                    self.files[file_name] = file_lines
        print(self.files)


file_reader = FileReader()
