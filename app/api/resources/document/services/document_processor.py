import io
from typing import List

from loguru import logger


class DocumentProcessor:
    def __init__(self):
        self.chunk_size = 1000
        self.chunk_overlap = 200

    def extract_text_from_file(
        self, file_content: bytes, content_type: str, filename: str
    ) -> str:
        """Extract text from a file"""

        try:
            if content_type.startswith("text/"):
                return file_content.decode("utf-8", errors="ignore")

            elif content_type == "application/pdf":
                return self._extract_from_pdf(file_content)

            elif content_type in [
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "application/msword",
            ]:
                return self._extract_from_docx(file_content)

            elif content_type in [
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "application/vnd.ms-excel",
            ]:
                return self._extract_from_excel(file_content)

            elif content_type in [
                "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                "application/vnd.ms-powerpoint",
            ]:
                return self._extract_from_pptx(file_content)
            else:
                raise ValueError(f"Unsupported content type: {content_type}")
        except Exception as e:
            print(f"Error extracting text from {filename}: {e}")
            logger.error(f"Error extracting text from {filename}: {e}")
            return ""

    def _extract_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF - requires PyPDF2 or pdfplumber"""
        try:
            import PyPDF2

            reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except ImportError:
            print("PyPDF2 not installed. PDF processing skipped.")
            return ""

    def _extract_from_docx(self, file_content: bytes) -> str:
        """Extract text from DOCX - requires python-docx"""
        try:
            from docx import Document as DocxDocument

            doc = DocxDocument(io.BytesIO(file_content))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except ImportError:
            print("python-docx not installed. DOCX processing skipped.")
            return ""

    def _extract_from_excel(self, file_content: bytes) -> str:
        """Extract text from Excel - requires openpyxl"""
        try:
            import openpyxl

            workbook = openpyxl.load_workbook(io.BytesIO(file_content))
            text = ""
            for sheet in workbook.worksheets:
                for row in sheet.iter_rows():
                    for cell in row:
                        if cell.value:
                            text += str(cell.value) + " "
                    text += "\n"
            return text
        except ImportError:
            print("openpyxl not installed. Excel processing skipped.")
            return ""

    def _extract_from_pptx(self, file_content: bytes) -> str:
        """Extract text from PPTX - requires python-pptx"""
        try:
            from pptx import Presentation

            prs = Presentation(io.BytesIO(file_content))
            text = ""
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text += shape.text + "\n"
            return text
        except ImportError:
            print("python-pptx not installed. PPTX processing skipped.")
            return ""

    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks with overlap"""
        if not text.strip():
            return []

        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + self.chunk_size

            # Try to break at word boundaries
            if end < text_length:
                # Find the last space before the chunk_size
                last_space = text.rfind(" ", start, end)
                if last_space > start:
                    end = last_space

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            # Move start position with overlap
            start = max(start + 1, end - self.chunk_overlap)

        return chunks

    def process_document(
        self, file_content: bytes, content_type: str, filename: str
    ) -> List[str]:
        """Process document: extract text and create chunks"""
        text = self.extract_text_from_file(file_content, content_type, filename)
        if not text.strip():
            return []

        chunks = self.chunk_text(text)
        logger.info(
            f"Processed document {filename}: {len(chunks)} chunks created {chunks}"
        )
        return chunks


document_processor = DocumentProcessor()
