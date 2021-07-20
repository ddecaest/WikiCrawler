from bs4 import BeautifulSoup
import requests

def the_nicifier(unformat_str):
    # TODO
    # Makes strings legible by wikipedia search motor
    temp_var = ''
    for letter in unformat_str:
        if letter == ' ':
            temp_var += '_'
        else:
            temp_var += str.lower(letter)
    return temp_var

def wikilink_maker(entry1):
    book_title = the_nicifier(entry1)
    wiki_html = requests.get(f'https://en.wikipedia.org/wiki/{book_title}').text
    return wiki_html

usr_entry = input('tester: ')

soup = BeautifulSoup(wikilink_maker(usr_entry), 'lxml')
table = soup.find('td', class_='infobox-data').text

print(table)
