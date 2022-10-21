import re
from urllib.parse import urljoin

## -- Task 2 -- ##


def find_urls(
    html: str,
    base_url: str = "https://en.wikipedia.org",
    output: str = None,
) -> set:
    """Find all the url links in a html text using regex
    Arguments:
        html (str): html string to parse
        base_url (str, optional): Base url used to append URLs paths to.
        output (str, optional): Name of output file to save URLs to.

    Returns:
        url_set (set) : set with all the urls found in html text
    """

    # Finding all tags of the form <a stuff="..." href="...">,
    # i.e. everything starting with "<a" and ending with ">" is collected
    anchor_pattern = re.compile(r"<a[^>]+>", flags=re.IGNORECASE)
    anchor_tags = re.findall(anchor_pattern, html)

    url_pattern = r"""
    href="              # URL must begin with hyper-ref
    (?P<url>[^#\s]+)    # Find all characters but # and whitespaces
    (?:\#|")            # Want to ignore after # or " (fragment or end of url)
    """

    url_set = set()  # Where to save extracted URLs

    # Finding matches of urls in anchor tags
    for anchor_tag in anchor_tags:
        # Find URL, if any, in anchor tag and add it to URL set
        search_result = re.search(url_pattern, anchor_tag, re.VERBOSE)
        if search_result:
            # extracting url from search result
            url = search_result.group("url")
            if url[:2] == "//":
                # Add protocol from base url if missing
                url = base_url.split("//")[0] + url
            elif url[0] == "/":
                # if url path only add base_url
                url = base_url + url

            url_set.add(url)

    # Write to file if requested
    if output:
        print(f"Writing to: {output}")
        with open(output, "w") as outfile:
            for url in url_set:
                outfile.write(url + "\n")

    # Otherwise return set of URLs
    return url_set


def find_articles(html: str, output=None) -> set:
    """Finds all the wiki articles inside a html text. Make call to find urls, and filter
    arguments:
        text (str) : the html text to parse
        output (str, optional): name of output file to save article URLs to.

    returns:
        articles (set) : a set with urls to all the articles found
    """

    # Get all urls from HTML string
    urls = find_urls(html)

    pattern = r"""
    (?P<article>            # Name of group
    https?://               # Match protocol
    \w{2}\.                 # Match any language code
    wikipedia.org/wiki/     # Wikipedia article must contain "wikipedia.org/wiki/"
    [^:]+)                  # Exclude all links with color in them after protocol
    """

    # Empty set of article paths to fill
    articles = set()

    # Iterate though urls and add only the wikipedia articles to articles set
    for url in urls:
        search_result = re.search(pattern, url, re.VERBOSE)

        if search_result:
            article = search_result.group("article")
            articles.add(article)

    # Write to file if wanted
    if output:
        print(f"Writing to: {output}")
        with open(output, "w") as outfile:
            for article in articles:
                outfile.write(article + "\n")

    return articles


## Regex example
def find_img_src(html: str):
    """Find all src attributes of img tags in an HTML string

    Args:
        html (str): A string containing some HTML.

    Returns:
        src_set (set): A set of strings containing image URLs

    The set contains every found src attibute of an img tag in the given HTML.
    """
    # img_pat finds all the <img alt="..." src="..."> snippets
    # this finds <img and collects everything up to the closing '>'
    img_pat = re.compile(r"<img[^>]+>", flags=re.IGNORECASE)
    # src finds the text between quotes of the `src` attribute
    src_pat = re.compile(r'src="([^"]+)"', flags=re.IGNORECASE)
    src_set = set()
    # first, find all the img tags
    for img_tag in img_pat.findall(html):
        # then, find the src attribute of the img, if any
        src = src_pat.find(img_tag)
        src_set.add(src)
    return src_set
