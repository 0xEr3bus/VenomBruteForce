from .important_static_functions import *


def main(url):
    forms = getting_forms(request(url), 'form')
    for form in forms:
        action, method = (get_form_action_and_method(form))
        print(success(f'Action: {action}, Method: {method}', 'yellow'))
        inputs = getting_specify_tags(form, 'input')
        tag_types, tag_names, submit = extracting_tags_attributes(inputs, 'type', 'name')
        for types, names in zip(tag_types, tag_names):
            print(success(f'Input Type: {types}, Input Name: {names}'))
        try:
            print(success(f'Submit Button Name: {submit[0][1]}'))
        except IndexError:
            print(error(f'Cannot Find The Submit Input Field Name'))
