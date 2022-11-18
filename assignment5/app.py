import datetime
from typing import List, Optional, Dict

import altair as alt
import json
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import starlette
from strompris import (
    ACTIVITIES,
    LOCATION_CODES,
    fetch_day_prices,
    fetch_prices,
    plot_activity_prices,
    plot_daily_prices,
    plot_prices,
    compute_tooltips,
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
location_code_keys = tuple(LOCATION_CODES.keys())

@app.get("/", response_class=HTMLResponse)
def render_strompris(
    request: Request,
    today: Optional[str] = Query(default=None),
):
    """Function handles the "GET /" request from strømpris web app to
       render the HTML template using Jinja.

    Args:
        request (Request): Request object from FastAPI.
        today (Optional[str], optional): String of a date in ISO formate. Defaults to Query(default=None). 
                                         If no date is provided the None will be changes to the date of today.

    Returns:
        _type_: Template response to strompris.html HTML template with parameters as a dict
                for rendering the HTML page.
                
    """

    # If no date is provided the current date is used.
    # Else the provided date is used.
    if today is None:
        today_date = datetime.date.today()
    else:
        today_date = datetime.date.fromisoformat(today)

    # Returning response to render HTML template
    return templates.TemplateResponse(
        "strompris.html",
        {
            "request": request,
            "location_codes": LOCATION_CODES,
            "today": today_date,
        },
    )


# GET /plot_prices.json should take inputs:
# - locations (list from Query)
# - end (date)
# - days (int, default=7)
# all inputs should be optional
# return should be a vega-lite JSON chart (alt.Chart.to_dict())
# produced by `plot_prices`
# (task 5.6: return chart stacked with plot_daily_prices)


@app.get("/plot_prices.json")
def plot_prices_json(
    locations: List[str] = Query(default=location_code_keys),
    end: Optional[str] = Query(default=None),
    days: int = Query(default=7),
) -> Dict:
    """Function which handles the "GET /plot_prices.json" request and
       returns an Altair chart with enegry prices from 
       https://www.hvakosterstrommen.no/ API.


    Args:
        locations (List[str], optional): List of strings containing location keys in Norway
                                         for which to retrieve a chart of energy prices. 
                                         Defaults to Query(default=location_code_keys).
        end (Optional[str], optional): End date up to which to retrieve energy prices. 
                                       Defaults to Query(default=None).
        days (int, optional): How many days back in time from end for which to retrieve energy prices. 
                              Defaults to Query(default=8).

    Returns:
        str: json string formatting of Altair chart containing energy prices.
    """

    # If no date is provided the current date is used.
    # Else the provided date is used.
    if end is None:
        end_date = datetime.date.today()
    else:
        end_date = datetime.date.fromisoformat(end)

    # Get dataset of prices. Adding 14 days to days to ensure we get tooltip for weekly difference
    df = fetch_prices(end_date=end_date, days=days + 14, locations=tuple(locations))
    
    #Compute tooltips to add to plot and add them as columns to data frame
    df = compute_tooltips(df, days)

    # Get altair chart
    chart = plot_prices(df)

    # Get altair chart with daily mean
    chart_mean = plot_daily_prices(df)

    # Make a side-by-side compound plot of the two charts
    chart = chart | chart_mean

    # Convert altair plot to json dict
    return chart.to_dict()


# Task 5.6:
# `GET /activity` should render the `activity.html` template
# activity.html template must be adapted from `strompris.html`
# with inputs:
# - request
# - location_codes: location code dict
# - activities: activity energy dict
# - today: current date


# Task 5.6:
# `GET /plot_activity.json` should return vega-lite chart JSON (alt.Chart.to_dict())
# from `plot_activity_prices`
# with inputs:
# - location (single, default=NO1)
# - activity (str, default=shower)
# - minutes (int, default=10)


# mount your docs directory as static files at `/help`


if __name__ == "__main__":
    import uvicorn

    # Run web application on ip addresss 127.0.0.1 at port 5000
    uvicorn.run(app, host="127.0.0.1", port=5000)
