import io
import re
import base64
from pypdf import PdfReader
import docx2txt
from docx import Document


def _read_pdf(bytes_data: bytes):
    """Read PDF file and extract text"""
    text_parts = []
    reader = PdfReader(io.BytesIO(bytes_data))
    for page in reader.pages:
        try:
            text_parts.append(page.extract_text() or '')
        except Exception:
            pass
    return '\n'.join(text_parts), None


def _read_docx(bytes_data: bytes):
    """Read DOCX file and extract text"""
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


def _read_txt(bytes_data: bytes):
    """Read TXT file and extract text"""
    try:
        text = bytes_data.decode('utf-8')
        return text, None
    except UnicodeDecodeError:
        try:
            text = bytes_data.decode('latin-1')
            return text, None
        except:
            return '', None


def split_sections(text):
    """Split text into sections based on common headings"""
    sections = {}
    
    # Common section patterns for job descriptions
    patterns = {
        'company': re.compile(r'(?i)\b(company|about us|about company|tên công ty|công ty)\b'),
        'title': re.compile(r'(?i)\b(job title|title|position|vị trí|chức danh)\b'),
        'summary': re.compile(r'(?i)\b(summary|about the role|mô tả công việc|tổng quan)\b'),
        'responsibilities': re.compile(r'(?i)\b(responsibilities|what you will do|your impact|nhiệm vụ|trách nhiệm)\b'),
        'requirements': re.compile(r'(?i)\b(requirements|qualifications|you are|bạn cần|yêu cầu)\b'),
        'skills': re.compile(r'(?i)\b(skills|tech stack|kỹ năng|công nghệ)\b'),
        'location': re.compile(r'(?i)\b(location|địa điểm|nơi làm việc)\b'),
        'employment_type': re.compile(r'(?i)\b(employment type|hình thức|loại công việc)\b'),
        'salary': re.compile(r'(?i)\b(salary|compensation|lương|thu nhập)\b'),
        'languages': re.compile(r'(?i)\b(languages|ngoại ngữ|tiếng)\b')
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


def _guess_company(text, sections):
    """Guess company name from sections or text"""
    # First try to get from company section
    if 'company' in sections:
        company_text = sections['company']
        lines = company_text.split('\n')
        for line in lines[1:]:  # Skip heading line
            line = line.strip()
            if line and len(line) < 100 and not re.search(r'(?i)about|company|us|tên|công ty', line):
                return line
    
    # Fallback: look for company-like text in first few lines
    lines = text.split('\n')[:10]
    for line in lines:
        line = line.strip()
        if line and len(line) < 100 and not re.search(r'(?i)job|position|title|vị trí|chức danh', line):
            # Check if it looks like a company name
            if re.search(r'(?i)inc|corp|company|ltd|llc|group|industries|solutions', line):
                return line
            # Or if it's in all caps (common for company names)
            if line.isupper() and len(line) > 3:
                return line
    
    return ""


def _guess_title(text, sections):
    """Guess job title from sections or text"""
    if 'title' in sections:
        title_text = sections['title']
        lines = title_text.split('\n')
        for line in lines[1:]:  # Skip heading line
            line = line.strip()
            if line and len(line) < 100:
                return line
    
    # Fallback: look for common job title patterns
    lines = text.split('\n')[:15]
    for line in lines:
        line = line.strip()
        if re.search(r'(?i)engineer|developer|manager|analyst|specialist|coordinator|assistant|director|lead|senior|junior', line):
            return line
    
    return ""


def _extract_list_items(text, max_items=10):
    """Extract list items from text, limiting to max_items"""
    if not text:
        return []
    
    # Remove the heading
    body = re.sub(r'(?i)\b(responsibilities|requirements|skills|qualifications|nhiệm vụ|trách nhiệm|yêu cầu|kỹ năng)\b', '', text, 1)
    
    # Split by bullet points
    items = re.split(r'(?:\n|\r|^)[\-\–\•\*]\s*', body)
    items = [re.sub(r'\s{2,}', ' ', i).strip(" -–•*") for i in items if len(i.strip()) > 5]
    
    # Fallback: split by lines if no bullet points found
    if len(items) <= 1:
        items = [l.strip() for l in body.splitlines() if len(l.strip()) > 10]
    
    # Filter by reasonable length and limit items
    out = []
    for s in items:
        if 10 <= len(s) <= 300:
            out.append(s)
        if len(out) == max_items:
            break
    
    return out


def _merge_description(sections):
    """Merge sections into a final description"""
    parts = []
    
    if 'summary' in sections:
        parts.append(sections['summary'])
    
    if 'responsibilities' in sections:
        parts.append("\n\nResponsibilities:\n- " + "\n- ".join(_extract_list_items(sections['responsibilities'], 5)))
    
    if 'requirements' in sections:
        parts.append("\n\nRequirements:\n- " + "\n- ".join(_extract_list_items(sections['requirements'], 5)))
    
    if not parts:
        # Fallback: use first few lines of text
        return sections.get('summary', '')[:500] + "..." if sections.get('summary', '') else ""
    
    return "\n".join(parts)


def parse_jd(file_stream, filename):
    """Parse job description file and return structured data"""
    b = file_stream.read() if hasattr(file_stream, 'read') else file_stream
    ext = filename.lower().rsplit('.', 1)[-1] if '.' in filename else ''
    
    if ext == 'pdf':
        text, _ = _read_pdf(b)
    elif ext in ('doc', 'docx'):
        text, _ = _read_docx(b)
    elif ext == 'txt':
        text, _ = _read_txt(b)
    else:
        raise ValueError('Unsupported file type')
    
    if not text:
        raise ValueError('Could not extract text from file')
    
    # Split text into sections
    sections = split_sections(text)
    
    # Extract key information
    company = _guess_company(text, sections)
    title = _guess_title(text, sections)
    summary = sections.get('summary', '')
    responsibilities = _extract_list_items(sections.get('responsibilities', ''), 5)
    requirements = _extract_list_items(sections.get('requirements', ''), 5)
    skills = _extract_list_items(sections.get('skills', ''), 5)
    location = sections.get('location', '').split('\n')[1] if 'location' in sections else ''
    employment_type = sections.get('employment_type', '').split('\n')[1] if 'employment_type' in sections else ''
    salary = sections.get('salary', '').split('\n')[1] if 'salary' in sections else ''
    languages = _extract_list_items(sections.get('languages', ''), 3)
    
    # Merge into final description
    description = _merge_description(sections)
    
    return {
        "company": company,
        "title": title,
        "summary": summary,
        "responsibilities": responsibilities,
        "requirements": requirements,
        "skills": skills,
        "location": location,
        "employment_type": employment_type,
        "salary": salary,
        "languages": languages,
        "description": description
    }
