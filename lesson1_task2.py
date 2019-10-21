import requests
from pprint import pprint
import json

main_link = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup'
land = 'en-ru'
word = 'provided'
appid = 'dict.1.1.20191019T132240Z.7a336cf3ce4dfa5c.1ae2bc0e453401abcb0850a339f31b2a523c931f'
req = requests.get(f'{main_link}?key={appid}&lang={land}&text={word}')
if req.ok:
    with open(f'translate_{word}_{land}_.json', 'wb') as file:
        file.write(req.content)

data = json.loads(req.text)

print("Слово ", data["def"][0]["text"], " перевод:")
for i in data["def"][0]["tr"]:
    print(i["text"])




