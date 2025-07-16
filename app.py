from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image
import os
import base64
from io import BytesIO

# Load API key từ .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

# Route hiển thị giao diện
@app.route("/")
def index():
    return render_template("index.html")

# Route xử lý ảnh
@app.route("/analyze", methods=["POST"])
def analyze():
    image_file = request.files["image"]
    image = Image.open(image_file.stream).convert("RGB")

    # Chuyển ảnh sang base64
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    b64_image = base64.b64encode(buffered.getvalue()).decode()

    # Gửi lên GPT-4o
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Tôi đưa ra 1 hình ảnh rồi bạn phân tích nó là gì và chỉ trả lời một câu đơn giản: This is a ... , luôn có This is a/an trước vật thể đó"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{b64_image}",
                            "detail": "low"  # tiết kiệm token
                        },
                    },
                ],
            }
        ],
    )

    label = response.choices[0].message.content.strip()
    return jsonify({"label": label})

@app.route("/ping")
def ping():
    return "OK"


if __name__ == "__main__":
    app.run(debug=True)
