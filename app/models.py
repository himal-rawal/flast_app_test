from datetime import datetime
from app import db  # Import db from the main app

class PasteText(db.Model):
    __tablename__ = 'paste_text'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(100), nullable=True)
    is_protected = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<PasteText {self.id}>'
