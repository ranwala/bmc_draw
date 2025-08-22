from PIL import Image
import base64
from io import BytesIO

def convert_image_to_base64():
    img = Image.open('images/logo.png')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    image_bytes = buffer.getvalue()
    return base64.b64encode(image_bytes).decode()