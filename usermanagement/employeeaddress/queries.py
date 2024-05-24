from graphene import ObjectType, List, JSONString, Int, String
from .models import EmployeeAddress
from usermanagement.utils import camel_to_kebab, organization_validation, super_staff_authorization
from .types import EmpAddressType

class EmpAddressQuery(ObjectType):
    emp_addresses = List(EmpAddressType, where = JSONString(), limit = Int(), offset = Int(), order = String())

    def resolve_emp_addresses(self, info, where = None, limit = 100, offset = 0, order = None):
        user_obj = super_staff_authorization(info)
        user_org = organization_validation(info)
        if user_org is None:
            raise Exception("You don't have organization. Please Create to access this")
        query = """select emp_add.*, oo.name as organization, au.first_name, au.last_name from employeeaddress_employeeaddress emp_add 
                left join employeedetails_employee ee on ee.id = emp_add.user_id 
                left join auth_user au on au.id = ee.user_id
                left join userorganization_userorganization uu on uu.user_id = ee.user_id 
                left join organization_organization oo on oo.id = uu.organization_id"""
        parameters = []
        if where is not None:
            search = where.get('search', None)
            organization = where.get('organization', None)
            whereQuery = ""
            if search is not None and search != "":
                whereQuery = """where (emp_add.street ilike %s or emp_add.city ilike %s or emp_add.state ilike %s
                or emp_add.country ilike %s) """
                parameters.extend([f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"])
            if organization is not None:
                if whereQuery != "":
                    whereQuery = whereQuery + "and" + " oo.id = %s"
                else:
                    whereQuery = "where oo.id = %s"
                parameters.extend([f"{organization}"])
            elif user_obj.is_superuser and user_org != 1:
                if whereQuery != "":
                    whereQuery = whereQuery + "and" + " oo.id = %s"
                else:
                    whereQuery = "where oo.id = %s"
                parameters.extend([f"{user_org}"])
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
        emp_address = EmployeeAddress.objects.raw(query, parameters)
        return emp_address
        