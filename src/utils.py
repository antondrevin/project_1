import datetime
import logging
import os

import finnhub  # type: ignore
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()


def day_time() -> str:
    """
    Приветствие
    """
    # now = datetime.datetime.now()
    now_time = int(datetime.datetime.now().strftime("%H"))

    if 18 <= now_time <= 21:
        resalt = "Добрый вечер"
    elif 6 <= now_time <= 10:
        resalt = "Доброе утро"
    elif 11 <= now_time <= 17:
        resalt = "Добрый день"
    else:
        resalt = "Доброй ночи"
    logging.info("обработка времени суток успешна")
    return resalt


def cards(df: pd.DataFrame) -> list[dict]:
    """
    общая информация о картах в формате:
    номер карты, сумма трат, кешбэк
    """
    filtered_df = df[df["Сумма платежа"] < 0]
    grouped_df = filtered_df.groupby("Номер карты")
    resalt_df = grouped_df["Сумма платежа"].sum().abs()
    cards_dict = resalt_df.to_dict()
    cards_list = []
    for k, v in cards_dict.items():
        cards_list.append({"last_digits": k[1:], "total_spent": round(v, 2), "cashback": round(v / 100, 2)})
    logging.info("Анализ карт завершен")
    return cards_list


def top_transakpion(df: pd.DataFrame) -> list[dict]:
    """
    топ 5 транзакций
    """
    df = df.sort_values("Сумма платежа")
    df_top = df[:5].to_dict(orient="records")
    top_list = []
    for i in df_top:
        top_list.append(
            {
                "date": i["Дата платежа"],
                "amount": i["Сумма платежа"] * (-1),
                "category": i["Категория"],
                "description": i["Описание"],
            }
        )
    logging.info("проведен анализ топ 5 транзакций")
    return top_list


def currencies(symbols: str) -> list[dict]:
    """Функция принимает валюту и возвращает курс"""
    base = "RUB"
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols}&base={base}"

    headers = {"apikey": os.getenv("APILAYER_KEY")}

    response = requests.get(url, headers=headers, data={})
    resalt_cur = []

    for k, v in response.json().get("rates").items():
        resalt_cur.append({"currency": k, "rate": round(1 / v, 2)})
    logging.info(f"выполнен API запрос о курсах валют: {symbols}")
    return resalt_cur


def stock_prices(stock: list) -> list[dict]:
    """
    Стоимость акций по API запросу
    """
    # Настройка клиента
    finnhub_client = finnhub.Client(api_key=os.getenv("APIFINN"))

    resalt_stock = []
    for i in stock:
        quote = finnhub_client.quote(i)
        resalt_stock.append({"stock": i, "price": quote["c"]})
    logging.info(f"выполне API запрос о стоимости акций: {stock}")

    return resalt_stock
