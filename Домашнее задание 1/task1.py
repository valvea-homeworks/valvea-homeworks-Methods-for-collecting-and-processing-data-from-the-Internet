import requests
import json

user='Valvea'

url=f'https://api.github.com/users/{user}/repos'

to_write={'Пользователь':user}

response=requests.get(url)
if response.ok:
    temp_info=json.loads(response.content)
    to_write["Репозиторий"]=list(map(lambda x:{'Название':x['name'],
                         'Cсылка':x['html_url']},temp_info))

    with open(f'{user}_repos.json','wb') as w_json:
        w_json.write(json.dumps(to_write,ensure_ascii=False).encode('utf-8'))
