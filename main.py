from Brute_Force.HTTP_POST.Automated.start import *
from pyfiglet import Figlet


def banner():  # Simple Banner Of The Program.
    fix_color_output()  # Fixing Color Output in windows and linux both.
    return colored(Figlet(font='standard').renderText('Venom Brute-Force'), 'blue')


def main():
    # python main.py -l admin -p wordlist/passwords.txt -u http://192.168.56.101/dvwa/login.php -v "Login failed"
    try:
        print("\n\n" + str(banner()) + "\n\n")
        Start().run()
    except KeyboardInterrupt:
        print(error('Ctrl + C Detected, Quiting...'))
        sys.exit(0)


if __name__ == '__main__':
    main()
