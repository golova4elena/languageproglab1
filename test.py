import json
import requests

url = 'http://127.0.0.1:8080'
print('Get without tz', requests.get(url).text)
print('Get with tz', requests.get(url + '/Asia/Novosibirsk').text)
print('Get with wrong tz', requests.get(url + '/ppp').text, '\n')

data = {'type': 'time', 'tz': 'Asia/Irkutsk'}
print('Post with wrong json: ', requests.post(url = url, data = data).text)
print('Time with tz: ', requests.post(url = url, data = json.dumps(data)).text)
data = {'type': 'time'}
print('Time without tz: ', requests.post(url = url, data = json.dumps(data)).text, '\n')

data = {'type': 'date', 'tz': 'America/Chicago'}
print('Date with tz: ', requests.post(url = url, data = json.dumps(data)).text)
data = {'type': 'date'}
print('Date without tz: ', requests.post(url = url, data = json.dumps(data)).text, '\n')

data = {'type': 'datediff', 'start': 'Europe/Moscow', 'end': 'Asia/Tokyo'}
print('Difference between two dates\t' + requests.post(url = url, data = json.dumps(data)).text)
data = {'type': 'datediff', 'start': 'Asia/Tokyo', 'end': 'Europe/Moscow'}
print('Difference between two dates (reverse)\t' + requests.post(url = url, data = json.dumps(data)).text)
data = {'type': 'datediff', 'end': 'Europe/Rome'}
print('Difference between server and tz\t' + requests.post(url = url, data = json.dumps(data)).text)
data = {'type': 'datediff', 'start': 'Europe/Rome'}
print('Difference between tz and server\t' + requests.post(url = url, data = json.dumps(data)).text)
data = {'type': 'datediff'}
print('Difference between same server tz\t' + requests.post(url = url, data = json.dumps(data)).text)
