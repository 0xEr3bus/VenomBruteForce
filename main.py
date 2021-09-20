from Brute_Force.HTTP_POST.Automated.start import *
from pyfiglet import Figlet


def banner():  # Simple Banner Of The Program.
    fix_color_output()  # Fixing Color Output in windows and linux both.
    return colored(Figlet(font='standard').renderText('Venom Brute-Force'), 'blue')


if __name__ == '__main__':
    # python main.py -l "admin" -u "https://facebook.com/login" -p /passwords.txt -v "Login Failed"
    print("\n\n" + str(banner()) + "\n\n")
    url = 'https://facebook.com/login'
    Start().run()
