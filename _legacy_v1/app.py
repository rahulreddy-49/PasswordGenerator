from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from utils.password_engine import PasswordEngine
from utils.encryption import PasswordEncryptor
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cyber-security-project-secret-key-12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
encryptor = PasswordEncryptor()
engine = PasswordEngine()

# --- Database Models ---
class StoredPassword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    encrypted_password = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "site_name": self.site_name,
            "username": self.username,
            "password": encryptor.decrypt(self.encrypted_password),
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

# Initialize database
with app.app_context():
    db.create_all()

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate')
def generate_page():
    return render_template('generate.html')

@app.route('/api/generate', methods=['POST'])
def api_generate():
    data = request.json
    length = int(data.get('length', 16))
    use_upper = data.get('upper', True)
    use_lower = data.get('lower', True)
    use_digits = data.get('digits', True)
    use_symbols = data.get('symbols', True)
    
    pwd = engine.generate(length, use_upper, use_lower, use_digits, use_symbols)
    analysis = engine.analyze(pwd)
    
    return jsonify({
        "password": pwd,
        "analysis": analysis
    })

@app.route('/analyze')
def analyze_page():
    return render_template('analyze.html')

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    data = request.json
    password = data.get('password', '')
    if not password:
        return jsonify({"error": "No password provided"}), 400
    
    analysis = engine.analyze(password)
    return jsonify(analysis)

@app.route('/vault')
def vault_page():
    passwords = StoredPassword.query.order_by(StoredPassword.created_at.desc()).all()
    return render_template('vault.html', passwords=[p.to_dict() for p in passwords])

@app.route('/api/vault/save', methods=['POST'])
def api_vault_save():
    data = request.json
    site = data.get('site')
    user = data.get('username')
    pwd = data.get('password')
    
    if not all([site, user, pwd]):
        return jsonify({"success": False, "error": "Missing fields"}), 400
    
    encrypted = encryptor.encrypt(pwd)
    new_entry = StoredPassword(site_name=site, username=user, encrypted_password=encrypted)
    db.session.add(new_entry)
    db.session.commit()
    
    return jsonify({"success": True})

@app.route('/api/vault/delete/<int:id>', methods=['DELETE'])
def api_vault_delete(id):
    entry = StoredPassword.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return jsonify({"success": True})

@app.route('/dashboard')
def dashboard():
    total_stored = StoredPassword.query.count()
    # Dummy data for demo purposes in requirements
    stats = {
        "total_generated": 1254, # This could be tracked in DB too if needed
        "total_secured": total_stored,
        "average_strength": "Excellent" if total_stored > 0 else "N/A",
        "recent_activity": [p.to_dict() for p in StoredPassword.query.order_by(StoredPassword.created_at.desc()).limit(5).all()]
    }
    return render_template('dashboard.html', stats=stats)

if __name__ == '__main__':
    app.run(debug=True)
