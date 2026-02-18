from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import db
from config import Config
from app import login_manager

auth_bp = Blueprint('auth', __name__)

class User(UserMixin):
    def __init__(self, id, name, email, password_hash):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash

@login_manager.user_loader
def load_user(user_id):
    conn = db.get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM user WHERE id=%s", (int(user_id),))
        row = cur.fetchone()
    return User(**row) if row else None

@auth_bp.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pw   = generate_password_hash(request.form['password'])
        conn = db.get_db()
        with conn.cursor() as cur:
            cur.execute(
              "INSERT INTO user (name,email,password_hash) VALUES (%s,%s,%s)",
              (name, email, pw)
            )
        conn.commit()
        flash('Account created—please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pw    = request.form['password']
        conn  = db.get_db()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM user WHERE email=%s", (email,))
            row = cur.fetchone()
        if row and check_password_hash(row['password_hash'], pw):
            user = User(**row)
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
