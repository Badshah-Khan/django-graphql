from graphene import ObjectType, List, JSONString, Int, String, Field
from django.contrib.auth.models import User
from .types import UserType, UserDetailsType
from userorganization.models import UserOrganization
from address.models import Address
from usermanagement.utils import camel_to_kebab, super_staff_authorization, organization_validation, user_authentication

class UserQuery(ObjectType):
    users = List(UserType, where = JSONString(), limit = Int(), offset = Int(), order = String())
    user_details = Field(UserDetailsType, id = Int(required = True))
    user_search = List(UserType, where = JSONString())

    def resolve_users(self, info, where = None, limit = 100, offset = 0, order = None, **kwargs):
        user_obj = super_staff_authorization(info)
        user_org = organization_validation(info)
        if user_org is None:
            return []
        query = """select u.*, uo.user_id as user_id, o.name as organization_name, o.id as organization, ee.dob, ee.joining_date, ee.profile, ee.mobile from auth_user u 
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
            not_user_id = None
            if user_obj.is_superuser:
                not_user_id = user_obj.id
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
            if not_user_id is not None:
                if whereQuery != "":
                    whereQuery = whereQuery + "and" + " u.id != %s"
                else:
                    whereQuery = "where u.id != %s"
                parameters.extend([f"{not_user_id}"])
            else:
                if whereQuery != "":
                    whereQuery = whereQuery + "and" + " u.is_superuser is false"
                else:
                    whereQuery = "where u.is_superuser is false"
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

    def resolve_user_details(self, info, id):
        super_staff_authorization(info)
        try:
            user_org = UserOrganization.objects.get(user = id)
        except UserOrganization.DoesNotExist:
            raise Exception("User Organization not linked!")
        try:
            org_address = Address.objects.get(organization = user_org.organization.id)
        except Address.DoesNotExist:
            org_address = None
        return {
            'user': user_org.user,
            'organization': user_org.organization,
            'address': org_address
        }
    
    def resolve_user_search(self, info, where = None):
        user_authentication(info)
        user_org = organization_validation(info)
        if user_org is None:
            return []
        query = """select u.*, uo.user_id as user_id, o.name as organization_name, o.id as organization, ee.dob, ee.joining_date, ee.profile, ee.mobile from auth_user u 
                    left join userorganization_userorganization uo on uo.user_id = u.id 
                    left join organization_organization o on uo.organization_id = o.id
                    left join employeedetails_employee ee on ee.user_id = u.id"""
        parameters = []
        if where is not None:
            whereQuery = ""
            search = where.get('search', None)     
            if search is not None or search != '':
                whereQuery = """where (u.username ilike %s or u.first_name ilike %s or u.last_name ilike %s
                )"""
                parameters.extend([f"%{search}%", f"%{search}%", f"%{search}%"])

            if whereQuery != "":
                whereQuery = whereQuery + "and" + " o.id = %s"
            else:
                whereQuery = "where o.id = %s"
            parameters.extend([f"{user_org}"])
            query = f"{query} {whereQuery}"

        return User.objects.raw(query, parameters)