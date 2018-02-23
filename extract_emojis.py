import requests
from bs4 import BeautifulSoup

datas = [
    'https://emojipedia.org/people/',
    'https://emojipedia.org/nature/',
    'https://emojipedia.org/food-drink/',
    'https://emojipedia.org/activity/',
    'https://emojipedia.org/travel-places/',
    'https://emojipedia.org/objects/',
    'https://emojipedia.org/symbols/',
    'https://emojipedia.org/flags/']

python_file = open('emojis.py', 'w')
python_file.write('emojis="""\n')

for url in datas:
    data = requests.get(url)  # type: requests.Response
    soup = BeautifulSoup(data.content, 'lxml')  # type: BeautifulSoup

    soup = soup.find("div", attrs={"class": "content"})
    for table_row in soup.find_all('li'):
        emoji_row = table_row.find('a')
        text = emoji_row.get_text()

        python_file.write(text + '\n')

python_file.write('"""')

python_file.close()
