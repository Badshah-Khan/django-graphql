from graphene import InputObjectType, String, Int, ObjectType, Field, Boolean, Date
from address.types import AddressType, AddressOrgInputType
from organization.types import OrganizationType

class LoginInput(InputObjectType):
    username = String()
    email = String()
    password = String(required=True)

class UserType(ObjectType):
    organization = Int()
    organization_name = String()
    user_id = Int()
    username = String()
    email = String()
    first_name = String()
    last_name = String()
    is_superuser = Boolean()
    is_staff = Boolean()
    is_active = Boolean()
    dob = Date()
    joining_date = Date()
    mobile = String()
    profile = String()

class TokenType(ObjectType):
    token = String()
    refresh_token = String()
    user = Field(UserType)

class UserInputType(InputObjectType):
    username = String(required = True)
    first_name = String(required = True)
    last_name = String()
    email = String(required = True)
    organization = Int(required = True)
    password = String(required = True)
    is_employee = Boolean(required = True)
    is_superuser = Boolean()
    is_staff = Boolean()
    dob = Date()
    joining_date = Date()
    mobile = String()
    address = Field(AddressOrgInputType)

class UserUpdateInputType(InputObjectType):
    first_name = String()
    last_name = String()
    organization = Int(required = True)
    dob = Date()
    joining_date = Date()
    mobile = String()

class UserDetailsType(ObjectType):
    user = Field(UserType)
    address = Field(AddressType)
    organization = Field(OrganizationType)

class ChangePasswordInputType(InputObjectType):
    old_password = String(required = True)
    new_password = String(required = True)