import lyricsgenius
import requests
import json
from bs4 import BeautifulSoup
from fbchat import log, Client
from fbchat.models import *

GENIUS = lyricsgenius.Genius("{KEY}")

COOKIES = 'PUT COOKIES HERE'

THREAD_ID = 'THREAD ID'

def main():
    client = Facebook('{USERNAME}', '{PASSWORD}', session_cookies = COOKIES)
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

    

def scapreLyrics(pageURL):
    page = requests.get(pageURL)
    HTML = BeautifulSoup(page.text, "html.parser")
    lyrics = HTML.find('div', class_= 'lyrics').get_text()
    return lyrics

if __name__ == "__main__":
    main()

