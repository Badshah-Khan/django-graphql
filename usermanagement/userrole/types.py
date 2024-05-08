from graphene import String, InputObjectType, Int, ObjectType

class RoleType(ObjectType):
    id = Int()
    user_id = Int()
    role_id = Int()
    user_role = String()
    first_name = String()
    last_name = String()
    organization = String()

class RoleInputType(InputObjectType):
    role = Int(required = True)
    user = Int(required = True)