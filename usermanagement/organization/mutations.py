from graphene import Mutation, Boolean, Field, Int, ObjectType, String
from .models import Organization
from .types import OrganizationType, OrganizationInputType
from .common import QrCodeGenerator

class CreateOrganization(Mutation):
    class Arguments:
        org_input = OrganizationInputType(required = True)

    success = Boolean()
    organization = Field(OrganizationType)

    def mutate(self, info, org_input):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        if user_obj.is_superuser != True:
            raise Exception("Not Allowed")
        
        organization = Organization.objects.create(name=org_input.name, org_email=org_input.org_email, org_phone=org_input.org_phone)
        return CreateOrganization(success=True, organization=organization)

class UpdateOrganization(Mutation):
    class Arguments:
        organization_id = Int(required=True)
        org_input = OrganizationInputType(required = True)

    success = Boolean()
    organization = Field(OrganizationType)

    def mutate(self, info, organization_id, org_input):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        if user_obj.is_superuser != True:
            raise Exception("Not Allowed")
        
        organization = Organization.objects.get(pk=organization_id)
        if org_input.name:
            organization.name = org_input.name
        if org_input.org_email:
            organization.org_email = org_input.org_email
        if org_input.org_phone:
            organization.org_phone = org_input.org_phone
        organization.save()
        return UpdateOrganization(success=True, organization = organization)
    
class DeleteOrganization(Mutation):
    class Arguments:
        organization_id = Int(required=True)

    success = Boolean()

    def mutate(self, info, organization_id):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        if user_obj.is_superuser != True:
            raise Exception("Not Allowed")
        
        organization = Organization.objects.get(pk=organization_id)
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
        if user_obj.is_superuser != True or user_obj.is_staff != True:
            raise Exception("Not Allowed")
        organization = Organization.objects.get(pk=organization_id)
        qr_instance = QrCodeGenerator(organization)
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
        
        qr_instance = QrCodeGenerator()
        url = qr_instance.generateQrCode()
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