# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from collections import namedtuple
import json
import requests


class Match:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    game_date = None
    away_team = None
    home_team = None
    away_line = None
    home_line = None
    winner_team = None
    winner_line = None


def get_odds(url):
    r = requests.get(url)

    data = r.text  # .encode('utf-8') # raw HTML

    soup = BeautifulSoup(data.encode('utf-8'), 'html.parser')

    return_results = []

    gamedates = soup.find_all(get_columndate)

    lines_tables = soup.find_all(get_lines_table)

    for row in gamedates:
        date_text = row.text
        print(date_text)

    # Process the tables (there should be only one)
    for table in lines_tables:
        # Get <tr> rows
        for row in table.find_all('tr'):
            # Row has our data

            o = Match()

            counter = 0
            for cell in row.find_all('td'):
                # First cell is date and teams

                if cell.has_attr('class') and 'cellTextNorm' in cell.get('class') and 'game-notes' not in cell.get('class'):
                    if counter == 0:
                        # First cell
                        # print(cell.text)
                        game_date = cell.find('span').text
                        team_away = cell.find_all('a')[0].text
                        team_home = cell.find_all('a')[1].text
                        o.game_date = game_date
                        o.away_team = team_away
                        o.home_team = team_home
                        # print(o)
                    elif counter == 2:
                        # Concensus odds cell
                        # print(cell.text)
                        line_contents = cell.find('a').contents
                        away_line = line_contents[2]
                        home_line = line_contents[4]
                        if "u-" not in away_line:
                            o.away_line = away_line.split('\xa0')[0]
                        if "u-" not in home_line:
                            o.home_line = home_line.split('\xa0')[0]

                counter += 1
            if(o.game_date is not None):
                if o.away_line is not None:
                    o.winner_line = o.away_line
                    o.winner_team = o.away_team
                else:
                    o.winner_line = o.home_line
                    o.winner_team = o.home_team
                if o.winner_line == "PK":
                    o.winner_line = "-0"
                print(o)
                return_results.append(o)

    return return_results


def get_lines_table(tag):
    return tag.has_attr('class') and 'frodds-data-tbl' in tag.get('class') and tag.name == 'table'


def get_table_rows(tag):
    return tag.name == 'tr'


def get_table_cells(tag):
    return tag.name == 'td'


def get_gamedates(tag):
    return tag.has_attr('class') and 'gamedate' in tag.get('class') and tag.name == 'div'


def get_columndate(tag):
    return tag.has_attr('class') and 'column-date' in tag.get('class') and tag.name == 'span'


def get_matchlists(tag):
    return tag.has_attr('class') and 'match-list' in tag.get('class') and tag.name == 'div'


Thing1 = namedtuple('Thing1', ['winner', 'line'], verbose=False)

print('Starting...')

# results = get_odds('http://m.vegasinsider.com/thisweek/3/NFL')
results = get_odds('http://www.vegasinsider.com/nfl/odds/las-vegas/')\

x = Thing1('DET', -10)
y = Thing1('CLE', -2)
z = Thing1('NE', -5)

lines = [x, y, z]

print(json.dumps([ob for ob in lines]))

print('Sorting...')

lines.sort(key=lambda x: x.line, reverse=False)

print(json.dumps([ob for ob in lines]))


print("procesing results...")

for ob in results:
    print(ob)

print('Sorting...')

results.sort(key=lambda x: x.winner_line, reverse=True)

for ob in results:
    print(ob)

print('Finished.')
