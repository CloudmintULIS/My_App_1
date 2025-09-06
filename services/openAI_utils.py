import base64
from io import BytesIO
from PIL import Image
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def identify_image(image: Image.Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    b64_image = base64.b64encode(buffered.getvalue()).decode()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Identify the main object in this photo.\n"
                            "Reply with the object name only (e.g., 'apple', 'car', 'dog').\n"
                            "If the object is a person, reply 'human'.\n"
                            "Always try to guess the most likely object, even if not 100% sure.\n"
                            "Only reply 'unidentified' if the image is completely blank or just noise.\n"
                            "Do not write full sentences"
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{b64_image}",
                            "detail": "low"
                        }
                    }
                ]
            }
        ]
    )

    label_text = response.choices[0].message.content.strip()
    return label_text
