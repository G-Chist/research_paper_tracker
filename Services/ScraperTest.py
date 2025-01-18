'''
Ignore this class for now
'''
import requests
from bs4 import BeautifulSoup
# import selenium


main_url='https://arxiv.org/abs/2307.11013'

page = requests.get(main_url)
soup = BeautifulSoup(page.content, 'html.parser')

# print(soup.prettify())

# title = soup.find('title')
# print(title.text)

submission_date_tag = soup.find(class_ = 'dateline').text
import re
submission_date = re.search(r'\d{2} \w+ \d{4}', submission_date_tag).group()

print(submission_date)
print(type(submission_date))