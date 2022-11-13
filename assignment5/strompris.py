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
from typing import Tuple

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
                                        price information. If no date is provided
                                        date of today is used. Defaults to None.
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
    "NO1": "Oslo",
    "NO2": "Kristiansand",
    "NO3": "Trondheim",
    "NO4": "Tromsø",
    "NO5": "Bergen",
}

# task 1:


def fetch_prices(
    end_date: datetime.date = None,
    days: int = 7,
    locations: Tuple[str] = tuple(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """Fetch prices for multiple days and locations into a single DataFrame.

    Args:
        end_date (datetime.date, optional): Last day of which to fetch data. Defaults to None.
        days (int, optional): Number of days up until and including end_days from which to fetch data.
                              Defaults to 7.
        locations (Tuple[str], optional): Tuple of Norwegian location code strings.
                                          Must be "NOx" where x is in [1, 5].
                                          Defaults to tuple(LOCATION_CODES.keys()).

    Returns:
        pd.DataFrame: Pandas data frame of all gathered electricity data.
                      First column contains electricity price in NOK per kWh for all
                      days and locations. Second column contains start time for when
                      measurement was taken. Third and fourth columns contain the Norwegian
                      location code and name respectively as strings.
    """

    for location in locations:
        # Check if all locations provided are of the valid choices.
        assert location in LOCATION_CODES.keys()

    # If no end date is provided choose the date today
    if end_date is None:
        end_date = datetime.date.today()

    # Given end_date this is the first day from which to gather data
    start_date = end_date - datetime.timedelta(days=days - 1)

    # Define pandas data frame in which to accumulate data
    df_full = pd.DataFrame()

    for location in locations:
        for d in range(days):
            # Select date from which to request electricity price
            date = start_date + datetime.timedelta(days=d)

            # Fetch data from API
            df_day = fetch_day_prices(date, location)

            # Add location code and location name as columns
            df_day["location_code"] = location
            df_day["location"] = LOCATION_CODES[location]

            # Concatenate fetched data to full dataframe
            df_full = pd.concat((df_full, df_day), axis=0)

    return df_full


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
    df = fetch_prices()
    # chart = plot_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    # chart.show()


if __name__ == "__main__":
    main()
