from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db, init_db, ExtractedData
from pdf_extractor import extract_pdf_data
import os
import tempfile
from typing import Optional
from datetime import datetime

app = FastAPI(title="PDF Extractor API", version="1.0.0")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()


@app.get("/")
async def root():
    return {
        "message": "PDF Extractor API",
        "endpoints": {
            "upload": "/extract",
            "list": "/extracted",
            "get_by_id": "/extracted/{id}"
        }
    }


@app.post("/extract")
async def extract_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a PDF file and extract all data from it.
    The extracted data will be saved to the database.
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        try:
            # Write uploaded file to temporary file
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
            
            # Extract data from PDF
            extracted_data = extract_pdf_data(tmp_file_path)
            
            # Save to database
            db_record = ExtractedData(
                filename=file.filename,
                raw_text=extracted_data["raw_text"],
                extracted_data=extracted_data["structured_data"],
                pdf_metadata=extracted_data["metadata"]
            )
            db.add(db_record)
            db.commit()
            db.refresh(db_record)
            
            return {
                "message": "PDF extracted successfully",
                "id": db_record.id,
                "filename": db_record.filename,
                "upload_date": db_record.upload_date.isoformat(),
                "extracted_data": {
                    "pages": extracted_data["pages"],
                    "tables_count": len(extracted_data["tables"]),
                    "text_length": len(extracted_data["raw_text"]),
                    "structured_data": extracted_data["structured_data"],
                    "metadata": extracted_data["metadata"]
                }
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
        
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)


@app.get("/extracted")
async def list_extracted(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all extracted PDF records.
    """
    records = db.query(ExtractedData).offset(skip).limit(limit).all()
    
    return {
        "total": len(records),
        "records": [
            {
                "id": record.id,
                "filename": record.filename,
                "upload_date": record.upload_date.isoformat(),
                "extracted_data": record.extracted_data,
                "metadata": record.pdf_metadata
            }
            for record in records
        ]
    }


@app.get("/extracted/{record_id}")
async def get_extracted(
    record_id: int,
    db: Session = Depends(get_db),
    include_text: bool = False
):
    """
    Get a specific extracted PDF record by ID.
    Set include_text=true to include the full raw text.
    """
    record = db.query(ExtractedData).filter(ExtractedData.id == record_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    response = {
        "id": record.id,
        "filename": record.filename,
        "upload_date": record.upload_date.isoformat(),
        "extracted_data": record.extracted_data,
        "metadata": record.pdf_metadata
    }
    
    if include_text:
        response["raw_text"] = record.raw_text
    
    return response


@app.delete("/extracted/{record_id}")
async def delete_extracted(
    record_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a specific extracted PDF record by ID.
    """
    record = db.query(ExtractedData).filter(ExtractedData.id == record_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    db.delete(record)
    db.commit()
    
    return {"message": "Record deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

