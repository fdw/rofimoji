from typing import Union
import html
import requests
from bs4 import BeautifulSoup

from extractors.CharacterFactory import Character


class NerdExtractor(object):
	def __init__(self: 'NerdExtractor'):
		self.__glyphs = {}

	def fetch_glyphs(self: 'NerdExtractor'):
		print('Downloading the glyph list')

		response = requests.get(
			'https://raw.githubusercontent.com/ryanoasis/nerd-fonts/gh-pages/_posts/2017-01-04-icon-cheat-sheet.md',
			timeout=60
		)  # type: requests.Response

		soup = BeautifulSoup(response.content.decode(response.encoding), 'html.parser')
		
		codes = soup.find_all(class_='codepoint')
		names = soup.find_all(class_='class-name')
		self.__glyphs = [Character(int(codes[i].string, 16), names[i].string) for i in range(len(codes))]

	
	def write_to_file(self: 'NerdExtractor'):
		if len(self.__glyphs) == 0:
			return

		symbol_file = open(f"../picker/data/nerd_font.csv", 'w')

		for character in self.__glyphs:
			symbol_file.write(f"{character.char} {html.escape(character.name)}\n")

		symbol_file.close()
		
	def extract(self: 'NerdExtractor'):
		self.fetch_glyphs()
		self.write_to_file()
		

if __name__ == '__main__':
	NerdExtractor().extract()
