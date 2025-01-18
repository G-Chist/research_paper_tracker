import os
import re

from bs4 import BeautifulSoup
import requests

from Services.ScraperTest import submission_date

"""
This class scrapes relevant information from articles in researchgate.
"""

class Scraper:
    """
    initialises the class
    """

    def __init__(self, main_url='https://www.researchgate.net/publication/360260855_Vulnerability_in_practice_Peeling_back_the_layers_avoiding_triggers_and_preventing_cascading_effects'):
        self.main_url = main_url

    def scrapeMain(self, main_url):
        page = requests.get(main_url)
        soup = BeautifulSoup(page.content, 'html.parser')

        title = self.scrapeForTitle(soup)
        authors = self.scrapeForAuthors(soup)
        submission_date = self.scrapeForSubmissionDate(soup)

        # I need to return title and authors
        return {
            'title': title,
            'authors': authors,
            'submission_date': submission_date
        }

    def scrapeForTitle(self, soup):
        title_tag = soup.find('title')
        return title_tag.text if title_tag else None

    def scrapeForAuthors(self, soup):
        # Find all <div> elements with the class 'authors'
        authors_divs = soup.find_all('div', class_='authors')

        # Initialize an empty list to store authors
        authors = []

        # Loop through each <div> with class 'authors' and extract author names
        for authors_div in authors_divs:
            # Find all <a> tags within the <div>
            author_links = authors_div.find_all('a')

            # Extract the text (author names) from each <a> tag and add to the authors list
            for author in author_links:
                authors.append(author.text)

        # returns the authors
        return authors

    def scrapeForSubmissionDate(self, soup):
        submission_date_tag = soup.find(class_='dateline').text
        submission_date = re.search(r'\d{2} \w+ \d{4}', submission_date_tag).group()
        return submission_date