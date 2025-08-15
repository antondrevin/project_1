import calendar
import logging

import pandas as pd


def categories_cashback(transactions: pd.DataFrame, year: str, month: str) -> dict:
    """
    анализ кешбэка по категориям за выбранный месяц
    """
    df = transactions
    # print(df)
    logging.info(f"Анализ кэшбэка по категориям за {year}-{month}")
    end_date = calendar.monthrange(int(year), int(month))[1]
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True)
    # print(df)
    filtered_df_date = df.loc[df["Дата платежа"] >= f"{year}-{month}-01"].loc[
        df["Дата платежа"] <= f"{year}-{month}-{end_date}"
    ]
    # print(filtered_df_date)
    filtered_df_negativ = filtered_df_date[filtered_df_date["Сумма платежа"] < 0]
    # print(filtered_df_negativ)
    grouped_df = filtered_df_negativ.groupby("Категория")
    resalt_df = grouped_df["Сумма платежа"].sum().abs()
    cards_dict = resalt_df.to_dict()
    resalt = {}
    for k, v in cards_dict.items():
        resalt[k] = int(v / 100)
    return resalt
