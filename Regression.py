from sklearn import datasets
from sklearn.model_selection import cross_val_predict
from sklearn import linear_model
#import matplotlib.pyplot as plt
import matplotlib.cm
import pandas as pd
import numpy as np
import math
from nltk.sentiment.vader import SentimentIntensityAnalyzer


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
    #plt.scatter(x_test, y_test, color='black')
    #plt.plot(x_test, y_pred, color='blue', linewidth=3)
    #plt.grid(True)
    #plt.axhline(y=0, color='k')
    #plt.show()


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
    data = pd.read_csv("ratingclean.csv")
    variable_list = extractDataWithRating(data)
    nltk_score_array = variable_list[0]
    Rate_array = variable_list[1]
    reg = doRegression(nltk_score_array, Rate_array)
    Intercept = float(reg[0].intercept_)
    Coefficient = float(reg[0].coef_)
    # Intercept is 7.593519690273348
    # Coefficient is 0.712726450162214
    data_rectified = ratingRectification(data, Coefficient, Intercept)
    plotRegression(nltk_score_array, Rate_array)
    ScoreResponded = data_rectified.loc[:, "Rating"].mean()








