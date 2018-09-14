import bs4 as bs
import urllib.request
import pandas as pd
import pickle
import sqlite3
import os

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

odell = [['Odell Beckham Jr.', 'odell-beckham-jr-14421', '2014', 'nygiants', '$420,000', '$5,888,144', '-', '-', '-',
          '-', '-', '$6,308,144'],
         ['Odell Beckham Jr.', 'odell-beckham-jr-14421', '2015', 'nygiants', '$840,479', '-', '-', '-', '-', '-',
          '$55,751', '$896,230'],
         ['Odell Beckham Jr.', 'odell-beckham-jr-14421', '2016', 'nygiants', '$1,366,018', '-', '-', '-', '-', '-', '-',
          '$1,366,018'],
         ['Odell Beckham Jr.', 'odell-beckham-jr-14421', '2017', 'nygiants', '$1,839,027', '-', '-', '-', '-', '-', '-',
          '$1,839,027'],
         ['Odell Beckham Jr.', 'odell-beckham-jr-14421', '2018', 'nygiants', '$1,459,000', '$20,000,000', '-', '-', '-',
          '-', '-', '$21,459,000']]

sample_headers = ['Player_Name', 'Spotrac_ID', 'Year', 'Team', 'Salary', 'Signing_Bonus', 'Roster_Bonus', 'Workout_Bonus', 'Restructure_Bonus', 'Option_Bonus', 'Incentive', 'Total_Cash']

odell_df = pd.DataFrame(odell, columns=sample_headers)

complete_salaries_df = current_player_salaries.append(odell_df, ignore_index=True)



complete_salaries_df.Total_Cash = complete_salaries_df.Total_Cash.str.replace('$', '')
complete_salaries_df.Total_Cash = complete_salaries_df.Total_Cash.str.replace(',', '')

complete_salaries_df.Total_Cash = complete_salaries_df.Total_Cash.str.replace('$', '')
complete_salaries_df.Total_Cash = complete_salaries_df.Total_Cash.str.replace(',', '')

complete_salaries_df.Salary = complete_salaries_df.Salary.str.replace('$', '')
complete_salaries_df.Salary = complete_salaries_df.Salary.str.replace(',', '')
complete_salaries_df.Salary = complete_salaries_df.Salary.str.replace('-', '')

complete_salaries_df.Signing_Bonus = complete_salaries_df.Signing_Bonus.str.replace('$', '')
complete_salaries_df.Signing_Bonus = complete_salaries_df.Signing_Bonus.str.replace(',', '')
complete_salaries_df.Signing_Bonus = complete_salaries_df.Signing_Bonus.str.replace('-', '')

complete_salaries_df.Roster_Bonus = complete_salaries_df.Roster_Bonus.str.replace('$', '')
complete_salaries_df.Roster_Bonus = complete_salaries_df.Roster_Bonus.str.replace(',', '')
complete_salaries_df.Roster_Bonus = complete_salaries_df.Roster_Bonus.str.replace('-', '')

complete_salaries_df.Workout_Bonus = complete_salaries_df.Workout_Bonus.str.replace('$', '')
complete_salaries_df.Workout_Bonus = complete_salaries_df.Workout_Bonus.str.replace(',', '')
complete_salaries_df.Workout_Bonus = complete_salaries_df.Workout_Bonus.str.replace('-', '')

complete_salaries_df.Restructure_Bonus = complete_salaries_df.Restructure_Bonus.str.replace('$', '')
complete_salaries_df.Restructure_Bonus = complete_salaries_df.Restructure_Bonus.str.replace(',', '')
complete_salaries_df.Restructure_Bonus = complete_salaries_df.Restructure_Bonus.str.replace('-', '')

complete_salaries_df.Option_Bonus = complete_salaries_df.Option_Bonus.str.replace('$', '')
complete_salaries_df.Option_Bonus = complete_salaries_df.Option_Bonus.str.replace(',', '')
complete_salaries_df.Option_Bonus = complete_salaries_df.Option_Bonus.str.replace('-', '')

complete_salaries_df.Incentive = complete_salaries_df.Incentive.str.replace('$', '')
complete_salaries_df.Incentive = complete_salaries_df.Incentive.str.replace(',', '')
complete_salaries_df.Incentive = complete_salaries_df.Incentive.str.replace('-', '')


