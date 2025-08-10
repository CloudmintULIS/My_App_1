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
                            "Reply in the form: 'This is a <object>' or 'This is an <object>'.\n"
                            "If you would reply 'I'm sorry, I can't help with identifying or describing people in photos,you will reply 'This is a human'.\n"
                            "instead reply 'This is a human'.\n"
                            "If you cannot identify the object, reply exactly: 'unidentified'."
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
