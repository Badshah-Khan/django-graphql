from graphene import InputObjectType, ObjectType, String, Date, Int

class HolydayInput(InputObjectType):
    ocation = String(required = True)
    description = String()
    num_of_days = Int(required = True)
    from_date = Date(required = True)
    to_date = Date(required = True)
    organization = Int(required = True)

class HolydayType(ObjectType):
    id = Int()
    ocation = String()
    description = String()
    num_of_days = Int()
    from_date = Date()
    to_date = Date()
    organization = Int()