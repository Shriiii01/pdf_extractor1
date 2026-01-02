import pdfplumber
from typing import Dict, Any, List
import json


def extract_pdf_data(pdf_path: str) -> Dict[str, Any]:
    """
    Extract all data from a PDF file.
    
    Returns a dictionary containing:
    - raw_text: All text content from the PDF
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

