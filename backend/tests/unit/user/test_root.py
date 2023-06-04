from tests.unit.user import client


def test_index(app, client):
    res = client.get('/user/home')
    assert res.status_code == 200
