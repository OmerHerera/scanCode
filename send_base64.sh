#!/bin/bash

# Usage: ./send_base64.sh path/to/image.jpg

if [ -z "$1" ]; then
  echo "Please provide the path to an image file."
  exit 1
fi

IMAGE_PATH="$1"

# Extract and normalize the file extension (lowercase, jpeg -> jpg)
EXT="${IMAGE_PATH##*.}"
EXT="$(echo "$EXT" | tr '[:upper:]' '[:lower:]')"

if [ "$EXT" = "jpeg" ]; then
  EXT="jpg"
fi

# Encode the image to base64 without line breaks and prepend data URL prefix
BASE64_DATA="data:image/$EXT;base64,$(base64 -i "$IMAGE_PATH" -b 0)"

# Create a temp file for JSON payload
TMP_JSON=$(mktemp)
echo "{\"image_base64\":\"$BASE64_DATA\"}" > "$TMP_JSON"

# Send POST request to the /scan/base64 endpoint
curl -X POST "http://127.0.0.1:8000/scan/base64" \
  -H "Content-Type: application/json" \
  -d @"$TMP_JSON"

# Clean up temp file
rm "$TMP_JSON"
