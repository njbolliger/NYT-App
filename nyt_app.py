'''
    Access NYT Article Search API
    Choose last 10 articles with pub_date in April 2023
    Populate a CSV from the data set: _id, pub_date, headline, section_name, word_count, snippet
    Clean snippet - truncate to 50 characters

    Assumptions and Comments:
    1. I assumed headline should be the text found in the "main" attribute rather than the schema/dictionary "headline"
    2. Since the API only returns 10 articles at a time and the sort parameter provides them in descending order, I only requested one page
    3. While multiple methods were not required, I provided them as an example of methods that could be expanded upon for other examples or data sets
    4. Generic error handling has been provided
'''

import requests, json, csv, sys, argparse
from csv import writer
import pandas as pd

BASE_URL = 'https://api.nytimes.com/'
COLLIST = ['_id', 'pub_date', 'headline', 'section_name', 'word_count', 'snippet']

def get_rsp(endpoint, params, headers):
    try:
        rsp = requests.get(endpoint, params=params, headers=headers)
    except Exception:
        print(f"Exception encountered: ", Exception)
        return(-1)
    else:
        return(rsp)

def nyt_article(rsp):
    try:
        ds = pd.json_normalize(rsp.json(),max_level=4)
        df = pd.DataFrame(ds['response.docs'][0])
        headline = pd.DataFrame(list(df['headline']))
        article = df[COLLIST].copy()
        article['headline'] = headline['main']
        article['snippet'] = article['snippet'].str[:50]
    except:
        print(f"Error encountered is json attributes")
        return(False, None)
    else:
        return(True, article)

def write_file(filename, article):
    try:
        article.to_csv(filename, index=False, encoding ='utf-8-sig', quoting=csv.QUOTE_ALL)

        attribution = ['Data provided by the New York Times - https://developer.nytimes.com']
        with open(filename, 'a') as file:
            writer_object = writer(file)
            writer_object.writerow([])
            writer_object.writerow(attribution)
            file.close()

    except:
        print(f"Error writing to csv file: ", filename)
        return(False)
    else:
        print(f"Data successfully pulled from API: ", BASE_URL, " and written to file: ", filename)
        return(True)

def main(api_key):
    # NYT Article Search
    endpoint = BASE_URL + 'svc/search/v2/articlesearch.json?api-key=' + api_key
    params = {'begin_date': '20230401', 'end_date': '20230430', 'sort': 'newest', 'page':0}
    headers = {"Accept": "application/json"}

    # Access the API
    rsp = get_rsp(endpoint, params, headers)
    if rsp == -1:
        exit()
    elif rsp.status_code != 200:
        print(f"Failure: invalid status code, {rsp.status_code}")
        exit()

    # Simplify the output
    retval, article = nyt_article(rsp)
    if retval is False:
        exit()

    # Write output to file
    write_file('nyt.csv', article)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='NYT App', description='From the NYT Article Search API, pull the last 10 articles dated April 2023 ')
    parser.add_argument('--api_key', help='api_key which was provided privately or your own api_key')
    args = parser.parse_args()
    vars = vars(args)

    main(vars['api_key'])
