import types
from preprocess import clean_text
from inference import ModelHandle, predict


def test_clean_text_basic():
    assert clean_text('<b>Hello</b>   World') == 'hello world'


def test_predict_mock():
    # Mock a sentence-transformers like handle that returns deterministic cosine
    class FakeEnc:
        def encode(self, arr):
            return [[1,0,0], [1,0,0]]  # cosine = 1

    handle = ModelHandle(kind="st", model=None, encoder=FakeEnc())
    score, feats = predict(handle, 'java python', 'python java developer')
    assert 0.99 <= score <= 1.0
    assert isinstance(feats, list)


