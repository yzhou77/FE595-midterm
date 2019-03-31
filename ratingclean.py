import pandas as pd
import numpy as np

def ratingclean(data):
    for i in range(len(data)):
        item = data["Rating"][i]
        if type(item) == float:
            data.loc[i,"Rating"] = np.nan
        elif len(item) > 10:
            data.loc[i,"Rating"] = np.nan
        elif item =="A":
            data.loc[i,"Rating"] = 10
        elif item =="A-":
            data.loc[i,"Rating"] = 9
        elif item =="B+":
            data.loc[i,"Rating"] = 8
        elif item =="B":
            data.loc[i,"Rating"] = 7
        elif item =="B-":
            data.loc[i,"Rating"] = 6
        elif item =="C+":
            data.loc[i,"Rating"] = 5
        elif item =="C":
            data.loc[i,"Rating"] = 4
        elif item =="C-":
            data.loc[i,"Rating"] = 3
        elif item =="D+":
            data.loc[i,"Rating"] = 2
        elif item =="D":
            data.loc[i,"Rating"] = 1
        elif "/" in item:
            a = item.split("/")[0]
            b = item.split("/")[1]
            c = round(float(a)/float(b)*10)
            if c > 10:
                c = 10
            if c < 1:
                c = 1
            data.loc[i,"Rating"] = c
    data.to_csv('ratingclean.csv')
    return data

if __name__ == '__main__':
    data = pd.read_csv("harry_potter_and_the_goblet_of_fire.csv")
    print (ratingclean(data))
