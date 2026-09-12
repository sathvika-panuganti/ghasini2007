import os

from pypdf import PdfReader
from docx import Document


def parse_resume(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    # ==========================================
    # PDF
    # ==========================================

    if extension == ".pdf":

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text.strip()


    # ==========================================
    # DOCX
    # ==========================================

    elif extension == ".docx":

        document = Document(file_path)

        text = ""

        for paragraph in document.paragraphs:

            if paragraph.text.strip():

                text += paragraph.text + "\n"

        return text.strip()


    else:

        raise ValueError(
            "Only PDF and DOCX files are supported."
        )