import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
from multiprocessing.pool import ThreadPool

headers = {
    "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}


query=input('Введите вакансию: ')


def seach_hh(query):
    i = 0
    query=query.replace(' ','+')
    base = []
    while True:
        url = f'https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&area=1&search_field=name&enable_snippets=true&Зарплата=&st=searchVacancy&text={query}&page={i}'
        page = bs(requests.get(url, headers=headers).text, 'html.parser')
        describe_vacancy = page.find_all('div', attrs={
            'class': 'vacancy-serp-item__row_header'})
        temp = list(map(lambda x: {'Зарплата': x.contents[1].text.replace('\xa0', ''), 'Ccылка': x.a['href'],
                                   'Наименование вакансии': x.a.text,
                                   'Ресурс': 'https://hh.ru'}, describe_vacancy))
        for d in temp:
            if d['Зарплата']:
                if '-' in d['Зарплата']:
                    temp_str = d['Зарплата'].split('-')
                    temp_cur = temp_str[1].split(' ')
                    d['Зарплата'] = {'минимальная': int(temp_str[0]),
                                     'максимальная': int(temp_cur[0]),
                                     'валюта': temp_cur[1]}

                else:
                    temp_str = d['Зарплата'].split(' ')
                    d['Зарплата'] = {'минимальная': int(temp_str[1]) if temp_str[0] == 'от' else None,
                                     'максимальная': int(temp_str[1]) if temp_str[0] == 'до' else None,
                                     'валюта': temp_str[2]}
            else:
                d['Зарплата'] = None

            d['Ccылка'] = d['Ccылка'][:d['Ccылка'].find('?')]

        base.extend(temp)
        i += 1
        if not page.find('a', attrs={'data-qa': 'pager-next'}):
            break

    return {'hh_result':base}


def seach_superjob(query):
    i = 1
    base=[]
    while True:
        url = f'https://www.superjob.ru/vacancy/search/?keywords={query}&geo%5Bt%5D%5B0%5D=4&page={i}'
        page = bs(requests.get(url, headers=headers).text, 'html.parser')
        describe_vacancy = page.find_all('div', attrs={'class': 'jNMYr'})
        temp = list(map(lambda x: {'Зарплата': x.contents[1].text.replace('\xa0', ''), 'Ccылка': url[:23] + x.a['href'],
                                   'Наименование вакансии': x.a.text,
                                   'Ресурс': url[:23]}, describe_vacancy))

        for d in temp:
            if d['Зарплата']=='По договорённости':
                d['Зарплата']=None
            elif '—' in d['Зарплата']:
                temp_str = d['Зарплата'].split('—')
                temp_cur = temp_str[1].split('руб./месяц')
                if len(temp_cur)==1:
                    temp_cur = temp_str[1].split('руб./день')

                d['Зарплата'] = {'минимальная': int(temp_str[0]),
                                 'максимальная': int(temp_cur[0]),
                                 'валюта':'руб./месяц'}

            else:
                temp_cur=d['Зарплата'].split('руб./месяц')
                if len(temp_cur)==1:
                    temp_cur = d['Зарплата'].split('руб./день')
                if temp_cur[0][:2]!='от' and temp_cur[0][:2]!='до':
                    d['Зарплата'] = {'минимальная': int(temp_cur[0]),
                                     'максимальная': int(temp_cur[0]),
                                     'валюта': 'руб./месяц'}
                else:
                    d['Зарплата'] = {'минимальная': int(temp_cur[0][2:]) if temp_cur[0][:2] == 'от' else None,
                                     'максимальная': int(temp_cur[0][2:]) if temp_cur[0][:2] == 'до' else None,
                                     'валюта' : 'руб./месяц'}

        base.extend(temp)
        i += 1

        if not page.find('a', attrs={'class': 'f-test-button-dalshe'}):
            break
    return {'super_job': base}


with ThreadPool(2) as th:
    result= th.map(lambda x:x(query),[seach_hh,seach_superjob])
    pprint(result[0])
    pprint(result[1])
