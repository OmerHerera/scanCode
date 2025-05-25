from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pyzbar.pyzbar import decode
from PIL import Image
import io
import httpx
import os
port = int(os.environ.get("PORT", 8000))
# when running uvicorn programmatically, pass port=port


app = FastAPI()

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
