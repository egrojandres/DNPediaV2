import requests
import json
import datetime
import os

class SearchDNP:
    def __init__(self, daysToReview):
        self.daysToReview = daysToReview
            
        # Provide your keys
        self.apikey = "PutYourApiKeyHere"
        self.apisecret = "PutYourSecretKeyHere"
        self.apiurl = "https://api.codepunch.com/dnfeed/v2/"
        self.keyPath, self.ignoreKeyPath, self.suspiciousUrlsPath = self.relative_path()
        self.url = []

    def relative_path (self):
        # Here get the relative current path in the folder
        ruta_ext_actual = os.path.abspath(__file__)
        path_automatico = os.path.dirname(os.path.dirname(ruta_ext_actual))
        keywordnt_path = os.path.join(
            path_automatico, "DNPediaV2", "ignoreKeywords.txt")
        keywords_path = os.path.join(
            path_automatico, "DNPediaV2", "keywords.txt")
        suspicious_path = os.path.join(
            path_automatico, "DNPediaV2", "suspiciousURLS.txt")
        return keywords_path, keywordnt_path, suspicious_path

    def get_api_token(self):
        AUTHURLFMT = f"{self.apiurl}auth/{self.apikey}/{self.apisecret}"
        #url = AUTHURLFMT.format(apiurl, apikey, apisecret)
        response = requests.get(AUTHURLFMT)
        if response.status_code == 200:
            apiresponse = response.json()
        else:
            raise Exception(f'Authentication: {response.status_code}')
        if bool(apiresponse['status']) != True:
            raise Exception(apiresponse['error'])
        return apiresponse['token']
            
    def get_api_data(self, token, command, parameters):
        APIURLFMT = f"{self.apiurl}{token}/{command}/"
        response = requests.get(APIURLFMT, params=parameters)
        if (response.status_code == 200):
            if response.content.startswith(b"Error: "):
                raise Exception(format(response.content[7:]))
        else:
            raise Exception(
                'Invalid response code: {}' . format(response.status_code))
        return response.content
    
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

    def ignoreKeywords(self, site, keywordnt):
        filterApplied = []
        for url in site:
            if not any(key in url for key in keywordnt):
                filterApplied.append(url)
        return filterApplied

    def exportTxt(self, listToCheck):
        unique_url = []
        # Save urls without repeating them
        [unique_url.append(elements)
         for elements in listToCheck if elements not in unique_url]     
        # Export the results to a .txt file
        with open(self.suspiciousUrlsPath, 'w+', encoding="utf-8") as results:
            for url in unique_url:
                if '-->' in url:
                    results.write(url + '\n')
                else: results.write('https://' + url + '\n')

    def DoAsearch(self, keyword):
        token = self.get_api_token()
        days = 0
        while days <= int(self.daysToReview):
            try:
                # Get the token and then the data
                search_on_day = datetime.date.today() - datetime.timedelta(days)
                print(f'{search_on_day}')

                datecode = search_on_day.strftime("%Y%m%d")
                
                parameters = { "date": datecode,"kw": keyword, "dcm":"eq",
                              'start':0, "limit": 500, "idn":2,
                                "sorton":"date", "sortoden":"asc", "dm":"data"}
                thedata = self.get_api_data(token,"added",parameters )
                domaindata = json.loads(thedata)

                self.url.append(f'--> {keyword} :{search_on_day}\n')
                for d in domaindata['data']:
                    print(d['domain'])
                    self.url.append(d['domain'])
            except Exception as e:
                print(f'{type(e)}, {str(e)} in: {search_on_day}, {keyword}')
            days += 1

            with open(self.ignoreKeyPath, "r") as eachKeywordnt:
                # Unique Keyword
                keywordnt = self.filterKeyword(
                    eachKeywordnt, self.ignoreKeyPath)
                # Filter url
                result = self.ignoreKeywords(self.url, keywordnt)
        #[print (u) for u in result] 
        self.exportTxt(result)
    
    def DoASearchFromKeys(self):
        with open(self.keyPath, "r") as eachKeyword:
            keywords = self.filterKeyword(eachKeyword, self.keyPath)
        for k in keywords:
            self.DoAsearch(k)
   
if __name__ == '__main__':
        while True:
            #	Get the token and then the data
            try:
                keyword = input("Please entry a Keyword to search\n")
                print("Press enter for Search by Keywords default list")
                dayForReview = input("Enter the number of days to be consulted\n")

                if dayForReview.isdigit() and int(dayForReview) in range(1, 8):
                    break
                else:
                    raise ValueError
            except ValueError as e:
                print(f"{e},Please enter a correct data or Enter Only days Betwen 1-7")
        NewSearch = SearchDNP(dayForReview)
        # Find domains
        if keyword == "":
            NewSearch.DoASearchFromKeys()
        else:
            NewSearch.DoAsearch(keyword)