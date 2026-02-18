# 🩺 DermaCarePro  
### AI-Powered Skin Disease Detection & Recommendation System

DermaCarePro is a full-stack Flask web application that uses a deep learning model to detect skin diseases from uploaded images and provide recommended solutions, doctors, and products.

---

## 🚀 Project Overview

This system integrates:

- 🧠 Deep Learning (PyTorch CNN model)
- 🌐 Flask Web Framework
- 🗄 SQLAlchemy + MySQL Database
- ☁️ Hugging Face Model Hosting
- 🚀 Render Cloud Deployment

Users can:

- Register & Login
- Upload skin images
- Get AI-based disease predictions
- View recommended doctors & products
- Track past activity

---

## 🧠 Machine Learning Pipeline

Dataset (HAM images + metadata) ->
Data Preprocessing
->
CNN Model Training (PyTorch)
->
Model Saved as .pth
->
Uploaded to Hugging Face
->
Flask App Downloads Model at Runtime
->
User Upload → Prediction → Result Display

---

## 🏗️ System Architecture

User
->
Flask Application
->
Prediction Module (PyTorch)
->
Database (Users, Activities, Doctors, Products)
->
Results + Recommendations

## 📂 Project Structure

```bash
skindisease/
│
├── app.py                     # Main Flask application
├── prediction.py              # Model inference logic
├── mymodel.py                 # Model architecture definition
├── db.py                      # Database models
├── auth.py                    # Authentication logic
├── activity.py                # Activity handling
├── forms.py                   # Flask form handling
├── config.py                  # Configuration settings
├── builddataset.py            # Dataset preparation script
├── train.py                   # Model training script
├── test.ipynb                 # Testing notebook
├── trial.ipynb                # Experiment notebook
│
├── requirements.txt           # Project dependencies
├── .gitignore                 # Ignored files & folders
├── README.md                  # Project documentation
│
├── templates/                 # HTML templates
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── result.html
│   ├── profile.html
│   └── other template files...
│
├── static/                    # Static assets
│   ├── uploads/               # User uploaded images (ignored in Git)
│   └── other assets...
│
├── HAM/                       # Training dataset (ignored in Git)
├── HAM10000_metadata.csv      # Dataset metadata (training use)
└── skin_disease_cnn.pth       # Trained model (hosted on Hugging Face)



```
## 🔍 Features

### 👤 User Management
- Secure signup & login
- Password hashing
- Session management
- Profile tracking

### 🖼 Image-Based Prediction
- Upload skin image
- AI model predicts disease
- Accuracy score displayed

### 🏥 Recommendations
- Suggested doctors
- Recommended products
- Activity tracking

### 📊 History Tracking
- View previous diagnoses
- Stored in database

---

## 🤖 Model Details

- Framework: PyTorch
- Architecture: Convolutional Neural Network (CNN)
- File Format: `.pth`
- Hosted On: Hugging Face Hub
- Loaded dynamically during app startup

---


## 🌐 Deployment Architecture

GitHub → Code Hosting

Hugging Face → Model Hosting

Render → Application Deployment


---

## 🛠️ Installation (Local Setup)

```bash
git clone https://github.com/yourusername/skin-disease-app.git
cd skin-disease-app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py

MODEL_URL = https://huggingface.co/informrohit12/skin-disease-cnn/resolve/main/skin_disease_cnn.pth

🔒 Security Features
Password hashing (Werkzeug)
Secure file upload handling
Session-based authentication
File size limits

👨‍💻 Tech Stack
| Layer         | Technology             |
| ------------- | ---------------------- |
| Backend       | Flask                  |
| ML            | PyTorch                |
| Database      | MySQL (SQLAlchemy ORM) |
| Deployment    | Render                 |
| Model Hosting | Hugging Face           |




```bash
⭐ Conclusion

DermaCarePro demonstrates an end-to-end AI healthcare application:

Model Training 
Backend Integration
Database Management
Cloud Deployment
A complete AI-powered dermatology support system.

