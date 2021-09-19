import sys
from .important_static_functions import *


def main(url):
    forms = getting_forms(request(url), 'form')
    for form in forms:
        action, method = (get_form_action_and_method(form))
        print(success(f'Action: {action}, Method: {method}', 'yellow'))
        inputs = getting_specify_tags(form, 'input')
        tag_types, tag_names, submit = extracting_tags_attributes(inputs, 'type', 'name')
        if len(tag_types) < 3 and len(tag_names) < 3:
            for types, names in zip(tag_types, tag_names):
                print(success(f'Input Type: "{types}", Input Name: "{names}"'))
            try:
                print(success(f'Submit Button Name: {submit[0][1]}'))
            except IndexError:
                print(error(f'Cannot Find The Submit Input Field Name'))
        else:
            field = 1
            print(error(f'More Than 2 inputs Field Found, Please use Manual mode.'))
            for types, names in zip(tag_types, tag_names):
                print(error(f'Input Type: "{types}", Input Name: "{names}"' + colored(f"<= {field} Field", 'blue')))
                field += 1
            sys.exit(0)
