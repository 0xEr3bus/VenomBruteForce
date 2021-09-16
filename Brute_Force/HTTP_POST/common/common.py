from bs4 import BeautifulSoup
import requests
from termcolor import colored
import colorama


def fix_color_output():
    """
    Fixing Color Output in terminal. Generally Fixes The problem of color in Windows CMD.
    """
    colorama.init()


def parsing(html_data):
    """
    [+] After capturing HTML data beautiful soup will parse this html data.
    Parsing Simple means the data will be readable by BS4's methods
    """
    parser = BeautifulSoup(html_data, "html.parser")
    return parser


def request(url):
    """
    [+] This method is used to get html data. Uses request and return content of webpage.
    => Example: <html>
                    ...
                </html>
    """
    try:
        html_data = requests.get(url).text
        return html_data
    except requests.exceptions.ConnectionError:
        return colored("[-] Cannot established Connection with the give url", 'red')


def getting_forms(html_data, tag):
    """
    [+] This Function is used to extract specific HTML tag from a given HTML data.
        => Example: <html>
                        <form>   =>   [+] Extracts specific tag in this case its 'form'. Format: list
                            <input>...</input>
                        </form>
                    </html>
    """
    tags = parsing(html_data).find_all(tag)
    return tags


def getting_specify_tags(html_data, tag):
    """
    [+] This Function is used to extract specific HTML tag from a given HTML data.
        => Example: <html>
                        <form>
                            <input>...</input>
                            <input>...</input>   =>   [+] Extracts Specify tags in this case its 'input'. Format: list
                            <input>...</input>
                        </form>
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


def get_form_action_and_method(form):
    """
    This method is used specially, its meant to extract form action and the method form uses.
    """
    action = form.get('action')
    method = form.get('method')
    return method, action


if __name__ == '__main__':
    print(extracting_tags_attributes(getting_specify_tags(request('https://facebook.com'), 'input'), 'type', 'name'))
