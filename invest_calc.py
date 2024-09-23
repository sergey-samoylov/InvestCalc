#!/usr/bin/env python3
"""Passive Investment - Strategy Checker."""

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf


def main():
    total_investment, total_shares = 0, 0
    dca_log = []  # dollar_cost_averaging_log

    ticker, start, end, interval, amount = get_share_params()
    data = get_ticker_data(ticker, start, end)

    for date, row in resample_data(data, interval).iterrows():
        price = row["Adj Close"]
        total_investment += amount
        total_shares += amount / price
        dca_log.append(
            {
                "Date": date,
                "Price": price,
                "Total Shares": total_shares,
                "Total Investment": total_investment,
                "Portfolio Value": total_shares * price,
            }
        )
    # dollar cost averaging dataframe
    dca_df = calculate_profit(dca_log, total_shares, total_investment, data)
    visualize(dca_df, ticker)


def get_share_params():
    ticker = input("Which share shall we test [TSLA]: ").upper()
    start_date = input("Start investment month [2017-01-01]: ")
    end_date = input("End investment month [2024-09-01]: ")
    interval = input("Invest every [3] months: ") + "ME"
    amount = int(input("Your amount to invest [300]: "))
    return ticker, start_date, end_date, interval, amount


def get_ticker_data(ticker, start, end):
    "Get all ticker data from Yahoo Finance."
    data = yf.download(ticker, start=start, end=end)
    data = data.dropna()
    return data


def resample_data(data, interval):
    "Leave only months when investments were to be made."
    return data.resample(interval).first()


def calculate_profit(dca_log, total_shares, total_investment, data):
    dca_df = pd.DataFrame(dca_log)

    final_portfolio_value = int(total_shares * data.iloc[-1]["Adj Close"])
    total_profit = int(final_portfolio_value - total_investment)

    print(f"Final Value {final_portfolio_value}")
    print(f"Total Profit {total_profit}")
    return dca_df


def visualize(dca_df, ticker):
    plt.figure(figsize=(10, 6))
    plt.plot(
        dca_df["Date"],
        dca_df["Portfolio Value"],
        label="Portfolio Value",
    )
    plt.plot(
        dca_df["Date"],
        dca_df["Total Investment"],
        label="Invested Amount",
    )
    plt.xlabel("Date")
    plt.ylabel("Value in $")
    plt.title(f"Dollar Cost Averaging for {ticker}")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
