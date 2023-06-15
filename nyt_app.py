'''
    Access NYT Article Search API
    Choose last 10 articles with pub_date in April 2023
    Populate a CSV from the data set: _id, pub_date, headline, section_name, word_count, snippet
    Clean snippet - truncate to 50 characters
    Optional: Upload the file to Google Drive

    Assumptions and Comments:
    1. I assumed headline should be the text found in the "main" attribute rather than the schema/dictionary "headline"
    2. Since the API only returns 10 articles at a time and the sort parameter provides them in descending order, I only requested one page
    3. Generic error handling has been provided
    4. google_apis.py is a script to send the file to Google Drive - credit belongs to Jie Jenn at his YouTube channel - https://www.youtube.com/watch?v=1-22Rnn7Zcc
    5. To execute this script: python nyt_app.py --api_key=<api_key which was provided privately or your own NYT api_key>
    6. It uses the following parameter definitions - (--api_key is the only mandatory parameter)

    parser = argparse.ArgumentParser(prog='NYT App', description='From the NYT Article Search API, pull the last 10 articles dated April 2023. '
             'If desired,the file can be sent to a Google Drive folder - a valid client secrets file must be in the current working directory and must be named "credentials.json"')
    parser.add_argument('--api_key', required=True, help='(Required)api_key which was provided privately or your own api_key')
    parser.add_argument('--file_name', help='file name to write data to and send to Google Drive')
    parser.add_argument('--file_path', help='path to file')
    parser.add_argument('--parent_folder_id', help='the XXX portion in a Google Drive URL (https://drive.google.com/drive/folders/XXX)')
'''

import requests, json, csv, sys, argparse, os
from csv import writer
import pandas as pd
from googleapiclient.http import MediaFileUpload
from google_apis import create_service
import mimetypes

BASE_URL = 'https://api.nytimes.com/'
COLLIST = ['_id', 'pub_date', 'headline', 'section_name', 'word_count', 'snippet']
GOOGLE_API_NAME = 'drive'
GOOGLE_API_VERSION = 'v3'
GOOGLE_SCOPES = ['https://www.googleapis.com/auth/drive']
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
def send_to_google_drive(file_name, file_path, parent_folder_id):

    client_file = 'credentials.json'

    service = create_service(client_file, GOOGLE_API_NAME, GOOGLE_API_VERSION, GOOGLE_SCOPES)

    mime_type, _ = mimetypes.guess_type(file_path)
    media_content = MediaFileUpload(file_path)
    request_body = {
        'name': file_name
    }

    if parent_folder_id:
        request_body['parents'] = [parent_folder_id]
    print('Uploading file {0}...'.format(file_name))

    service.files().create(
        body=request_body,
        media_body=media_content
    ).execute()

def main(api_key, file_name, file_path, parent_folder_id):
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
    write_file(file_name, article)

    if parent_folder_id is not None:
        send_to_google_drive(file_name, file_path+'\\'+file_name, parent_folder_id)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='NYT App', description='From the NYT Article Search API, pull the last 10 articles dated April 2023. '
             'If desired,the file can be sent to a Google Drive folder - a valid client secrets file must be in the current working directory and must be named "credentials.json"')
    parser.add_argument('--api_key', required=True, help='(Required)api_key which was provided privately or your own api_key')
    parser.add_argument('--file_name', help='file name to write data to and send to Google Drive')
    parser.add_argument('--file_path', help='path to file')
    parser.add_argument('--parent_folder_id', help='the XXX portion in a Google Drive URL (https://drive.google.com/drive/folders/XXX)')

    args = parser.parse_args()
    print(args)

    if args.file_name is None:
        print('Using default file name: nyt.csv')
        file_name = 'nyt.csv'
    else:
        file_name = args.file_name
    if args.file_path is None:
        print("Using default file path: '.'")
        file_path = '.'
    else:
        file_path = args.file_path
    if args.parent_folder_id is None:
        print('Google parent folder not specified. File will not be sent to Google Drive')

    main(args.api_key, file_name, file_path, args.parent_folder_id)

