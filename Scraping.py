import requests                   
import pandas as pd
from bs4 import BeautifulSoup
#import matplotlib.pyplot as plt
import re
import time
import pandas as pd
from Get_id import get_id

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
    return data


if __name__ == '__main__':
    Name = 'the goblet of fire'
    id = get_id(Name)
    data = getData(id)
    print (data.head())
