import requests
from bs4 import BeautifulSoup

data = requests.get('https://emojipedia.org/emoji/')  # type: requests.Response
soup = BeautifulSoup(data.content, 'lxml')  # type: BeautifulSoup

python_file = open('emojis.py', 'w')
python_file.write('emojis="""\n')

for table_row in soup.find_all('tr'):
    emoji_row = table_row.find('td')
    text = emoji_row.get_text()

    python_file.write(text + '\n')
python_file.write('"""')

python_file.close()
