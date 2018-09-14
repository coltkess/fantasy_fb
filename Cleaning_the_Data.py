import pickle
import pandas as pd

# I needed to bring my dataframe into this file, but only wanted to do it once. So the code block below was only necessary to run one time. After I ran the whole process to get the dataframe, pickling saved it to an object which I could un-pack without running the whole scrape again.
#from reference_scraper import fantasy_df
#pickle_out = open("fantasy.pickle", "wb")
#pickle.dump(fantasy_df, pickle_out)
#pickle_out.close()

pickle_in = open("fantasy.pickle", "rb")
fantasy_df = pickle.load(pickle_in)

print(fantasy_df.Team.unique())
# First lets create a separate DataFrame that contains the player names, their player page links, and the player ID on Pro-Football-Reference. This way we can have a separate CSV file that just contains the necessary information to extract individual player data for Pro-Football-Reference sometime in the future.
#
# To extract the Pro-Football-Reference player ID from the player link, we will need to use a regular expression.
# Regular expressions are a sequence of characters used to match some pattern in a body of text.
# The regular expression that we can use to match the pattern of the player link and extract the ID is as follows:
#
# /.*/.*/(.*)\.
#
# What the above regular expression essentially says is match the string with the following pattern:
#
# - One '/'.
# - Followed by 0 or more characters (this is represented by the '.*' characters).
# - Followed by another '/' (the 2nd '/' character).
# - Followed by 0 or more characters (again the '.*' characters) .
# - Followed by another (3rd) '/'.
# - Followed by a grouping of 0 or more characters (the '(.*)' characters).
# - This is the key part of our regular expression. The '()' characters create a grouping around the characters we
#   want to extract. Since the player IDs are found between the 3rd '/' and the '.', we use '(.*)' to extract all the
#   characters found in that part of our string.
# - Followed by a '.', character after the player ID.
#
# We can extract the IDs by passing the above regular expression into the pandas extract method.
#
#
# Extract the player id from the player links
# expand=False returns the IDs as a pandas Series
player_ids = fantasy_df.player_nfl_link.str.extract("/.*/.*/(.*)\.", expand=False)

# Add a Player_ID column to our fantasy_df
fantasy_df["Player_ID"] = player_ids

# Add the beginning of the pfr url to the player link column
pfr_url = "https://www.pro-football-reference.com/"
fantasy_df.player_nfl_link = pfr_url + fantasy_df.Player_ID

# Get the Player name, IDs, and links# Get th
player_id_df = fantasy_df.loc[:, ["Player", "Player_ID", "player_nfl_link"]]

# Save them to a CSV file
#player_id_df.to_csv("pfr_player_ids_and_links.csv", index=False)

# View the column titles, if they have data, and what type of data is stored.
#fantasy_df.info()

# The .info() above returns the following:
# RangeIndex: 10650 entries, 0 to 10649
# Data columns (total 34 columns):
# Season              10650 non-null int64
# Rk                  10650 non-null object
# Player              10650 non-null object
# Team                10650 non-null object
# Position            10650 non-null object
# Age                 10650 non-null object
# G                   10650 non-null object
# GS                  10650 non-null object
# Pass_Cmp            10650 non-null object
# Pass_Att            10650 non-null object
# Pass_Yds            10650 non-null object
# Pass_TD             10650 non-null object
# Pass_INT            10650 non-null object
# Rush_Att            10650 non-null object
# Rush_Yds            10650 non-null object
# Rush_YpA            10650 non-null object
# Rush_TD             10650 non-null object
# Rec_Tgt             10650 non-null object
# Rec                 10650 non-null object
# Rec_Yds             10650 non-null object
# Rec_YpR             10650 non-null object
# Rec_TD              10650 non-null object
# Two_PT_Made         10650 non-null object
# Two_PT_Pass         10650 non-null object
# Fantasy_Pts         10650 non-null object
# PPR_Pts             10650 non-null object
# DraftKings_Pts      10650 non-null object
# FanDuel_Pts         10650 non-null object
# VBD                 10650 non-null object
# PosRank             10650 non-null object
# OvRank              10650 non-null object
# player_nfl_link     10650 non-null object
# player_team_link    10650 non-null object
# Player_ID           10650 non-null object
# dtypes: int64(1), object(33)
# memory usage: 2.8+ MB

