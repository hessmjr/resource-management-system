import requests


def inc(x):
    return x + 1

def another():
    return 'what'

def test_answer():
    # assert inc(3) == 5
    assert inc(3) == 4
    assert another() == 'what'

def test_reqest():
    r = requests.get('http://httpbin.org/')
    assert r.status_code == 200

def test_ui():
    r = requests.get('http://localhost:5000/')
    assert r.status_code == 200

test_answer()
test_reqest()
test_ui()
