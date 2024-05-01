from graphene import Mutation, Boolean, Int, ObjectType, String, ID
from .models import Organization
from userorganization.models import UserOrganization
from address.models import Address
from .types import OrganizationInputType, OrganizationUpdateInputType, AddressInputType
from .common import CommonMethodOrg

class CreateOrganization(Mutation):
    class Arguments:
        input = OrganizationInputType(required = True)
        address = AddressInputType(required = True)

    success = Boolean()

    def mutate(self, info, input, address):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        if user_obj.is_superuser != True:
            raise Exception("Not Allowed")
        token_obj = info.context.user[1]
        user_org = token_obj['data']['organization']
        logo_url = ""
        if input.logo is not None:
            logo_instance = CommonMethodOrg()
            base_64 = input.logo.split("base64,")[1] 
            logo_url = logo_instance.upload_logo(base_64)
            del input['logo']
        organization = Organization.objects.create(**input, logo = logo_url)
        qr_instance = CommonMethodOrg(organization)
        url = qr_instance.generateQrCode()
        organization.qr_code = url
        organization.save()
        if organization:
            Address.objects.create(**address, organization = organization)
            if user_org is None:
                print("userId", user_obj.id)
                UserOrganization.objects.create(organization = organization, user = user_obj)
        return CreateOrganization(success=True)

class UpdateOrganization(Mutation):
    class Arguments:
        organization_id = Int(required=True)
        input = OrganizationUpdateInputType(required = True)

    success = Boolean()

    def mutate(self, info, organization_id, input):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        if user_obj.is_superuser != True:
            raise Exception("Not Allowed")
        token_obj = info.context.user[1]
        user_org = token_obj['data']['organization']
        if user_org != 1:
            raise Exception("Not Permit!")
        organization = Organization.objects.get(pk=organization_id)
        if input.name:
            organization.name = input.name
        if input.org_email:
            organization.org_email = input.org_email
        if input.org_phone:
            organization.org_phone = input.org_phone
        if input.slug:
            organization.slug = input.slug
        if input.logo and "logo" not in input.logo:
            logo_instance = CommonMethodOrg()
            base_64 = input.logo.split("base64,")[1] 
            url = logo_instance.upload_logo(base_64)
            organization.logo = url
        organization.save()
        return UpdateOrganization(success=True)
    
class DeleteOrganization(Mutation):
    class Arguments:
        id = ID(required=True)

    success = Boolean()

    def mutate(self, info, id):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        if user_obj.is_superuser != True:
            raise Exception("Not Allowed")
        token_obj = info.context.user[1]
        user_org = token_obj['data']['organization']
        if user_org != 1:
            raise Exception("Not Permit!")
        
        organization = Organization.objects.get(pk=id)
        logo = organization.logo,
        qr_code = organization.qr_code
        common_instance = CommonMethodOrg()
        print("logo", logo)
        common_instance.delete_file(logo)
        common_instance.delete_file(qr_code)
        organization.delete()
        return DeleteOrganization(success=True)
    
class GenerateQrCode(Mutation):
    class Arguments:
        organization_id = Int(required=True)

    success = Boolean()

    def mutate(self, info, organization_id):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        if user_obj.is_superuser != True and user_obj.is_staff != True:
            raise Exception("Not Allowed")
        organization = Organization.objects.get(pk=organization_id)
        qr_instance = CommonMethodOrg(organization)
        url = qr_instance.generateQrCode()
        organization.qr_code = url
        organization.save()
        return GenerateQrCode(success = True)
    
class UploadLogo(Mutation):
    class Arguments:
        organization_id = Int(required=True)
        data = String(required = True)

    success = Boolean()

    def mutate(self, info, organization_id, data):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        if user_obj.is_superuser != True or user_obj.is_staff != True:
            raise Exception("Not Allowed")
        
        logo_instance = CommonMethodOrg()
        url = logo_instance.upload_logo(data)
        organization = Organization.objects.get(pk=organization_id)
        organization.logo = url
        organization.save()

        return UploadLogo(success=True)
    
class OrganizationMutation(ObjectType):
    create_organization = CreateOrganization.Field()
    update_organization = UpdateOrganization.Field()
    delete_organization = DeleteOrganization.Field()
    generate_qr_code = GenerateQrCode.Field()
    upload_logo = UploadLogo.Field()