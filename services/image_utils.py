import cloudinary
import cloudinary.uploader
from datetime import datetime
from io import BytesIO
from PIL import Image
from models.image_model import save_vocab_card, get_next_vocab_card_id
from dotenv import load_dotenv
import os

load_dotenv()

# Cấu hình Cloudinary (chỉ cần gọi 1 lần ở module này)
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def async_upload(username, image, label_clean):
    """Hàm chạy background để upload ảnh"""
    try:
        upload_image_and_save(username, image, label_clean)
    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")

def upload_image_and_save(username: str, image: Image.Image, label_clean: str) -> (bool, str, str):
    """
    Upload ảnh lên Cloudinary với tên {id}_{username}_{timestamp}
    và lưu thông tin vào database.
    """
    try:
        # 1️⃣ Lấy ID kế tiếp từ sequence vocab_cards_id_seq
        image_id = get_next_vocab_card_id()

        # 2️⃣ Tạo tên file: {id}_{username}_{timestamp}
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{image_id}_{username}_{timestamp}"

        # 3️⃣ Chuyển ảnh PIL thành bytes
        img_bytes = BytesIO()
        image.save(img_bytes, format="JPEG")
        img_bytes.seek(0)

        # 4️⃣ Upload lên Cloudinary
        result = cloudinary.uploader.upload(
            img_bytes,
            folder="vocab_images",
            public_id=filename,
            overwrite=True
        )
        image_url = result["secure_url"]

        # 5️⃣ Lưu vào DB (dùng ID đã lấy)
        success, error = save_vocab_card(username, image_url, label_clean, image_id)
        if not success:
            return False, None, error

        return True, image_url, None

    except Exception as e:
        return False, None, str(e)
