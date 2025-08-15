from unittest.mock import patch

from freezegun import freeze_time

from src.utils import cards, currencies, day_time, stock_prices, top_transakpion


@freeze_time("2025-04-01 16:00:00")
def test_dey_time_1():
    created_at = "Добрый день"
    assert created_at == day_time()


@freeze_time("2025-04-01 07:00:00")
def test_dey_time_2():
    created_at = "Доброе утро"
    assert created_at == day_time()


@freeze_time("2025-04-01 01:00:00")
def test_dey_time_3():
    created_at = "Доброй ночи"
    assert created_at == day_time()


@freeze_time("2025-04-01 20:00:00")
def test_dey_time_4():
    created_at = "Добрый вечер"
    assert created_at == day_time()


def test_cards(sample_df):
    assert cards(sample_df) == [
        {"cashback": 2.0, "last_digits": "1111", "total_spent": 200},
        {"cashback": 3.0, "last_digits": "2222", "total_spent": 300},
        {"cashback": 4.0, "last_digits": "3333", "total_spent": 400},
        {"cashback": 5.0, "last_digits": "4444", "total_spent": 500},
        {"cashback": 1.0, "last_digits": "5091", "total_spent": 100},
        {"cashback": 6.0, "last_digits": "5555", "total_spent": 600},
        {"cashback": 7.0, "last_digits": "6666", "total_spent": 700},
        {"cashback": 8.0, "last_digits": "7777", "total_spent": 800},
        {"cashback": 9.0, "last_digits": "8888", "total_spent": 900},
    ]


def test_top_transakpion(sample_df):
    assert top_transakpion(sample_df) == [
        {"amount": 900, "category": "Супермаркеты", "date": "03.12.2024", "description": "FixPrice"},
        {"amount": 800, "category": "Супермаркеты", "date": "02.12.2024", "description": "Metro"},
        {"amount": 700, "category": "Кафе", "date": "01.12.2024", "description": "Кофейня"},
        {"amount": 600, "category": "Супермаркеты", "date": "03.11.2024", "description": "Ашан"},
        {"amount": 500, "category": "Кафе", "date": "02.11.2024", "description": "Шоколадница"},
    ]


def test_currencies():
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"rates": {"USD": 0.023}}
        result = currencies("USD")
        assert result == [{"currency": "USD", "rate": 43.48}]


def test_stock_prices():
    stocks = ["AAPL", "TSLA"]
    result = stock_prices(stocks)
    assert isinstance(result, list)
    assert any(stock["stock"] == "AAPL" for stock in result)
    assert any(stock["stock"] == "TSLA" for stock in result)
