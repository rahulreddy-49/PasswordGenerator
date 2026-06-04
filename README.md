# Secure Password Generator AI

A premium cybersecurity-themed Flask web application for generating, analyzing, and storing secure passwords.

## 🚀 Features

- **Dark Futuristic UI**: Sleek glassmorphism design with neon accents.
- **AI Password Engine**: Uses `zxcvbn` and entropy math for deep security analysis.
- **Encrypted Vault**: Store your passwords securely using `AES-256` encryption (via `cryptography`).
- **Real-time Strength Meter**: Visual feedback with crack time estimation.
- **Modern Dashboard**: Track your security stats and recent activities.
- **Fully Responsive**: Works perfectly on mobile, tablet, and desktop.

## 🛠️ Tech Stack

- **Backend**: Python, Flask, Flask-SQLAlchemy, SQLite
- **Security**: Cryptography (Fernet), zxcvbn
- **Frontend**: Bootstrap 5, Font Awesome, Custom CSS/JS

## 📂 Project Structure

```bash
PasswordGeneratorAI/
├── app.py             # Main application & Database configurations
├── database.db        # SQLite database file (auto-generated)
├── secret.key         # Encryption key (auto-generated)
├── requirements.txt   # Project dependencies
├── utils/
│   ├── encryption.py  # AES-256 logic
│   └── password_engine.py # Generation & Analysis logic
├── static/
│   ├── css/style.css  # Futuristic styling
│   └── js/script.js   # Interactive frontend logic
└── templates/         # HTML Jinja2 templates
```

## ⚙️ Installation & Setup

1. **Clone or Extract** the project folder.
2. **Open Terminal** in the project directory.
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Application**:
   ```bash
   python app.py
   ```
5. **Access the App**:
   Open `http://127.0.0.1:5000` in your browser.

## 🔒 Security Note
This project generates a `secret.key` file in the root directory. This key is used to encrypt/decrypt your passwords in the vault. **Do not delete or share this key**, or you will lose access to your stored passwords!
