from Brute_Force.HTTP_POST.Automated.Brute_Force import *
from Brute_Force.HTTP_POST.Manual.main_attack import *
from pyfiglet import Figlet


def banner():  # Simple Banner Of The Program.
    fix_color_output()  # Fixing Color Output in windows and linux both.
    return colored(Figlet(font='standard').renderText('Venom Brute-Force'), 'blue')


def main():
    print(str(banner()) + "\n")
    try:
        if sys.argv[1] == 'man':
            BruteForceManual().brute_force()
        elif sys.argv[1] == 'auto':
            BruteForce().start()
    except IndexError:
        print(colored("Available Modes\n\t Automated: args => auto (Usage: ./bruteforce auto)\n\t "
                      "Manual: args => man (Usage: ./bruteforce man)", 'cyan'))


if __name__ == '__main__':
    main()
