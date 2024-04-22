from graphene import InputObjectType, String, Int, ObjectType, Field, Boolean

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

class TokenType(ObjectType):
    access_token = String()
    refresh_token = String()
    user = Field(UserType)

class UserInputType(InputObjectType):
    username = String(required = True)
    first_name = String(required = True)
    last_name = String()
    email = String(required = True)
    organization = Int(required = True)
    password = String(required = True)
    
class ResolveUserType(ObjectType):
    def __init__(self, user, organization):
        self.user = user
        self.organization = organization
    
    def format(self) -> UserType:
        return UserType(
            user_id=self.user.id,
            username=self.user.username,
            first_name=self.user.first_name,
            last_name=self.user.last_name,
            email=self.user.email,
            is_superuser = self.user.is_superuser,
            is_active = self.user.is_active,
            is_staff = self.user.is_staff,
            organization = self.organization.id,
            organization_name = self.organization.name
        )