from wiki_scraper import parse_text_and_links, tokenize


def test_parse_text_and_links_no_content(tmp_path):
    html = "<html><body>No content here</body></html>"
    text, links = parse_text_and_links(html)
    assert text == ""
    assert links == []


def test_tokenize():
    text = "Hello, World! It's 2025."
    tokens = tokenize(text)
    assert tokens == ['hello', 'world', "it's"]