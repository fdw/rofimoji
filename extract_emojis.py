import requests
from bs4 import BeautifulSoup, NavigableString

max_tries = 5
for i in range(max_tries):
    print("Downloading emojis... try %s" % (i + 1))
    data = requests.get('https://www.unicode.org/emoji/charts-11.0/full-emoji-list.html', timeout=60)  # type: requests.Response
    if data:
        break

if not data:
    print("Could not fetch emoji data. Try again later or use another URL.")
    exit(10)

soup = BeautifulSoup(data.content, 'lxml')  # type: BeautifulSoup
table = soup.find('table')

python_file = open('emojis.py', 'w')
python_file.write('emojis="""')

for row in table.find_all('tr'):
    if row.th:
        continue
    emoji = row.find('td', {'class': 'chars'}).string
    description = row.find('td', {'class': 'name'}).string.replace('⊛ ', '')

    python_file.write(emoji + " " + description + '\n')
python_file.write('"""')

python_file.close()
