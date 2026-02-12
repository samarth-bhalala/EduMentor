"""
PDF parsing and text extraction utilities
"""
import PyPDF2
from typing import List
import re

def extract_text(file) -> str:
    """
    Extract all text from a PDF file
    
    Args:
        file: Path to PDF file (string) or file-like object
        
    Returns:
        Combined text from all pages
    """
    try:
        # Handle string path or file object
        if isinstance(file, str):
            with open(file, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                text = ""
                
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                return text.strip()
        else:
            # File-like object
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting PDF: {str(e)}")

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Alias for extract_text() - backward compatibility
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Extracted text as string
    """
    return extract_text(pdf_path)

def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    """
    Split text into chunks of approximately chunk_size words
    
    Args:
        text: Input text
        chunk_size: Approximate number of words per chunk
        
    Returns:
        List of text chunks
    """
    # Clean text
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Split into words
    words = text.split()
    
    # Create chunks
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk:  # Only add non-empty chunks
            chunks.append(chunk)
    
    return chunks

def process_pdf(pdf_path: str, chunk_size: int = 500) -> List[str]:
    """
    Complete pipeline: Extract text from PDF and chunk it
    
    Args:
        pdf_path: Path to PDF file
        chunk_size: Words per chunk
        
    Returns:
        List of text chunks
    """
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text, chunk_size)
    return chunks
