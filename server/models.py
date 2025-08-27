from datetime import datetime
from db import db


class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    degree = db.Column(db.String(255))
    languages = db.Column(db.Text)  # JSON string
    exp1 = db.Column(db.String(255))
    exp2 = db.Column(db.String(255))
    skill1 = db.Column(db.String(120))
    skill2 = db.Column(db.String(120))
    avatar_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        import json
        return {
            'id': self.id,
            'name': self.name or '',
            'degree': self.degree or '',
            'languages': (json.loads(self.languages) if self.languages else []),
            'exp1': self.exp1 or '',
            'exp2': self.exp2 or '',
            'skill1': self.skill1 or '',
            'skill2': self.skill2 or '',
            'avatar_url': ("/" + self.avatar_path) if self.avatar_path else ''
        }


