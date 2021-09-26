from Brute_Force.HTTP_POST.Automated.Brute_Force import *
from pyfiglet import Figlet


def banner():  # Simple Banner Of The Program.
    fix_color_output()  # Fixing Color Output in windows and linux both.
    return colored(Figlet(font='standard').renderText('Venom Brute-Force'), 'blue')


def main():
    print("\n\n" + str(banner()) + "\n\n")
    BruteForce().run()


if __name__ == '__main__':
    main()
