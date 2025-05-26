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

- Scan barcode from image path:

```bash
GET /scan/upload
```

- Example:

```bash
curl -X POST "http://127.0.0.1:8000/scan/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/image.jpg"

```

- Scan barcode from base64:

```bash
POST /scan/base64
```

#### Prepare your base64 image string

- You can convert your image to base64 with a command like:

```bash
base64 -i path/to/image.jpg
```

- Copy the output (it will be a long string).

#### Make the curl request

```bash
curl -X POST "http://127.0.0.1:8000/scan/base64" \
  -H "Content-Type: application/json" \
  -d '{"image_base64": "<BASE64_ENCODED_IMAGE>"}'

```

- Example with a real-ish value:

```bash
curl -X POST "http://127.0.0.1:8000/scan/base64" \
  -H "Content-Type: application/json" \
  -d '{"image_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."}'

```

- Or Use the craft a script to generate this payload easily

```bash
chmod +x send_base64.sh
./send_base64.sh path/to/your/image.jpg

```

### 🛠 Barcode Scanning – macOS Setup Notes

This project uses pyzbar for barcode scanning, which depends on the native zbar shared library.
On macOS, even if zbar is installed, Python may not automatically locate the required .dylib file.

### 🔧 Problem

You may see this error when running the app locally:

```vbnet
ImportError: Unable to find zbar shared library
```

#### ✅ Solution

- Install zbar using Homebrew (if not already installed):

```bash
brew install zbar
```

- Add the `libzbar.dylib` path to your environment so Python can find it:

```bash
echo 'export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH' >> ~/.zshrc
source ~/.zshrc
```

- Restart your terminal, then run the app:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### 🧠 Notes

On Intel Macs, use /usr/local/lib instead of /opt/homebrew/lib:

```bash
echo 'export DYLD_LIBRARY_PATH=/usr/local/lib:$DYLD_LIBRARY_PATH' >> ~/.zshrc
```
