import requests
from bs4 import BeautifulSoup
import pandas as pd
import threading

lock = threading.Lock()

def webscrape_directory_page(url, data):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    for member in soup.select('.listerItem'):
        member_url_selector = member.select('h2 a')
        member_url = f'https://www.ftlchamber.com/{member_url_selector[0]["href"]}'
        try:
            website = member.select('.website a')[0].text
            print('yippy!')
        except:
            website = ''
        try:
            email = member.select('.email a')[0].text
            print('you got it baws')
        except:
            email = ''

        print(member_url)
        res = requests.get(member_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        try:
            business_name = soup.select('#interior_content h1')[0].text
        except:
            business_name = ''

        try:
            contact = soup.select('.member_contact_info .member_name h3')[0].text
            contact_name_parts = contact.split(':')[1].strip().split(' ')
            contact_first_name = contact_name_parts[0]
            contact_last_name = contact_name_parts[1]
            print('got it!')
        except:
            contact_first_name = ''
            contact_last_name = ''

        try:
            phone_number = soup.select('.phoneformat')[0].text.split(':')[1].strip()
            print('you betcha!')
        except:
            phone_number = ''

        with lock:
            data.append({'Business Name': business_name,
                   'Contact First Name': contact_first_name,
                   'Contact Last Name': contact_last_name,
                   'Phone Number': phone_number,
                   'Email': email,
                   'Website': website})

start_urls = [f'https://www.ftlchamber.com/membership/{i}/' for i in range(1, 47)]
data = []

for url in start_urls:
    print(url)
    thread = threading.Thread(target=webscrape_directory_page, args=(url, data))
    thread.start()

while threading.active_count() > 1:
    pass

columns = ['Business Name', 'Website', 'Contact First Name', 'Contact Last Name', 'Phone Number', 'Email']
df = pd.DataFrame(data=data, columns=columns)
df.sort_values(by='Business Name', inplace=True)
df.to_excel('Business_Info_FTL.xlsx', index=False)