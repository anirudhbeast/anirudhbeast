from stock_analyzer.core.risk_management import position_size, risk_reward


def test_position_size():
    assert position_size(100000, 0.01, 100, 95) == 200


def test_risk_reward():
    assert risk_reward(100, 95, 110) == 2.0
