from flask import Blueprint, request, jsonify
from models.models import db, StoredPassword
from utils.password_engine import PasswordEngine
from utils.encryption import PasswordEncryptor

api_bp = Blueprint('api', __name__)
engine = PasswordEngine()
encryptor = PasswordEncryptor()

@api_bp.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        data = request.json or {}
    else:
        data = request.args

    length = int(data.get('length', 16))
    use_upper = str(data.get('upper', 'true')).lower() == 'true'
    use_lower = str(data.get('lower', 'true')).lower() == 'true'
    use_digits = str(data.get('digits', 'true')).lower() == 'true'
    use_symbols = str(data.get('symbols', 'true')).lower() == 'true'
    
    pwd = engine.generate(length, use_upper, use_lower, use_digits, use_symbols)
    analysis = engine.analyze(pwd)
    
    return jsonify({
        "password": pwd,
        "analysis": analysis
    })

@api_bp.route('/analyze', methods=['POST'])
def analyze():
    data = request.json or {}
    password = data.get('password', '')
    if not password:
        return jsonify({"error": "No password provided"}), 400
    
    analysis = engine.analyze(password)
    return jsonify(analysis)

import hashlib

@api_bp.route('/check-breach', methods=['POST'])
def check_breach():
    data = request.json or {}
    email = data.get('email', '')
    password = data.get('password', '')
    
    # Mocking breach results for demo purposes
    # In a real SaaS, this would call HIBP API
    has_breach = False
    details = []
    
    if email and "pwned" in email:
        has_breach = True
        details = ["LinkedIn (2016)", "Adobe (2013)"]
    
    if password == "123456" or password == "password":
        has_breach = True
        details.append("Commonly leaked password")

    return jsonify({
        "breached": has_breach,
        "count": len(details),
        "details": details,
        "recommendation": "Change your password immediately!" if has_breach else "Your account appears safe."
    })

@api_bp.route('/vault', methods=['GET'])
def get_vault():
    category = request.args.get('category')
    query = StoredPassword.query
    if category and category != 'All':
        query = query.filter_by(category=category)
    
    passwords = query.order_by(StoredPassword.created_at.desc()).all()
    return jsonify([p.to_dict(decryptor=encryptor) for p in passwords])

@api_bp.route('/save', methods=['POST'])
def save_password():
    data = request.json or {}
    site = data.get('site')
    user = data.get('username')
    pwd = data.get('password')
    cat = data.get('category', 'Other')
    
    if not all([site, user, pwd]):
        return jsonify({"success": False, "error": "Missing fields"}), 400
    
    encrypted = encryptor.encrypt(pwd)
    new_entry = StoredPassword(site_name=site, username=user, encrypted_password=encrypted, category=cat)
    db.session.add(new_entry)
    db.session.commit()
    
    return jsonify({"success": True})

@api_bp.route('/stats', methods=['GET'])
def get_stats():
    total = StoredPassword.query.count()
    
    # Calculate more detailed stats
    passwords = StoredPassword.query.all()
    weak = 0
    strong = 0
    categories_count = {}
    
    for p in passwords:
        decrypted = encryptor.decrypt(p.encrypted_password)
        analysis = engine.analyze(decrypted)
        if analysis['score'] < 3:
            weak += 1
        else:
            strong += 1
        
        cat = p.category
        categories_count[cat] = categories_count.get(cat, 0) + 1

    return jsonify({
        "total_passwords": total,
        "weak_passwords": weak,
        "strong_passwords": strong,
        "categories": categories_count,
        "security_score": round((strong / total * 100) if total > 0 else 0, 1),
        "recent_activity": [p.to_dict() for p in passwords[:5]]
    })
