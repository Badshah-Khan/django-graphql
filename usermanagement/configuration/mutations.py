from graphene import Mutation, Boolean, Int, ObjectType
from .models import Configuration
from .types import ConfigurationInput

class CreateConfiguration(Mutation):
    class Arguments:
        input = ConfigurationInput(required = True)

    success = Boolean()

    def mutate(self, info, input):
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        token_obj = info.context.user[1]
        user_org = token_obj['data']['organization']
        if user_obj.is_superuser != True and user_obj.is_staff != True:
            raise Exception("Not Allowed")
        organization = input.get('organization')
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
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        token_obj = info.context.user[1]
        user_org = token_obj['data']['organization']
        if user_obj.is_superuser != True and user_obj.is_staff != True:
            raise Exception("Not Allowed")
        if user_org != input.organization:
            raise Exception("Not Allowed")
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
        is_auth = info.context.is_auth
        if not is_auth:
            raise Exception("Unauthorized")
        user_obj = info.context.user[0]
        if user_obj.is_superuser != True:
            raise Exception("Not Allowed")
        configuration = Configuration.objects.get(pk=id)
        configuration.delete()
        return DeleteConfiguration(success=True)
    
class ConfigurationMutation(ObjectType):
    create_configuration = CreateConfiguration.Field()
    update_configuration = UpdateConfiguration.Field()
    delete_configuration = DeleteConfiguration.Field()