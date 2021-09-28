import optparse
import requests
from bs4 import BeautifulSoup
from ..Automated.important_static_functions import *


class BruteForceManual:
    def __init__(self):
        parser = optparse.OptionParser()
        parser.add_option('-u', '--url', dest='url')
        parser.add_option('-l', '--login_name', dest='username')
        parser.add_option('-p', '--passwords', dest='passwords')
        parser.add_option('-f', '--fields', dest='import_fields')
        parser.add_option('-y', '--verification', dest='verification')
        options, arguments = parser.parse_args()
        self.url = options.url
        self.username = options.username
        self.passwords = options.passwords
        self.fields = options.import_fields
        self.verification = options.verification

    def getting_fields_from_commandline_input(self):
        input_fields = self.fields.split(':')
        username_field = input_fields[0]
        password_field = input_fields[1]
        submit_field = input_fields[2]
        return username_field, password_field, submit_field

    def fields_verification(self):
        bs4_parsed_data = request(self.url)
        forms = getting_forms(bs4_parsed_data, 'form')
        for form in forms:
            inputs_field = getting_specify_tags(form, 'input')
            tag_types, tag_names, submit = extracting_tags_attributes(inputs_field, 'type', 'name')
            if len(tag_types) < 3 and len(tag_names) < 3:
                username_field, password_field, submit_field = self.getting_fields_from_commandline_input()
                for types, names in zip(tag_types, tag_names):
                    if types == 'password':
                        if names == password_field:
                            print(colored(f"[+] Password Field Matches\nScraped: {names}, User Input: "
                                          f"{password_field}", 'green'))
                        else:
                            print(colored(f'[-] Cannot Find the give field in the form, {password_field}', 'red'))
                            sys.exit(0)
                    else:
                        if names == username_field:
                            print(colored(f"[+] Password Field Matches\nScraped: {names}, User Input: "
                                          f"{username_field}", 'green'))
                        else:
                            print(colored(f'[-] Cannot Find the give field in the form, {username_field}', 'red'))
                            sys.exit(0)
                if submit[0][1] == submit_field:
                    print(colored(f"[+] Submit Field Matches\nScraped: {submit[0][1]}, User Input: "
                                  f"{submit_field}", 'green'))
                else:
                    print(colored(f'[-] Cannot Find the give field in the form, {submit_field}', 'red'))
                    sys.exit(0)
