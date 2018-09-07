from Cleaning_the_Data import fantasy_df
import bs4 as bs
import urllib.request
import pandas as pd

# I'm incredibly frustrated with how difficult this data is to find. Spotrack has salaries back to the 2011 season, so that's what I'll start with.

#def salary_scrape(year):
#site_byte = urllib.request.urlopen("https://www.spotrac.com/nfl/rankings/{}/cash/offense/".format(2011)).read() #Change 2011 to 'year' when you're ready to make this a function.
#soup = bs.BeautifulSoup(site_byte, 'lxml')
#column_headers = [th.getText() for th in soup.find("table", class_="datatable noborder").findAll('th')]

#column_headers[0] = "Rank"
#column_headers[1] = "Team"
#print(column_headers)
#print(soup.prettify())
#player_names = [h.getText() for h in soup.tbody.select("h3")]
#player_positions = [sp.getText() for sp in soup.tbody.select("span")]
#player_salaries = []
#print(player_positions[0:])

ppp = ['bills', 'colts', 'dolphins', 'pats', 'jets', 'ravens', 'bengals', 'browns', 'jaguars', 'steelers', 'titans', 'broncos', 'chiefs', 'raiders', 'chargers', 'seahawks', 'cards', 'cowboys', 'giants', 'eagles', 'redskins', 'bears', 'lions', 'packers', 'vikings', 'bucs', 'falcons', 'panthers', 'saints', 'rams', 'niners']
team_names = sorted(ppp)
print(len(team_names))
usa_byte = urllib.request.urlopen("https://usatoday30.usatoday.com/sports/nfl/salaries/bills.htm")
soup = bs.BeautifulSoup(usa_byte, 'lxml')
table = soup.select("#cnt_sandbox_q3")
table_soup = bs.BeautifulSoup(str(table), 'lxml')
#print(table_soup.prettify())
r5 = [b.getText().split() for b in table_soup.findAll("tr", limit=1)]
column_headers = r5[0]


def extract_player_data(table_rows_variable):
    """
    Extract and return the desired information from the td elements within the table rows.
    :param table_rows_variable:
    :return:
    """
    # Create the emply list to store the player data
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



team_df_list = []

season_dfs_list = []

errors_list = []

count = 0
usa_today_url = "https://usatoday30.usatoday.com/sports/nfl/salaries/{team}.htm"

for team in team_names:
    try:
        url = usa_today_url.format(team=team)

        html = urllib.request.urlopen(url)

        soup = bs.BeautifulSoup(html, 'lxml')

        column_headers = ["Team", "Player, position", "Salary", "Bonus", "Total"]

        table_rows = soup.select("#cnt_sandbox_q3 tr")

        player_data = extract_player_data(table_rows)

        if player_data[0][1] == "Salary":
            player_data = player_data[1:]

        for i in player_data:
            i.insert(0, team)

        print(player_data)

        team_df = pd.DataFrame(player_data, columns=column_headers)

        team_df_list = team_df.get_values().tolist()

        season_dfs_list.append(team_df)


    except Exception as e:
        error = [url, e]
        errors_list.append(error)

salaries_2000 = pd.concat(season_dfs_list, ignore_index=True)
#season_salaries_df = pd.DataFrame(season_df_list, columns=column_headers)

print(salaries_2000.head())
