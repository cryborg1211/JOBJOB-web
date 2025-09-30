import io
import re
from typing import Optional

from fastapi import UploadFile, HTTPException


HTML_TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def clean_text(text: str) -> str:
    """Lowercase, strip HTML, normalize whitespace."""
    if text is None:
        return ""
    t = text.replace("\x00", " ")
    t = HTML_TAG_RE.sub(" ", t)
    t = t.lower()
    t = WS_RE.sub(" ", t).strip()
    return t


async def extract_text_from_file(file: UploadFile) -> str:
    """Extract text from .txt, .pdf, or .docx UploadFile."""
    filename = file.filename or "uploaded"
    name = filename.lower()

    try:
        if name.endswith(".txt"):
            data = await file.read()
            return clean_text(data.decode("utf-8", errors="ignore"))
        elif name.endswith(".pdf"):
            from pdfminer.high_level import extract_text
            buf = await file.read()
            return clean_text(extract_text(io.BytesIO(buf)))
        elif name.endswith(".docx"):
            from docx import Document
            buf = await file.read()
            doc = Document(io.BytesIO(buf))
            txt = "\n".join(p.text for p in doc.paragraphs)
            return clean_text(txt)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
    finally:
        await file.close()


