from bs4 import BeautifulSoup
import requests
from termcolor import colored
import colorama


def fix_color_output():
    """
    Fixing Color Output in terminal. Generally Fixes The problem of color in Windows CMD.
    """
    colorama.init()


def parsing(url):
    """
    [+] This method is used to get html data. Uses request and return content of webpage.
    => Example: <html>
                    ...
                </html>
    [+] After capturing HTML data beautiful soup will parse this html data.
        Parsing Simple means the data will be readable by BS4's methods
    """
    try:
        html_data = requests.get(url).text
        parser = BeautifulSoup(html_data, "html.parser")
        return parser
    except requests.exceptions.ConnectionError:
        return colored("[-] Cannot established Connection with the give url", 'red')


def getting_specify_tags(html_data, tag):
    """
    [+] This Function is used to extract specific HTML tag from a given HTML data.
        => Example: <html>
                        <input>...</input>
                        <input>...</input>   =>   [+] Extracts Specify tags in this case its 'input'. Format: list
                        <input>...</input>
                    </html>
    """
    tags = html_data.find_all(tag)
    return tags


def extracting_tags_attributes(list_of_tags, tag_types, tag_names):
    """
    [+] This function is used to extract attributes of give list.
        => Example:
            <input name='pass' type='password'>...</input>      => The attribute of given list, in this case its 'input'
            <input name='email' type='text'>...</input>             This function will extracts two given attributes.
            <input name='submit_form' type='submit'>...</input>     I.E: type, name
    """
    tag_type = []
    tag_name = []
    for list_tag in list_of_tags:
        tag_type.append(list_tag.get(tag_types)), tag_name.append(list_tag.get(tag_names))
    return tag_type, tag_name


print(extracting_tags_attributes(getting_specify_tags(parsing('https://facebook.com'), 'input'), 'type', 'name'))
