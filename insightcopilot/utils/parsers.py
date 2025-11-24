import PyPDF2
import re
from typing import List

def read_pdf(file_path: str) -> str:
    """
    Reads a PDF file and returns its text content.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        A string containing the text from the PDF.
    """
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
        return text
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"An error occurred: {e}"

def clean_text(text: str) -> str:
    """
    Cleans the extracted text by removing excessive newlines and spaces.

    Args:
        text (str): The text to clean.

    Returns:
        A cleaned string.
    """
    # Replace multiple newlines with a single one
    text = re.sub(r'\n\s*\n', '\n', text)
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    return text.strip()

def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    """
    Splits a long text into smaller chunks.

    Args:
        text (str): The text to split.
        chunk_size (int): The maximum size of each chunk.
        chunk_overlap (int): The number of characters to overlap between chunks.

    Returns:
        A list of text chunks.
    """
    if not text:
        return []
        
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap
    return chunks

# Example usage:
if __name__ == "__main__":
    # Create a dummy PDF for testing if it doesn't exist
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter

        dummy_pdf_path = "dummy_test.pdf"
        c = canvas.Canvas(dummy_pdf_path, pagesize=letter)
        c.drawString(100, 750, "This is a test PDF document. It contains some text to be parsed.")
        c.showPage()
        c.drawString(100, 750, "This is the second page with more text and  extra   spaces.")
        c.save()
        print(f"Created dummy PDF: {dummy_pdf_path}")

        # Test PDF reading and cleaning
        pdf_text = read_pdf(dummy_pdf_path)
        print("\n--- Original Text ---")
        print(repr(pdf_text))

        cleaned_text = clean_text(pdf_text)
        print("\n--- Cleaned Text ---")
        print(repr(cleaned_text))

        # Test chunking
        long_text = "This is a very long string designed to test the chunking functionality. " * 100
        text_chunks = chunk_text(long_text, chunk_size=200, chunk_overlap=50)
        print(f"\n--- Text Chunking ---")
        print(f"Original length: {len(long_text)}")
        print(f"Number of chunks: {len(text_chunks)}")
        print("First chunk:", repr(text_chunks[0]))
        print("Second chunk:", repr(text_chunks[1]))

    except ImportError:
        print("\nSkipping PDF creation test: reportlab is not installed.")
        print("You can install it with: pip install reportlab")
    except Exception as e:
        print(f"\nAn error occurred during testing: {e}")
