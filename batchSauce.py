import webbrowser
import requests
import time
from config import saucenao_API_key
from os import listdir
from os.path import isfile, join
from saucenao_api import SauceNao

# Uses sauceNAO and sauceNAO_api to find sources for large batches of images
# SauceNAO limits search results to 4 every 30 seconds and 99 a day
# Currently have working methods for twitter url images and local files.

# Cleans twitter image urls for saucenao and opens webbrowser to sauceNAO for image after time limit.
def twitter_url():
    f = open("ursl.txt", "r")
    cleaned_Urls = []
    for x in f:
        t = x[8:]
        t = t.replace("/", "%2F").replace("?", "%3F").replace("=", "%3D").replace("&", "%26")
        t = "https://saucenao.com/search.php?db=999&url=https%3A%2F%2F" + t
        cleaned_Urls.append(t)

    count = 4
    for url in cleaned_Urls:
        count = count - 1
        webbrowser.open_new(url)
        # sauceNAO has limit to number of uses before timeout. Script waits so we do not trigger timeout.
        if (count == 0):
            count = 4
            time.sleep(40) 


# Opens local folder of images and opens most similar result in browser.
def files():
    #Needs own API key, can register at https://saucenao.com/user.php?page=search-api
    sauce = SauceNao(saucenao_API_key)
    onlyfiles = [f for f in listdir('Images') if isfile(join('Images', f))]
    count = 4
    for filename in onlyfiles:
        count = count - 1
        fileSource = open('Images/' + filename, "rb")
        results = sauce.from_file(fileSource)  # or from_file()
        if(bool(results)):
            webbrowser.open(''.join(results[0].urls)) # Opens must relevant source
        else:
            print("Image Not Found")
        if (count == 0):
            count = 4
            time.sleep(40) 

# twitter_url()
# files()
print("Finished")