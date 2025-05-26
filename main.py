from fastapi import FastAPI, Query, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pyzbar.pyzbar import decode
from PIL import Image
import io
import httpx
import os
import base64
from pydantic import BaseModel

port = int(os.environ.get("PORT", 8000))

app = FastAPI()

# Add this CORS middleware setup right after creating the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://byegluten.vercel.app", "https://lovable.dev"],  # update with your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/scan")
async def scan_barcode_from_url(image_url: str = Query(..., description="URL of the image to scan")):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(image_url)
            response.raise_for_status()
            image_bytes = response.content

        img = Image.open(io.BytesIO(image_bytes))
        barcodes = decode(img)

        if not barcodes:
            return JSONResponse(status_code=404, content={"error": "No barcode found"})

        results = [barcode.data.decode("utf-8") for barcode in barcodes]
        return {"barcodes": results}

    except httpx.RequestError as e:
        return JSONResponse(status_code=400, content={"error": f"Failed to fetch image: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/scan/upload")
async def scan_barcode_from_upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents))
        barcodes = decode(img)

        if not barcodes:
            return JSONResponse(status_code=404, content={"error": "No barcode found"})

        results = [barcode.data.decode("utf-8") for barcode in barcodes]
        return {"barcodes": results}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

class ImageBase64Request(BaseModel):
    image_base64: str

@app.post("/scan/base64")
async def scan_barcode_from_base64(data: ImageBase64Request):
    try:
        # Remove data URL prefix if present (e.g. "data:image/png;base64,")
        if "," in data.image_base64:
            _, encoded = data.image_base64.split(",", 1)
        else:
            encoded = data.image_base64

        image_bytes = io.BytesIO(base64.b64decode(encoded))
        img = Image.open(image_bytes)
        barcodes = decode(img)

        if not barcodes:
            return JSONResponse(status_code=404, content={"error": "No barcode found"})

        results = [barcode.data.decode("utf-8") for barcode in barcodes]
        return {"barcodes": results}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Optional: if running programmatically, pass port=port
