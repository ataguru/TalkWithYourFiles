from abc import ABC, abstractmethod
from PyPDF2 import PdfReader
from docx import Document


class FileHandler(ABC):
    """Abstract base class for file handlers."""

    @abstractmethod
    def read_file(self, file):
        """Read the file and extract the text.

        Parameters:
        file (UploadedFile): The file to read.

        Returns:
        str: The extracted text.

        """
        pass

class PDFHandler(FileHandler):
    """File handler for PDF files."""

    def read_file(self, file):
        """
        Read a PDF file and extract the text.

        Parameters:
        file (UploadedFile): The PDF file to read.

        Returns:
        str: The extracted text.
        
        """
        try:
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text
        except Exception as e:
            print(f"Error reading file: {e}")
            return ""  # return an empty string if an error occurs



class DocxHandler(FileHandler):
    """File handler for Word (.docx) files."""

    def read_file(self, file):
        """Read a Word file and extract the text.

        Parameters:
        file (UploadedFile): The Word file to read.

        Returns:
        str: The extracted text.

        """
        try:
            doc = Document(file)
            return " ".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            print(f"Error reading Word file: {e}")
            return ""

class TxtHandler(FileHandler):
    """File handler for text (.txt) files."""

    def read_file(self, file):
        """Read a text file and extract the text.

        Parameters:
        file (UploadedFile): The text file to read.

        Returns:
        str: The extracted text.

        """
        try:
            return file.read().decode('utf-8')
        except Exception as e:
            print(f"Error reading text file: {e}")
            return ""

class FileHandlerFactory:
    """Factory for creating file handlers based on file type."""

    @staticmethod
    def get_file_handler(file_type):
        """Get the appropriate file handler for the given file type.

        Parameters:
        file_type (str): The MIME type of the file.

        Returns:
        FileHandler: The appropriate file handler.

        Raises:
        ValueError: If the file type is not supported.

        """
        if file_type == "application/pdf":
            return PDFHandler()
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return DocxHandler()
        elif file_type == "text/plain":
            return TxtHandler()
        else:
            raise ValueError("Invalid file type")