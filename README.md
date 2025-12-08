# 🏫 NEU Student Information Manager

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue" />
  <img src="https://img.shields.io/badge/build-passing-brightgreen" />
  <img src="https://img.shields.io/badge/python-3.10%2B-yellow" />
  <img src="https://img.shields.io/badge/license-MIT-lightgrey" />
</p>

---

## 📑 Table of Contents
- [Project Introduction](#-project-introduction)
- [Screenshots & Demo](#-screenshots--demo)
- [Installation Guide](#-installation-guide)
- [Usage & Examples](#-usage--examples)
- [Troubleshooting](#-troubleshooting)
- [Dependencies](#-dependencies)
- [Development Team](#-development-team)
- [References](#-references)
- [License](#-license)
- [Badges](#-badges)

---

## 📘 Project Introduction

**NEU Student Information Manager** is a management system designed for the National Economics University (NEU), enabling administrators to manage students, tuition fees, academic programs, and related operations efficiently.

### 🎯 Objectives
- Provide fast and accurate student management.
- Automate tuition data processing and annual fee tracking.
- Deliver a clean and user-friendly interface for administrators.

The system has been **fully deployed on a production server** and integrated with a **CI/CD pipeline**, ensuring automatic build & deployment on every update.

### 🚀 Try It Now
- **Demo Server**: *[https://web-production-75f3e.up.railway.app/financial/](https://web-production-75f3e.up.railway.app/financial/)*
- **YouTube Introduction Video**: *[https://www.youtube.com/watch?v=i3MQsx_knPE](https://www.youtube.com/watch?v=i3MQsx_knPE)*

---

### 🌐 Dashboard Interface
![Dashboard](screenshots/dashboard.png)

### 🧾 Student Management
![Student Management](screenshots/student-list.png)

### 💰 Tuition Fee Management
![Tuition Fee](screenshots/tuition.png)

### 🎞️ Demo GIF
![GIF Demo](screenshots/demo.gif)

---

## 🔧 Installation Guide

### 1️⃣ Clone the project
```bash
git clone https://github.com/Dai-Nguyen1506/neu_student_infomation_manager.git
cd neu_student_infomation_manager
```

### 2️⃣ Create virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure the database
- Create a MySQL database
- Import the provided SQL file
- Update `config.py` with database credentials

### 5️⃣ Run the Flask server
```bash
flask run
```
Server runs at: `http://localhost:5000`

---

## 📚 Usage & Examples

### 💡 Main Features
- Student CRUD management
- Tuition fee & academic year tracking
- Academic program management
- Plotly-powered dashboard & charts
- Validation & error handling system

### 🧪 Example API Calls
```python
# Get all students
GET /students

# Add a new student
POST /students/add
```

---

## 🛠️ Troubleshooting

### ❗ DatabaseError: Access denied
➡️ Check MySQL credentials in `config.py`.

### ❗ ModuleNotFoundError
➡️ Run `pip install -r requirements.txt`.

### ❗ 500 Internal Server Error
➡️ Check terminal logs — usually caused by invalid input.

---

## 📦 Dependencies

### Backend
- Flask
- MySQL Connector
- Flask-Bcrypt
- Flask-WTF
- Jinja2

### Frontend
- Bootstrap 5
- Plotly
- FontAwesome Icons

### Database
- MySQL 8.0+

---

## 👨‍💻 Development Team

### Students of National Economics University
- Nguyen Trong Dai
- Mai Huy Dang
- Nguyen Ngan An
- Mai Tuan Manh

### Academic Advisor
- Dr. Tran Duc Minh

---

## 📖 References
- Flask Documentation
- MySQL Docs
- Bootstrap Docs
- Plotly Guide
- Python Official Docs

---

## 📄 License
This project is licensed under the **MIT License**.

---

## 🏷️ Badges
<p align="center">
  <img src="https://img.shields.io/badge/status-active-blue" />
  <img src="https://img.shields.io/badge/maintenance-ongoing-orange" />
</p>

---

README will continue to be updated with future releases.
