import Brute_Force.HTTP_POST.common.common as AS
from bs4 import BeautifulSoup


def getting_tags_attributes(html_data, find_type, find_name):
    tag_type, tag_name = html_data.get(find_type), html_data.get(find_name)
    if tag_type != 'hidden':
        return tag_type, tag_name
    else:
        input_type, tag_name = None, None
        return input_type, tag_name


url = 'https://www.github.com/login'
response = AS.request(url)
forms = AS.getting_forms(response, 'form')
# print(forms)
for form in forms:
    inputs = AS.getting_specify_tags(form, 'input')
    for input_field in inputs:
        print(input_field)
# print(getting_tags_attributes(data, 'type', 'name'))
