from graphene import InputObjectType, String, Int

class HolydaysInput(InputObjectType):
    ocation = String(required = True)
    description = String()
    num_of_days = Int(required = True)
    organization = Int(required = True)