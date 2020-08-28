import requests


user='Valvea'

token='my_or_you_token'

url='https://api.github.com/user'

headers={'Authorization':f'token {token}'}

with open('response_github.txt','w+') as w:
    w.write('without token:\n'+requests.get(url).text+'\n')
    w.write('with token:\n'+ requests.get(url,headers=headers).text+'\n')
