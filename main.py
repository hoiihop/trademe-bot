import json
import time
import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import telepot


def send_message(result, token, users):
    bot = telepot.Bot(token)

    for user_id in users:
        for msg in result.values():
            bot.sendMessage(user_id, msg)
            time.sleep(1)
        time.sleep(1)


def get_request(url, header, session):
    response = session.get(url, headers=header)
    print(response.status_code)
    if response.ok:
        return BeautifulSoup(response.text, 'lxml')         
    else:
        return []


def get_data(soup): 
    data = {}   
    host = 'https://www.trademe.co.nz'
    cards = soup.find_all('li', class_='tmp-search-card-list-view')

    for card in cards:        
        try:
            url = host + card.find('a', class_='tmp-search-card-list-view__link').get('href')
            card_id = card.find('div', class_='tmp-search-card-list-view__card-aside').find('div', class_='tmp-search-card-list-view__media').get('data-listing-id')
            # name = card.find('div', class_='tmp-search-card-list-view__title').text
            data[card_id] = url
            print(card_id)
        except:
            continue 

    return data   


def write_json(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)  


def read_json(file_name):
    try:
        with open(file_name, 'r') as f:
            res = json.load(f).keys()
        return res
    except:
        return []


def main():
    file_name = 'test.json'
    users = [592705159, ]
    token = '560792137:AAHWiu6wW5gNnEvDCk6ve07EmmeBwvHvN4s'
    urls = [
        'https://www.trademe.co.nz/browse/categoryattributesearchresults.aspx?sort_order=expiry_desc&134=15&135=46&136=&153=&132=PROPERTY&122=0%2C0&49=100000%2C400000&29=&123=0%2C0&search=1&sidebar=1&cid=5748&rptpath=350-5748-',
        'https://www.trademe.co.nz/browse/categoryattributesearchresults.aspx?sort_order=expiry_desc&134=15&135=45&136=&153=&132=PROPERTY&122=0%2C0&49=100000%2C400000&29=&123=0%2C0&search=1&sidebar=1&cid=5748&rptpath=350-5748-'
    ]
    session = requests.Session()
    header = {
        'User-Agent': generate_user_agent()
    }
    result = {}

    for url in urls:
        soup = get_request(url, header, session)
        if soup:
            print(url)
            data = get_data(soup)
            result.update(data)           
    
    data_from_file = read_json(file_name)
    
    if data_from_file:
        write_json(result, file_name)
        for item in data_from_file:
            if result.get(item):
                result.pop(item)
    else:
        write_json(result, file_name) 

    send_message(result, token, users)    

if __name__ == '__main__':
    main()
