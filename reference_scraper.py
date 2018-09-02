#matplotlib inline

import bs4 as bs
import urllib.request
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#def rankings_scraper(year, sports_reference_url):
    # Uses urllib.request to turn the URL into bytes legible by BeautifulSoup.


    # Takes the site bytes and turns them into a bs4.BeautifulSoup object, which looks like html,
    # and reads like it if the .prettify() method is applied.


#print(soup.prettify)

# Returns a list of bs4 elements within `soup` surrounded by a 'th' tag, returns them in a list.
#def year_to_player_dict_creator(year##TODO if you want to make this a function, which you do, you need to change this back to a variable.):

site_byte = urllib.request.urlopen("https://www.pro-football-reference.com/years/{}/fantasy.htm".format(2017)).read()
soup = bs.BeautifulSoup(site_byte, 'lxml')
column_headers = [th.getText() for th in soup.findAll('tr', limit=2)[1].findAll('th')]
column_headers[1] = 'Player'
column_headers[2] = 'Team'
column_headers[3] = 'Position'
column_headers[7] = 'Pass Cmp'
column_headers[8] = 'Pass Att'
column_headers[9] = 'Pass Yds'
column_headers[10] = 'Pass TD'
column_headers[11] = 'Pass INT'
column_headers[12] = 'Rush Att'
column_headers[13] = 'Rush Yds'
column_headers[14] = 'Rush Y/A'
column_headers[15] = 'Rush TD'
column_headers[16] = 'Rec Tgt'
column_headers[18] = 'Rec Yds'
column_headers[19] = 'Rec Y/R'
column_headers[20] = 'Rec TD'
column_headers[21] = '2PT Made'
column_headers[22] = '2PT Pass'
column_headers[23] = 'Fantasy Pts'
column_headers[24] = 'PPR Pts'
column_headers[25] = 'DraftKings Pts'
column_headers[26] = 'FanDuel Pts'
column_headers[28] = 'FanDuel Pts'
column_headers.extend(["player_nfl_link", "player_team_link"])
table_rows = soup.select("#fantasy tr")[1:]


def extract_player_data(table_rows_variable):
    """
    Extract and return the desired information from the td elements within the table rows.
    :param table_rows_variable:
    :return:
    """
    # Create the emply list to store the player data
    player_data = []
    for row in table_rows_variable:  # for each row, do the following:
        # Get the text for each table data (td) element in the row
        # Some player names end with
        player_list = [
            td.get_text()[:-2] if td.get_text().endswith("*+") else td.get_text()[:-1] if td.get_text().endswith(
                "+") or td.get_text().endswith("*") else td.get_text() for td in row.find_all("td")]
        # there are some empty table rows, which are the repeated
        # column headers in the table
        # we skip over those rows and and continue the for loop
        if not player_list:
            continue
            # Extracting the player links
            # Instead of a list we create a dictionary, this way we can easily
            # match the player name with their pfr url
            # For all "a" elements in the row, get the text
            # NOTE: Same " HOF" text issue as the player_list above
        links_dict = {(link.get_text()): link["href"] for link in row.find_all("a", href=True)}
        player_list.insert(0,
                           '')  # TODO figure out why this is even necessary. I have an "Rk" table header, but no data for it.
        player_list.append(links_dict.get(player_list[1], ""))
        player_list.append(links_dict.get(player_list[2], ""))
        player_data.append(player_list)
    return player_data


# data = extract_player_data(table_rows)

# df_2017 = pd.DataFrame(data, columns=column_headers)

season_dfs_list = []

errors_list = []

url_template = "https://www.pro-football-reference.com/years/{year}/fantasy.htm"
# for each year from 2000 to (and including) 2017
for year in range(2017, 2018):
    # Using try/except block to catch and inspect any urls that cause an error
    try:
        # get the season URL
        url = url_template.format(year=year)

        # get the html
        html = urllib.request.urlopen(url)

        # create the beautiful soup object
        soup = bs.BeautifulSoup(html, 'lxml')

        # get column headers
        column_headers = [th.getText() for th in soup.findAll('tr', limit=2)[1].findAll('th')]
        column_headers[1] = 'Player'
        column_headers[2] = 'Team'
        column_headers[3] = 'Position'
        column_headers[7] = 'Pass_Cmp'
        column_headers[8] = 'Pass_Att'
        column_headers[9] = 'Pass_Yds'
        column_headers[10] = 'Pass_TD'
        column_headers[11] = 'Pass_INT'
        column_headers[12] = 'Rush_Att'
        column_headers[13] = 'Rush_Yds'
        column_headers[14] = 'Rush_YpA'
        column_headers[15] = 'Rush_TD'
        column_headers[16] = 'Rec_Tgt'
        column_headers[18] = 'Rec_Yds'
        column_headers[19] = 'Rec_YpR'
        column_headers[20] = 'Rec_TD'
        column_headers[21] = 'Two_PT_Made'
        column_headers[22] = 'Two_PT_Pass'
        column_headers[23] = 'Fantasy_Pts'
        column_headers[24] = 'PPR_Pts'
        column_headers[25] = 'DraftKings_Pts'
        column_headers[26] = 'FanDuel_Pts'
        column_headers.extend(["player_nfl_link", "player_team_link"])

        # select the data from the tale using the '#fantasy tr' CSS selector
        table_rows = soup.select("#fantasy tr")[1:]

        # extract player data from the table rows
        player_data = extract_player_data(table_rows)

        # create the dataframe for the current fantasy season
        year_df = pd.DataFrame(player_data, columns=column_headers)

        # add the year of the season to the dataframe
        year_df.insert(0, "Season", year)

        # append the current dataframe to the list of dataframes
        season_dfs_list.append(year_df)

    except Exception as e:
        # store the url and the error it causes in a list
        error = [url, e]
        # then append it to the list of errors
        errors_list.append(error)

