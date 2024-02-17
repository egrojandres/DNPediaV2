##################################################################
# At moment continue with txt file for search on each keywords.
# Upgrades:
# 1. reduce the keyword file DONE
# 2. Change the Keywords .txt file to DB type file to reorganize the searches.
# 5. Start with Tkinter window in main script
# 2.2 Create a new def to read and clasify the searches that were performed
# 3. Create filters: Filter by response: Parking sites
# 4. Add new Class to search on a new source: Phistats

#################################################################

import requests
import datetime
import json
import os

class Search:

    # Here get the relative current path in the folder

    ruta_ext_actual = os.path.abspath(__file__)
    path_automatico = os.path.dirname(os.path.dirname(ruta_ext_actual))
    keywordnt_path = os.path.join(
        path_automatico, "BootstrapConsoleTk", "ignoreKeywords.txt")
    keywords_path = os.path.join(
        path_automatico, "BootstrapConsoleTk", "keywords.txt")

    # Here you stablish the apikeys secret to do a research

    apikey = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    apisecret = "777777777777777777"
    apiurl = "https://api.codepunch.com/dnfeed/v2/"
    url = []

    # Constructor function
    def __init__(self, dayForReview):
        self.dayForReview = dayForReview

    # Filter all the Urls researched for ignore the ignore keywords
    def ignoreKeywords(self, site, keywordnt):

        filterApplied = []
        for url in site:
            if not any(key in url for key in keywordnt):
                filterApplied.append(url)
        return filterApplied

    # check if the files from keywords and ignorekeywords was modified: eliminate the repeat key and sort the list
    def filterKeyword(self, typeText, filePath):
        unique_keyword = []
        key_words = [kw.strip() for kw in typeText]
        [unique_keyword.append(kw)
         for kw in key_words if kw not in unique_keyword]
        unique_keyword.sort()
        with open(filePath, 'w+') as changes:
            for w in unique_keyword:
                changes.write(w + '\n')
        return unique_keyword

    # get_api_token
    def get_api_token(self):
        parameters = {"c": "auth", "k": Search.apikey, "s": Search.apisecret}
        response = requests.get(Search.apiurl, params=parameters)
        if (response.status_code == 200):
            if response.content.startswith(b"OK: "):
                # print('authentication OK')
                return response.content[4:]
            else:
                raise Exception(
                    'Authentication: {}' . format(response.content))
        else:
            raise Exception(
                'Authentication: {}' . format(response.status_code))

    # get_api_data
    def get_api_data(self, parameters):
        response = requests.get(Search.apiurl, params=parameters)
        if (response.status_code == 200):
            if response.content.startswith(b"Error: "):
                raise Exception(format(response.content[7:]))
        else:
            raise Exception(
                'Invalid response code: {}' . format(response.status_code))
        return response.content

    # Export the results to a suspicious URL file txt
    def exportTxt(self, listToCheck, key):
        unique_url = []
        # Save urls without repeating them
        [unique_url.append(elements)
         for elements in listToCheck if elements not in unique_url]

        # Export the results to a .txt file
        suspicious_urls_path = os.path.join(
            Search.path_automatico, "BootstrapConsoleTk", "suspiciousURLS.txt")

        with open(suspicious_urls_path, 'w+', encoding="utf-8") as results:
            # For clasify
            results.write(key+'\n')
            for url in unique_url:
                results.write('https://' + url + '\n')

    # Make a search with a Keyword
    def DoAsearch(self, keyword):
        kw = '%'+keyword+'%'
        days = 0
        while days < int(self.dayForReview):
            try:
                # Get the token and then the data
                token = self.get_api_token()
                search_on_day = datetime.date.today() - datetime.timedelta(days)
                datecode = search_on_day.strftime("%Y%m%d")
                parameters = {"t": token, "d": datecode,
                              "f": "json", "limit": 500, "kw": kw}
                thedata = self.get_api_data(parameters)
                domaindata = json.loads(thedata)

                for d in domaindata['domains']:
                    Search.url.append(d['domain'])
            except Exception as e:
                print(f'{type(e)}, {str(e)} in: {search_on_day}, {keyword}')
            days += 1

            with open(Search.keywordnt_path, "r") as eachKeywordnt:

                # Unique Keyword
                keywordnt = self.filterKeyword(
                    eachKeywordnt, Search.keywordnt_path)
                # Filter url
                result = self.ignoreKeywords(Search.url, keywordnt)
        self.exportTxt(result, keyword)

    def DoASearchFromKeys(self):

        with open(Search.keywords_path, "r") as eachKeyword:
            keywords = self.filterKeyword(eachKeyword, Search.keywords_path)
        for k in keywords:
            self.DoAsearch(k)


if __name__ == '__main__':

    while True:
        try:
            # Change Number, Depend of User Entry betwen 1 to 7
            keyword = input("Please entry a Keyword to search\n")
            print("Press enter for Search by Keywords default list")
            dayForReview = input("Enter the number of days to be consulted\n")

            if dayForReview.isdigit() and int(dayForReview) in range(1, 50):
                break
            else:
                raise ValueError
        except ValueError as e:
            print(f"{e},Please enter a correct data or Enter Only days Betwen 1-50")

    # Create a new object
    NewSearch = Search(dayForReview)
    # Conditional to search from a Keyword or all the Dictionary
    if keyword == "":
        NewSearch.DoASearchFromKeys()
    else:
        NewSearch.DoAsearch(keyword)
