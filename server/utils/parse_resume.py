import io
import re
import base64
from pypdf import PdfReader
import docx2txt
from docx import Document


def _placeholder_avatar(name: str) -> str:
    initials = ''.join([p[0].upper() for p in (name or 'NA').split()[:2]]) or 'NA'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#14b8a6"/>
      <stop offset="100%" stop-color="#22d3ee"/>
    </linearGradient>
  </defs>
  <circle cx="128" cy="128" r="128" fill="url(#g)"/>
  <text x="50%" y="55%" text-anchor="middle" font-size="88" font-family="Arial,Helvetica,sans-serif" fill="#00100f" dy=".35em">{initials}</text>
</svg>'''
    return 'data:image/svg+xml;base64,' + base64.b64encode(svg.encode('utf-8')).decode('ascii')


def _read_pdf(bytes_data: bytes):
    text_parts = []
    reader = PdfReader(io.BytesIO(bytes_data))
    for page in reader.pages:
        try:
            text_parts.append(page.extract_text() or '')
        except Exception:
            pass
    # pypdf XObject parsing is heavy; skip extracting image for stability
    return '\n'.join(text_parts), None


def _read_docx(bytes_data: bytes):
    buf = io.BytesIO(bytes_data)
    text = docx2txt.process(buf)
    buf.seek(0)
    avatar = None
    try:
        document = Document(buf)
        for rel in document.part.related_parts.values():
            blob = getattr(rel, '_blob', None)
            if blob:
                avatar = 'data:image/png;base64,' + base64.b64encode(blob).decode('ascii')
                break
    except Exception:
        pass
    return text or '', avatar


YEAR = r'(19|20)\d{2}'
YEAR_RANGE = re.compile(rf'(?i)\b{YEAR}\b.*?\b({YEAR}\b|present|hiện tại)')


def _guess_name(lines):
    for s in lines[:8]:
        t = s.strip()
        if not t:
            continue
        if re.search(r'(?i)(họ\s+và\s+tên|name)\s*[:：]', t):
            return re.split(r'[:：]', t, 1)[-1].strip().title()
        if t.isupper() and len(t) < 60:
            return t.title()
    return ''


def _guess_degree(text):
    m = re.search(r'(?i)Bachelor|Engineer|Master|PhD|Đại học|Cử nhân|Thạc sĩ|Tiến sĩ', text)
    return m.group(0) if m else ''


def _guess_languages(text):
    langs = []
    for lang in ['English','Vietnamese','Japanese','Korean','Chinese','French','German']:
        if re.search(lang, text, re.I):
            level = re.search(r'(?i)A1|A2|B1|B2|C1|C2|IELTS\s*\d(?:\.\d)?|TOEIC\s*\d+|Native', text)
            langs.append(f"{lang} {level.group(0) if level else ''}".strip())
    return langs


def _guess_experiences(lines):
    items = []
    for i, line in enumerate(lines):
        m = YEAR_RANGE.search(line.replace('–','-').replace('—','-'))
        if m:
            company = lines[i+1] if i+1 < len(lines) else ''
            role = lines[i+2] if i+2 < len(lines) else ''
            items.append(' — '.join([m.group(0), company, role]).strip(' —'))
        if len(items) >= 2:
            break
    return items


def _guess_skills(text):
    dictionary = ['React','Angular','Vue','Node.js','Python','Java','SQL','AWS','Docker','Kubernetes','ML','NLP']
    return [k for k in dictionary if re.search(rf'\b{re.escape(k)}\b', text, re.I)][:6]


def extract_profile(file_stream, filename):
    b = file_stream.read() if hasattr(file_stream, 'read') else file_stream
    ext = filename.lower().rsplit('.', 1)[-1] if '.' in filename else ''
    if ext == 'pdf':
        text, avatar = _read_pdf(b)
    elif ext in ('doc','docx'):
        text, avatar = _read_docx(b)
    else:
        raise ValueError('Unsupported file type')

    lines = [l for l in (text or '').splitlines() if l.strip()]
    name = _guess_name(lines)
    degree = _guess_degree(text)
    languages = _guess_languages(text)
    experiences = _guess_experiences(lines)
    skills = _guess_skills(text)
    if not avatar:
        avatar = _placeholder_avatar(name or 'User')
    return {
        'name': name,
        'degree': degree,
        'languages': languages,
        'experiences': experiences,
        'skills': skills,
        'avatar_data_url': avatar,
    }



