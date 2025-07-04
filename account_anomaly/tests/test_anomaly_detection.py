import datetime


def test_find_anomalies_detects_unusual_moves(account_move_class):
    AccountMove = account_move_class
    neg = AccountMove(name='neg', amount=-5, date=datetime.date.today())
    big = AccountMove(name='big', amount=20000, date=datetime.date.today())
    ok = AccountMove(name='ok', amount=100, date=datetime.date.today())

    result = AccountMove.find_anomalies()

    assert neg in result
    assert big in result
    assert ok not in result


def test_find_anomalies_uses_threshold(account_move_class):
    AccountMove = account_move_class
    mid = AccountMove(name='mid', amount=5000, date=datetime.date.today())

    result = AccountMove.find_anomalies(threshold=4000)

    assert mid in result
