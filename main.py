import camelot
import cv2
from fastapi import FastAPI, File, HTTPException, UploadFile
import numpy as np
import os
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
import io
import tempfile

app = FastAPI()


# Preprocessing function to improve OCR accuracy for both images and PDFs
def preprocess_image_for_ocr(image):
    """
    Preprocesses an image to enhance its quality for OCR.
    It converts the image to grayscale, applies Gaussian blurring,
    and then uses adaptive thresholding to enhance text visibility.

    Args:
        image (PIL.Image.Image): The input image to preprocess.

    Returns:
        PIL.Image.Image: The preprocessed image ready for OCR.
    """
    # Convert the image to a NumPy array and then to grayscale
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise and improve thresholding
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply adaptive thresholding to make text stand out
    processed_img = cv2.adaptiveThreshold(blurred, 255,
                                          cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY,
                                          11, 2)

    # Convert the NumPy array back to a PIL image
    return Image.fromarray(processed_img)


@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    """
    Endpoint to perform OCR on uploaded image or PDF files.

    Accepts files of types: PNG, JPG, PDF. For PDFs, it also attempts table
     detection. Extracts text and returns it as a JSON response. In the case
     of PDFs, also extracts table data using Camelot.

    Args:
        file (UploadFile): The uploaded file containing an image or PDF.

    Returns:
        dict: A JSON response containing the extracted text and table data.
    """
    # Check if the uploaded file is of an allowed content type
    if file.content_type.lower() not in ["image/png",
                                         "image/jpg",
                                         "application/pdf"]:
        raise HTTPException(status_code=400,
                            detail="File format not supported.")

    try:
        # Read the uploaded file's content into memory
        file_data = await file.read()

        extracted_text = ""
        table_data = []

        if file.content_type == "application/pdf":
            # Convert PDF to image
            images = convert_from_bytes(file_data)

            # Write the PDF to a temporary file
            tmp_pdf_path = ""
            try:
                with tempfile.NamedTemporaryFile(suffix=".pdf",
                                                 delete=False) as tmp_pdf:
                    tmp_pdf.write(file_data)
                    tmp_pdf_path = tmp_pdf.name

                # Use Camelot to detect tables in the PDF (stream or lattice )
                tables = camelot.read_pdf(tmp_pdf_path, pages="1-end",
                                          flavor='stream')
                if not tables:
                    tables = camelot.read_pdf(tmp_pdf_path, pages="1-end",
                                              flavor='lattice')

                # Extract tables into structured data
                for table in tables:
                    table_data.append(table.df.to_dict())
            finally:
                if os.path.exists(tmp_pdf_path):
                    os.remove(tmp_pdf_path)
            # Extract text from each image page
            for image in images:
                processed_image = preprocess_image_for_ocr(image)
                extracted_text += pytesseract.image_to_string(processed_image)

        else:
            # Convert bytes in to PIL image
            image = Image.open(io.BytesIO(file_data))

            # Preprocess the image for better OCR accuracy
            processed_image = preprocess_image_for_ocr(image)

            # Perform OCR on the processed image
            extracted_text = pytesseract.image_to_string(processed_image)

        # Return extracted text and tables as json (if any)
        return {
            "extracted_text": extracted_text,
            "tables": table_data
        }

    except ValueError as ve:
        raise HTTPException(status_code=400,
                            detail=f"Value error: {str(ve)}")
    except IOError as ioe:
        raise HTTPException(status_code=500,
                            detail=f"IO error: {str(ioe)}")
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Error processing file: {str(e)}")
