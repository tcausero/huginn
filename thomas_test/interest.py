from pytrends.request import TrendReq
import pandas as pd

pytrends = TrendReq(hl='en-US', #language
                    tz=360) #timezone (US CST is 360)

def get_keyword():
    keyword = input('keyword: ')
    return keyword

def get_mid(keyword):
    print(pytrends.suggestions(keyword))
    mid = input('Enter the mid you are interested in: ')
    return mid

def get_interest(keyword, mid):
    pytrends.build_payload([mid], #up to 5 terms in the list
                           cat=0, #default to no category
                           timeframe='all', #Date to start from 
                           geo='', #two letter country abreviation (default to world)
                           gprop='news') #what property to filter to (images, news, youtube or froogle 
                                     #(for Google Shopping results))
    data = pytrends.interest_over_time() #two columns (mid name <-> interest and isPartial) + index = date
    data.drop(columns = 'isPartial', inplace = True) #rermove isPartial column
    data.columns = [keyword] #rename the column with the keyword name instead of the mid name
    return data