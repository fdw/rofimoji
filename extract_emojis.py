import requests
from bs4 import BeautifulSoup

max_tries = 5
for i in range(max_tries):    
    data = requests.get('https://emojipedia.org/emoji/')  # type: requests.Response
    if data:
        break

if not data:
    print("Could not fetch emoji data. Try again later or use another URL.")
    exit(10)

soup = BeautifulSoup(data.content, 'lxml')  # type: BeautifulSoup

python_file = open('emojis.py', 'w')
python_file.write('emojis="""')

for table_row in soup.find_all('tr'):
    emoji_row = table_row.find('td')
    text = emoji_row.get_text()

    python_file.write(text + '\n')
python_file.write('"""')

python_file.close()
