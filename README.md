# PDF Extractor API

A FastAPI-based service for extracting data from PDF files and storing it in a database.

## Features

- Upload PDF files via REST API
- Extract text, tables, and metadata from PDFs
- Store extracted data in SQLite database (easily configurable for PostgreSQL)
- Retrieve and list extracted records
- Customizable data extraction based on PDF structure

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the API server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

2. Upload a PDF:
```bash
curl -X POST "http://localhost:8000/extract" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_file.pdf"
```

3. View API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

- `POST /extract` - Upload and extract data from a PDF
- `GET /extracted` - List all extracted records
- `GET /extracted/{id}` - Get a specific record by ID
- `DELETE /extracted/{id}` - Delete a record by ID

## Customization

The PDF extraction logic can be customized in `pdf_extractor.py`. The `extract_structured_data()` function is designed to be modified based on your specific PDF structure.

## Database

By default, the application uses SQLite (`pdf_extractor.db`). To use PostgreSQL, set the `DATABASE_URL` environment variable:

```bash
export DATABASE_URL="postgresql://user:password@localhost/dbname"
```

## Example Response

```json
{
  "message": "PDF extracted successfully",
  "id": 1,
  "filename": "document.pdf",
  "upload_date": "2024-01-01T12:00:00",
  "extracted_data": {
    "pages": 5,
    "tables_count": 2,
    "text_length": 5000,
    "structured_data": {
      "key_value_pairs": {...},
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

