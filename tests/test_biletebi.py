import HomePage


def test_search_event(page):
    home = HomePage(page)

    home.open()
    home.search_event("concert")

    results = home.get_search_results()

    assert results.count() > 0