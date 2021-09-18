import sys
from .important_static_functions import *
from .scraping import main
import optparse
from tabulate import tabulate
from termcolor import colored


class Start:
    def __init__(self):
        parser = optparse.OptionParser()
        parser.add_option('-u', '--url', dest='url')
        parser.add_option('-p', '--passwords', dest='passwords')
        parser.add_option('-l', '--login_name', dest='login_name')
        parser.add_option('-v', '--verification', dest='verification')
        (options, argument) = parser.parse_args()
        self.url = options.url
        self.passwords = options.passwords
        self.login_name = options.login_name
        self.verification = options.verification
        if self.url is None or self.passwords is None or self.login_name is None or self.verification is None:
            print(error('Proper Arguments Not Given:'))
            print(self.script_usage())
            sys.exit(0)

    @staticmethod
    def script_usage():
        mydata = [[colored("Username", 'yellow'), colored("-l", 'green'), colored("A valid Username Not Given.", 'red')],
                  [colored("Passwords", 'yellow'), colored("-p", 'green'), colored("List Of Possible Passwords.", 'red')],
                  [colored("URL", 'yellow'), colored("-u", 'green'), colored("Website Want to Attack.", 'red')],
                  [colored("Verification", 'yellow'), colored("-v", 'green'), colored("To Verify if login is made", 'red')]]
        head = [colored("Name", 'blue'), colored("Arguments", 'blue'), colored("Help", 'blue')]
        return tabulate(mydata, headers=head)

    def run(self):
        main(self.url)
