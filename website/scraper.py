import re

from bs4 import BeautifulSoup
import requests

"""
This class scrapes relevant information from articles in researchgate.
"""

class Scraper:
    """
    initialises the class
    """
    def __init__(self, main_url):
        self.main_url = main_url


    """
    main function of scraper
    :param main_url: main url of arxiv article
    :return: dictionary object containing title, authors, submission date
    
    """
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


    """
    method to scrape title of article
    :param soup: BeautifulSoup object
    :return: title of article
    """
    def scrapeForTitle(self, soup):
        title_tag = soup.find('title')
        return title_tag.text if title_tag else None


    """
    method to scrape author names of article
    :param soup: BeautifulSoup object
    :return: list of authors of article
    """
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

    """
    method to scrape submission date of article
    :param soup: BeautifulSoup object
    :return: submission date of article
    """
    def scrapeForSubmissionDate(self, soup):
        submission_date_tag = soup.find(class_='dateline').text
        submission_date = re.search(r'\d{2} \w+ \d{4}', submission_date_tag).group()
        return submission_date