# Lots of this data should be numaric, but isn't. To convert it, we can apply the 'to_numeric' function to the whole DataFrame. But we also need to set the 'errors' parameter to "ignore" to avoid raising any errors.
fantasy_df = fantasy_df.apply(pd.to_numeric, errors="ignore")

# After running the code above, we try .info() again and get the following:
#fantasy_df.info()

# RangeIndex: 10650 entries, 0 to 10649
# Data columns (total 34 columns):
# Season              10650 non-null int64
# Rk                  0 non-null float64
# Player              10650 non-null object
# Team                10650 non-null object
# Position            10650 non-null object
# Age                 10649 non-null float64
# G                   10552 non-null float64
# GS                  10409 non-null float64
# Pass_Cmp            10649 non-null float64
# Pass_Att            10649 non-null float64
# Pass_Yds            10649 non-null float64
# Pass_TD             10649 non-null float64
# Pass_INT            10649 non-null float64
# Rush_Att            10649 non-null float64
# Rush_Yds            10649 non-null float64
# Rush_YpA            5431 non-null float64
# Rush_TD             10649 non-null float64
# Rec_Tgt             10005 non-null float64
# Rec                 10649 non-null float64
# Rec_Yds             10649 non-null float64
# Rec_YpR             7772 non-null float64
# Rec_TD              10649 non-null float64
# Two_PT_Made         507 non-null float64
# Two_PT_Pass         283 non-null float64
# Fantasy_Pts         9062 non-null float64
# PPR_Pts             9209 non-null float64
# DraftKings_Pts      9364 non-null float64
# FanDuel_Pts         9366 non-null float64
# VBD                 1326 non-null float64
# PosRank             10650 non-null int64
# OvRank              1404 non-null float64
# player_nfl_link     10650 non-null object
# player_team_link    10650 non-null object
# Player_ID           10650 non-null object
# dtypes: float64(26), int64(2), object(6)
# memory usage: 2.8+ MB

# This is good, it means our numbers are stored as numbers now. However, we still need to replace the empty cells in numeric columns with 0 instead of NaN.

# Get the column names for the numaric columns:
num_cols = fantasy_df.columns[fantasy_df.dtypes != object]

# Replace all the NaNs with 0:
fantasy_df.loc[:, num_cols] = fantasy_df.loc[:, num_cols].fillna(0)

#Run the .info() method again and we get:
#fantasy_df.info()

# RangeIndex: 10650 entries, 0 to 10649
# Data columns (total 34 columns):
# Season              10650 non-null int64
# Rk                  10650 non-null float64
# Player              10650 non-null object
# Team                10650 non-null object
# Position            10650 non-null object
# Age                 10650 non-null float64
# G                   10650 non-null float64
# GS                  10650 non-null float64
# Pass_Cmp            10650 non-null float64
# Pass_Att            10650 non-null float64
# Pass_Yds            10650 non-null float64
# Pass_TD             10650 non-null float64
# Pass_INT            10650 non-null float64
# Rush_Att            10650 non-null float64
# Rush_Yds            10650 non-null float64
# Rush_YpA            10650 non-null float64
# Rush_TD             10650 non-null float64
# Rec_Tgt             10650 non-null float64
# Rec                 10650 non-null float64
# Rec_Yds             10650 non-null float64
# Rec_YpR             10650 non-null float64
# Rec_TD              10650 non-null float64
# Two_PT_Made         10650 non-null float64
# Two_PT_Pass         10650 non-null float64
# Fantasy_Pts         10650 non-null float64
# PPR_Pts             10650 non-null float64
# DraftKings_Pts      10650 non-null float64
# FanDuel_Pts         10650 non-null float64
# VBD                 10650 non-null float64
# PosRank             10650 non-null int64
# OvRank              10650 non-null float64
# player_nfl_link     10650 non-null object
# player_team_link    10650 non-null object
# Player_ID           10650 non-null object
# dtypes: float64(26), int64(2), object(6)
# memory usage: 2.8+ MB

# All of our cells are filled. Now we save the CLEAN file to a CSV.
#fantasy_df.to_csv("pfr_nfl_fantasy_data_CLEAN.csv", index=False)

