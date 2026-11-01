from crypto_trading.strategies import MajorsStrategy

def test_majors_buy():
    s = MajorsStrategy()
    signal = s.generate_signal({"price": 70000, "ema_50": 65000})
    assert signal == "BUY"

def test_majors_hold():
    s = MajorsStrategy()
    signal = s.generate_signal({"price": 65000, "ema_50": 65000})
    assert signal == "HOLD"
