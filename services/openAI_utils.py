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
                            "Reply with exactly ONE word only, in singular form (e.g., apple not apples, pear not pears).\n"
                            "- If it is a real human, reply: human\n"
                            "- If it is an anime/manga style drawing, reply: anime\n"
                            "- If it is a western cartoon style drawing, reply: cartoon\n"
                            "- If it is a digital art or generic illustration, reply: illustration\n"
                            "- Otherwise, reply with the singular object name (e.g., apple, car, dog, pear)\n"
                            "- If the image is blank or just noise, reply: unidentified\n"
                            "Do not explain. Only output one word."
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
