from graphene import Mutation, Boolean, Int, ObjectType
from .models import Configuration
from .types import ConfigurationInput
from usermanagement.utils import super_staff_authorization, organization_validation, super_authorization

class CreateConfiguration(Mutation):
    class Arguments:
        input = ConfigurationInput(required = True)

    success = Boolean()

    def mutate(self, info, input):
        super_staff_authorization(info)
        organization = input.get('organization')
        user_org = organization_validation(info, organization)
        if user_org != organization:
            raise Exception("Invalid Organization!")
        try:
            configuration = Configuration.objects.get(organization = user_org, organization_name = input.organization_name)
            if configuration is not None:
                configuration.configuration = input.configutation
                configuration.save()
        except Configuration.DoesNotExist:
            del input['organization']
            Configuration.objects.create(**input, organization_id = organization)
        return CreateConfiguration(success=True)

class UpdateConfiguration(Mutation):
    class Arguments:
        id = Int(required=True)
        input = ConfigurationInput(required = True)

    success = Boolean()

    def mutate(self, info, id, input):
        super_staff_authorization(info)
        organization = input.get('organization')
        organization_validation(info, organization)
        configuration = Configuration.objects.get(pk=id)
        config = input.get('configuration', None)
        if config is not None:
            configuration.configuration = config
        configuration.save()
        return UpdateConfiguration(success=True)
    
class DeleteConfiguration(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    def mutate(self, info, id):
        super_authorization(info)
        configuration = Configuration.objects.get(pk=id)
        configuration.delete()
        return DeleteConfiguration(success=True)
    
class ConfigurationMutation(ObjectType):
    create_configuration = CreateConfiguration.Field()
    update_configuration = UpdateConfiguration.Field()
    delete_configuration = DeleteConfiguration.Field()