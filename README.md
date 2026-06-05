# 🛡️ CipherVault: Professional Password Management Platform

CipherVault is a high-security, professional grade password generation and storage platform. It features a complete separation of Frontend (JS/Bootstrap 5) and Backend (Python/Flask REST API), following modern industry-standard architecture.

## 🚀 Key Features

*   **Advanced Generator**: Customizable secure password generation.
*   **Security Analyzer**: Entropy scoring and crack-time estimation using `zxcvbn`.
*   **Encrypted Vault**: SQLite-backed storage with AES-256 (Fernet) encryption.
*   **Hacker Dashboard**: Real-time statistics and security health monitoring.
*   **Cybersecurity UI**: Glassmorphism design with neon glowing accents.

---

## 🏗️ Project Architecture

```text
PasswordGenerator/
├── backend/            # Flask REST API
│   ├── app.py          # Entry Point & CORS Setup
│   ├── config/         # App Configurations
│   ├── models/         # Database Schema (SQLAlchemy)
│   ├── routes/         # Modular API Endpoints
│   ├── utils/          # Encryption & Generation Engines
│   └── requirements.txt
│
└── frontend/           # Separate Frontend UI
    ├── index.html      # Landing Page
    ├── css/            # Cyber-theme Styles
    └── js/             # API Integration (Fetch)
```

---

## 🛠️ Installation & Setup

### 1. Prerequisites
Ensure you have Python 3.8+ installed.

### 2. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate it:
   - **Windows**: `venv\Scripts\activate`
   - **Mac/Linux**: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the server:
   ```bash
   python app.py
   ```
   *The API will be available at http://127.0.0.1:5000*

### 3. Frontend Setup
The frontend is independent. You can simply open the HTML files in a browser, or use a Live Server (recommended).
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Open `index.html` in your browser.
   *Tip: Use the VS Code extension "Live Server" for the best experience.*

---

## 💻 Tech Stack

*   **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, Bootstrap Icons.
*   **Backend**: Python, Flask (RESTful API), Flask-CORS, Flask-SQLAlchemy.
*   **Database**: SQLite.
*   **Security**: `cryptography` (Fernet) for AES, `zxcvbn` for AI-based analysis.

## 🎓 Career Impact
This project demonstrates:
1. **Separation of Concerns**: Decoupled frontend/backend logic.
2. **REST API Design**: Handling GET, POST, DELETE requests with JSON.
3. **Data Security**: Real-world encryption practices.
4. **Modern UI/UX**: Professional dashboard and responsiveness.

---

## 🎓 Beginner's Guide: Why this Architecture?

Traditional web apps often mix Python and HTML together. **CipherVault** uses a "Decoupled Architecture":

- **Portability**: You could swap the Backend for a different language (like Node.js) without ever touching the Frontend design.
- **Scalability**: In a real-world scenario, the Frontend could be hosted on a CDN (like Vercel) while the Backend runs on a powerful server (Azure/AWS).
- **Professionalism**: This is how modern apps like Spotify, Netflix, and Instagram are built.

---

## 📜 License
MIT License

