from Get_id import get_id
from Scraping import getData
from ratingclean import ratingclean
from Regression import extractDataWithRating, doRegression, plotRegression, ratingRectification
import pandas as pd
import numpy as np
import requests as req
from flask import Flask
import cgi, cgitb

def getrate(Name):
    id = get_id(Name)
    getData(id)
    data2 = pd.read_csv(id + '.csv')
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

def search(request):
    res = []
    Name = request.GET.get('text')
    ScoreResponded = getrate(Name)
    res.append(Name)
    res.append(ScoreResponded)
#    return render_template('../../templates/Portal.html', data=a2)
    return render(request, '../templates/Portal.html', {'context': json.dumps(res)})

if __name__ == '__main__':
    Name = 'the goblet of fire'
    Name = 'The revengers'
    if req.method == 'POST':
        Name = req.form['txt']
    score = getrate(Name)
    print('The correction score of this movie is :', score)





