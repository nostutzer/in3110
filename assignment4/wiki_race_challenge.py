from ast import keyword
from typing import List

from requesting_urls import get_html
from filter_urls import find_articles
import re
import numpy as np
import random
import multiprocessing as mp


def get_number_of_matches(article: str) -> int:
    """Worker function that searches and returns number of matches of keyword in
       HTML of the input article link

    Args:
        article (str): URL of some Wikipedia article

    Returns:
        int: Number of matches of globalized search keyword (see initializer) in
             HTML string corresponding to input article URL.
    """
    # Get HTML string from input article URL
    article_html = get_html(article)

    # Find all matches of search keyword and compute length of corresponding list
    num_matches = len(
        re.findall(rf"\s?{final_keyword}\s?", article_html, re.IGNORECASE)
    )
    return num_matches


def initializer(keyword: str):
    """Parallel pool initializer function. Its job is only to globalize
       input keyword so it can be recognized inside get_number_of_matches

    Args:
        keyword (str): Input keyword to search a for in wikipedia article HTML.
    """
    # Globalizing input argument
    global final_keyword
    final_keyword = keyword


def find_path(start: str, finish: str) -> List[str]:
    """Find the shortest path from `start` to `finish`

    Arguments:
      start (str): wikipedia article URL to start from
      finish (str): wikipedia article URL to stop at

    Returns:
      path (list[str]):
        List of URLs representing the path from `start` to `finish`.
        The first item should be `start`.
        The last item should be `finish`.
        All items of the list should be URLs for wikipedia articles.
        Each article should have a direct link to the next article in the list.
    """

    # Path list to save each "step"
    path = [start]

    # Defining current URL
    current_url = start

    # Get the HTML of final URL
    final_html = get_html(finish)

    # Extract all main-title tags
    title_pattern = re.compile(r"<h1.*</h1>", flags=re.IGNORECASE)
    title_tag = re.search(title_pattern, final_html).group()

    # From all main-title tags extract the title and use it as search keyword
    title_pattern = re.compile(
        r'<span class="mw-page-title-main">(.+)</span>', flags=re.IGNORECASE
    )

    # Final keyword is title of target article
    finish_keyword = re.search(title_pattern, title_tag).group(1)

    # Informative print-outs
    print(f"Target keyword: {finish_keyword} \nSearching for matches:")
    print("# steps from start: ", len(path) - 1, "\nCurrent URL: ", current_url)

    # While we are not at the final article keep searching
    while current_url != finish:

        # Extract HTML of current article page
        html = get_html(current_url)

        # From current HTML get all wikipedia article URLs
        paths = find_articles(html)

        # Filter out all non-english articles
        paths = list([p for p in paths if "//en." in p])

        # If the target article is in the extracted paths we can stop
        # Else we look for matches in the HTMLs of the extracted article URLs.
        if finish in paths:
            path.append(finish)
            break
        else:
            # Define pool of parallel processes.
            # Each process takes a URL from the current wikipedia page
            # and requests the corresponding HTML. Finally the number of
            # matches to the final keyword are computed and gathered in a list.
            with mp.Pool(
                50, initializer=initializer, initargs=(finish_keyword,)
            ) as pool:
                # Compute number of final keyword matches for each URL in current article
                num_matches = np.array(pool.map(get_number_of_matches, paths))

            # From list of keyword matches find the one with most "hits"
            idx = np.argmax(num_matches)

            # Pick article URL with most hits
            article = paths[idx]

            # If any hits and if we have not picked the best URL before
            # we "click" on the link and choose it as new current URL
            if np.any(num_matches > 0) and article not in path:
                current_url = article
                path.append(current_url)

            # If no matches are found chose a random URL from current page.
            else:
                current_url = random.sample(paths, 1)[0]
                num_matches = [0]
                idx = 0
                if current_url not in path:
                    path.append(current_url)

        # Infomative print-out
        print("-" * 85)
        print(f"Target keyword: {finish_keyword}", f" # matches: {num_matches[idx]}")
        print("# steps from start: ", len(path) - 1, "\nCurrent URL: ", current_url)
        print("-" * 85)

    # More informative print-outs
    print("Number of URLs 'clicked': ", len(path) - 1)
    print("Last five URLs:\n", path[-5:])

    # Assert whether start and finish are the ones chosen as input
    assert path[0] == start
    assert path[-1] == finish

    # Return the "chain" of paths we "clicked" through
    return path


if __name__ == "__main__":
    # Define start and finish place for wikipedia golf game
    start = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    finish = "https://en.wikipedia.org/wiki/Peace"

    # Find shortest URL path between start and finish URLs
    paths = find_path(start, finish)
