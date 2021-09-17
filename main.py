import Brute_Force.HTTP_POST.common.common as AS

# url = 'https://facebook.com/login'
url = 'http://testhtml5.vulnweb.com/#/popular'
forms = AS.getting_forms(AS.request(url), 'form')
for form in forms:
    action, method = (AS.get_form_action_and_method(form))
    print(AS.success(f'Action: {action}, Method: {method}', 'yellow'))
    inputs = AS.getting_specify_tags(form, 'input')
    tag_types, tag_names, submit = AS.extracting_tags_attributes(inputs, 'type', 'name')
    for types, names in zip(tag_types, tag_names):
        print(AS.success(f'Input Type: {types}, Input Name: {names}'))
    try:
        print(AS.success(f'Submit Button Name: {submit[0][1]}'))
    except IndexError:
        print(AS.error(f'Cannot Find The Submit Input Field Name'))
