import re

from bs4 import BeautifulSoup
import requests

"""
main function of scraper to return the title, authors, submission date from arxiv.org
:param main_url: main url of arxiv article
:return: dictionary object containing title, authors, submission date
"""
def scrapeMain(main_url):
    page = requests.get(main_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = scrapeForTitle(soup)
    authors = scrapeForAuthors(soup)
    submission_date = scrapeForSubmissionDate(soup)

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
def scrapeForTitle(soup):
    title_tag = soup.find('title')
    return title_tag.text if title_tag else None


"""
method to scrape author names of article
:param soup: BeautifulSoup object
:return: list of authors of article
"""
def scrapeForAuthors(soup):
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
def scrapeForSubmissionDate(soup):
    submission_date_tag = soup.find(class_='dateline').text
    submission_date = re.search(r'\d{2} \w+ \d{4}', submission_date_tag).group()
    return submission_date