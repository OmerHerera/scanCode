# scanCode

A simple Python FastAPI service that extracts barcode(s) from an image URL.

## Requirements

- Python 3.11 (or compatible)

- Homebrew (macOS) for system dependencies

- zbar installed via Homebrew for barcode decoding

## Setup Instructions

- First time after cloning the project

- Install system dependency zbar:

```bash
brew install zbar
```

### Create and activate a Python virtual environment

```bash
python3.11 -m venv venv
source venv/bin/activate
```

Install Python dependencies:

```bash
install --upgrade pip
pip install -r requirements.txt
```

### Start the server

```bash
uvicorn main:app
```

### For subsequent runs (after dependencies are installed)

- Activate the virtual environment:

```bash
source venv/bin/activate
```

### Start the server

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### API Usage

- Scan barcode from image URL:

```bash
GET /scan?image_url=<URL_OF_IMAGE>
```

- Example:

```bash
curl "http://127.0.0.1:8000/scan?image_url=https://example.com/barcode.png"
```

- Example

```bash
curl "http://127.0.0.1:8000/scan?image_url=https://example.com/your-image.png"
```
