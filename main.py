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
from dotenv import load_dotenv
import os
from flask import Flask, request, send_file

load_dotenv(override=True)
api_key = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def generate_pdf():
    if request.method == 'POST':
        image_file = request.files['image']
        
        buffered = BytesIO()
        image = Image.open(image_file)
        image.save(buffered, format="PNG")
        encoded_string = base64.b64encode(buffered.getvalue()).decode()
        
        MODEL_NAME = "claude-3-opus-20240229"
        
        binary_data = image_file.read()
        base_64_encoded_data = base64.b64encode(binary_data)
        base64_string = base_64_encoded_data.decode('utf-8')
        
        message_list = [
            {
                "role": 'user',
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": base64_string}},
                    {"type": "text", "text": "Elaborate on the text in the image in a bullet point list format. Emphasize the important points within the text inside the image. At each bu"}
                ]
            }
        ]
        
        resp