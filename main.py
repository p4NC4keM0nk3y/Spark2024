from anthropic import Anthropic
from PIL import Image
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pathlib import Path
import base64
import json
from anthropic import Anthropic
from dotenv import load_dotenv
import os
api_key="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"

client = Anthropic(api_key=api_key)



image_path = "/Users/micahbragg/Desktop/cs shit/spark-2024/Helloworld.png"

with Image.open(image_path) as image:
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    encoded_string = base64.b64encode(buffered.getvalue()).decode()

message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": 'image/png',
                        "data": encoded_string,
                    },
                },
                {
                    "type": "text",
                    "text": "Describe this image."
                }
            ],
        }
    ],
)

extracted_text = message.model_dump_json()["messages"][0]["content"][0]["text"]

pdf_path = "/Users/micahbragg/Desktop/cs shit/spark-2024/TestPDF"
c = canvas.Canvas(pdf_path, pagesize=letter)
c.drawString(100, 750, extracted_text)
c.showPage()
c.save()

print(f"Extracted text has been written {pdf_path}")