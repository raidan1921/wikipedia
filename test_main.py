import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_traverse(monkeypatch):
    # Mock traverse_articles_async to return a predictable list
    async def fake_traverse_async(article, depth):
        return ['foo', 'bar', 'foo']
    monkeypatch.setattr('main.traverse_articles_async', fake_traverse_async)
    return fake_traverse_async


def test_word_frequency_success():
    response = client.get('/word-frequency', params={'article': 'Test', 'depth': 0})
    assert response.status_code == 200
    data = response.json()
    # 'foo' appears twice, 'bar' once
    assert data['foo']['count'] == 2
    assert data['bar']['count'] == 1


def test_keywords_success():
    payload = {
        'article': 'Test',
        'depth': 0,
        'ignore_list': ['bar'],
        'percentile': 0
    }
    response = client.post('/keywords', json=payload)
    assert response.status_code == 200
    data = response.json()
    # 'bar' should be ignored, 'foo' retained
    assert 'bar' not in data
    assert 'foo' in data


def test_validation_errors():
    # Missing required params/body
    resp = client.get('/word-frequency', params={'depth': 1})
    assert resp.status_code == 422
    resp = client.post('/keywords', json={})
    assert resp.status_code == 422