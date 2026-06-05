from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class StoredPassword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    encrypted_password = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), default='Other')  # Banking, Social, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self, decryptor=None):
        data = {
            "id": self.id,
            "site_name": self.site_name,
            "username": self.username,
            "category": self.category,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        if decryptor:
            data["password"] = decryptor.decrypt(self.encrypted_password)
        return data
