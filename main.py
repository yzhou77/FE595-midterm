import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
from Get_id import get_id
import numpy as np
from sklearn import datasets
from sklearn.model_selection import cross_val_predict
from sklearn import linear_model
import matplotlib.pyplot as plt
import matplotlib.cm
import math
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from rotten_tomatoes_client import RottenTomatoesClient

def getData(movie_id):
    page = requests.get('https://www.rottentomatoes.com/m/'+ movie_id + '/reviews/')
    soup = BeautifulSoup(page.content, 'html.parser')
    Divs=soup.select("span.pageInfo")
    pageinfo = Divs[0].get_text()
    LastSpace = pageinfo.rfind(' ')
    page = int(pageinfo[LastSpace+1:])
    divs=soup.select("div.review_table_row")
    res = []
    for p in range(1,page+1):
        page = requests.get('https://www.rottentomatoes.com/m/'+ movie_id + '/reviews/?page='+str(p)+'&sort=')
        soup = BeautifulSoup(page.content, 'html.parser')
        divs=soup.select("div.review_table_row")
        print ('Currently scraping page: ', p)
        for div in divs:
            date = div.select("div.review_area .review_date")[0].get_text()
            review = div.select("div.review_area .the_review")[0].get_text()
            score = div.select("div.review_area .small")[1].get_text()
            if len(score) > 15:
                num = score.find(':')
                Score = score[num+2:]
            else:
                Score = None
            res.append((date, review, Score))
    data =  pd.DataFrame(res, columns = ['Date', 'Review','Rating'])
    data.to_csv(movie_id+ '.csv')


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


def extractDataWithRating(data):
    nltk_score_list = []
    Rate_list = []
    analyzer = SentimentIntensityAnalyzer()
    for i in range(0, len(data)):
        nltk_score = []
        Rate = []
        if pd.notnull(data.iloc[i][4]) == True:
            nltk_dict = analyzer.polarity_scores(data.iloc[i][3])
            nltk_score.append(nltk_dict['compound'])
            nltk_score_list.append(nltk_score)
            Rate.append(data.iloc[i][4])
            Rate_list.append(Rate)
    nltk_score_array = np.array(nltk_score_list)
    Rate_array = np.array(Rate_list)
    data_list = []
    data_list.append(nltk_score_array)
    data_list.append(Rate_array)
    return data_list


def doRegression(nltk_score_array, Rate_array):
    lr = linear_model.LinearRegression()
    reg = []
    reg.append(lr.fit(nltk_score_array, Rate_array))
    return reg

def plotRegression(nltk_score_array, Rate_array):
    if len(nltk_score_array) != len(Rate_array):
        print("The mapping of arguments are not one-to-one. Please check your data again.")
    x_train = nltk_score_array
    x_test = nltk_score_array[-len(nltk_score_array):]
    y_train = Rate_array
    y_test = Rate_array[-len(Rate_array):]
    regr = linear_model.LinearRegression()
    regr.fit(x_train, y_train)
    y_pred = regr.predict(x_test)
    plt.scatter(x_test, y_test, color='black')
    plt.plot(x_test, y_pred, color='blue', linewidth=3)
    plt.grid(True)
    plt.axhline(y=0, color='k')
    plt.show()


def ratingRectification(data, coefficient, intercept):
    analyzer = SentimentIntensityAnalyzer()
    for i in range(len(data)):
        if pd.notnull(data.iloc[i][4]) == False:
            nltk_dict = analyzer.polarity_scores(data.iloc[i][3])
            nltk_score = nltk_dict['compound']
            score = coefficient * nltk_score + intercept
            data.loc[i, "Rating"] = math.floor(score)
    data.to_csv('ratingRectification.csv')
    return data


if __name__ == '__main__':
    Name = 'the goblet of fire'
    id = get_id(Name)
    getData(id)
    data2 = pd.read_csv(id+ '.csv')
    ratingclean(data2)
    data = pd.read_csv("ratingclean.csv")
    variable_list = extractDataWithRating(data)
    nltk_score_array = variable_list[0]
    Rate_array = variable_list[1]
    reg = doRegression(nltk_score_array, Rate_array)
    Intercept = float(reg[0].intercept_)
    Coefficient = float(reg[0].coef_)
    data_rectified = ratingRectification(data, Coefficient, Intercept)
    ScoreResponded = data_rectified.loc[:, "Rating"].mean()
    print(ScoreResponded)

