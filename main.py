from Get_id import get_id
from Scraping import getData
from ratingclean import ratingclean
from Regression import extractDataWithRating,doRegression,plotRegression,ratingRectification
import pandas as pd


def getrate(Name):
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
    return ScoreResponded

if __name__ == '__main__':
    Name = 'the goblet of fire'
    Name = 'The avengers'
    score = getrate(Name)
    print('The correction score of this movie is :', score)



