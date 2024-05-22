from graphene import InputObjectType, JSONString, String, Int

class ConfigurationInput(InputObjectType):
    organization_name = String(required = True)
    organization = Int(required = True)
    configuration = JSONString(required = True)