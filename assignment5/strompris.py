#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""

import datetime

import altair as alt
import pandas as pd
import requests
import requests_cache

# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()


# task 5.1:


def fetch_day_prices(date: datetime.date = None, location: str = "NO1") -> pd.DataFrame:
    """Fetch one day of data for one location from hvakosterstrommen.no API. Note that
    when passing daylight saving we omit the last hour of that day for simplicity sake.

    Args:
        date (datetime.date, optional): Date from which to download electricity
                                        price information. Defaults to None.
        location (str, optional): Norwegian location code from which to
                                  gather electricity price. Defaults to "NO1".

    Returns:
        pd.DataFrame: Data frame containing the electricity price (first column)
                      in NOK per kWh at any hour during the selected day (second column)"""
    if date is None:
        # If no date is provided choose the date today
        date = datetime.date.today()

    # First allowed date 2nd October 2022, raise error if date is before min_date
    min_date = datetime.date(2022, 10, 2)
    assert min_date <= date

    # Extracting year, month and day from datetime object as string
    year = date.strftime("%Y")
    # Using formatting %m and %d to ensure zero padded month and day respectively
    month = date.strftime("%m")
    day = date.strftime("%d")

    # API's URL
    url = f"https://www.hvakosterstrommen.no/api/v1/prices/{year}/{month}-{day}_{location}.json"
    # Request json from API
    r = requests.get(url)

    # Re-formatting requested json into pandas data frame.
    df = pd.DataFrame(r.json())

    # We want only columns with "NOK_per_kWh" and "time_start"
    df = df[["NOK_per_kWh", "time_start"]]

    # Convert date time in last tow columns to wanted datetime format
    df["time_start"] = pd.to_datetime(df["time_start"], utc=True).dt.tz_convert(
        "Europe/Oslo"
    )

    # If number of rows, i.e. number of hours in date is more than 24 we are in
    # daylight saving and will omit the last hour of that day for simplicity sake
    # (there might be better ways we could implement in the future).
    if df.shape[0] > 24:
        df = df.iloc[:-1, :]

    return df


# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = {
    "NO1": "Oslo / Øst-Norge",
    "NO2": "Kristiansand / Sør-Norge",
    "NO3": "Trondheim / Midt-Norge",
    "NO4": "Tromsø / Nord-Norge",
    "NO5": "Bergen / Vest-Norge",
}

# task 1:


def fetch_prices(
    end_date: datetime.date = None,
    days: int = 7,
    locations=tuple(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """Fetch prices for multiple days and locations into a single DataFrame

    Make sure to document arguments and return value...
    ...
    """
    if end_date is None:
        end_date = ...

    ...


# task 5.1:


def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot energy prices over time

    x-axis should be time_start
    y-axis should be price in NOK
    each location should get its own line

    Make sure to document arguments and return value...
    """
    ...


# Task 5.4


def plot_daily_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot the daily average price

    x-axis should be time_start (day resolution)
    y-axis should be price in NOK

    You may use any mark.

    Make sure to document arguments and return value...
    """
    ...


# Task 5.6

ACTIVITIES = {
    # activity name: energy cost in kW
    ...
}


def plot_activity_prices(
    df: pd.DataFrame, activity: str = "shower", minutes: float = 10
) -> alt.Chart:
    """
    Plot price for one activity by name,
    given a data frame of prices, and its duration in minutes.

    Make sure to document arguments and return value...
    """

    ...


def main():
    """Allow running this module as a script for testing."""
    df = fetch_day_prices(datetime.date(2022, 10, 30), "NO1")
    df = fetch_day_prices(datetime.date(2022, 10, 29), "NO1")

    # df = fetch_prices()
    # chart = plot_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    # chart.show()


if __name__ == "__main__":
    main()
