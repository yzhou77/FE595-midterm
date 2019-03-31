import pandas as pd

def ratingclean(data):
    raw_rating = data["Rating"]
    rating = raw_rating.dropna(axis=0,how='all')
    clean = []
    for item in rating:
        if len(item) > 10:
            pass
        elif item =="A":
            clean.append(10)
        elif item =="A-":
            clean.append(9)
        elif item =="B+":
            clean.append(8)
        elif item =="B":
            clean.append(7)
        elif item =="B-":
            clean.append(6)
        elif item =="C+":
            clean.append(5)
        elif item =="C":
            clean.append(4)
        elif item =="C-":
            clean.append(3)
        elif item =="D+":
            clean.append(2)
        elif item =="D":
            clean.append(1)
        elif "/" in item:
            a = item.split("/")[0]
            b = item.split("/")[1]
            c = round(float(a)/float(b)*10)
            clean.append(c)
    return clean

if __name__ == '__main__':
    data = pd.read_csv("harry_potter_and_the_goblet_of_fire.csv")
    print (ratingclean(data))