from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import pymysql
from prediction import predict

import requests  # <-- ADD THIS

# ===============================
# Hugging Face Model Auto-Download
# ===============================
MODEL_URL = os.environ.get("https://huggingface.co/informrohit12/skin-disease-cnn/resolve/main/skin_disease_cnn.pth")
MODEL_PATH = "skin_disease_cnn.pth"


def download_model():
    if not os.path.exists(MODEL_PATH):
        if not MODEL_URL:
            raise RuntimeError("MODEL_URL environment variable not set.")
        print("Downloading model from Hugging Face...")
        with requests.get(MODEL_URL, stream=True) as r:
            r.raise_for_status()
            with open(MODEL_PATH, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print("Model download complete.")


download_model()


# Ensure Flask uses PyMySQL
pymysql.install_as_MySQLdb()

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Flask1234@localhost/DermaCarePro'  # Update password if needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size limit (16MB)

# Import and initialize the db object and Flask-Migrate
from db import db, init_db
init_db(app)  # Initialize the database with the app

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Models are imported here
from db import User, Activity, Doctor, Product  # Assuming models are imported from db.py

# Home route
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    last_activity = Activity.query.filter_by(user_id=user.id).order_by(Activity.timestamp.desc()).first()

    return render_template('profile.html', user=user, last_activity=last_activity)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        dob = request.form['dob']
        gender = request.form['gender']
        weight = request.form.get('weight', type=float)
        blood_group = request.form.get('blood_group')
        location = request.form.get('location')

        # Calculate age from DOB
        dob_datetime = datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - dob_datetime.year - ((today.month, today.day) < (dob_datetime.month, dob_datetime.day))

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please login.", "danger")
            return redirect(url_for('login'))

        # Create and add user
        new_user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password, method='pbkdf2:sha256'),
            dob=dob_datetime,
            age=age,
            gender=gender,
            weight=weight,
            blood_group=blood_group,
            location=location
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully. Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

# Forgot password
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            return render_template('reset_password.html', email=email)
        else:
            flash('Email not found. Please register or try again.')
            return redirect(url_for('forgot_password'))
    return render_template('forgot_password.html')

@app.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.form['email']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    if new_password != confirm_password:
        flash('Passwords do not match.')
        return redirect(url_for('forgot_password'))

    # Update password using db.session.execute()
    user = User.query.filter_by(email=email).first()
    if user:
        user.password_hash = generate_password_hash(new_password, method='pbkdf2:sha256')
        db.session.commit()
        flash('Password updated successfully. Please login.')
        return redirect(url_for('login'))
    else:
        flash('Email not found.')
        return redirect(url_for('forgot_password'))
    
# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# Dashboard route for uploading image and prediction
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        image = request.files.get('image')
        if image:
            # Ensure the upload folder exists
            upload_folder = app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            # Secure the filename and save the image
            filename = secure_filename(image.filename)
            filepath = os.path.join(upload_folder, filename)
            image.save(filepath)

            # Use the model to make a prediction
            class_id, disease = predict(filepath)

            # Fetch all doctors and products (no location filter needed)
            all_doctors = Doctor.query.all()
            all_products = Product.query.all()

            # Create and save activity record
            activity = Activity(
                user_id=user.id,
                image_filename=filename,
                disease=disease,
                accuracy=class_id,
                recommended_solution="Recommended treatment or solution for " + disease,
                question_data={}  # Empty for now, but you can add relevant data if necessary
            )
            db.session.add(activity)
            db.session.commit()

            # Associate the first doctor and product (no location-based selection)
            if all_doctors:
                activity.doctor = all_doctors[0]  # Example: First doctor in the list
            if all_products:
                activity.product = all_products[0]  # Example: First product in the list

            db.session.commit()

            # Redirect to the result page with the activity and recommendations
            return redirect(url_for('result', activity_id=activity.id))

        else:
            flash('Please upload an image.', 'danger')

    return render_template('dashboard.html', user=user)


# Result route for displaying prediction results
@app.route('/result/<int:activity_id>')
def result(activity_id):
    activity = Activity.query.get_or_404(activity_id)

    # Fetch all doctors and products (no location filter)
    all_doctors = Doctor.query.all()
    all_products = Product.query.all()

    return render_template('result.html', activity=activity, all_doctors=all_doctors, all_products=all_products)


# Last activity
@app.route('/last_activity')
def last_activity():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    activity = Activity.query.filter_by(user_id=user.id).order_by(Activity.timestamp.desc()).first()

    # Check if the activity is None, and pass a flag to handle it
    return render_template('last_activity.html', activity=activity, no_activity=activity is None)


# About Us
@app.route('/about')
def about_us():
    return render_template('about.html')

# Run the app
if __name__ == '__main__':
    # app.run(debug=True, port=5001)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

