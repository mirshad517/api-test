from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import mysql.connector
from mysql.connector import Error
from pathlib import Path
import os

app = FastAPI(
    title="NEAR BY TURF - sparteck",
    description='Add review image api',
)

# Database configuration
# ... (unchanged)

# Uploads directory
uploads_dir = Path("uploads")
uploads_dir.mkdir(exist_ok=True)

# Initialize database connection
# ... (unchanged)

# Expose the "uploads" directory
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")


@app.post("/upload-file/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        # Save the uploaded file
        file_path = uploads_dir / file.filename
        with file_path.open("wb") as buffer:
            buffer.write(file.file.read())

        # Insert file information into the database
        # ... (unchanged)

        return JSONResponse(content={"message": "File uploaded successfully", "file_link": f"https://api-test-mzxz.onrender.com/uploads/{file.filename}"})

    except Error as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
