import bs4 as bs
import urllib.request
import pandas as pd


def getSchools():
    page = urllib.request.urlopen("https://www.sports-reference.com/cbb/seasons/2018-school-stats.html").read()
    soup = bs.BeautifulSoup(page, 'lxml')
    count = 0
    table = soup.find("tbody")
    school_dict = dict()
    for row in table.findAll('td', {"data-stat": "school_name"}):
        school_name = row.getText()
        for a in row.find_all('a', href=True):
            link = a['href'].strip()
            name = link[13:].split("/")[0]
            school_dict[name] = school_name
    return school_dict

def getDfs():
    school_set = getSchools()
    dfs = []
    final_df = pd.DataFrame()
    for school in school_set:
        urls = "https://www.sports-reference.com/cbb/schools/" + school + "/2018-schedule.html"
        page = urllib.request.urlopen(urls).read()
        soup = bs.BeautifulSoup(page, 'lxml')
        count = 0
        pre_df = dict()
        school_set = getSchools()
        table = soup.find("tbody")
        featuresWanted = {'opp_name', 'pts', 'opp_pts',
                          'game_location', 'game_result', 'overtimes', 'wins', 'losses',
                          'date_game'}  # add more features here!!
        rows = table.find_all('tr')
        for row in rows:
            if (row.find('th', {"scope": "row"}) != None):
                for f in featuresWanted:
                    cell = row.find("td", {"data-stat": f})
                    a = cell.text.strip().encode()
                    text = a.decode("utf-8")
                    if f in pre_df:
                        pre_df[f].append(text)
                    else:
                        pre_df[f] = [text]

        df = pd.DataFrame.from_dict(pre_df)
        df["opp_name"] = df["opp_name"].apply(lambda row: (row.split("(")[0]).rstrip())
        df["school_name"] = school_set[school]
        df["school_name"] = df["school_name"].apply(removeNCAA)
        final_df = pd.concat([final_df, df])
    return final_df

def removeNCAA(x):
    if ("NCAA" in x):
        return x[:-5]
    else:
        return x
print(getDfs())

#def csvDump():
#    df = getDfs()
#    df.to_csv("scraped_data.csv")


#csvDump()