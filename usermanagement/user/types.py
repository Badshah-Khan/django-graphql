from graphene import InputObjectType, String, Int, ObjectType, Field, Boolean, Date

class LoginInput(InputObjectType):
    username = String(required=True)
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
    dob = Date()
    joining_date = Date()
    mobile = String()

class UserUpdateInputType(InputObjectType):
    first_name = String()
    last_name = String()
    organization = Int(required = True)
    dob = Date()
    joining_date = Date()
    mobile = String()