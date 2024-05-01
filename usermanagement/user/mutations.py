from graphene import ObjectType,  Mutation, Field, ID, Boolean
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from userorganization.models import UserOrganization
from organization.models import Organization
from employeedetails.models import Employee
from employeeaddress.models import EmployeeAddress
from .types import LoginInput, TokenType, UserInputType, UserUpdateInputType

class Login(Mutation):
    class Arguments:
        input = LoginInput(required=True)

    result = Field(TokenType)

    def mutate(self, info, input):
        print('login_input', input)
        if input.username is None and input.email is None:
            raise Exception("Email OR Username is Missing!")
        # Authenticate the user
        password = input.get('password')
        del input['password']
        user = None
        try:
            user = User.objects.get(**input)
        except User.DoesNotExist:
            raise Exception("User doesn't exist!")
        if user is None or user.check_password(password) is False:
            raise Exception("Invalid username or password")
        try:
            user_org = UserOrganization.objects.get(user = user.id)
            user.organization = user_org.organization.id
            user.organization_name = user_org.organization.name
        except UserOrganization.DoesNotExist:
            user.organization = None
            user.organization_name = None
            user_org = None
        user.user_id = user.id
        try:
            emp_details = Employee.objects.get(user=user.id)
            if emp_details:
                user.dob = emp_details.dob
                user.joining_date = emp_details.joining_date
        except Employee.DoesNotExist:
            # Handle the case where no matching employee is found
            print("Employee not found for the specified user.")

        # Generate JWT tokens for the authenticated user
        refresh = RefreshToken.for_user(user)
        if user_org is not None:
            refresh['data'] = {
                'organization': user_org.organization.id
            }
        else:
            refresh['data'] = {
                'organization': None
            }
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Return the tokens
        return Login(
            result=TokenType(
                token=access_token,
                refresh_token=refresh_token,
                user = user
            )
        )

class CreateUser(Mutation): 
    class Arguments:
        input = UserInputType(required = True)

    success = Boolean()
    def mutate(self, info, input):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        
        user_obj = info.context.user[0]
        token_obj = info.context.user[1]
        organization = token_obj['data']['organization']
        
        if user_obj.is_superuser != True and user_obj.is_staff != True:
            raise Exception("Not Allowed")
        if user_obj.is_superuser != True and organization != input.organization:
            raise Exception("Unauthorized")
        if user_obj.is_active is not True:
            raise Exception("You can't perform this action!")
        dob = input.get('dob', None)
        joining_date = input.get('joining_date', None)
        mobile = input.get('mobile', None)
        del input['organization']
        if dob is not None:
            del input['dob']
        if joining_date is not None:
            del input['joining_date']
        if mobile is not None:
            del input['mobile']
        is_employee = input.get('is_employee', False)
        del input['is_employee']
        address = input.get('address', None)
        del input['address']

        user = User.objects.create_user(**input)
        user_org = Organization.objects.get(pk = organization)
        if user and is_employee != False:
            UserOrganization.objects.create(user = user, organization = user_org)
        if is_employee:
            employee = Employee.objects.create(dob = dob, joining_date=joining_date, mobile=mobile, user = user)
        if address is not None:
            EmployeeAddress.objects.create(**address, user = employee)
        return CreateUser(success = True)

class UpdateUser(Mutation): 
    class Arguments:
        input = UserUpdateInputType(required = True)
        user_id = ID(required = True)

    success = Boolean()
    def mutate(self, info, input, user_id):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        
        user_obj = info.context.user[0]
        token_obj = info.context.user[1]
        organization = token_obj['data']['organization']
        
        if organization != input.organization:
            raise Exception("Unauthorized")
        if user_obj.is_superuser != True or user_obj.is_staff != True:
            raise Exception("Not Allowed")

        dob = input.get('dob', None)
        joining_date = input.get('joining_date', None)
        mobile = input.get('mobile', None)
        first_name = input.get('first_name', None)
        last_name = input.get('last_name', None)
        user = User.objects.get(pk = user_id)
        if user.is_superuser and organization != 1:
            raise Exception("Not Allowed")
        if user_obj.is_staff == True and user.is_staff == True:
            raise Exception("Not Allowed")
        if user_obj.is_active is not True:
            raise Exception("You can't perform this action!")

        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        user.save()

        try:
            emp_instance = Employee.objects.get(user_id = user_id)
            if dob is not None:
                emp_instance.dob = dob
            if joining_date is not None:
                emp_instance.joining_date = joining_date
            if mobile is not None:
                emp_instance.mobile = mobile
            emp_instance.save()
        except Employee.DoesNotExist:
            Employee.objects.create(dob=dob, mobile = mobile, joining_date = joining_date, user_id = user_id)
        return UpdateUser(success = True)
    
class ActivateORDeactivateUser(Mutation):
    class Arguments:
        id = ID(required = True)

    success = Boolean()

    def mutate(self, info, id):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        
        user_obj = info.context.user[0]
        token_obj = info.context.user[1]
        organization = token_obj['data']['organization']
        if user_obj.is_superuser != True and user_obj.is_staff != True:
            raise Exception("Not Allowed")
        if user_obj.is_active is not True:
            raise Exception("You can't perform this action!")

        user = User.objects.get(pk = id)
        user_org = UserOrganization.objects.get(user = user.id)

        if user_obj.is_staff == True and user_org.organization != organization:
            raise Exception("Not Allowed")
        if user.is_superuser:
            raise Exception("Not Allowed")
        
        user.is_active = not user.is_active
        user.save()
        return ActivateORDeactivateUser(success = True)


# Register the mutation
class LoginMutation(ObjectType):
    login = Login.Field()
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    activate_deactivate_user = ActivateORDeactivateUser.Field()