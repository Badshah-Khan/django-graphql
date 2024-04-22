from graphene import Mutation, Boolean, Field, Int, ObjectType
from .models import Organization
from .types import OrganizationType, OrganizationInputType

class CreateOrganization(Mutation):
    class Arguments:
        org_input = OrganizationInputType(required = True)

    success = Boolean()
    organization = Field(OrganizationType)

    def mutate(self, info, org_input):
        organization = Organization.objects.create(name=org_input.name, org_email=org_input.org_email, org_phone=org_input.org_phone)
        return CreateOrganization(success=True, organization=organization)

class UpdateOrganization(Mutation):
    class Arguments:
        organization_id = Int(required=True)
        org_input = OrganizationInputType(required = True)

    success = Boolean()
    organization = Field(OrganizationType)

    def mutate(self, info, organization_id, org_input):
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
        organization = Organization.objects.get(pk=organization_id)
        organization.delete()
        return DeleteOrganization(success=True)
    
class OrganizationMutation(ObjectType):
    create_organization = CreateOrganization.Field()
    update_organization = UpdateOrganization.Field()
    delete_organization = DeleteOrganization.Field()