fantasy_df = pd.concat(season_dfs_list, ignore_index=True)

print(column_headers)
print(fantasy_df.head())



    #player_dict = dict()
    #team_dict = dict()
    #for row in table.findAll("td", {"data-stat": "player"}):
    #    player_name = row.getText()
    #    for a in row.find_all('a', href=True):
    #        link = a['href'].strip()
    #        name = link[11:]
    #        player_dict[name] = player_name
    ##for row in table.findAll("td", {"data-stat": "team"}):
    #    team_name = row.getText()
    #    for a in row[1].find_all('a', href=True):
    #        team_link = a['href'].strip()
    #        team = team_link[7:]
    #        team_dict[team] = team_name
#
    ##features = {"team", "fantasy_pos", "age", "g", "gs", "pass_cmp", "pass_att", "pass_yds", "pass_td", "pass_int", "rush_att", "rush_yds", "rush_yds_per_att", "rush_td", "targets", "rec", "rec_yds", "rec_yds_per_rec", "rec_td", "two_pt_md", "two_pt_pass", "fantasy_points", "fantasy_points_ppr", "draftkings_points", "fanduel_points", "vbd", "fantasy_rank_pos", "fantasy_rank_overall"}
    ##for f in features:
    ##    for row in table.find_all("td", {"data-stat": f}):
    ##        stat = row.find_all
    ##        cell = row.find("td", {"data-stat": f})
    ##        a = cell.text.strip().encode()
    ##        text = a.decode("utf-8")
    ##        if f in pre_df:
    ##            pre_df[f].append(text)
    ##        else:
    ##            pre_df[f] = [text]
    #year_to_players_dict = {year: player_dict}
    #return column_headers

#print(year_to_player_dict_creator(2017))
        #df = pd.DataFrame.from_dict(pre_df)
        #df["team"] = df["team"].apply()



                #a = cell.text.strip().encode()
                #text = a.decode("utf-8")
                #if f in pre_df



# This works. It produces the output: 'Todd Gurley*+'.
# fantasy_2017 = year_to_player_dict_creator('2017')
# print(fantasy_2017['2017']['GurlTo01.htm'])




   ## Strips the html and produces a list of header name strings.
   #headers = [headers_w_html[i].text for i in range(len(headers_w_html))]

   ## Finds the 'tbody' tag in the soup (aka in all the page HTML).
   #html = soup.find('tbody')

   ## Finds the 'td' tags in the 'html' object above, places them in a list
   #children = html.find_all('td')

   ## Creates a list of just the text in the object 'children'
   #items = [i.text for i in children]

   ## Strips the white space off either side of the text in 'items'.
   #stripped = [i.strip() for i in items]

   #rankings_w_zeros = [stripped[rank] or "0" for rank in range(len(stripped))]

   ## 'stripped' is a list of between roughly 500 and 3,000 strings -- every cell item for every team.
   ## This line of code splits this long list into separate lists for each team. It does so by iterating through the
   ## 'stripped' and splitting it into lists with the same number of objects as the header list.
   ## This is what makes the function work for any table.
   #teams = [rankings_w_zeros[i:i + len(headers)] for i in range(0, len(rankings_w_zeros), len(headers))]

   ## This takes each item in the headers list and makes it a key, then takes the each of the lists in 'teams' and
   ## distributes their objects to len(headers) lists, which make up the values associated with each
   ## header key.
   #headers_values_dict = {}

   #for h in range(len(headers)):
   #    headers_values_dict[headers[h]] = [i[h] for i in teams]

   ## This uses pandas to put the headers_values_dict into a dataframe with each header string as the headers
   ## and each value item as the components.
   #table = pd.DataFrame(data=headers_values_dict)

   ## Finally, this generates the .csv file and saves it in the current working drive.
   ## return table.to_csv("{}.csv".format(page_title))

    ##def find_hero_ranking_urls(url):
    ##    site_byte = urllib.request.urlopen(url).read()
    ##
    ##    # Takes the site bytes and turns them into a bs4.BeautifulSoup object, which looks like html,
    ##    # and reads like it if the .prettify() method is applied.
    ##
    ##    soup = bs.BeautifulSoup(site_byte, 'lxml')
    ##
    ##    rankings = soup.find('div', class_="team-list mCustomScrollbar")
    ##
    ##    rankings_soup = bs.BeautifulSoup(str(rankings), 'lxml')
    ##
    ##    dictionary = {}
    ##    for link in rankings_soup.find_all('a'):
    ##        dictionary[link.get('title')] = link.get('href')
    ##
    ##    dict_keys = dictionary.keys()
    ##
    ##    reduced_keys = []
    ##
    ##    for i in dict_keys:
    ##        if 'D1' in i[0:2]:
    ##            reduced_keys.append(i)
    ##        elif "D2" in i[0:2]:
    ##            reduced_keys.append(i)
    ##        elif 'D3' in i[0:2]:
    ##            reduced_keys.append(i)
    ##        elif 'FBS' in i[0:3]:
    ##            reduced_keys.append(i)
    ##        elif 'FCS' in i[0:3]:
    ##            reduced_keys.append(i)
    ##
    ##    reduced_dictionary = {k: dictionary[k] for k in reduced_keys if k in dictionary}
    ##
    ##    return reduced_dictionary
    ##
    ##
    ##url_dict = find_hero_ranking_urls('https://herosports.com/')
    ##
    ##for k, v in url_dict.items():
    ##    print("{}: {}".format(k, v))
    ##
    ### for k, v in url_dict.items():
    ###    rankings_scraper(k, v)