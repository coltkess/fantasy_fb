import bs4 as bs
import urllib.request
import pandas as pd
import pickle
import sqlite3

# # first step is to create the list of teamcodes spotrac uses in their URLs. Usually it's just team-city, but I might as well grab them. Luckily, the reference tutorial already had all of them, which made it easy. https://wcontractor.github.io/nfl-salary-part2.html
# team_codes = []
#
# # I decided to do it the way he did it in the tutorial with the read file functionality. I saved the urls in another document, then experimented with the slices until I got what I needed.
# with open("spotrac_urls.txt", "r+") as f:
#     for line in f:
#         team_codes.append(line[28:-6])
#
# # print(team_codes)
# # ['arizona-cardinals', 'atlanta-falcons', 'baltimore-ravens', 'buffalo-bills', 'carolina-panthers', 'chicago-bears', 'cincinnati-bengals', 'cleveland-browns', 'dallas-cowboys', 'denver-broncos', 'detroit-lions', 'green-bay-packers', 'houston-texans', 'indianapolis-colts', 'jacksonville-jaguars', 'kansas-city-chiefs', 'los-angeles-chargers', 'los-angeles-rams', 'miami-dolphins', 'minnesota-vikings', 'new-england-patriots', 'new-orleans-saints', 'new-york-giants', 'new-york-jets', 'oakland-raiders', 'philadelphia-eagles', 'pittsburgh-steelers', 'san-francisco-49ers', 'seattle-seahawks', 'tampa-bay-buccaneers', 'tennessee-titans', 'washington-redskins']
#
# # This is used later on, and formatted with MongoDB in mind, since it's structured like this: teams_dict = {team-code: {'Player Name': 'player-code-####}}
#
# teams_dict = {}
#
# Now we get into the real stuff. This function takes a team argument, which is really one of the team-code ites from the list above.
#
# def get_player_ids(team):
#    # first I have to open the team's salary cap url, using the team-code item as part of the url. Then make and sort through the soup.
#     byte_byte = urllib.request.urlopen("https://www.spotrac.com/nfl/{team}/cap/".format(team=team))
#     soups = bs.BeautifulSoup(byte_byte, 'lxml')
#     table = soups.find("table", class_="datatable")
#     tablesoup = bs.BeautifulSoup(str(table), 'lxml')
#
#     # keys are the players' names - the anchortext which leads to the player pages.
#     keys = [link.get_text() for link in tablesoup.find_all("a", href=True)]
#     # vls are the links to the player pages themselves
#     vls = [link["href"] for link in tablesoup.find_all("a", href=True)]
#
#
#     # I had to clean up the player names and links to make sure they were all legit and I had 53 of them for each team. If I didn't, something went wrong.
#     player_keys = []
#     link_values = []
#     for k in keys:
#         if '(' not in k:
#             player_keys.append(k)
#     # ONE item in the philadelphia eagles page has a value of '-'. So this line of code removes that ONE item.
#     if '-' in player_keys:
#         player_keys.remove('-')
#     # Every second value in my vls list just "#", so those have to go.
#     for v in vls:
#         if v != '#':
#             link_values.append(v)
#
#    # This splits the values (the links) and grabs just the numeral player code.
#     splt_vls = [l.rsplit('/')[-2] for l in link_values]
#
#     # Lots of NFL players have apostrophes in their names, but apostrophes don't work in
#     # URLs, so those have to go. This also adds the dash between first/last names.
#     players = [v.replace(' ', '-').replace("'", "").lower() for v in player_keys]
#
#     # create a blank dictionary for player urls
#     player_ids_dict = {}
#
#     spotrac_player_id = ["{}-{}".format(players[i], splt_vls[i]) for i in range(len(player_keys))]
#
#       # adds key:value pairs to the player_ids_dict = {'Player Name': 'spotrac-player-id'}
#     for i in range(len(player_keys)):
#         player_ids_dict[player_keys[i]] = spotrac_player_id[i]
#
#       # checks to see if the team is already in the dictionary, and if it isn't, adds it.
#     if team not in teams_dict:
#         teams_dict[team] = player_ids_dict
#
#      This function doesn't actually return anything, it's purely meant to add teams to the "teams_dict" above.
#
#
# Here's where I run the function above, looping through all the items in team_codes and producing items for teams_dict, which is used below.
# errors_list = []
#
# for team in team_codes:
#     try:
#         get_player_ids(team)
#     except Exception as e:
#         # see reference_scraper.py line 148-152
#         error = [team, e]
#         errors_list.append(error)
#
# I could have figured out a fancy way to get the columns, but sometimes it's faster to just type out ten items than it is to parse through html.
# column_headers = ['Year', 'Team', 'Salary', 'Signing_Bonus', 'Roster_Bonus', 'Workout_Bonus', 'Restructure_Bonus', 'Option_Bonus', 'Incentive', 'Total_Cash']
#
# This function is used in the function below to divide the salary data into even segments to correspond to the columns above.
# def chunks(lst, n):
#     for i in range(0, len(lst), n):
#         yield lst[i:i + n]
#
# These are the lists I need to fill to make this work. Well, the first one at least. After a few runs where I would get part-way through before the code below would error out, I decided to use the try/except syntax and add the errors to a list to address later.
# all_players_salaries_dfs_list = []
# player_errors = []
#
# spotrac_url = "https://www.spotrac.com/nfl/{A}/{B}/cash-earnings/"
#
# # def extract_player_data(player_name, player_earnings_url):
# for team_name, player_dict in teams_dict.items():
#     for player_name, player_id in player_dict.items():
#         try:
#             player_byte = urllib.request.urlopen(spotrac_url.format(A=team_name, B=player_id))
#             soup = bs.BeautifulSoup(player_byte, 'lxml')
#             table = soup.find("table", class_="earningstable")
#             table_soup = bs.BeautifulSoup(str(table), 'lxml')
#
#             for row in table_soup:  # For each row, do the following:
#                 # 1. Get the text for each table data "td" element (basically, each cell) in the row
#                 player_list = [td.get_text() for td in row.find_all("td")]
#
#                 player_salary_history = []
#                 # This runs through the
#                 for i in player_list:
#                     player_salary_history.append(i)
#                     if "season" in i:
#                         break
#                 player_salary_history.pop()
#
#                 player_chunks = list(chunks(player_salary_history, 10))
#
#             teams_lst = table_soup.find_all("img", src=True)
#             slices = [str(i).rsplit("/", 3)[-2] for i in teams_lst]
#             teams = [i.rsplit(".")[-2] for i in slices]
#
#             for i in range(len(player_chunks)):
#                 player_chunks[i][1] = teams[i]
#
#             player_df = pd.DataFrame(player_chunks, columns=column_headers)
#
#             player_df.insert(0, "Player_Name", player_name)
#             player_df.insert(1, "Spotrac_ID", player_id)
#             player_df_list = player_df.values.tolist()
#             print(player_df_list[0])
#             all_players_salaries_dfs_list.append(player_df)
#         except Exception as e:
#             # see reference_scraper.py line 148-152
#             player_errors = [player_name, e]
#             errors_list.append(player_errors)
#
# print(player_errors)
# salaries_df = pd.concat(all_players_salaries_dfs_list, ignore_index=True)
#
# pickle_outtt = open("current_player_salaries.pickle", "wb")
# pickle.dump(salaries_df, pickle_outtt)
# pickle_outtt.close()

