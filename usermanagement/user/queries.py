from graphene import ObjectType, List, JSONString, Int, String
from django.contrib.auth.models import User
from .types import UserType
import re


class UserQuery(ObjectType):
    users = List(UserType, where = JSONString(), limit = Int(), offset = Int(), order = String())

    def resolve_users(self, info, where = None, limit = 100, offset = 0, order = None, **kwargs):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        if user_obj.is_superuser != True and user_obj.is_staff != True:
            raise Exception("Not Allowed")
        if user_obj.is_active is not True:
            raise Exception("You can't perform this action!")
        query = """select u.*, uo.user_id as user_id, o.name as organization_name, o.id as organization, ee.dob, ee.joining_date, ee.mobile from auth_user u 
                    left join userorganization_userorganization uo on uo.user_id = u.id 
                    left join organization_organization o on uo.organization_id = o.id
                    left join employeedetails_employee ee on ee.user_id = u.id"""
        parameters = []
        if where is not None:
            search = where.get('search', None)
            organization = where.get('organization', None)
            isActive = where.get('isActive', None)
            isStaff = where.get('isStaff', None)
            userId = where.get('userId', None)
            whereQuery = ""
            if search is not None and search != "":
                whereQuery = """where (u.username ilike %s or u.first_name ilike %s or u.last_name ilike %s
                or o.name ilike %s) """
                parameters.extend([f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"])
            if organization is not None:
                if whereQuery != "":
                    whereQuery = whereQuery + "and" + " o.id = %s"
                else:
                    whereQuery = "where o.id = %s"
                parameters.extend([f"{organization}"])
            if isActive is not None:
                if whereQuery != "":
                    whereQuery = whereQuery + "and" + " u.is_active = %s"
                else:
                    whereQuery = "where u.is_active = %s"
                parameters.extend([f"{isActive}"])
            if isStaff is not None:
                if whereQuery != "":
                    whereQuery = whereQuery + "and" + " u.is_staff = %s"
                else:
                    whereQuery = "where u.is_staff = %s"
                parameters.extend([f"{isStaff}"])
            if userId is not None:
                if whereQuery != "":
                    whereQuery = whereQuery + "and" + " u.id = %s"
                else:
                    whereQuery = "where u.id = %s"
                parameters.extend([f"{userId}"])

            query = f"{query} {whereQuery}"
                

        if order is not None:
            order = order.split(" ")
            orderBy = order[0]
            dir = order[1]
            orderByQuery = f'order by "{camel_to_kebab(orderBy)}" {dir}'
            query = f"{query} {orderByQuery}"
        
        limitQuery = "limit %s offset %s"
        query = f"{query} {limitQuery}"
        parameters.extend([f"{limit}", f"{offset}"])
        user_organizations = User.objects.raw(query, parameters)
        return user_organizations

def camel_to_kebab(camel_case):
    pattern = re.compile(r'(?<!^)(?=[A-Z])(?!$)')
    kebab_case = pattern.sub('_', camel_case).lower()
    return kebab_case