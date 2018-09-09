import bs4 as bs
import urllib.request
import pandas as pd
import pickle

team_codes = []

with open("spotrac_urls.txt", "r+") as f:
    for line in f:
        team_codes.append(line[28:-6])

# print(team_codes)
# ['arizona-cardinals', 'atlanta-falcons', 'baltimore-ravens', 'buffalo-bills', 'carolina-panthers', 'chicago-bears', 'cincinnati-bengals', 'cleveland-browns', 'dallas-cowboys', 'denver-broncos', 'detroit-lions', 'green-bay-packers', 'houston-texans', 'indianapolis-colts', 'jacksonville-jaguars', 'kansas-city-chiefs', 'los-angeles-chargers', 'los-angeles-rams', 'miami-dolphins', 'minnesota-vikings', 'new-england-patriots', 'new-orleans-saints', 'new-york-giants', 'new-york-jets', 'oakland-raiders', 'philadelphia-eagles', 'pittsburgh-steelers', 'san-francisco-49ers', 'seattle-seahawks', 'tampa-bay-buccaneers', 'tennessee-titans', 'washington-redskins']

teams_dict = {}


def get_player_ids(team):
    # byte_byte = urllib.request.urlopen("https://www.spotrac.com/nfl/cleveland-browns/cap/")
    byte_byte = urllib.request.urlopen("https://www.spotrac.com/nfl/{team}/cap/".format(team=team))
    soups = bs.BeautifulSoup(byte_byte, 'lxml')

    table = soups.find("table", class_="datatable")
    tablesoup = bs.BeautifulSoup(str(table), 'lxml')

    keys = [link.get_text() for link in tablesoup.find_all("a", href=True)]
    vls = [link["href"] for link in tablesoup.find_all("a", href=True)]

    player_keys = []
    link_values = []
    for k in keys:
        if '(' not in k:
            player_keys.append(k)
    # ONE item in the philadelphia eagles page has a value of '-'. So this line of code removes that ONE item.
    if '-' in player_keys:
        player_keys.remove('-')
    # every other value is just "#", so those have to go.
    for v in vls:
        if v != '#':
            link_values.append(v)

    splt_vls = [l.rsplit('/')[-2] for l in link_values]

    # Lots of NFL players have apostrophes in their names, but apostrophes don't work in
    # URLs, so those have to go. This also adds the dash between first/last names.
    players = [v.replace(' ', '-').replace("'", "").lower() for v in player_keys]

    # create a blank dictionary for player urls
    player_ids_dict = {}

    # spotrac_url = "https://www.spotrac.com/nfl/{A}/{B}/cash-earnings/"

    spotrac_player_id = ["{}-{}".format(players[i], splt_vls[i]) for i in range(len(player_keys))]

    for i in range(len(player_keys)):
        player_ids_dict[player_keys[i]] = spotrac_player_id[i]

    if team not in teams_dict:
        teams_dict[team] = player_ids_dict



errors_list = []

for team in team_codes:
    try:
        get_player_ids(team)

    except Exception as e:
        # see reference_scraper.py line 148-152
        error = [team, e]
        errors_list.append(error)


column_headers = ['Year', 'Team', 'Salary', 'Signing_Bonus', 'Roster_Bonus', 'Workout_Bonus', 'Restructure_Bonus', 'Option_Bonus', 'Incentive', 'Total_Cash']


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


all_players_salaries_dfs_list = []
player_errors = []

spotrac_url = "https://www.spotrac.com/nfl/{A}/{B}/cash-earnings/"

# def extract_player_data(player_name, player_earnings_url):
for team_name, player_dict in teams_dict.items():
    for player_name, player_id in player_dict.items():
        try:
            player_byte = urllib.request.urlopen(spotrac_url.format(A=team_name, B=player_id))
            soup = bs.BeautifulSoup(player_byte, 'lxml')
            table = soup.find("table", class_="earningstable")
            table_soup = bs.BeautifulSoup(str(table), 'lxml')

            for row in table_soup:  # For each row, do the following:
                # 1. Get the text for each table data "td" element (basically, each cell) in the row
                player_list = [td.get_text() for td in row.find_all("td")]

                player_salary_history = []
                # This runs through the
                for i in player_list:
                    player_salary_history.append(i)
                    if "season" in i:
                        break
                player_salary_history.pop()

                player_chunks = list(chunks(player_salary_history, 10))

            teams_lst = table_soup.find_all("img", src=True)
            slices = [str(i).rsplit("/", 3)[-2] for i in teams_lst]
            teams = [i.rsplit(".")[-2] for i in slices]

            for i in range(len(player_chunks)):
                player_chunks[i][1] = teams[i]

            player_df = pd.DataFrame(player_chunks, columns=column_headers)

            player_df.insert(0, "Player_Name", player_name)
            player_df.insert(1, "Spotrac_ID", player_id)
            player_df_list = player_df.values.tolist()
            print(player_df_list[0])
            all_players_salaries_dfs_list.append(player_df)
        except Exception as e:
            # see reference_scraper.py line 148-152
            player_errors = [player_name, e]
            errors_list.append(player_errors)

print(player_errors)
salaries_df = pd.concat(all_players_salaries_dfs_list, ignore_index=True)

pickle_outtt = open("current_player_salaries.pickle", "wb")
pickle.dump(salaries_df, pickle_outtt)
pickle_outtt.close()
