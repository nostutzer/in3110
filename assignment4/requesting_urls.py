from typing import Dict, Optional

import requests

## -- Task 1 -- ##


def get_html(url: str, params: Optional[Dict] = None, output: Optional[str] = None):
    """Get an HTML page and return its contents.

    Args:
        url (str):
            The URL to retrieve.
        params (dict, optional):
            URL parameters to add.
        output (str, optional):
            (optional) path where output should be saved.
            The URL is saved to first line of output file, while the
            HTML string is saved to the subsequent lines.
    Returns:
        html (str):
            The HTML of the page, as text.
    """
    # passing the optional parameters argument to the get function
    response = requests.get(url, params=params)

    # getting the html text string from response object
    html_str = response.text

    if output:
        # if output is specified, the response txt and url get printed to a
        # txt file with the name in `output`
        with open(output, "w") as outfile:
            # Writing URL data to outfile in first line:
            outfile.write(url + "\n")

            # Writing HTML string to outfile from second line and on:
            outfile.write(html_str)

    return html_str
