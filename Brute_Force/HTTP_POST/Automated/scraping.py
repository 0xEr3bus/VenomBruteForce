from .important_static_functions import *
from .Brute_Force import BruteForce


def extraction(form, passwords_list, threads=None, verbose=None):
    """
    Declaring Password Field and Username Field as Empty.
    """
    password_field_name = ''
    username_field_name = ''
    """
    Extracting Form Action and Method, storing in variable, 'action' and 'method'.
    """
    action, method = (get_form_action_and_method(form))
    print(success(f'Action: {action}, Method: {method}'))
    """
    Extracting all inputs tag, from form.
    """
    inputs = getting_specify_tags(form, 'input')
    """
    Extracting Tag Type and Name, storing  in variable, 'tag_type', and 'tag_name'
    """
    tag_types, tag_names, submit = extracting_tags_attributes(inputs, 'type', 'name')
    """
    Condition ->
        Checking length of tag_type and tag_name.
    """
    if len(tag_types) < 3 and len(tag_names) < 3:
        """
        Printing types and names in a better format. 
        """
        for types, names in zip(tag_types, tag_names):
            if types == 'password':
                password_field_name = names
            else:
                username_field_name = names
        print(success(f'Password Field: "{password_field_name}"'))
        print(success(f'Username Field: "{username_field_name}"'))
        """
        try/except :
            Printing Submit Input/Button Name:
            If/Else For Verbose Mode.
        """
        try:
            submit = submit[0][1]
            if submit is None:
                submit = ''
                print(success(f'Submit Button Name: {submit}\n\n', 'blue'))
                if verbose is None:
                    BruteForce(passwords_list, username_field_name, password_field_name, submit, threads).brute_force()
                else:
                    BruteForce(username_field_name, password_field_name, submit, passwords_list, verbose)
        except IndexError:
            print(error(f'Cannot Find The Submit Input Field Name'))
    else:
        """
        Exiting due to more than two inputs fields.
        """
        print(error(f'More Than two inputs Field Found, Please use Manual mode.'))
        field = 1
        """
        For more information, printing the inputs in a better format.
        """
        for types, names in zip(tag_types, tag_names):
            print(error(f'Input Name: "{names}"' + colored(f" <= Field number {field}", 'blue')))
            field += 1
        sys.exit(0)


def main(url, username, verification):
    """
    Extracting Forms and storing in a list, called 'forms'
    """
    forms = getting_forms(request(url), 'form')
    """
    Iterating over each form.
    """
    if len(forms) == 1:
        for form in forms:
            extraction(form, url, username, verification)
    elif len(forms) > 1:
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
            extraction(form, url, username, verification)
        except IndexError:
            print(colored(f'[-] Form With Index {form_to_search} Not Found.', 'red'))
            sys.exit(0)
        except ValueError:
            print(colored('[-] Integer Required.', 'red'))
            sys.exit(0)
    else:
        print(error(f'More Than One Form Found: {len(forms)}'))
