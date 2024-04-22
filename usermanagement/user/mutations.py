from graphene import ObjectType, String, Mutation, Field, Int
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from userorganization.models import UserOrganization
from organization.models import Organization
from .types import LoginInput, UserType, TokenType, UserInputType, ResolveUserType

class Login(Mutation):
    class Arguments:
        login_input = LoginInput(required=True)

    token = Field(TokenType)

    def mutate(self, info, login_input):
        # Authenticate the user
        user = authenticate(
            username=login_input.username,
            password=login_input.password
        )

        if user is None:
            raise Exception("Invalid username or password")

        user_org = UserOrganization.objects.get(user = user.id)
        user_type = ResolveUserType(user, user_org.organization)

        # Generate JWT tokens for the authenticated user
        refresh = RefreshToken.for_user(user)
        refresh['data'] = {
            'organization': user_org.organization.id
        }
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Return the tokens
        return Login(
            token=TokenType(
                access_token=access_token,
                refresh_token=refresh_token,
                user = user_type.format()
            )
        )

class CreateUser(Mutation): 
    class Arguments:
        input = UserInputType(required = True)

    user = Field(UserType)
    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        token_obj = info.context.user[1]
        organization = token_obj['data']['organization']

        if organization != input.organization:
            raise Exception("Unauthorized")
        if user_obj.is_superuser != True or user_obj.is_staff != True:
            raise Exception("Not Allowed")
        del input['organization']
        user = User.objects.create_user(**input)
        user_org = Organization.objects.get(pk = organization)
        if user:
            UserOrganization.objects.create(user = user, organization = user_org)
        user_type = ResolveUserType(user, user_org)
        return CreateUser(user = user_type.format())

# Register the mutation
class LoginMutation(ObjectType):
    login = Login.Field()
    create_user = CreateUser.Field()
