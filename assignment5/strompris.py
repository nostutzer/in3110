#!/usr/bin/env python3
"""
This module fetches data 
from https://www.hvakosterstrommen.no/strompris-api
and visualize it as an Altair chart.
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

def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """Plotting energy prices data over time as interactive Altair line plot.

    Args:
        df (pd.DataFrame): Data frame with energy prices for given period of time and location
                           in Norway.

    Returns:
        alt.Chart: Interactive Altair chart in which the energy prices in NOK per kWh is plotted
                   as a function of time, separately for each location.
    """

    # Define chart of data
    chart = (
        alt.Chart(df)  # Provide altair with the data frame
        .mark_line()  # Want line plot
        .encode(
            x="time_start:T",  # Time on the x-axis
            y="NOK_per_kWh:Q",  # Energy price in NOK per kWh on y-axis
            color="location",  # One line plot per location
            tooltip=[
                "NOK_per_kWh",
                "time_start",
                "location_code",
                "location",
                "hourly_diff:Q",
                "daily_diff:Q",
                "weekly_diff:Q",
            ],  # Show tooltips when hovering over point in plot
        )
        .interactive()
    )   
    return chart

def compute_tooltips(df: pd.DataFrame, days: int) -> pd.DataFrame:
    """Helper function which for each hour in the input data frame
    computes the difference in energy price to; 
    - the previous hour 
    - the same hour of the previous day
    - the same hour and day of the previous week
    and adds these as separate columns to the data frame. 
    These columns can can then be used as tooltips in altair chart. 

    Args:
        df (pd.DataFrame): Data frame with hourly energy price 
                           for different regions of Norway.
        days (int): how many days back in time we want to retrieve 
                    energy prices.

    Returns:
        pd.DataFrame: Output data frame will be the same as input data frame, 
                      but with hourly, daily and weekly energy price differences
                      added as columns. The output data frame will also be shortened to
                      only contain the wanted number of days as rows.
    """
    # Add column to input DataFrame with difference in energy price to previous hour.
    
    # The groupby makes sure only differences are taken between prices in same location.
    df["hourly_diff"] = df[
        ["location_code", 
        "NOK_per_kWh"]
        ].groupby(["location_code"]).diff(1)
    
    # Add column to input DataFrame with difference in energy price to previous day (same hour)
    df["daily_diff"] = df[
        ["location_code", 
        "NOK_per_kWh"]
        ].groupby(["location_code"]).diff(24)
    
    # Add column to input DataFrame with difference in energy price to previous week (same day and hour)
    df["weekly_diff"] = df[
        ["location_code", 
        "NOK_per_kWh"]
        ].groupby(["location_code"]).diff(24 * 7)
    
    # We only return "days" of the previous data
    time_mask = (df.time_start > 
                pd.to_datetime(df.time_start.iloc[-1].date()
                               - datetime.timedelta(days=days - 1), 
                               utc = True))

    return df[time_mask]

def plot_daily_prices(df: pd.DataFrame) -> alt.Chart:
    """Function which from provided pandas data frame generates
    an altair line/point chart showing the daily average 
    energy price per region of Norway. Chart x-axis will
    be day of the week, y-axis will be daily mean NOK per kWh
    and tooltips showing up when hovering the curser above 
    plot points will include;
    - daily mean NOK per kWh 
    - exact date of average measurement
    - location name
    - location code

    Args:
        df (pd.DataFrame): Data frame of energy prices in different regions of Norway

    Returns:
        alt.Chart: Altair chart with daily average energy prices in
                   different regions of Norway to be shown on web app. 
    """

    # Define chart of data
    chart = (
        alt.Chart(df)  # Provide altair with the data frame
        .mark_line(point=True)  # Want line plot with dots
        .encode(
            x="day(time_start)",  # Day of the week on the x-axis
            y=alt.Y(field = "NOK_per_kWh", 
                    aggregate= "mean", 
                    axis = alt.Axis(title="Daily mean NOK_per_kWh")),  # Daily averaged energy price in NOK per kWh on y-axis
            color="location",  # One line plot per location
            tooltip=[
                "mean(NOK_per_kWh):Q",
                "yearmonthdate(time_start)",    # Show exact date when hovering over point in plot
                "location_code",                
                "location",                      
                ],                              # Show tooltips when hovering over point in plot
        ).interactive()
    )   
    return chart


def main():
    """Allow running this module as a script for testing."""
    # Get dataset of prices. Adding 14 days to days to ensure 
    # we get tooltip for weekly difference
    df = fetch_prices(days=7 + 14)
    
    #Compute tooltips to add to plot and add them as columns to data frame
    df = compute_tooltips(df, 7)

    # Get altair chart
    chart = plot_prices(df)

    # Get altair chart with daily mean
    chart_mean = plot_daily_prices(df)

    # Make a side-by-side compound plot of the two charts
    chart = chart | chart_mean

    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()


if __name__ == "__main__":
    main()
