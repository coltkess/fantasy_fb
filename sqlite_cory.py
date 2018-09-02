import sqlite3
from reference_scraper import fantasy_df

conn = sqlite3.connect('fantasy_football_since_2000.db')

c = conn.cursor()

# The triple quotes create a docstring. It allows us to write a string that's multiple lines without any special breaks or anything like that.
c.execute("""CREATE TABLE fantasy_stats (
            Rk integer,
            Player text,
            Team text,
            Position text,
            Age integer,
            G integer,
            GS integer,
            Pass_Cmp integer,
            Pass_Att integer,
            Pass_Yds integer,
            Pass_TD integer,
            Rush_Att integer,
            Rush_Yds integer,
            Rush_YpA float,
            Rush_TD integer,
            Rec_Tgt integer,
            Rec integer,
            Rec_Yds integer,
            Rec_YpR float,
            Rec_TD integer,
            Two_Pt_Made integer,
            Two_Pt_Pass integer,
            Fantasy_Pts float,
            PPR_Pts float,
            DraftKings_Pts float,
            FanDuel_Pts float,
            VBD integer,
            PosRank integer,
            OvRank integer,
            player_nfl_link text,
            player_team_link text
)""")