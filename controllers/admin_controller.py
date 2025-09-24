from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import admin_model
from services import admin_utils

# Chỉ import Blueprint, model và utils thôi
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ===================== Middleware =====================

@admin_bp.before_request
def check_admin():
    """Kiểm tra quyền admin trước khi vào bất kỳ route nào"""
    if "user_id" not in session or session.get("role") != "admin":
        flash("Bạn không có quyền truy cập trang này!")
        return redirect(url_for("auth.login"))


# ===================== Dashboard =====================

@admin_bp.route("/")
def dashboard():
    """Trang dashboard: hiển thị danh sách user, vocab cards và thống kê"""
    users = admin_model.get_all_users()
    vocab_cards = admin_model.get_all_vocab_cards()
    stats = admin_model.get_user_stats()
    word_info = admin_model.get_all_word_info()

    return render_template(
        "admin.html",
        users=users,
        vocab_cards=vocab_cards,
        user_stats=stats,
        word_info=word_info
    )


# ===================== User Management =====================

@admin_bp.route("/add_user", methods=["POST"])
def add_user():
    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]

    if not admin_utils.validate_username(username):
        flash("Username không hợp lệ!")
        return redirect(url_for("admin.dashboard"))

    hashed_password = admin_utils.hash_password(password)
    success, error = admin_model.add_user(username, hashed_password, role)

    flash("Thêm user thành công!" if success else f"Lỗi: {error}")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    success, error = admin_model.delete_user(user_id)
    flash("Xóa user thành công!" if success else f"Lỗi: {error}")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    if request.method == "POST":
        username = request.form.get("username")
        role = request.form.get("role")

        if not admin_utils.validate_username(username):
            flash("Username không hợp lệ!")
            return redirect(url_for("admin.edit_user", user_id=user_id))

        success, error = admin_model.update_user(user_id, username, role)

        if success:
            flash("Cập nhật user thành công!")
            return redirect(url_for("admin.dashboard"))
        else:
            flash(f"Lỗi: {error}")
            return redirect(url_for("admin.edit_user", user_id=user_id))

    user = admin_model.get_user_by_id(user_id)
    return render_template("edit_user.html", user=user)



# ===================== Vocab Management =====================

@admin_bp.route("/delete_vocab/<int:vocab_id>")
def delete_vocab(vocab_id):
    success, error = admin_model.delete_vocab(vocab_id)
    flash("Xóa vocab card thành công!" if success else f"Lỗi: {error}")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/edit_vocab/<int:vocab_id>", methods=["GET", "POST"])
def edit_vocab(vocab_id):
    if request.method == "POST":
        word = request.form["word"]
        image_path = request.form["image_path"]

        success, error = admin_model.update_vocab(vocab_id, word, image_path)
        if success:
            flash("Cập nhật vocab card thành công!")
            return redirect(url_for("admin.dashboard"))
        else:
            flash(f"Lỗi: {error}")
            return redirect(url_for("admin.edit_vocab", vocab_id=vocab_id))

    vocab = admin_model.get_vocab_by_id(vocab_id)
    return render_template("edit_vocab.html", vocab=vocab)

# ===================== Word Info Management =====================

@admin_bp.route("/add_word_info", methods=["POST"])
def add_word_info():
    word = request.form["word"]
    phonetic = request.form.get("phonetic")
    audio = request.form.get("audio")
    definition = request.form.get("definition")
    example = request.form.get("example")

    success, error = admin_model.add_word_info(word, phonetic, audio, definition, example)
    flash("Thêm word_info thành công!" if success else f"Lỗi: {error}")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/delete_word_info/<int:word_id>")
def delete_word_info(word_id):
    success, error = admin_model.delete_word_info(word_id)
    flash("Xóa word_info thành công!" if success else f"Lỗi: {error}")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/edit_word_info/<int:word_id>", methods=["GET", "POST"])
def edit_word_info(word_id):
    if request.method == "POST":
        word = request.form["word"]
        phonetic = request.form.get("phonetic")
        audio = request.form.get("audio")
        definition = request.form.get("definition")
        example = request.form.get("example")

        success, error = admin_model.update_word_info(word_id, word, phonetic, audio, definition, example)
        if success:
            flash("Cập nhật word_info thành công!")
            return redirect(url_for("admin.dashboard"))
        else:
            flash(f"Lỗi: {error}")
            return redirect(url_for("admin.edit_word_info", word_id=word_id))

    word_info = admin_model.get_word_info_by_id(word_id)
    return render_template("edit_word_info.html", word=word_info)
