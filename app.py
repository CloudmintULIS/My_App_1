from flask import Flask
from controllers.auth_controller import auth_bp
from controllers.main_controller import main_bp
from controllers.review_controller import review_bp
from controllers.quiz_controller import quiz_bp
from controllers.openAI_controller import openAI_bp
from controllers.admin_controller import admin_bp
from controllers.image_controller import image_bp
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load biến môi trường (API key)
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__, template_folder='view')
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Đăng ký các blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(review_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(openAI_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(main_bp)
app.register_blueprint(image_bp)

@app.route("/ping")
def ping():
    return "OK"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
