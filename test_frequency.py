import pytest
from frequency import compute_frequency, filter_by_percentile


def test_compute_frequency_empty():
    assert compute_frequency([]) == {}


def test_compute_frequency_basic():
    words = ['a', 'b', 'a']
    freq = compute_frequency(words)
    assert freq['a']['count'] == 2
    assert freq['b']['count'] == 1
    assert freq['a']['percentage'] == pytest.approx(66.67, 0.01)
    assert freq['b']['percentage'] == pytest.approx(33.33, 0.01)


def test_filter_by_percentile_and_ignore():
    freq_dict = {
        'a': {'count': 2, 'percentage': 50},
        'b': {'count': 1, 'percentage': 25},
        'c': {'count': 1, 'percentage': 25}
    }
    # ignore 'b', percentile=50 should keep top half (a)
    filtered = filter_by_percentile(freq_dict, 50, {'b'})
    assert 'a' in filtered and 'b' not in filtered
    assert 'c' not in filtered