pickle_in = open("current_player_salaries.pickle", "rb")
current_player_salaries = pickle.load(pickle_in)

alias_for_jupyter = current_player_salaries

current_player_salaries.Total_Cash = current_player_salaries.Total_Cash.str.replace('$', '')
current_player_salaries.Total_Cash = current_player_salaries.Total_Cash.str.replace(',', '')

current_player_salaries.Salary = current_player_salaries.Salary.str.replace('$', '')
current_player_salaries.Salary = current_player_salaries.Salary.str.replace(',', '')
current_player_salaries.Salary = current_player_salaries.Salary.str.replace('-', '')

current_player_salaries.Signing_Bonus = current_player_salaries.Signing_Bonus.str.replace('$', '')
current_player_salaries.Signing_Bonus = current_player_salaries.Signing_Bonus.str.replace(',', '')
current_player_salaries.Signing_Bonus = current_player_salaries.Signing_Bonus.str.replace('-', '')

current_player_salaries.Roster_Bonus = current_player_salaries.Roster_Bonus.str.replace('$', '')
current_player_salaries.Roster_Bonus = current_player_salaries.Roster_Bonus.str.replace(',', '')
current_player_salaries.Roster_Bonus = current_player_salaries.Roster_Bonus.str.replace('-', '')

current_player_salaries.Workout_Bonus = current_player_salaries.Workout_Bonus.str.replace('$', '')
current_player_salaries.Workout_Bonus = current_player_salaries.Workout_Bonus.str.replace(',', '')
current_player_salaries.Workout_Bonus = current_player_salaries.Workout_Bonus.str.replace('-', '')

current_player_salaries.Restructure_Bonus = current_player_salaries.Restructure_Bonus.str.replace('$', '')
current_player_salaries.Restructure_Bonus = current_player_salaries.Restructure_Bonus.str.replace(',', '')
current_player_salaries.Restructure_Bonus = current_player_salaries.Restructure_Bonus.str.replace('-', '')

current_player_salaries.Option_Bonus = current_player_salaries.Option_Bonus.str.replace('$', '')
current_player_salaries.Option_Bonus = current_player_salaries.Option_Bonus.str.replace(',', '')
current_player_salaries.Option_Bonus = current_player_salaries.Option_Bonus.str.replace('-', '')

current_player_salaries.Incentive = current_player_salaries.Incentive.str.replace('$', '')
current_player_salaries.Incentive = current_player_salaries.Incentive.str.replace(',', '')
current_player_salaries.Incentive = current_player_salaries.Incentive.str.replace('-', '')

print(current_player_salaries.head())

conn = sqlite3.connect('player_salaries')

c = conn.cursor()

current_player_salaries.to_sql(name='salary_info', con=conn, if_exists='replace', index=False, dtype={'Player_Name': 'text',
        'Spotrac_ID': 'text',
        'Year': 'integer',
        'Team': 'text',
        'Salary': 'integer',
        'Signing_Bonus': 'integer',
        'Roster_Bonus': 'integer',
        'Workout_Bonus': 'integer',
        'Restructure_Bonus': 'integer',
        'Option_Bonus': 'integer',
        'Incentive': 'integer',
        'Total_Cash': 'integer'})
c.close()

# def create_table():
#    c.execute("""CREATE TABLE salary_info (
#                Player_Name text,
#                Spotrac_ID text,
#                Year integer,
#                Team text,
#                Salary integer,
#                Signing_Bonus integer,
#                Roster_Bonus integer,
#                Workout_Bonus integer,
#                Restructure_Bonus integer,
#                Option_Bonus integer,
#                Incentive integer,
#                Total_Cash integer
#    )""")
#    c.close()
#
# create_table()

# def insert_player(dataframe):
#    with conn:
#        c.execute("INSERT INTO salary_info VALUES ")
#
