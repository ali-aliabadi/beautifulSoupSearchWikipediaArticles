from bs4 import BeautifulSoup
from requests import get


def title_maker(name):
    return name[0].upper() + name.replace(' ', '_')[1::].lower()


input_request = "please input the title of topic that you are looking for."
print(input_request + '..')

title = input()
title = title_maker(title)

page = get('https://en.wikipedia.org/wiki/' + title)


soup = BeautifulSoup(page.content, 'html.parser')
ta = soup.find('table')

