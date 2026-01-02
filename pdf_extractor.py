import pdfplumber
from typing import Dict, Any, List
import json
import os

# Try to register HEIF opener if available
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass


def extract_pdf_data(pdf_path: str) -> Dict[str, Any]:
    """
    Extract all data from a PDF file or image file (using OCR).
    
    Returns a dictionary containing:
    - raw_text: All text content from the PDF/image
    - tables: List of tables found in the PDF
    - metadata: PDF metadata (author, title, etc.)
    - pages: Number of pages
    - structured_data: Extracted structured data (customize based on your PDF structure)
    """
    extracted_data = {
        "raw_text": "",
        "tables": [],
        "metadata": {},
        "pages": 0,
        "structured_data": {}
    }
    
    # Check if file is an image
    file_type = _detect_file_type(pdf_path)
    
    if file_type == "image":
        return _extract_from_image(pdf_path)
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Extract metadata
            extracted_data["metadata"] = {
                "title": pdf.metadata.get("Title", ""),
                "author": pdf.metadata.get("Author", ""),
                "subject": pdf.metadata.get("Subject", ""),
                "creator": pdf.metadata.get("Creator", ""),
                "producer": pdf.metadata.get("Producer", ""),
                "creation_date": str(pdf.metadata.get("CreationDate", "")),
                "modification_date": str(pdf.metadata.get("ModDate", ""))
            }
            
            extracted_data["pages"] = len(pdf.pages)
            
            # Extract text from all pages
            all_text = []
            all_tables = []
            
            for page_num, page in enumerate(pdf.pages, start=1):
                # Extract text
                page_text = page.extract_text()
                if page_text:
                    all_text.append(f"--- Page {page_num} ---\n{page_text}")
                
                # Extract tables
                tables = page.extract_tables()
                if tables:
                    for table_num, table in enumerate(tables):
                        all_tables.append({
                            "page": page_num,
                            "table_number": table_num + 1,
                            "data": table
                        })
            
            extracted_data["raw_text"] = "\n\n".join(all_text)
            extracted_data["tables"] = all_tables
            
            # Extract structured data (customize this based on your PDF structure)
            extracted_data["structured_data"] = extract_structured_data(
                extracted_data["raw_text"],
                extracted_data["tables"]
            )
            
    except Exception as e:
        raise Exception(f"Error extracting PDF data: {str(e)}")
    
    return extracted_data


def extract_structured_data(text: str, tables: List[Dict]) -> Dict[str, Any]:
    """
    Extract structured data from text and tables.
    Customize this function based on your specific PDF structure.
    
    This is a template - modify it to match your PDF format.
    """
    structured = {
        "key_value_pairs": {},
        "tables_count": len(tables),
        "text_length": len(text),
        "lines": text.split("\n")[:50]  # First 50 lines as sample
    }
    
    # Example: Extract key-value pairs (customize based on your PDF)
    # Look for patterns like "Key: Value" or "Key - Value"
    lines = text.split("\n")
    for line in lines:
        if ":" in line:
            parts = line.split(":", 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                if key and value:
                    structured["key_value_pairs"][key] = value
    
    return structured


def _detect_file_type(file_path: str) -> str:
    """Detect if file is PDF or image"""
    # Check file extension
    ext = os.path.splitext(file_path)[1].lower()
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.heic', '.heif']
    if ext in image_extensions:
        return "image"
    
    # Try to read first bytes to check if it's actually a PDF
    try:
        with open(file_path, 'rb') as f:
            header = f.read(4)
            # PDF files start with %PDF
            if header[:4] == b'%PDF':
                return "pdf"
            # HEIC files start with specific bytes
            if header[:4] == b'\x00\x00\x00\x24' or header[:8] == b'\x00\x00\x00\x20ftyp':
                return "image"
    except:
        pass
    
    return "pdf"


def _extract_from_image(image_path: str) -> Dict[str, Any]:
    """Extract text from image using OCR"""
    extracted_data = {
        "raw_text": "",
        "tables": [],
        "metadata": {
            "file_type": "image",
            "filename": os.path.basename(image_path)
        },
        "pages": 1,
        "structured_data": {}
    }
    
    try:
        import subprocess
        import tempfile
        
        # Use subprocess to call tesseract directly (avoids pandas dependency)
        # First, convert HEIC to a format tesseract can handle if needed
        from PIL import Image
        
        # Open and convert image if needed
        img = Image.open(image_path)
        
        # Convert to RGB if necessary (tesseract works better with RGB)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_img:
            img.save(tmp_img.name, 'PNG')
            tmp_img_path = tmp_img.name
        
        try:
            # Call tesseract directly via subprocess
            result = subprocess.run(
                ['tesseract', tmp_img_path, 'stdout', '-l', 'eng'],
                capture_output=True,
                text=True,
                check=True
            )
            extracted_data["raw_text"] = result.stdout
            
        finally:
            # Clean up temp file
            if os.path.exists(tmp_img_path):
                os.unlink(tmp_img_path)
        
        # Extract structured data
        extracted_data["structured_data"] = extract_structured_data(
            extracted_data["raw_text"],
            extracted_data["tables"]
        )
        
    except FileNotFoundError:
        raise Exception("Tesseract OCR not found. Please install tesseract: brew install tesseract")
    except ImportError as e:
        raise Exception(f"PIL/Pillow not available. Please install Pillow: {str(e)}")
    except subprocess.CalledProcessError as e:
        raise Exception(f"Tesseract OCR error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error extracting from image: {str(e)}")
    
    return extracted_data

