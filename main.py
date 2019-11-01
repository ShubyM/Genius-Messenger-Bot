import lyricsgenius
import requests
import json
from bs4 import BeautifulSoup
from fbchat import log, Client
from fbchat.models import *

GENIUS = lyricsgenius.Genius("sSrEtcF9IWH5X_h6WEBRHny2tcEneYkSzCXUDGDkchQxcU1xbT4cPhZh8cp4QgmB")


COOKIES = {'c_user': '100004418385553', 'datr': 'eE6mXTssnbjRG-8e7XtDQ6As', 'fr': '1woTObromiNOetvDF.AWVKc50ojLXde2VaRhBeWk2WPOk.Bdpk54.fR.AAA.0.0.Bdpk54.AWXKPZAy', 'noscript': '1', 'sb': 'eE6mXbsjpdJeg3vTCO8CR2cE', 'spin': 'r.1001296022_b.trunk_t.1571180156_s.1_v.2_', 'xs': '9%3AqUqwJg-gp5wh_A%3A2%3A1571180152%3A1737%3A2920'}

THREAD_ID = '2131940626892478'

def main():
    client = Facebook('shadownarutoex@gmail.com', 'manihatethissomuch', session_cookies = COOKIES)
    print(client.getSession())
    client.listen()

class Facebook(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        message = message_object.text
        messageID = message_object.uid
       
        if 'music:' in message.lower():
            lyrics = getLyrics2(message[6:len(message)])
            if (lyrics != None or lyrics != ''):
                message_id=self.send(
                    Message(text = lyrics), thread_id = THREAD_ID , thread_type = ThreadType.GROUP)

def getLyrics(query):
    """ Method to return lyrics of a song searched on rap genius,
    paramter is a string which can be a song name or a query on rap genius"""

    if ('hakun' in query.lower()):
        return 'Hakuna Matata! What a wonderful phrase \n Hakuna Matata! Ain\'t no passing craze'

    json = GENIUS.search_genius(query)
    url = (json.get('hits')[0].get('result').get('url'))
    lyrics = GENIUS._scrape_song_lyrics_from_url(url)

    if 'Chorus' in lyrics:
        startChorus = lyrics.find('[Chorus')
        endChorus = lyrics.find('[', startChorus + 6)

    elif 'Hook' in lyrics:
        startChorus = lyrics.find('Hook')
        return lyrics[startChorus : startChorus + 281]

    elif 'Verse' in lyrics:
        startChorus = lyrics.find('Verse')
        endChorus = lyrics.find('Verse', startChorus + 6)

    else:
        return lyrics[0: 281]

    toReturn = lyrics[startChorus : endChorus]

    if len(toReturn) > 281:
        return toReturn[0: 281]

    else:
        return toReturn


def getLyrics2(query):
    ''' Making this bymyself cuz kevin a bitch'''
    URL = 'https://api.genius.com/search'
    TOKEN = "xNBeSpotSfbLaXuRiRMTNWIX6qOfuQ44gjoLYECiLBbIp17Bs749zjsr6kHFRrhI"

    params = {
        'q' : query,
        'access_token' : TOKEN
    }

    search_results = requests.get(url = URL, params = params)
    search_results = search_results.json()['response']
    pageURL = search_results.get('hits')[0].get('result').get('url')

    lyrics = scapreLyrics(pageURL)

    if 'Chorus' in lyrics:
        startChorus = lyrics.find('[Chorus')
        endChorus = lyrics.find('[', startChorus + 6)

    elif 'Verse' in lyrics:
        startChorus = lyrics.find('Verse')
        endChorus = lyrics.find('Verse', startChorus + 6)

    else:
        return lyrics[0: 281]

    toReturn = lyrics[startChorus : endChorus]

    if len(toReturn) > 281:
        return toReturn[0: 281]

    else:
        return toReturn

def scapreLyrics(pageURL):
    page = requests.get(pageURL)
    HTML = BeautifulSoup(page.text, "html.parser")
    lyrics = HTML.find('div', class_= 'lyrics').get_text()
    return lyrics

if __name__ == "__main__":
    main()

