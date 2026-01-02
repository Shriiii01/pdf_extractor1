# PDF Extractor API

FastAPI service for extracting text from PDF files and images using OCR.

## Requirements

- Python 3.8+
- Tesseract OCR

Install Tesseract:
- macOS: `brew install tesseract`
- Ubuntu: `sudo apt-get install tesseract-ocr`

## Installation

1. Fork or clone the repository:
```bash
git clone https://github.com/Shriiii01/pdf_extractor1.git
cd pdf_extractor1
```

2. Install Python requirements:
```bash
pip install -r requirements.txt
```

3. Start the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## Test the API

Upload a PDF or image file:
```bash
curl -X POST "http://localhost:8000/extract" -F "file=@your_file.pdf"
```

View API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

- `POST /extract` - Upload and extract PDF/image
- `GET /extracted` - List all records
- `GET /extracted/{id}` - Get specific record
- `DELETE /extracted/{id}` - Delete record

## Database

Uses SQLite by default (`pdf_extractor.db`). To use PostgreSQL, set:
```bash
export DATABASE_URL="postgresql://user:password@localhost/dbname"
```
