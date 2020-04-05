##################################
# GET INTEREST FILE (volume of Google Searches per month)

from pytrends.request import TrendReq

def get_pytrend():
    """Get pytrends to scrap Google Trends data"""
    pytrends = TrendReq(hl='en-US', #language
                        tz=360) #timezone (US CST is 360)
    return pytrends

def get_keyword():
    """Ask for the keyword (entity or person) you would like some information about"""
    keyword = input('keyword: ')
    return keyword

def get_mid(keyword):
    """Ask for the mid your are interested in. Pytrends has a very useful method '.suggestions' which enables to 
    specify your research (Ex: Apple could be a company or a fruit)
    """
    pytrends = get_pytrend()
    print(pytrends.suggestions(keyword))
    mid = input('Enter the mid you are interested in: ')
    return mid

def get_interest(keyword, mid):
    """Get the time series of interest by month for the selected entity (keyword and mid)
    
    :argument keyword: entity name
    :argument mid: returned by the above function to get precision
    
    :return: dataframe with dates as index and one column named keyword which corresponds to the interest by month
    """
    pytrends = get_pytrend()
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