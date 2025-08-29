import pandas as pd
from pathlib import Path

COL_MAP = {
    "job id": "job_id",
    "experience": "experience",
    "qualifications": "qualifications",
    "salary range": "salary_range",
    "location": "location",
    "country": "country",
    "latitude": "latitude",
    "longitude": "longitude",
    "work type": "work_type",
    "company size": "company_size",
    "job posting date": "job_posting_date",
    "preference": "preference",
    "contact person": "contact_person",
    "contact": "contact",
    "job title": "job_title",
    "role": "role",
    "job portal": "job_portal",
    "job description": "job_description",
    "benefits": "benefits",
    "skills": "skills",
    "responsibilities": "responsibilities",
    "company name": "company_name",
    "company profile": "company_profile",
}

def _find_csv():
    # ưu tiên server/../database/job_descriptions.csv, fallback server/database/...
    here = Path(__file__).resolve().parent
    candidates = [
        here.parent.parent / "database" / "job_descriptions.csv",
        here.parent / "database" / "job_descriptions.csv",
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError("Không tìm thấy database/job_descriptions.csv")

def load_jobs_df():
    path = _find_csv()
    df = pd.read_csv(path)
    # chuẩn hoá tên cột
    new_cols = {}
    for c in df.columns:
        k = c.strip().lower()
        new_cols[c] = COL_MAP.get(k, k.replace(" ", "_"))
    df = df.rename(columns=new_cols)
    # fill NaN
    df = df.fillna("")
    return df

def job_row_to_dict(row) -> dict:
    """Trả về object hiển thị: company, title, description (gộp)."""
    company = (row.get("company_name") or "").strip()
    title = (row.get("job_title") or row.get("role") or "").strip()

    # gộp các thông tin "khác" vào mô tả
    parts = []
    def add(label, key):
        v = (row.get(key) or "").strip()
        if v:
            parts.append(f"{label}: {v}")
    add("Địa điểm", "location")
    add("Quốc gia", "country")
    add("Hình thức", "work_type")
    add("Mức lương", "salary_range")
    add("Kinh nghiệm", "experience")
    add("Kỹ năng", "skills")
    add("Trách nhiệm", "responsibilities")
    add("Phúc lợi", "benefits")
    add("Mô tả", "job_description")
    add("Giới thiệu công ty", "company_profile")
    desc = "\n".join(parts)[:4000]

    return {
        "id": row.get("job_id") or row.get("id") or "",
        "company": company,
        "title": title,
        "description": desc,
    }
