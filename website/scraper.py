import re

from bs4 import BeautifulSoup
import requests


"""
main function of scraper to return the title, authors, submission date from arxiv.org
:param main_url: main url of arxiv article
:return: dictionary object containing title, authors, submission date
"""
def scrapeMain(main_url):
    try:
        # Ensure the URL is valid
        if not main_url.startswith('http'):
            raise ValueError("Invalid URL. Please provide a valid HTTP/HTTPS URL.")

        # Fetch the web page content
        page = requests.get(main_url, timeout=10)  # Timeout for network requests
        page.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
    except requests.exceptions.RequestException as e:
        return {'error': f"Failed to fetch the webpage: {e}"}
    except ValueError as e:
        return {'error': str(e)}

    try:
        soup = BeautifulSoup(page.content, 'html.parser')

        title = scrapeForTitle(soup)
        authors = scrapeForAuthors(soup)
        submission_date = scrapeForSubmissionDate(soup)

        # Check for missing data and handle gracefully
        if not title:
            title = "Title not found"
        if not authors:
            authors = ["Authors not found"]
        if not submission_date:
            submission_date = "Submission date not found"

        return {
            'title': title,
            'authors': authors,
            'submission_date': submission_date
        }
    except Exception as e:
        return {'error': f"An error occurred while processing the webpage: {e}"}


"""
method to scrape title of article
:param soup: BeautifulSoup object
:return: title of article
"""
def scrapeForTitle(soup):
    try:
        title_tag = soup.find('title')
        return title_tag.text if title_tag else None
    except Exception as e:
        return None


"""
method to scrape author names of article
:param soup: BeautifulSoup object
:return: list of authors of article
"""
def scrapeForAuthors(soup):
    try:
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
        return authors if authors else None
    except Exception as e:
        return None

"""
method to scrape submission date of article
:param soup: BeautifulSoup object
:return: submission date of article
"""
def scrapeForSubmissionDate(soup):
    try:
        submission_date_tag = soup.find(class_='dateline').text
        if submission_date_tag:
            submission_date = re.search(r'\d{2} \w+ \d{4}', submission_date_tag).group()
            return submission_date if submission_date else None
        return None
    except Exception as e:
        return None

