"""
Notebook loader module to extract preprocessing functions from resume-job.ipynb
"""
import re
from typing import Dict, Any, Callable
import pandas as pd
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize

# Initialize NLTK components
try:
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
except LookupError:
    # Download required NLTK data if not available
    nltk.download("punkt", quiet=True)
    nltk.download("wordnet", quiet=True)
    nltk.download("stopwords", quiet=True)
    nltk.download("omw-1.4", quiet=True)
    nltk.download("averaged_perceptron_tagger", quiet=True)
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()

# Regex patterns from notebook
URL_RE = re.compile(r"https?://\S+|www\.\S+")
EMAIL_RE = re.compile(r"\S+@\S+")
PHONE_RE = re.compile(r"(\+?\d[\d\-\s\(\)]{6,}\d)")
MULTI_SPACE_RE = re.compile(r"\s+")
NON_ALPHANUMERIC_RE = re.compile(r"[^A-Za-z0-9\+\#\.\-\s]")


def strip_html(text: str) -> str:
    """Remove HTML tags from text"""
    if pd.isna(text):
        return ""
    return BeautifulSoup(str(text), "lxml").get_text(separator=" ")


def basic_clean(text: str, remove_digits: bool = False) -> str:
    """
    Basic text cleaning function extracted from notebook
    - Remove HTML tags
    - Remove URLs, emails, phone numbers
    - Remove non-alphanumeric characters (except +, #, ., -)
    - Normalize whitespace
    - Convert to lowercase
    """
    if pd.isna(text):
        return ""
    s = str(text)
    s = strip_html(s)
    s = URL_RE.sub(" ", s)
    s = EMAIL_RE.sub(" ", s)
    s = PHONE_RE.sub(" ", s)
    s = NON_ALPHANUMERIC_RE.sub(" ", s)
    if remove_digits:
        s = re.sub(r"\d+", " ", s)
    s = MULTI_SPACE_RE.sub(" ", s)
    return s.strip().lower()


def penn_to_wordnet_pos(tag: str) -> str:
    """Convert Penn Treebank POS tag to WordNet POS tag"""
    if tag.startswith('J'):
        return wordnet.ADJ
    if tag.startswith('V'):
        return wordnet.VERB
    if tag.startswith('N'):
        return wordnet.NOUN
    if tag.startswith('R'):
        return wordnet.ADV
    return wordnet.NOUN


def tokenize_lemmatize(text: str, keep_pos: str = None, keep_only_tech: bool = False, 
                      tech_vocab: set = None, min_len: int = 2) -> str:
    """
    Tokenize and lemmatize text function extracted from notebook
    - Tokenize using NLTK
    - POS tagging
    - Remove stopwords
    - Lemmatize based on POS
    - Filter by minimum length
    """
    if not text:
        return ""
    tokens = word_tokenize(text)  # NLTK tokenizer
    # POS tagging
    pos_tags = pos_tag(tokens)
    out_tokens = []
    for tok, tag in pos_tags:
        tok_lower = tok.lower().strip()
        if tok_lower in stop_words:
            continue
        if len(tok_lower) < min_len:
            continue
        pos = penn_to_wordnet_pos(tag)
        lemma = lemmatizer.lemmatize(tok_lower, pos=pos)
        lemma = lemma.strip()
        if not lemma:
            continue
        if keep_only_tech:
            if tech_vocab is None:
                continue
            # exact-match to tech vocab (vocab should be lowercased)
            if lemma in tech_vocab:
                out_tokens.append(lemma)
        else:
            out_tokens.append(lemma)
    return " ".join(out_tokens)


# Note: Notebook loading functionality removed for simplicity
# The preprocessing functions are directly implemented above


# Export the main functions
__all__ = ['basic_clean', 'tokenize_lemmatize', 'strip_html', 'penn_to_wordnet_pos']
