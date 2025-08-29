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


class JobPosting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(160))
    title = db.Column(db.String(160))
    description = db.Column(db.Text)             # JD gộp cuối
    summary = db.Column(db.Text)
    responsibilities = db.Column(db.Text)        # JSON string list
    requirements = db.Column(db.Text)            # JSON string list
    skills = db.Column(db.Text)                  # JSON string list
    location = db.Column(db.String(160))
    employment_type = db.Column(db.String(60))
    salary = db.Column(db.String(120))
    languages = db.Column(db.Text)               # JSON string list
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        import json
        j = lambda s: (json.loads(s) if s else [])
        return {
          "id": self.id, "company": self.company or "", "title": self.title or "",
          "description": self.description or "", "summary": self.summary or "",
          "responsibilities": j(self.responsibilities),
          "requirements": j(self.requirements), "skills": j(self.skills),
          "location": self.location or "", "employment_type": self.employment_type or "",
          "salary": self.salary or "", "languages": j(self.languages)
        }


class SwipeDecision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, nullable=True)
    job_id = db.Column(db.String(80), index=True)
    action = db.Column(db.String(10))  # 'skip' | 'apply'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


