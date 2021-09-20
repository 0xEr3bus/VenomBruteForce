import sys
from .important_static_functions import *


def main(url):
    """
    Extracting Forms and storing in a list, called 'forms'
    """
    forms = getting_forms(request(url), 'form')
    """
    Iterating over each form.
    """
    for form in forms:
        """
        Extracting Form Action and Method, storing in variable, 'action' and 'method'.
        """
        action, method = (get_form_action_and_method(form))
        print(success(f'Action: {action}, Method: {method}', 'yellow'))
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
                print(success(f'Input Type: "{types}", Input Name: "{names}"'))
            """
            try/except :
                Printing Button Name:
            """
            try:
                print(success(f'Submit Button Name: {submit[0][1]}'))
            except IndexError:
                print(error(f'Cannot Find The Submit Input Field Name'))
        else:
            """
            Exiting due to more than two inputs fields.
            """
            print(error(f'More Than 2 inputs Field Found, Please use Manual mode.'))
            field = 1
            """
            For more information, printing the inputs in a better format.
            """
            for types, names in zip(tag_types, tag_names):
                print(error(f'Input Name: "{names}"' + colored(f" <= Field number {field}", 'blue')))
                field += 1
            sys.exit(0)
