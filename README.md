# NYT-App
Description:
    Access NYT Article Search API
    Choose last 10 articles with pub_date in April 2023
    Populate a CSV from the data set: _id, pub_date, headline, section_name, word_count, snippet
    Clean snippet - truncate to 50 characters
Usage: python nyt_app.py api-key={api_key supplied separately - or - your own NYT registered api_key}
Assumptions and Comments:
    1. I assumed "headline" meant the text found in the "main" attribute rather than the schema/dictionary "headline"
    2. Since the API only returns 10 articles at a time and the sort parameter provides them in descending order, I only requested one page
    3. While multiple methods were not required, I provided them as an example of methods that could be expanded upon for other examples or data sets
    4. Generic error handling has been provided
