"""FastAPI web app that generates an interactive Altair plot of 
energy prices of five different regions within Norway
downloaded from the https://www.hvakosterstrommen.no/strompris-api . 
The plot is rendered as a nice informative web app using FastAPI."""

import os
import datetime
from typing import List, Optional, Dict

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from starlette.routing import Mount, BaseRoute
from starlette.staticfiles import StaticFiles

from strompris import (
    LOCATION_CODES,
    fetch_prices,
    plot_daily_prices,
    plot_prices,
    compute_tooltips,
)

def route_to_docs() -> List[BaseRoute]:
    """Helper function which will mount the Sphinx
    documentation directory as a StaticFile. The function
    then returns a BaseRoute used to handle the "GET /help"
    request when clicking on web app "help" button in 
    navigation bar

    Returns:
        List[BaseRoute]: BaseRoute static routes used to initialize app and links
                         to the sphinx documentation.
    """

    # Path to docs when simply running app.py as script
    path2docs = "docs/_build/html"

    # If imported as module from docs folder
    # we construct absolute path for documentation
    # directory. Else an error is triggered when the 
    # documentation directory is not found.
    if __name__ != "__main__" and "docs" in os.getcwd():
        path2docs = os.getcwd() + "/_build/html"

    docs = Mount(
        path = "/help",     # Want to get to sphinx docs when "/help" is appended to API url
        app = StaticFiles(directory=path2docs, html=True), # Generating static files in docs folder
        name = "help"
    )
    return [docs]


# Define app and template objects
app = FastAPI(routes=route_to_docs())
templates = Jinja2Templates(directory="templates")

# Get location code keys
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
                              Defaults to Query(default=7).

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

if __name__ == "__main__":
    import uvicorn

    # Run web application on ip addresss 127.0.0.1 at port 5000
    uvicorn.run(app, host="127.0.0.1", port=5000)
