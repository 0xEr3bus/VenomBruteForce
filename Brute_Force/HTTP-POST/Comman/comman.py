from bs4 import BeautifulSoup
import sys
import requests
from termcolor import colored
import colorama


class Scrapper:
    def __init__(self, url):
        """Fixing Color Output in terminal."""
        colorama.init()
        """
        [+] This method is used to get html data. Uses request and return content of webpage.
        => Example: <html>
                        ...
                    </html>
        [+] After capturing HTML data beautiful soup will parse this html data.
        """
        try:
            html_data = requests.get(url).text
            self.parser = BeautifulSoup(html_data, "html.parser")
        except requests.exceptions.ConnectionError:
            print(colored("[-] Cannot established Connection with the give url", 'red'))
            sys.exit(0)
