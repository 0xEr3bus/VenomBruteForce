import sys
from .important_static_functions import *
from .scraping import main
import optparse
from tabulate import tabulate
from termcolor import colored


class Start:
    def __init__(self):
        fix_color_output()
        """Fixing Color Output on Windows and Linux both."""
        parser = optparse.OptionParser()
        """Setting up command line arguments."""
        parser.add_option('-u', '--url', dest='url')
        """ Adding option of URL. The URl which has to be attacked"""
        parser.add_option('-p', '--passwords', dest='passwords')
        """Adding option of passwords list. The list of possible password to try."""
        parser.add_option('-l', '--login_name', dest='login_name')
        """Adding option of username. This username must be valid in order to gain password."""
        parser.add_option('-y', '--verification', dest='verification')
        """ Adding option of verification. 
            Verification of the password: 
                    Example:
                            "Incorrect Credentials" => response of server, means the Credentials are incorrect.
                            If  "Incorrect Credentials" not in response => Login successful"""
        parser.add_option('-v', '--verbose', dest='verbose', action="store_false")
        """Verbose Mode: Show Error and Request in real time """
        (options, argument) = parser.parse_args()
        """Parsing The Arguments"""
        """Important Fields =>"""
        self.url = options.url
        self.passwords = options.passwords
        self.login_name = options.login_name
        self.verification = options.verification
        self.verbose = options.verbose
        """Verification Of This Important Fields:"""
        if self.url is None or self.passwords is None or self.login_name is None or self.verification is None:
            print(error('Proper Arguments Not Given:'))
            print(self.script_usage())
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
            [colored("Verification", 'yellow'), colored("-v", 'green'), colored("To Verify if login is made", 'red')]]
        head = [colored("Name", 'blue'), colored("Arguments", 'blue'), colored("Help", 'blue')]
        return tabulate(my_data, headers=head)

    def run(self):
        if self.verbose is None:
            main(self.url, self.login_name, self.verification, self.passwords)
        else:
            main(self.url, self.login_name, self.verification, self.passwords, self.verbose)


if __name__ == '__main__':
    Start().run()
