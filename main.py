from anthropic import Anthropic
from PIL import Image
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph
import base64
import json
from dotenv import load_dotenv
import os
from flask import Flask, request, send_file, render_template

load_dotenv(override=True)
api_key = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def generate_pdf():
    if request.method == 'POST':
        image_data = request.form['image']
        try:
            # Process the base64-encoded image data
            image_data = image_data.split(',')[1]
            decoded_data = base64.b64decode(image_data)
            image = Image.open(BytesIO(decoded_data))

            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            encoded_string = base64.b64encode(buffered.getvalue()).decode()

            MODEL_NAME = "claude-3-opus-20240229"
            base64_string = encoded_string

            message_list = [
                {
                    "role": 'user',
                    "content": [
                        {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": base64_string}},
                        {"type": "text", "text": "Elaborate on the text in the image in a bullet point list format. Emphasize the important points within the text inside the image."}
                    ]
                }
            ]

            response = client.messages.create(
                model=MODEL_NAME,
                max_tokens=2048,
                messages=message_list
            )

            extracted_text = response.content[0].text

            pdf_buffer = BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            normal_style = styles['Normal']
            normal_style.fontSize = 14
            normal_style.leading = 14

            paragraph = Paragraph(response.content[0].text, normal_style)
            paragraph.wrapOn(c, 6.5*inch, 9*inch)
            paragraph.drawOn(c, 1*inch, 8*inch)

            c.showPage()
            c.save()
            pdf_buffer.seek(0)

            return send_file(pdf_buffer, as_attachment=True, download_name='generated.pdf', mimetype='application/pdf')

        except Exception as e:
            return f"Error processing the image: {str(e)}", 500

    return render_template('index.html')

if __name__ == '__main__':
    app.run()