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
YEAR_RANGE = re.compile(rf'(?i)\b{YEAR}\b.*?\b({YEAR}\b|present|ongoing|hiện tại)')


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


def split_sections(text):
    """Split text into sections based on common headings"""
    sections = {}
    
    # Common section patterns
    patterns = {
        'edu': re.compile(r'(?i)\b(education|học vấn|bằng cấp|trình độ)\b'),
        'ach': re.compile(r'(?i)\bkey achievements?\b|\bachievements?\b|\bthành tựu\b'),
        'exp': re.compile(r'(?i)\b(experience|kinh nghiệm|làm việc)\b'),
        'skill': re.compile(r'(?i)\b(skills?|kỹ năng|năng lực)\b'),
        'lang': re.compile(r'(?i)\b(languages?|ngoại ngữ|tiếng)\b')
    }
    
    lines = text.split('\n')
    current_section = None
    current_content = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if line matches any section heading
        matched_section = None
        for section, pattern in patterns.items():
            if pattern.search(line):
                matched_section = section
                break
        
        if matched_section:
            # Save previous section
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content).strip()
            
            # Start new section
            current_section = matched_section
            current_content = [line]
        elif current_section:
            current_content.append(line)
    
    # Save last section
    if current_section and current_content:
        sections[current_section] = '\n'.join(current_content).strip()
    
    return sections


def extract_education_recent(edu_text):
    """Extract the most recent education entry with year range"""
    if not edu_text:
        return ""
    
    # Find year ranges in the text
    year_matches = list(YEAR_RANGE.finditer(edu_text))
    if not year_matches:
        return edu_text.split('\n')[0].strip() if edu_text else ""
    
    # Find the most recent education entry
    best_match = None
    best_year = 0
    
    for match in year_matches:
        start_year = int(match.group(1))
        end_year_str = match.group(2)
        
        # Handle "present", "ongoing", "hiện tại"
        if re.search(r'(?i)present|ongoing|hiện tại', end_year_str):
            end_year = 9999  # Consider ongoing as most recent
        else:
            end_year = int(end_year_str) if end_year_str.isdigit() else start_year
        
        # Choose the entry with the highest end year (most recent)
        if end_year > best_year:
            best_year = end_year
            best_match = match
    
    if not best_match:
        return edu_text.split('\n')[0].strip()
    
    # Extract the education entry around the year range
    start_pos = max(0, best_match.start() - 100)
    end_pos = min(len(edu_text), best_match.end() + 100)
    
    entry_text = edu_text[start_pos:end_pos].strip()
    
    # Try to extract degree and school
    lines = entry_text.split('\n')
    if len(lines) >= 2:
        # First line might be degree, second might be school
        degree = lines[0].strip()
        school = lines[1].strip()
        
        # Clean up the year range
        year_range = best_match.group(0).replace('–', '-').replace('—', '-')
        
        return f"{degree} — {school} ({year_range})"
    else:
        # Fallback: return the entry with year range
        return entry_text


def extract_achievements(ach_text):
    """Extract achievements from text, limiting to top 3 reasonable length items"""
    if not ach_text:
        return []
    
    # Remove the heading
    body = re.sub(r'(?i)\bkey achievements?\b|\bachievements?\b|\bthành tựu\b', '', ach_text, 1)
    
    # Split by bullet points
    items = re.split(r'(?:\n|\r|^)[\-\–\•\*]\s*', body)
    items = [re.sub(r'\s{2,}', ' ', i).strip(" -–•*") for i in items if len(i.strip()) > 3]
    
    # Fallback: split by lines if no bullet points found
    if len(items) <= 1:
        items = [l.strip() for l in body.splitlines() if len(l.strip()) > 5]
    
    # Filter by reasonable length and limit to top 3
    out = []
    for s in items:
        if 5 <= len(s) <= 280:
            out.append(s)
        if len(out) == 3:
            break
    
    return out


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
    
    # Split text into sections
    sections = split_sections(text)
    
    name = _guess_name(lines)
    degree = extract_education_recent(sections.get("edu", ""))
    languages = _guess_languages(text)
    experiences = _guess_experiences(lines)
    skills = _guess_skills(text)
    achievements = extract_achievements(sections.get("ach", ""))
    
    if not avatar:
        avatar = _placeholder_avatar(name or 'User')
    
    return {
        'name': name,
        'degree': degree,
        'languages': languages,
        'experiences': experiences,
        'skills': skills,
        'achievements': achievements,
        'avatar_data_url': avatar,
    }



