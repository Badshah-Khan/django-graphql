import re

def camel_to_kebab(camel_case):
    pattern = re.compile(r'(?<!^)(?=[A-Z])(?!$)')
    kebab_case = pattern.sub('_', camel_case).lower()
    return kebab_case

def user_authentication(info):
    is_auth = info.context.is_auth
    if not is_auth:
        raise Exception("Unauthorized")
    else:
        pass
    return info.context.user[0]

def super_authorization(info):
    user_authentication(info)
    user_obj = info.context.user[0]
    if user_obj.is_superuser != True:
        raise Exception("Not Allowed!")
    else:
        pass
    return user_obj

def super_staff_authorization(info):
    user_authentication(info)
    user_obj = info.context.user[0]
    if user_obj.is_superuser != True and user_obj.is_staff != True:
        raise Exception('Not Allowed!')
    else:
        pass
    return user_obj

def organization_validation(info, org = None):
    token_obj = info.context.user[1]
    user_org = token_obj['data']['organization']
    if org is not None and user_org != org:
        raise Exception("Invalid Organization")
    return user_org