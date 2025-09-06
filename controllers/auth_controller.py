from flask import Blueprint, render_template, request, redirect, url_for, session
from models import auth_model
from services import auth_utils

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        user = auth_model.get_user_by_username(username)
        if user and auth_utils.verify_password(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']

            if user['role'] == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('main.index'))
        else:
            return render_template('login.html', error='Tài khoản không tồn tại.')

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        confirm = request.form['confirm_password']

        if not username or not password or not confirm:
            return render_template('register.html', error='All fields are required.')

        if password != confirm:
            return render_template('register.html', error='Mật khẩu không trùng khớp.')

        if not auth_utils.validate_username(username):
            return render_template('register.html', error='Tên đăng nhập không hợp lệ.')

        existing_user = auth_model.get_user_by_username(username)
        if existing_user:
            return render_template('register.html', error='Tên đăng nhập đã tồn tại.')

        hashed_password = auth_utils.hash_password(password)
        success, error = auth_model.add_user(username, hashed_password)
        if success:
            return redirect(url_for('auth.login'))
        else:
            return render_template('register.html', error=f"Error: {error}")

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
