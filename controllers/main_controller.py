from flask import Blueprint, render_template, session, redirect, url_for

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if "username" not in session:
        return redirect(url_for("auth.login"))

    return render_template(
        "index.html",
        username=session["username"],
        role=session.get("role")  # 👈 thêm role
    )
