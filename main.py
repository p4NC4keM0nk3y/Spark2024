from anthropic import Anthropic
from PIL import Image
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pathlib import Path
import base64


client = Anthropic()
image_path = "/Users/micahbragg/Desktop/cs shit/spark-2024/Helloworld.png"
with Image.oepn(image_path) as image: 
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    encoded_string = base64.b64encode(buffered.getvalue()).decode()
response = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Hello!",
                },
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": encoded_string,
                    },
                },
            ],
        },
    ],
    model="claude-3-opus-2024-0229",
)
extracted_text = response.model_dump_json(["messages"][0]["content"][0]["text"])
pdf_path = "/Users/micahbragg/Desktop/cs shit/spark-2024/TestPDF"
c = canvas.Canvas(pdf_path, pagesize=letter)
c.drawString(100,750,extracted_text)
c.showPage()
c.save()
print(f"Extracted text has been written {pdf_path}")
##print(response.model_dump_json(indent=2))