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
    assert neg.is_anomaly is True
    assert big.is_anomaly is True
    assert ok.is_anomaly is False


def test_find_anomalies_uses_threshold(account_move_class):
    AccountMove = account_move_class
    mid = AccountMove(name='mid', amount=5000, date=datetime.date.today())

    result = AccountMove.find_anomalies(threshold=4000)

    assert mid in result
    assert mid.is_anomaly is True


def test_find_anomalies_resets_flag(account_move_class):
    AccountMove = account_move_class
    mov = AccountMove(name='mov', amount=20000, date=datetime.date.today())

    AccountMove.find_anomalies()
    assert mov.is_anomaly is True

    mov.amount = 100
    result = AccountMove.find_anomalies()

    assert mov not in result
    assert mov.is_anomaly is False
