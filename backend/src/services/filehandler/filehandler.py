import zipfile

class FileHandler:
    def unzip_file(self, zip_path: str, extract_to: str) -> None:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)