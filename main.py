import requests
from bs4 import BeautifulSoup
import sqlite3

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


def look_up(usr_entry, cur, conn):
    book_name = the_nicifier(usr_entry)
    cur.execute("select * from books where Book_Name = :bookName", {"bookName": book_name})
    query_result = cur.fetchall()
    if len(query_result) == 0:
        soup = BeautifulSoup(wikilink_maker(usr_entry), 'lxml')
        author_name = soup.find('td', class_='infobox-data').text
        cur.execute(f"INSERT INTO books VALUES ('{author_name}', '{book_name}')")
        conn.commit()
        print('Fetching from wikipedia and inserting author to database!')
        return author_name
    else:
        author_name, book_name = query_result[0]
        print('Fetching from database!')
        return author_name


if __name__ == "__main__":
    conn = sqlite3.connect(':memory:')
    cur = conn.cursor()
    cur.execute("CREATE TABLE books (Author text, Book_Name text)")
    while True:
        usr_entry = input('tester: ')
        if usr_entry == 'print':
            for row in cur.execute('SELECT * FROM books ORDER BY book_name'):
                print(row)
        else:
            print(look_up(usr_entry, cur, conn))