# Strømpris Web App
In this directory you will find the code and documentation
to the Strømpris web app which gathers energy price data
from the [Hva koster strømmen](https://www.hvakosterstrommen.no/strompris-api) API and displays an informative and interactive plot in a web page.

## Requeirements and Installation
In order to run the codes in this directory we recommend that a new `conda` environment is created first. Specifically, there are several dependencies that one needs to install to run the codes in this directory. All these dependencies are found in the [`requirements.txt`](requirements.txt) file. We can, using this file, directly create a `conda` environment with all the needed dependencies (and also some more that were used to run code in the previous assignments) by simply running 

> `$ conda create --name <name of my environment> --file requirements.txt`

in a terminal. Make sure that you are in the `assignment5` directory before you create the environment; so that the `requirements.txt` file is found.
To activate your environment type 

> `$ conda activate <name of my environment>`

As all the requirements are listed in the `requiremnts.txt` file we will omit listing them all here and only list the most central ones used for this assignment;

* `altair`
* `altair-viewer`
* `beautifulsoup4`
* `fastapi`
* `pandas`
* `pytest`
* `requests`
* `requests-cache`
* `uvicorn`

## Running the Code

Once a new `conda` environment with all the requirements is created and activated we can run the codes. 

There are two main codes in this directory; 
1) `strompris.py` -- containing all the functions that interact with the [Hva koster strømmen](https://www.hvakosterstrommen.no/strompris-api) API, collect the data as `pandas` DataFrames and makes some interactive `altair` charts.
2) `app.py` -- Contains the `FastAPI` app which renders the `HTML` page from the `template/strompris.html` template, with the `altair` plots made using the `strompris.py` code.

### Usage Example; `strompris.py`
In the `strompris.py` code there is a main block which will be run when the code is executed as a script; `python -m strompris strompris.py`. The code in the `strompris.py` main block is a nice usage example of how the functions in the code are to be used:

```python
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
```

### Usage Example; `app.py`

In order to run the web app in `app.py` we simply need to run 
``

> `$ python -m app app.py`

in the terminal. Then the following should appear in the terminal;

```
    INFO:     Started server process [33694]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    INFO:     Uvicorn running on http://127.0.0.1:5000 (Press CTRL+C to quit)
```
To access the web app now simply copy and paste the URL printed in the terminal `http://127.0.0.1:5000` into your favorite internet browser. The web app page itself is pretty self explanatory and will hence not be described here.

### Running Unit Tests
If changes are made to the code you should test whether the modifications still pass the unit tests provided in the `test` sub-directory. The unit tests are simply run by typing 

> `python -m pytest -v test`

```
    ======================================= test session starts ========================================
    platform darwin -- Python 3.10.4, pytest-7.1.3, pluggy-1.0.0 -- /opt/homebrew/Caskroom/miniconda/base/envs/in4110/bin/python3
    cachedir: .pytest_cache
    rootdir: /Users/nilsoles/Documents/IN3110-nilsoles/assignment5
    plugins: anyio-3.6.1
    collected 13 items

    tests/test_app.py::test_main_page PASSED                                                     [  7%]
    tests/test_app.py::test_form_input PASSED                                                    [ 15%]
    tests/test_app.py::test_plot_prices_json[None-None-None] PASSED                              [ 23%]
    tests/test_app.py::test_plot_prices_json[locations1-2022-11-05-2] PASSED                     [ 30%]
    tests/test_app.py::test_plot_prices_json[locations2-2022-11-03-1] PASSED                     [ 38%]
    tests/test_strompris.py::test_fetch_day_prices_defaults PASSED                               [ 46%]
    tests/test_strompris.py::test_fetch_day_prices_columns PASSED                                [ 53%]
    tests/test_strompris.py::test_fetch_day_prices[date0-NO1] PASSED                             [ 61%]
    tests/test_strompris.py::test_fetch_day_prices[date1-NO5] PASSED                             [ 69%]
    tests/test_strompris.py::test_fetch_prices_default PASSED                                    [ 76%]
    tests/test_strompris.py::test_fetch_prices PASSED                                            [ 84%]
    tests/test_strompris.py::test_plot_prices PASSED                                             [ 92%]
    tests/test_strompris.py::test_plot_daily_prices PASSED                                       [100%]

    ========================================= warnings summary =========================================
    tests/test_app.py::test_plot_prices_json[None-None-None]
    tests/test_app.py::test_plot_prices_json[locations1-2022-11-05-2]
    tests/test_app.py::test_plot_prices_json[locations2-2022-11-03-1]
    tests/test_strompris.py::test_plot_prices
    tests/test_strompris.py::test_plot_daily_prices
    /opt/homebrew/Caskroom/miniconda/base/envs/in4110/lib/python3.10/site-packages/altair/utils/core.py:317: FutureWarning: iteritems is deprecated and will be removed in a future version. Use .items instead.
        for col_name, dtype in df.dtypes.iteritems():

    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    ================================== 13 passed, 5 warnings in 0.91s ==================================
```

## Sphinx Documentation
For a more comprehensive documentation of the functions in the codes in this directory we have provided a `Sphinx` generated documentation page. This documentation can either be accessed by opening the [`docs/_build/html/index.html`](docs/_build/html/index.html) file in a browser or by first running the web app (`app.py`) and then clicking on the "help" button in the navigation bar. Also found in the navigation bar is the FastAPI generated documentation of the web app itself.