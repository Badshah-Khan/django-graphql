import re

def camel_to_kebab(camel_case):
    pattern = re.compile(r'(?<!^)(?=[A-Z])(?!$)')
    kebab_case = pattern.sub('_', camel_case).lower()
    return kebab_case