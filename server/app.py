import os
import uuid
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from db import init_db, db
from models import Candidate

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

# Initialize DB
init_db(app)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'uploads', 'avatars')
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route('/uploads/avatars/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)


@app.post('/api/candidates')
def create_candidate():
    try:
        name = request.form.get('name', '')
        degree = request.form.get('degree', '')
        languages_text = request.form.get('languages', '')
        exp1 = request.form.get('exp1', '')
        exp2 = request.form.get('exp2', '')
        skill1 = request.form.get('skill1', '')
        skill2 = request.form.get('skill2', '')

        # parse languages
        languages = [x.strip() for x in languages_text.split(',') if x.strip()]
        avatar_path = None
        file = request.files.get('avatar')
        if file and file.filename:
            ext = os.path.splitext(file.filename)[1].lower()
            if ext not in {'.png', '.jpg', '.jpeg'}:
                return jsonify({'error': 'Only .png, .jpg, .jpeg allowed'}), 400
            file.seek(0, 2)
            size = file.tell(); file.seek(0)
            if size > 5 * 1024 * 1024:
                return jsonify({'error': 'Avatar must be ≤ 5MB'}), 400
            fname = f"{uuid.uuid4().hex}.png"
            save_path = os.path.join(UPLOAD_DIR, fname)
            # Save directly; Pillow conversion could be added if needed
            file.save(save_path)
            avatar_path = os.path.relpath(save_path, os.path.dirname(__file__)).replace('\\', '/')

        cand = Candidate(
            name=name,
            degree=degree,
            languages=json.dumps(languages, ensure_ascii=False),
            exp1=exp1,
            exp2=exp2,
            skill1=skill1,
            skill2=skill2,
            avatar_path=avatar_path,
        )
        db.session.add(cand)
        db.session.commit()
        return jsonify(cand.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.get('/api/candidates/<int:cid>')
def get_candidate(cid):
    cand = Candidate.query.get_or_404(cid)
    return jsonify(cand.to_dict())


@app.put('/api/candidates/<int:cid>')
def update_candidate(cid):
    cand = Candidate.query.get_or_404(cid)
    try:
        data = request.form if request.form else request.json or {}
        def g(k, default=''):
            return data.get(k, getattr(cand, k))
        cand.name = g('name')
        cand.degree = g('degree')
        languages_text = data.get('languages')
        if languages_text is not None:
            langs = [x.strip() for x in languages_text.split(',') if x.strip()]
            cand.languages = json.dumps(langs, ensure_ascii=False)
        cand.exp1 = g('exp1')
        cand.exp2 = g('exp2')
        cand.skill1 = g('skill1')
        cand.skill2 = g('skill2')

        file = request.files.get('avatar') if request.files else None
        if file and file.filename:
            ext = os.path.splitext(file.filename)[1].lower()
            if ext not in {'.png', '.jpg', '.jpeg'}:
                return jsonify({'error': 'Only .png, .jpg, .jpeg allowed'}), 400
            file.seek(0, 2); size = file.tell(); file.seek(0)
            if size > 5 * 1024 * 1024:
                return jsonify({'error': 'Avatar must be ≤ 5MB'}), 400
            fname = f"{uuid.uuid4().hex}.png"
            save_path = os.path.join(UPLOAD_DIR, fname)
            file.save(save_path)
            cand.avatar_path = os.path.relpath(save_path, os.path.dirname(__file__)).replace('\\', '/')

        db.session.commit()
        return jsonify(cand.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.post('/api/parse-resume')
def deprecated_parse():
    return jsonify({'error': 'Endpoint deprecated'}), 410


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)


