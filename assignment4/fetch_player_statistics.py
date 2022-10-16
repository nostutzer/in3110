import os
import re
from operator import itemgetter
from typing import Dict, List
from urllib.parse import urljoin

import numpy as np
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from cycler import cycler
from requesting_urls import get_html
import pandas as pd

## --- Task 8, 9 and 10 --- ##

try:
    import requests_cache
except ImportError:
    print("install requests_cache to improve performance")
    pass
else:
    requests_cache.install_cache()

base_url = "https://en.wikipedia.org"


def find_best_players(url: str) -> None:
    """Find the best players in the semifinals of the nba.

    This is the top 3 scorers from every team in semifinals.
    Displays plot over points, assists, rebounds

    arguments:
        - html (str) : html string from wiki basketball
    returns:
        - None
    """
    # gets the teams
    teams = get_teams(url)
    # assert len(teams) == 8

    # Gets the player for every team and stores in dict (get_players)
    all_players = {team["name"]: get_players(team["url"]) for team in teams}

    # get player statistics for each player,
    # using get_player_stats
    for team, players in all_players.items():
        for i, player in enumerate(players):
            player_name = player["name"]
            player_url = player["url"]
            # print(all_players[team][player_name])
            # print(team, player_name, player_url)
            player_stats = get_player_stats(player_url, team)
            # print(player_stats)
            if len(player_stats) >= 3:
                all_players[team][i]["points"] = player_stats["points"]
                all_players[team][i]["assists"] = player_stats["assists"]
                all_players[team][i]["rebounds"] = player_stats["rebounds"]
            else:
                all_players[team][i]["points"] = 0
                all_players[team][i]["assists"] = 0
                all_players[team][i]["rebounds"] = 0

    # at this point, we should have a dict of the form:
    # {
    #     "team name": [
    #         {
    #             "name": "player name",
    #             "url": "https://player_url",
    #             # added by get_player_stats
    #             "points": 5,
    #             "assists": 1.2,
    #             # ...,
    #         },
    #     ]
    # }

    # Select top 3 for each team by points:
    best = {}
    for team, players in all_players.items():
        # Construct Pandas dataframe for each team to better extract top 3
        df = pd.DataFrame(players)
        # Sort and extract top 3 based on points
        top_3 = df.nlargest(3, "points")

        # "records" gives list of player dicts
        best[team] = top_3.to_dict("records")

    stats_to_plot = ["points", "assists", "rebounds"]
    for stat in stats_to_plot:
        plot_best(best, stat=stat)


def plot_best(best: Dict[str, List[Dict]], stat: str = "points") -> None:
    """Plots a single stat for the top 3 players from every team.

    Arguments:
        best (dict) : dict with the top 3 players from every team
            has the form:

            {
                "team name": [
                    {
                        "name": "player name",
                        "points": 5,
                        ...
                    },
                ],
            }

            where the _keys_ are the team name,
            and the _values_ are lists of length 3,
            containing dictionaries about each player,
            with their name and stats.

        stat (str) : [points | assists | rebounds] which stat to plot.
            Should be a key in the player info dictionary.
    """
    stats_dir = "NBA_player_statistics/"
    # Check if output directry exists, otherwise create it
    if not os.path.exists(stats_dir):
        os.mkdir(stats_dir)

    # Setting colors to cycle through
    my_cycler = cycler(color=["r", "g", "b"])
    plt.rc("axes", prop_cycle=my_cycler)

    # Making a figure and axis object
    fig, ax = plt.subplots(figsize=(10, 8))

    # Number of players in total
    num_players = 24
    offset = 0

    xticks = []

    # Maximum number of stat
    max_stat = 0

    # Iterate though each team
    for i, (team, players) in enumerate(best.items()):
        # Save xtick position of each team
        xticks.append(i + 1 + offset)
        for j, player in enumerate(players):
            # Add bar for player
            ax.bar(i + j + offset, player[stat], width=0.9)

            # Add name of player
            ax.text(
                i + j + offset - 0.3,
                player[stat] + 0.3,
                player["name"],
                rotation=90,
                fontsize=9,
            )
            max_stat = np.max((max_stat, player[stat]))

        # update offset of bars for each team
        offset += 4

    # Set axis labels
    ax.set_ylabel(f"{stat}")
    ax.set_xlabel("Team")

    # change tick labels to team name
    ax.set_xticks(xticks)
    ax.set_xticklabels(best.keys(), rotation=45)

    # setting y-limit so names don't get squished
    ax.set_ylim(0, max_stat * 1.35)

    # Add legend
    ax.legend(["first", "second", "third"])

    # set figure title
    ax.set_title(f"Best players of each team in terms of: {stat}")

    # save image to png
    fig.savefig(stats_dir + stat + ".png", bbox_inches="tight")
    plt.show()


