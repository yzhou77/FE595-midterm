import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
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
from Scraping import getData
from ratingclean import ratingclean
from Regression import extractDataWithRating
from Regression import doRegression
from Regression import plotRegression
from Regression import ratingRectification

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
    print(getrate(Name))
