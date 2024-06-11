import os
import pathlib

from pypdf import PdfWriter


def merge_pdfs(*file_paths: pathlib.Path) -> PdfWriter:
    writer = PdfWriter()
    for file_path in file_paths:
        assert os.path.exists(file_path), f'File "{file_path}" does not exist.'
        assert file_path.suffix == ".pdf", f'File "{file_path}" is not a pdf file.'
        with open(file_path, "rb") as file:
            writer.append(file)
    return writer