complete_salaries_df = complete_salaries_df.replace(to_replace={'arizona2': 'ARI', 'patriots': 'NWE', 'rams2': 'LAR', 'eagles1': 'PHI', 'vikings': 'MIN', 'bengals': 'CIN', '49erslogo': 'SFO', 'colts': 'IND', 'oakland': 'OAK', 'browns': 'CLE', 'nygiants': 'NYG', 'panthers': 'CAR', 'falcons': 'ATL', 'bucs': 'TAM', 'bears': 'CHI', 'dolphins': 'MIA', 'svg_': 'LAC', 'hawks3': 'SEA', 'dallas': 'DAL', 'ravens': 'BAL', 'lions': 'DET', 'broncos': 'DEN', 'buffalo': 'BUF','neworleans': 'NOR', 'packers': 'GNB', 'washington': 'WAS', 'kansascity': 'KAN', 'tennessee': 'TEN', 'texans': 'HOU', 'chargers2': 'SDG', 'jets': 'NYJ', 'jaguars': 'JAX', 'rams3': 'STL', 'Pittsburgh-Steelers-logo-psd22874': 'PIT'})

names = complete_salaries_df['Player_Name'].tolist()
years = complete_salaries_df['Year'].tolist()
teams = complete_salaries_df['Team'].tolist()

names_under = [i.replace(' ', '_') for i in names]

my_id = []
if len(names) == len(names_under):
    for i in range(len(names_under)):
        my_id.append("{}_{}_{}".format(names_under[i], years[i], teams[i]))
    # else:
    #     print(len(names), len(names_under))

complete_salaries_df.insert(0, 'my_ids', my_id)

basepath = "/Users/coltkess/Desktop/"
file_name = "fantasy_fb_since2000.csv"
pathtofile = os.path.join(basepath, file_name)

fantasy_stats_df = pd.read_csv("/Users/coltkess/PycharmProjects/fantasy_fb_contract_year/fantasy_football_since2000.csv")

names2 = fantasy_stats_df['Player'].tolist()
years2 = fantasy_stats_df['Season'].tolist()
teams2 = fantasy_stats_df['Team'].tolist()

names_under2 = [i.replace(' ', '_') for i in names2]

my_id2 = []
if len(names2) == len(names_under2):
    for i in range(len(names_under2)):
        my_id2.append("{}_{}_{}".format(names_under2[i], years2[i], teams2[i]))

fantasy_stats_df.insert(0, 'my_ids', my_id2)

full_df = pd.merge(fantasy_stats_df, complete_salaries_df, on='my_ids', how='inner')

full_df = full_df.drop(columns=['Rk'])

full_df = full_df.apply(pd.to_numeric, errors="ignore")

num_cols = full_df.columns[full_df.dtypes != object]

full_df.loc[:, num_cols] = full_df.loc[:, num_cols].fillna(0)

print(full_df.info())

conn = sqlite3.connect('/Users/coltkess/PycharmProjects/fantasy_fb_contract_year/full_db')
c = conn.cursor()

full_df.to_sql(name='full_data_frame', con=conn, if_exists='replace', index=False, dtype={'my_ids': 'object', 'Season': 'integer', 'Player': 'object', 'Team_x': 'object', 'Position': 'object', 'Age': 'integer', 'G': 'integer', 'GS': 'integer', 'Pass_Cmp': 'integer', 'Pass_Att': 'integer', 'Pass_Yds': 'integer', 'Pass_TD': 'integer', 'Pass_INT': 'integer', 'Rush_Att': 'integer', 'Rush_Yds': 'integer', 'Rush_YpA': 'float', 'Rush_TD': 'integer', 'Rec_Tgt': 'integer', 'Rec': 'integer', 'Rec_Yds': 'integer', 'Rec_YpR': 'float', 'Rec_TD': 'integer', 'Two_PT_Made': 'integer', 'Two_PT_Pass': 'integer', 'Fantasy_Pts': 'float', 'PPR_Pts': 'float', 'DraftKings_Pts': 'float', 'FanDuel_Pts': 'float', 'VBD': 'integer', 'PosRank': 'integer', 'OvRank': 'integer', 'player_nfl_link': 'object', 'player_team_link': 'object', 'Player_Name': 'object', 'Spotrac_ID': 'object', 'Year': 'integer', 'Team_y': 'object', 'Salary': 'integer', 'Signing_Bonus': 'integer', 'Roster_Bonus': 'integer', 'Workout_Bonus': 'integer', 'Restructure_Bonus': 'integer', 'Option_Bonus': 'integer', 'Incentive': 'integer', 'Total_Cash': 'integer'
})
c.close()


# def insert_player(dataframe):
#    with conn:
#        c.execute("INSERT INTO salary_info VALUES ")
#
