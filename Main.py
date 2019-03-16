from bs4 import BeautifulSoup
from requests import get


def title_maker(name):
    """

    :param name: the title of the page to standardize
    :return: replace all ' ' with '_' and make the first letter uppercase and others lower case

    """

    return name[0].upper() + name.replace(' ', '_')[1::].lower()


def standardize_keyword_0(keyword):
    """

    :param keyword: the keyword to standardize
    :return: standardized keyword (first letter upper and others lower case + replace '_' with ' ')
    """

    return keyword[0].upper() + keyword[1::].lower().replace('_', ' ')


def standardize_keyword_1(keyword):
    """

    :param keyword: the keyword to standardize
    :return: standardized keyword (make all letters lower case + replace '_' with ' ')
    """

    return keyword.lower().replace('_', ' ')


def standardize_text(text):
    """

    :param text: the text of first sentence of article
    :return: standardized format of the text by replacing ('.' and ';') with ('\n\t') and deleting refrences
    """

    text = text.replace('.', '.\n\t')
    text = text.replace(';', '.\n\t')

    for i in range(len(text)):
        try:
            if text[i] == '[':
                for j in range(i, len(text)):
                    if text[j] == ']':
                        try:
                            betw = int(text[i + 1:j:])
                            text = text[:i:] + text[j + 1::]
                            break

                        except ValueError:
                            print('hey')
                            break
        except IndexError:
            break

    if text[len(text) - 2] == ']':
        for i in range(len(text) - 2, -1, -1):
            if text[i] == '[':
                try:
                    betw = int(text[i + 1:len(text) - 2:])
                    text = text[:i:]
                    break

                except ValueError:
                    break

    return text


def find_first_prag(prags, keyword):
    """

    :param prags: a list of some of the p tags in html
    :param keyword: the keyword that with it we found the special pragrapgh
    :return: the text of the first pragraph of the article if exist else the text of first pragraph in the page
    """

    keyword0 = standardize_keyword_0(keyword)
    keyword1 = standardize_keyword_1(keyword)

    for prag in prags:
        sentence = prag.get_text()
        if keyword0 in sentence or keyword1 in sentence:
            return standardize_text(sentence)

    return standardize_keyword_1(prags[0].get_text())


input_request = "please input the title of topic that you are looking for."
print(input_request + '..')

soup = ''
title = ''

flag = True
while flag:
    title = input()
    title = title_maker(title)

    page = get('https://en.wikipedia.org/wiki/' + title)

    soup = BeautifulSoup(page.content, 'html.parser')

    b_tags = soup.find_all('b', limit=2)

    if b_tags[1].string == 'Wikipedia does not have an article with this exact name.':
        print('wikipedia dose not have an article with this exact name')
        print('please input something else')
    else:
        flag = False

main_div = soup.find('div', class_='mw-parser-output')
first_image = main_div.find('img')

p_tags = soup.find_all('p', limit=5)

text = find_first_prag(p_tags, title)

print()  # go to new line
print('#' * 50)
print()
print('title :', standardize_keyword_0(title))
print('descreption :', text)
print('link of first image :', first_image['src'][2::])
print()
print('#' * 50)
