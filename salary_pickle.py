import pickle
import pandas as pd

# I needed to bring my dataframe into this file, but only wanted to do it once. So the code block below was only necessary to run one time. After I ran the whole process to get the dataframe, pickling saved it to an object which I could un-pack without running the whole scrape again.
#from salary_scraper import salaries_2000
#pickle_out2 = open("salary2000.pickle", "wb")
#pickle.dump(salaries_2000, pickle_out2)
#pickle_out2.close()

pickle_in = open("salary2000.pickle", "rb")
salaries2000 = pickle.load(pickle_in)

salaries2000["Player"], salaries2000["Position"] = salaries2000["Player, position"].str.split(",").str

del salaries2000["Player, position"]

print(salaries2000.head())