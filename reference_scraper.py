import bs4 as bs
import urllib.request
import pandas as pd

#def rankings_scraper(year, sports_reference_url):
    # Uses urllib.request to turn the URL into bytes legible by BeautifulSoup.
site_byte = urllib.request.urlopen("https://www.pro-football-reference.com/years/2017/fantasy.htm").read()

    # Takes the site bytes and turns them into a bs4.BeautifulSoup object, which looks like html,
    # and reads like it if the .prettify() method is applied.
soup = bs.BeautifulSoup(site_byte, 'lxml')

#print(soup.prettify)

# Returns a list of bs4 elements within `soup` surrounded by a 'th' tag, returns them in a list.
table = soup.find('tbody')
player_dict = dict()
for row in table.findAll("td", {"data-stat": "player"}):
    player_name = row.getText()
    for a in row.find_all('a', href=True):
        link = a['href'].strip()
        name = link[11:]
        player_dict[name] = player_name

print(player_dict)




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