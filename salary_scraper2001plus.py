import bs4 as bs
import urllib.request
import pandas as pd
import numpy as np

#ppp = ['bills', 'colts', 'dolphins', 'pats', 'jets', 'ravens', 'bengals', 'browns', 'jaguars', 'steelers', 'titans', 'broncos', 'chiefs', 'raiders', 'chargers', 'seahawks', 'cards', 'cowboys', 'giants', 'eagles', 'redskins', 'bears', 'lions', 'packers', 'vikings', 'bucs', 'falcons', 'panthers', 'saints', 'rams', 'niners']
#team_names = sorted(ppp)
#print(len(team_names))

column_headers = ['Year', 'Team', 'Salary', 'Signing Bonus', 'Roster Bonus', 'Workout Bonus', 'Restructure Bonus', 'Option Bonus', 'Incentive', 'Total Cash']

spotrac_url = ("https://www.spotrac.com/nfl/atlanta-falcons/{}/cash-earnings/")

def fetch_soup(first_last_num):
    spotrac_byte = urllib.request.urlopen(spotrac_url.format(first_last_num))
    soup = bs.BeautifulSoup(spotrac_byte, 'lxml')
    table = soup.find("table", class_="earningstable")
    table_soup = bs.BeautifulSoup(str(table), 'lxml')
    return table_soup


def extract_player_data(table_rows_variable):
    """
    Extract and return the desired information from the td elements within the table rows.
    :param table_rows_variable:
    :return:
    """
    # Create the empty list to store the player data
    player_data = []
    for row in table_rows_variable:  # For each row, do the following:
        # 1. Get the text for each table data (td) element in the row
        player_list = [td.get_text() for td in row.find_all("td")]
        # There are some empty table rows, which are the repeated column headers in the table.
        # We want our function to skip over those rows and and continue the for loop.
        if not player_list:
            continue
            # Extracting the player links:
        player_data.append(player_list)
    return player_data


matt_ryan = extract_player_data(table_soup)

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]


ryan_chunks = list(chunks(matt_ryan[0], 10))

print(ryan_chunks)

ryan_today = []

for i in range(len(ryan_chunks)):
    ryan_today.append(ryan_chunks[i])
    if ryan_chunks[i][0] == '2018':
        break

print(ryan_today)

matt_ryan_db = pd.DataFrame(ryan_today, columns=column_headers)

print(matt_ryan_db.tail())


# team_df_list = []
#
# season_dfs_list = []
#
# errors_list = []
#
# count = 0
# usa_today_url = "https://usatoday30.usatoday.com/sports/nfl/salaries/{team}.htm"

# for team in team_names:
#     try:
#         url = usa_today_url.format(team=team)
#
#         html = urllib.request.urlopen(url)
#
#         soup = bs.BeautifulSoup(html, 'lxml')
#
#         column_headers = ["Team", "Player, position", "Salary", "Bonus", "Total"]
#
#         table_rows = soup.select("#cnt_sandbox_q3 tr")
#
#         player_data = extract_player_data(table_rows)
#
#         if player_data[0][1] == "Salary":
#             player_data = player_data[1:]
#
#         for i in player_data:
#             i.insert(0, team)
#
#         print(player_data)
#
#         team_df = pd.DataFrame(player_data, columns=column_headers)
#
#         team_df_list = team_df.get_values().tolist()
#
#         season_dfs_list.append(team_df)
#
#
#     except Exception as e:
#         error = [url, e]
#         errors_list.append(error)

#salaries_2000 = pd.concat(season_dfs_list, ignore_index=True)
#season_salaries_df = pd.DataFrame(season_df_list, columns=column_headers)

