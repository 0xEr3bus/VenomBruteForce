import sys
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


def getting_forms(html_data, to_find):
    """
    [+] This Function is used to extract specific HTML tag from a given HTML data.
        => Example: <html>
                        <form>   =>   [+] Extracts specific tag in this case its 'form'. Format: list
                            <input>...</input>
                        </form>
                    </html>
    """
    tags = parsing(html_data).find_all(to_find)
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


def extracting_tags_attributes(list_of_tags, tag_types, tag_names, ignore=None):
    """
    [+] This function is used to extract attributes of give list.
        => Example:
            <input name='pass' type='password'>...</input>      => The attribute of given list, in this case its 'input'
            <input name='email' type='text'>...</input>             This function will extracts two given attributes.
            <input name='submit_form' type='submit'>...</input>     I.E: type, name, Here Ignore means to ignore any
    """
    if ignore is None:
        tag_type = []
        tag_name = []
        submit_button = []
        for list_tag in list_of_tags:
            temp_tag_type, temp_tag_name = list_tag.get(tag_types), list_tag.get(tag_names)
            if temp_tag_type != 'hidden':
                if temp_tag_type == 'submit':
                    submit_button.append((temp_tag_type, temp_tag_name))
                else:
                    tag_type.append(temp_tag_type), tag_name.append(temp_tag_name)
        return tag_type, tag_name, submit_button


def get_form_action_and_method(form):
    """
    This method is used specially, its meant to extract form action and the method form uses.
    """
    action, method = form.get('action'), form.get('method')
    return action, method


def error(data: str):
    """Returns A Red Error Message!"""
    return colored('[-] ' + str(data), 'red')


def success(data: str, color: str = None):
    if color is None:
        """Returns A green Success Message!"""
        return colored('[+] ' + str(data), 'green')
    else:
        return colored("[+] " + str(data), color)


def brute_force_request(url: str, data: dict, timeout: int = None):
    try:
        if timeout is None:
            response = requests.post(url, data=data, timeout=10)
            return response
        else:
            response = requests.post(url, data=data, timeout=timeout)
            return response
    except requests.exceptions.ConnectionError:
        print(colored('[-] Hosts seems to be down. Please Verify connection with the host.', 'red'))
        sys.exit(0)


def read(path):
    """
    This Function takes parameter path; this path parameter is path to the wordlist of password.
    this will strip and make a list of passwords and return the list.
    """
    words = []
    try:
        with open(path, 'rb') as words_file:
            words += words_file.readlines()

        print(colored(f"Read in {len(words)} words from {path}", 'yellow'))
    except IsADirectoryError:
        print(error('The Given Wordlist is Not A File. Its a directory.'))
        sys.exit(0)
    except PermissionError:
        print(error('The Given File Cannot Be accessed, Permission Error.'))
        sys.exit(0)
    except FileNotFoundError:
        print(error('The Given Wordlist Not Found. Check The File Location.'))
        sys.exit(0)
    return words


def clean_word(word):
    """
    This Function Is Used to clean a word. and decodes to UTF-8 or Latin-1
    """
    if not word:
        return
    try:
        word = word.strip().decode('utf-8')
    except UnicodeDecodeError:
        try:
            word = word.strip().decode('Latin-1')
        except UnicodeError:
            print(error(f'Error In Decoding This Word {word}'))
            return
    return word


def connection_check(url):
    try:
        requests.get(url)
    except requests.exceptions.ConnectionError:
        print(colored('[-] Hosts seems to be down. Please Verify connection with the host.', 'red'))
        sys.exit(0)
    except requests.exceptions.ReadTimeout:
        print(error('Time Out Error'))
        sys.exit(0)
