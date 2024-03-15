from anthropic import Anthropic
from PIL import Image
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pathlib import Path
import base64


client = Anthropic()

with open(Path(__file__).parent.joinpath("logo.png"), "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

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

print(response.model_dump_json(indent=2))