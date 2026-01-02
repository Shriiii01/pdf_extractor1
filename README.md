# 📄 PDF Extractor API

A powerful, production-ready FastAPI service for extracting text, tables, and metadata from PDF files and images. Supports both native PDF text extraction and OCR (Optical Character Recognition) for image-based documents.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

- 🔍 **PDF Text Extraction** - Extract text and tables from PDF documents using `pdfplumber`
- 📸 **OCR Support** - Extract text from images (JPG, PNG, HEIC, HEIF) using Tesseract OCR
- 🗄️ **Database Storage** - Automatically store extracted data in SQLite (PostgreSQL compatible)
- 🔄 **RESTful API** - Clean REST API with automatic OpenAPI documentation
- 📊 **Structured Data** - Extract key-value pairs and structured information
- 🎯 **Metadata Extraction** - Capture PDF metadata (author, title, creation date, etc.)
- 🚀 **Fast & Scalable** - Built on FastAPI for high performance
- 📝 **Interactive Docs** - Built-in Swagger UI and ReDoc documentation

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Tesseract OCR (for image extraction support)

#### Install Tesseract OCR

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:**
Download from [GitHub Tesseract releases](https://github.com/UB-Mannheim/tesseract/wiki)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Shriiii01/pdf_extractor1.git
cd pdf_extractor1
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Start the server:**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## 📖 Usage

### Upload and Extract PDF/Image

```bash
curl -X POST "http://localhost:8000/extract" \
  -F "file=@document.pdf"
```

### Upload Image File (with OCR)

```bash
curl -X POST "http://localhost:8000/extract" \
  -F "file=@image.jpg"
```

### List All Extracted Records

```bash
curl http://localhost:8000/extracted
```

### Get Specific Record

```bash
curl http://localhost:8000/extracted/1
```

### Get Record with Full Text

```bash
curl "http://localhost:8000/extracted/1?include_text=true"
```

### Delete Record

```bash
curl -X DELETE http://localhost:8000/extracted/1
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information and available endpoints |
| `POST` | `/extract` | Upload PDF/image and extract data |
| `GET` | `/extracted` | List all extracted records (supports `skip` and `limit` query params) |
| `GET` | `/extracted/{id}` | Get specific record by ID (supports `include_text` query param) |
| `DELETE` | `/extracted/{id}` | Delete a record by ID |

## 📊 Example Response

### Successful Extraction

```json
{
  "message": "PDF extracted successfully",
  "id": 1,
  "filename": "document.pdf",
  "upload_date": "2026-01-02T20:53:05.249198",
  "extracted_data": {
    "pages": 5,
    "tables_count": 2,
    "text_length": 5000,
    "structured_data": {
      "key_value_pairs": {
        "Name": "John Doe",
        "Email": "john@example.com"
      },
      "tables_count": 2,
      "text_length": 5000,
      "lines": ["Line 1", "Line 2", "..."]
    },
    "metadata": {
      "title": "Document Title",
      "author": "Author Name",
      "creation_date": "2024-01-01"
    }
  }
}
```

### List Records Response

```json
{
  "total": 10,
  "records": [
    {
      "id": 1,
      "filename": "document.pdf",
      "upload_date": "2026-01-02T20:53:05.249198",
      "extracted_data": {...},
      "metadata": {...}
    }
  ]
}
```

## 🗄️ Database

### Default Configuration

The application uses **SQLite** by default, creating a database file `pdf_extractor.db` in the project directory.

### Database Schema

**Table: `extracted_data`**

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key (auto-increment) |
| `filename` | String | Original filename |
| `upload_date` | DateTime | Timestamp of upload |
| `raw_text` | Text | Full extracted text content |
| `extracted_data` | JSON | Structured extracted data |
| `pdf_metadata` | JSON | PDF/image metadata |

### Using PostgreSQL

To use PostgreSQL instead of SQLite, set the `DATABASE_URL` environment variable:

```bash
export DATABASE_URL="postgresql://user:password@localhost/dbname"
python main.py
```

### Query Database Directly

```bash
sqlite3 pdf_extractor.db "SELECT * FROM extracted_data;"
```

## 📁 Project Structure

```
pdf_extractor1/
├── main.py              # FastAPI application and endpoints
├── pdf_extractor.py     # PDF/image extraction logic
├── database.py          # Database models and configuration
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .gitignore          # Git ignore rules
└── pdf_extractor.db    # SQLite database (created automatically)
```

## 🛠️ Customization

### Customize Data Extraction

Edit `pdf_extractor.py` to customize how structured data is extracted:

```python
def extract_structured_data(text: str, tables: List[Dict]) -> Dict[str, Any]:
    # Add your custom extraction logic here
    structured = {
        "custom_field": "custom_value",
        # ... your custom fields
    }
    return structured
```

### Supported File Types

**PDF Files:**
- `.pdf` - Standard PDF documents

**Image Files (with OCR):**
- `.jpg`, `.jpeg` - JPEG images
- `.png` - PNG images
- `.heic`, `.heif` - HEIC/HEIF images (iPhone photos)
- `.gif` - GIF images
- `.bmp` - BMP images
- `.tiff` - TIFF images

## 📚 API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Both provide interactive API documentation where you can test endpoints directly.

## 🔧 Configuration

### Environment Variables

- `DATABASE_URL` - Database connection string (default: SQLite)
- `PORT` - Server port (default: 8000)

### Server Configuration

Edit `main.py` to change server settings:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 🧪 Testing

### Test PDF Extraction

```bash
python -c "from pdf_extractor import extract_pdf_data; print(extract_pdf_data('test.pdf'))"
```

### Test Image Extraction

```bash
python -c "from pdf_extractor import extract_pdf_data; print(extract_pdf_data('test.jpg'))"
```

## 🐛 Troubleshooting

### Tesseract Not Found

If you get `Tesseract OCR not found`:
- Install Tesseract using the instructions above
- Verify installation: `tesseract --version`

### Import Errors

If you encounter import errors:
```bash
pip install --upgrade -r requirements.txt
```

### Database Locked

If you see database locked errors:
- Ensure only one instance of the server is running
- Check for other processes accessing the database

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Support

For issues, questions, or contributions, please open an issue on [GitHub](https://github.com/Shriiii01/pdf_extractor1/issues).

## 🎯 Use Cases

- **Document Processing** - Automatically extract data from invoices, receipts, forms
- **Content Management** - Index and search PDF content
- **Data Migration** - Extract structured data from legacy documents
- **OCR Pipeline** - Convert scanned documents to searchable text
- **Form Processing** - Extract form fields and values automatically

---

Made with ❤️ using FastAPI and Python

