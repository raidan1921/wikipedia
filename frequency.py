def compute_frequency(words: list[str]) -> dict[str, dict[str, float]]:
    """Compute count and percentage for each word."""
    total = len(words)
    freq: dict[str, int] = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1

    result: dict[str, dict[str, float]] = {}
    for w, count in freq.items():
        result[w] = {
            'count': count,
            'percentage': round(count / total * 100, 2)
        }
    return result


def filter_by_percentile(
    freq_dict: dict[str, dict[str, float]],
    percentile: int,
    ignore_list: set[str]
) -> dict[str, dict[str, float]]:
    """Filter out ignored words and keep those above the percentile threshold."""
    filtered = {w: data for w, data in freq_dict.items() if w not in ignore_list}
    percentages = sorted([data['percentage'] for data in filtered.values()])
    if not percentages:
        return {}

    k = max(0, min(len(percentages) - 1, int(len(percentages) * percentile / 100)))
    threshold = percentages[k]
    return {w: data for w, data in filtered.items() if data['percentage'] >= threshold}