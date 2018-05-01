# content of test_sample.py
def inc(x):
    return x + 1

def another():
    return 'what'

def test_answer():
    # assert inc(3) == 5
    assert inc(3) == 4
    assert another() == 'what'

test_answer()
