from graphene import ObjectType, List, JSONString, Int, String
from .models import UserRole
from .types import RoleType
from usermanagement.utils import camel_to_kebab, super_staff_authorization, organization_validation


class UserRoleQuery(ObjectType):
    roles = List(RoleType, where = JSONString(), limit = Int(), offset = Int(), order = String())

    def resolve_roles(self, info, where = None, limit = 100, offset = 0, order = None):
        super_staff_authorization(info)
        organization = organization_validation(info)
        query = """select au.first_name, uu.user_id, uu.role_id, au.last_name, oo.name as organization, uu2.role as user_role, uu.id from userrole_userrole uu 
                    left join auth_user au on au.id = uu.user_id 
                    left join usertype_usertype uu2 on uu2.id = uu.role_id 
                    left join organization_organization oo on oo.id = uu2.organization_id"""
        parameters = []

        whereQuery = ""
        if where is not None:
            search = where.get('search', None)
            user_organization = where.get('organization', None)
            id = where.get('id', None)
            if search is not None and search != "":
                whereQuery = """where (au.username ilike %s or au.first_name ilike %s or au.last_name ilike %s
                or oo.name ilike %s or uu2.role ilike %s) """
                parameters.extend([f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"])
            if id is not None:
                if whereQuery != "":
                    whereQuery = whereQuery + "and" + " uu.id = %s"
                else:
                    whereQuery = "where uu.id = %s"
                parameters.extend([f"{id}"])
            if whereQuery != "":
                whereQuery = whereQuery + "and" + " oo.id = %s"
            else:
                whereQuery = "where oo.id = %s"
            if user_organization is not None:
                parameters.extend([f"{user_organization}"])
            else:
                parameters.extend([f"{organization}"])
        else:
            whereQuery = "where oo.id = %s"
            parameters.extend([f"{organization}"])
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
        result = UserRole.objects.raw(query, parameters)
        return result
