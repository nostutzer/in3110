import datetime
from typing import List, Optional

import altair as alt
import json
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from strompris import (
    ACTIVITIES,
    LOCATION_CODES,
    fetch_day_prices,
    fetch_prices,
    plot_activity_prices,
    plot_daily_prices,
    plot_prices,
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
location_code_keys = tuple(LOCATION_CODES.keys())

# `GET /` should render the `strompris.html` template
# with inputs:
# - request
# - location_codes: location code dict
# - today: current date


@app.get("/", response_class=HTMLResponse)
def render_strompris(
    request: Request,
    locations_codes: List[str] = Query(default=location_code_keys),
    today: Optional[str] = Query(default=None),
):
    locations = [LOCATION_CODES[location] for location in locations_codes]
    if today is None:
        today = datetime.date.today()
    else:
        today = datetime.date.fromisoformat(today)

    return templates.TemplateResponse(
        "strompris.html",
        {
            "request": request,
            "location_codes": LOCATION_CODES,
            "locations": locations,
            "today": today,
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


@app.get("/plot_prices.json", response_class=HTMLResponse)
def plot_prices_json(
    request: Request,
    locations: List[str] = Query(default=location_code_keys),
    end: Optional[str] = Query(default=None),
    days: int = Query(default=8),
):
    print(locations)
    print(days)
    print(end)
    if end is None:
        end = datetime.date.today()
    else:
        end = datetime.date.fromisoformat(end)

    # Get dataset of prices
    df = fetch_prices(end_date=end, days=days, locations=tuple(locations))

    # Get altair chart
    chart = plot_prices(df)

    # Convert altair plot to json
    chart_json = json.dumps(chart.to_dict())

    return chart_json


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
    # use uvicorn to launch your application on port 5000
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=5000)
