# PDF Extractor API

A FastAPI service for extracting text, tables, and metadata from PDF files and images using OCR.

## Features

- Extract text and tables from PDF documents
- Extract text from images (JPG, PNG, HEIC, HEIF) using OCR
- Store extracted data in SQLite database
- RESTful API with automatic documentation
- Extract structured data and metadata

## Installation

### Prerequisites

- Python 3.8+
- Tesseract OCR

Install Tesseract:
- macOS: `brew install tesseract`
- Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
- Windows: Download from [Tesseract releases](https://github.com/UB-Mannheim/tesseract/wiki)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Shriiii01/pdf_extractor1.git
cd pdf_extractor1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## Usage

### Upload PDF or Image

```bash
curl -X POST "http://localhost:8000/extract" -F "file=@document.pdf"
```

### List All Records

```bash
curl http://localhost:8000/extracted
```

### Get Specific Record

```bash
curl http://localhost:8000/extracted/1
```

### Delete Record

```bash
curl -X DELETE http://localhost:8000/extracted/1
```

## API Endpoints

- `GET /` - API information
- `POST /extract` - Upload and extract PDF/image
- `GET /extracted` - List all records (supports `skip` and `limit` params)
- `GET /extracted/{id}` - Get record by ID (supports `include_text` param)
- `DELETE /extracted/{id}` - Delete record by ID

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Example Response

```json
{
  "message": "PDF extracted successfully",
  "id": 1,
  "filename": "document.pdf",
  "upload_date": "2026-01-02T20:53:05",
  "extracted_data": {
    "pages": 5,
    "tables_count": 2,
    "text_length": 5000,
    "structured_data": {
      "key_value_pairs": {},
      "tables_count": 2,
      "text_length": 5000
    },
    "metadata": {
      "title": "Document Title",
      "author": "Author Name"
    }
  }
}
```

## Database

The application uses SQLite by default (`pdf_extractor.db`).

**Table: `extracted_data`**
- `id` - Primary key
- `filename` - Original filename
- `upload_date` - Upload timestamp
- `raw_text` - Full extracted text
- `extracted_data` - Structured data (JSON)
- `pdf_metadata` - PDF/image metadata (JSON)

### Using PostgreSQL

Set the `DATABASE_URL` environment variable:
```bash
export DATABASE_URL="postgresql://user:password@localhost/dbname"
```

## Supported File Types

**PDF:** `.pdf`

**Images (with OCR):** `.jpg`, `.jpeg`, `.png`, `.heic`, `.heif`, `.gif`, `.bmp`, `.tiff`

## Customization

Edit `pdf_extractor.py` to customize data extraction logic:
```python
def extract_structured_data(text: str, tables: List[Dict]) -> Dict[str, Any]:
    # Add your custom extraction logic
    return structured
```

## Project Structure

```
pdf_extractor1/
├── main.py              # FastAPI application
├── pdf_extractor.py     # Extraction logic
├── database.py          # Database models
├── requirements.txt     # Dependencies
└── pdf_extractor.db     # SQLite database
```

## Troubleshooting

**Tesseract not found:**
- Install Tesseract using the instructions above
- Verify: `tesseract --version`

**Import errors:**
```bash
pip install --upgrade -r requirements.txt
```

## License

MIT License

## Contributing

Contributions welcome! Please open an issue or submit a pull request.