def get_teams(url: str) -> list:
    """Extracts all the teams that were in the semi finals in nba

    arguments:
        - url (str) : url of the nba finals wikipedia page
    returns:
        teams (list) : list with all teams
            Each team is a dictionary of {'name': team name, 'url': team page
    """
    # Get the table
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="Bracket").find_next("table")

    # find all rows in table
    rows = table.find_all("tr")
    rows = rows[2:]
    # maybe useful: identify cells that look like 'E1' or 'W5', etc.
    seed_pattern = re.compile(r"^[EW][1-8]$")

    # lots of ways to do this,
    # but one way is to build a set of team names in the semifinal
    # and a dict of {team name: team url}

    team_links = {}  # dict of team name: team url
    in_semifinal = set()  # set of teams in the semifinal

    # Loop over every row and extract teams from semi finals
    # also locate the links tot he team pages from the First Round column
    for row in rows:
        cols = row.find_all("td")
        # useful for showing structure
        # print([c.get_text(strip=True) for c in cols])

        # TODO:
        # 1. if First Round column, record team link from `a` tag
        # 2. if semifinal column, record team name

        # quarterfinal, E1/W8 is in column 1
        # team name, link is in column 2
        if len(cols) >= 3 and seed_pattern.match(cols[1].get_text(strip=True)):
            team_col = cols[2]
            a = team_col.find("a")
            team_links[team_col.get_text(strip=True)] = urljoin(base_url, a["href"])

        elif len(cols) >= 4 and seed_pattern.match(cols[2].get_text(strip=True)):
            team_col = cols[3]
            in_semifinal.add(team_col.get_text(strip=True))

        elif len(cols) >= 5 and seed_pattern.match(cols[3].get_text(strip=True)):
            team_col = cols[4]
            in_semifinal.add(team_col.get_text(strip=True))

    # return list of dicts (there will be 8):
    # [
    #     {
    #         "name": "team name",
    #         "url": "https://team url",
    #     }
    # ]

    assert len(in_semifinal) == 8
    return [
        {
            "name": team_name.rstrip("*"),
            "url": team_links[team_name],
        }
        for team_name in in_semifinal
    ]


def get_players(team_url: str) -> list:
    """Gets all the players from a team that were in the roster for semi finals
    arguments:
        team_url (str) : the url for the team
    returns:
        player_infos (list) : list of player info dictionaries
            with form: {'name': player name, 'url': player wikipedia page url}
    """
    print(f"Finding players in {team_url}")

    # Get base URL
    base_url = team_url.split("/wiki/")[0]

    # Get the table
    html = get_html(team_url)
    soup = BeautifulSoup(html, "html.parser")
    roster = soup.find(id="Roster")

    # Find "table" inside table
    table = roster.find_next("table").find("table")

    players = []
    # Loop over every row and get the names from roster
    rows = table.find_all("tr")

    # Skipping first row as this is a table header
    for row in rows[1:]:
        # Get the columns
        cols = row.find_all("td")

        # find name links (a tags)
        # and add to players a dict with
        # {'name':, 'url':}
        a_tags = cols[2].find("a")  # .get("href")

        # Dict of player info
        player_info = {
            "name": re.sub(
                r"\(.*\)", "", a_tags.get("title")
            ),  # Remove all "stuff" in parenthesis after name
            "url": base_url + a_tags.get("href"),  # Append to base URL
        }
        players.append(player_info)

    # return list of players
    return players


def get_player_stats(player_url: str, team: str) -> dict:
    """Gets the player stats for a player in a given team
    arguments:
        player_url (str) : url for the wiki page of player
        team (str) : the name of the team the player plays for
    returns:
        stats (dict) : dictionary with the keys (at least): points, assists, and rebounds keys
    """
    print(f"Fetching stats for player in {player_url}")

    # Get the table with stats
    html = get_html(player_url)
    soup = BeautifulSoup(html, "html.parser")

    # find NBA regular season section and the table in that section
    nba_regular_season = soup.find(
        class_="mw-headline",
        id=re.compile(r"(NBA)|(Regular.?season)", re.IGNORECASE),
    )
    table = nba_regular_season.find_next("table", {"class": "wikitable"})

    # Find column names
    table_head = table.find_all("th")
    # Extracting abreviations
    table_head = [head.text.strip() for head in table_head]

    # Empty statistics dict
    stats = {}

    # get all table rows
    rows = table.find_all("tr")
    # Loop over rows and extract the stats, skipping header row
    for row in rows[1:]:
        cols = row.find_all("td")

        # Task specifies only season 2021-22
        if "2021" in cols[table_head.index("Year")].text:
            # Check correct team (some players change team within season)
            if team in cols[table_head.index("Team")].text:
                # load stats from columns and remove all non digit or comma signs
                stats_list = [re.sub(r"[^\d\.]+", "", stat.text) for stat in cols[2:]]

                # keys should be 'points', 'assists', etc.
                # Converting stats to float
                stats["points"] = float(stats_list[table_head[2:].index("PPG")])
                stats["assists"] = float(stats_list[table_head[2:].index("APG")])
                stats["rebounds"] = float(stats_list[table_head[2:].index("RPG")])

    return stats


# run the whole thing if called as a script, for quick testing
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/2022_NBA_playoffs"
    find_best_players(url)
    # print(
    #     get_player_stats("https://en.wikipedia.org/wiki/James_Wiseman", "Golden State")
    # )
