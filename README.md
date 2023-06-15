# NYT-App
Description:
    Access NYT Article Search API
    Choose last 10 articles with pub_date in April 2023
    Populate a CSV from the data set: _id, pub_date, headline, section_name, word_count, snippet
    Clean snippet - truncate to 50 characters
    Optional: Upload the file to Google Drive
Usage: python nyt_app.py api-key={api_key supplied separately - or - your own NYT registered api_key}
Assumptions and Comments:
    1. I assumed headline should be the text found in the "main" attribute rather than the schema/dictionary "headline"
    2. Since the API only returns 10 articles at a time and the sort parameter provides them in descending order, I only requested one page
    3. Generic error handling has been provided
    4. google_apis.py is a script to send the file to Google Drive - credit belongs to Jie Jenn at his YouTube channel - https://www.youtube.com/watch?v=1-22Rnn7Zcc
    5. It uses the following parameter definitions (--api_key is the only mandatory parameter):

    parser = argparse.ArgumentParser(prog='NYT App', description='From the NYT Article Search API, pull the last 10 articles dated April 2023. '
             'If desired,the file can be sent to a Google Drive folder - a valid client secrets file must be in the current working directory and must be named "credentials.json"')
    parser.add_argument('--api_key', required=True, help='(Required)api_key which was provided privately or your own api_key')
    parser.add_argument('--file_name', help='file name to write data to and send to Google Drive')
    parser.add_argument('--file_path', help='path to file')
    parser.add_argument('--parent_folder_id', help='the XXX portion in a Google Drive URL (https://drive.google.com/drive/folders/XXX)')
