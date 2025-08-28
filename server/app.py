import os
import uuid
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from db import init_db, db
from models import Candidate, JobPosting, SwipeDecision
from utils.parse_resume import extract_profile
from utils.parse_jd import parse_jd
from utils.jobs_feed import load_jobs_df, job_row_to_dict

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

# Initialize DB
init_db(app)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'uploads', 'avatars')
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Cache nhẹ
_JOBS_DF = None
def get_df():
    global _JOBS_DF
    if _JOBS_DF is None:
        _JOBS_DF = load_jobs_df()
    return _JOBS_DF


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
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Missing file field'}), 400
        f = request.files['file']
        filename = f.filename or ''
        ext = '.' + filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        if ext not in {'.pdf', '.doc', '.docx'}:
            return jsonify({'error': 'Only PDF, DOC, DOCX are allowed'}), 400
        f.seek(0, 2); size = f.tell(); f.seek(0)
        if size > 10 * 1024 * 1024:
            return jsonify({'error': 'File size must be ≤ 10MB'}), 400
        data = extract_profile(f.stream, filename)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.post('/api/parse-jd')
def parse_jd_api():
    try:
        f = request.files.get('file')
        if not f:
            return jsonify({'error': 'Thiếu file'}), 400
        
        ok_ext = {'.pdf', '.doc', '.docx', '.txt'}
        from pathlib import Path
        ext = Path(f.filename).suffix.lower()
        if ext not in ok_ext:
            return jsonify({'error': 'Chỉ nhận PDF/DOC/DOCX/TXT'}), 400
        
        f.seek(0, 2)
        size = f.tell()
        f.seek(0)
        if size > 10 * 1024 * 1024:
            return jsonify({'error': 'File size must be ≤ 10MB'}), 400
        
        data = parse_jd(f.stream, f.filename)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.post('/api/jobs')
def create_job():
    try:
        j = request.get_json() or {}
        job = JobPosting(
            company=j.get('company', ''),
            title=j.get('title', ''),
            description=j.get('description', ''),
            summary=j.get('summary', ''),
            responsibilities=json.dumps(j.get('responsibilities', []), ensure_ascii=False),
            requirements=json.dumps(j.get('requirements', []), ensure_ascii=False),
            skills=json.dumps(j.get('skills', []), ensure_ascii=False),
            location=j.get('location', ''),
            employment_type=j.get('employment_type', ''),
            salary=j.get('salary', ''),
            languages=json.dumps(j.get('languages', []), ensure_ascii=False),
        )
        db.session.add(job)
        db.session.commit()
        return jsonify({'id': job.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.get('/api/jobs/<int:id>')
def get_job(id):
    job = db.session.get(JobPosting, id)
    if not job:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(job.to_dict()), 200


@app.put('/api/jobs/<int:id>')
def update_job(id):
    job = db.session.get(JobPosting, id)
    if not job:
        return jsonify({'error': 'Not found'}), 404
    
    try:
        j = request.get_json() or {}
        
        if 'company' in j:
            job.company = j['company']
        if 'title' in j:
            job.title = j['title']
        if 'description' in j:
            job.description = j['description']
        if 'summary' in j:
            job.summary = j['summary']
        if 'responsibilities' in j:
            job.responsibilities = json.dumps(j['responsibilities'], ensure_ascii=False)
        if 'requirements' in j:
            job.requirements = json.dumps(j['requirements'], ensure_ascii=False)
        if 'skills' in j:
            job.skills = json.dumps(j['skills'], ensure_ascii=False)
        if 'location' in j:
            job.location = j['location']
        if 'employment_type' in j:
            job.employment_type = j['employment_type']
        if 'salary' in j:
            job.salary = j['salary']
        if 'languages' in j:
            job.languages = json.dumps(j['languages'], ensure_ascii=False)
        
        db.session.commit()
        return jsonify(job.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.get('/api/jobs')
def api_jobs():
    """Trả danh sách job để quẹt: ?offset=0&limit=20"""
    try:
        offset = int(request.args.get("offset", 0))
        limit = min(int(request.args.get("limit", 20)), 50)
    except:
        return {"error": "offset/limit không hợp lệ"}, 400
    
    try:
        df = get_df()
        end = min(offset + limit, len(df))
        rows = [job_row_to_dict(df.iloc[i].to_dict()) for i in range(offset, end)]
        return {"items": rows, "nextOffset": end if end < len(df) else None}
    except Exception as e:
        return {"error": f"Lỗi load jobs: {str(e)}"}, 500


@app.post('/api/decisions')
def api_decisions():
    """Lưu hành động quẹt: {candidate_id?, job_id, action: 'skip'|'apply'}"""
    try:
        j = request.get_json() or {}
        job_id = str(j.get("job_id", "")).strip()
        action = j.get("action", "")
        if not job_id or action not in ("skip", "apply"):
            return {"error": "Thiếu job_id/action"}, 400
        
        cand_id = j.get("candidate_id")  # có thể None
        rec = SwipeDecision(candidate_id=cand_id, job_id=job_id, action=action)
        db.session.add(rec)
        db.session.commit()
        return {"ok": True, "id": rec.id}
    except Exception as e:
        db.session.rollback()
        return {"error": f"Lỗi lưu decision: {str(e)}"}, 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)


