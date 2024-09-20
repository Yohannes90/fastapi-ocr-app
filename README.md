# OCR Service with FastAPI

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Built With](#built-with)
- [Running the Code](#running-the-code)
- [Usage](#usage)

## Overview
This project provides a backend Optical Character Recognition (OCR) service built using FastAPI. The service extracts text from PDFs and images (such as PNG and JPG) and can detect and extract table data from PDFs, returning both the extracted text and structured tables in JSON format. The service can also be containerized using Docker, making it easy to deploy across different environments.

## Features
- **OCR Text Extraction**: Extract text from images and PDF files.
- **Table Detection**: Detect and extract tabular data from PDF documents.
- **REST API**: Provides a FastAPI endpoint to handle file uploads and return the OCR results.
- **Docker Support**: The service can be containerized using Docker for easier setup and deployment.

## Requirements
- **Python 3.8+**: The code requires Python 3.8 or later versions.
- **pip**: Python's package installer.
- **Tesseract-OCR**: The Tesseract-OCR tool, used for OCR functionality.
- **Poppler**: Required for PDF to image conversion (for PDFs).
- **Docker**: (Optional) For containerizing the application.

### System Dependencies:
To run the project without Docker, the following system dependencies are required:
- **Tesseract-OCR**: Install via `apt` (for Linux), `brew` (for macOS), or from the [official website](https://github.com/tesseract-ocr/tesseract).
- **Poppler**: Needed to convert PDFs to images, install using `apt` (Linux) or `brew install poppler` (macOS).

## Built With
- **[FastAPI](https://fastapi.tiangolo.com/)** - A modern, fast (high-performance) web framework for building APIs with Python.
- **[pytesseract](https://pypi.org/project/pytesseract/)** - Python wrapper for Google's Tesseract-OCR Engine.
- **[Camelot](https://pypi.org/project/camelot-py/)** - Library to extract tables from PDFs.
- **[Uvicorn](https://www.uvicorn.org/)** - A fast ASGI server for FastAPI.

## Running the Code

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/fastapi-ocr-app.git
cd fastapi-ocr-app
```

### Step 2: Set Up Virtual Environment
Create and activate a virtual environment using venv:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment (on MacOS/Linux)
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### Step 2: Install Dependencies
Ensure you have Python and pip installed. Then, install the project dependencies:

```bash
pip install -r requirements.txt
```

### Step 3: Install System Dependencies
If you haven't already, install `Tesseract` and `Poppler` for handling image and PDF processing:
- **Linux**:
  ```bash
  sudo apt-get install tesseract-ocr poppler-utils
  ```
- **macOS**:
  ```bash
  brew install tesseract poppler
  ```

### Step 4: Run the Application
Start the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload
```

The application will be accessible at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Deactivating the Virtual Environment
Once you are done, deactivate the virtual environment using:
```bash
deactivate
```

## Usage
### API Endpoint: `POST /ocr`

- **Accepts**: Image (`.png`, `.jpg`) or PDF (`.pdf`) files via `multipart/form-data`.
- **Returns**: Extracted text and, if present, structured table data in JSON format.

#### Example Request (using `curl`):
```bash
curl -X POST "http://127.0.0.1:8000/ocr" -F "file=@test_image.png"
```

#### Sample Response:
```json
{
  "extracted_text": "Sample extracted text from the image...",
  "tables": [
    {
      "0": {"0": "Header1", "1": "Header2"},
      "1": {"0": "Row1Column1", "1": "Row1Column2"}
    }
  ]
}
```
