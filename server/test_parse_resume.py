from pathlib import Path
from io import BytesIO
from utils.parse_resume import extract_profile


def test_parse_sample_pdf():
    path = Path(__file__).parent / 'test' / 'White simple Sales Representative Cv Resume.pdf'
    b = path.read_bytes()
    data = extract_profile(BytesIO(b), path.name)
    assert isinstance(data, dict)
    assert data.get('name') and len(data['name']) >= 3
    langs = ' '.join(data.get('languages') or []).lower()
    assert 'english' in langs or langs == ''
    assert isinstance(data.get('experiences'), list) and len(data['experiences']) >= 1
    deg = data.get('degree','')
    assert isinstance(deg, str)
    assert data.get('avatar_data_url','').startswith('data:image/')


