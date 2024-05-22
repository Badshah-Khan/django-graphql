from graphene_django import DjangoObjectType
from .models import Leave
from graphene import InputObjectType, String, Int, Date, Boolean

class LeaveType(DjangoObjectType):
    class Meta:
        model = Leave
        fields = '__all__'

class LeaveInput(InputObjectType):
    leave_type = String(required = True)
    reason = String()
    from_date = Date(required = True)
    to_date = Date(required = True)
    organization = Int(required = True)
    is_half_day = Boolean()