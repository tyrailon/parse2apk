import requests

from datetime import date, timedelta
#from telebot import TeleBot


today = date.today()
yesterday = today - timedelta(days=1)
tomorrow  = today + timedelta(days=1)

dtd = yesterday.strftime('%Y-%m-%d')
dtn = today.strftime('%Y-%m-%d')
dti = tomorrow.strftime('%Y-%m-%d')

user_id = 12345
headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0' }
#codepage = "cp1251"
codepage = 'utf-8'

# yesterday
url = 'https://old.24score.pro/?date=' + dtd
r = requests.get(url, headers = headers)
fname = 'score_' + dtd + '.html'
print(fname,url)
with open(fname, 'w', encoding=codepage) as output_file:
  output_file.write(r.text)

url = 'http://m.flashscorekz.com/?d=-1&s=5'
r = requests.get(url, headers = headers)
fname='mobik_' + dtd + '.html'
print(fname,url)
with open(fname, 'w', encoding=codepage) as output_file:
  output_file.write(r.text)

# today
url = 'https://arbworld.net/en/moneyway/football-1-x-2'
r = requests.get(url, headers = headers)
fname='money_' + dtn + '.html'
print(fname,url)
with open(fname, 'w', encoding=codepage) as output_file:
  output_file.write(r.text)

url = 'https://arbworld.net/en/dropping-odds/football-over-under-2-5'
r = requests.get(url, headers = headers)
fname='moneytotal_' + dtn + '.html'
print(fname,url)
with open(fname, 'w', encoding=codepage) as output_file:
  output_file.write(r.text)

# tomorrow
url = 'https://www.soccervital.com/soccer-games/?date=' + tomorrow.strftime('%d-%m-%Y')
r = requests.get(url, headers = headers)
fname='vista_' + dti + '.html'
print(fname,url)
with open(fname, 'w', encoding=codepage) as output_file:
  output_file.write(r.text)


 #with open(f"1xstavka_{create_time}.csv", 'w') as file:
 #                   file_writer = csv.DictWriter(file, fieldnames=keys)
 #                   file_writer.writeheader()
 #                   file_writer.writerows(data)
 #               with open(f"1xstavka_{create_time}.csv", 'rb') as file:
 #                   bot.send_document(config['telegram_id_for_send_data'], document=file)

#with open(fname, 'w', encoding=codepage) as output_file:
#  bot.send_document(config['telegram_id_for_send_data'], document=file)
