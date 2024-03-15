from anthropic import Anthropic
from PIL import Image
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph
from pathlib import Path
import base64
import json
from anthropic import Anthropic
from dotenv import load_dotenv
import os
load_dotenv(override=True)

api_key=os.getenv("ANTHROPIC_API_KEY")

client = Anthropic(api_key=api_key)
image_path = "/Users/micahbragg/Desktop/cs shit/spark-2024/Helloworld2.png"

with Image.open(image_path) as image:
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    encoded_string = base64.b64encode(buffered.getvalue()).decode()


MODEL_NAME = "claude-3-opus-20240229"

with open(image_path, "rb") as image_file:
    binary_data = image_file.read()
    base_64_encoded_data = base64.b64encode(binary_data)
    base64_string = base_64_encoded_data.decode('utf-8')


message_list = [
    {
        "role": 'user',
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": base64_string}},
            {"type": "text", "text": "Elaborate on the text in the image in a bullet point list format.Emphasize the important points within the text inside the image.At each bu"}
        ]
    }
]

response = client.messages.create(
    model=MODEL_NAME,
    max_tokens=2048,
    messages=message_list
)
print(response.content[0].text)

#extracted_text = message.model_dump_json()["messages"][0]["content"][0]["text"]

pdf_path = "/Users/micahbragg/Desktop/cs shit/spark-2024/TestPDF.pdf"
c = canvas.Canvas(pdf_path, pagesize=letter)

styles = getSampleStyleSheet()
normal_style = styles['Normal']
normal_style.fontSize = 12
normal_style.leading = 14

paragraph = Paragraph(response.content[0].text, normal_style)
paragraph.wrapOn(c, 6.5*inch, 9*inch)  # Adjust the width and height as needed
paragraph.drawOn(c, 1*inch, 8*inch)  # Adjust the position as needed

c.showPage()
c.save()
print(f"Extracted text has been written {pdf_path}")