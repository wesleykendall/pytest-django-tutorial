from django import urls


def test_marketing_site(client):
    """
    Verify that the marketing site renders as expected
    """
    url = urls.reverse('marketing:landing')
    resp = client.get(url)
    assert resp.status_code == 200
    assert b'Welcome to Meme Creator!' in resp.content
