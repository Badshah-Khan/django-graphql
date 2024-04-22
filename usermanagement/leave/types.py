from graphene_django import DjangoObjectType
from .models import Leave
from graphene import relay

class LeaveType(DjangoObjectType):
    class Meta:
        model = Leave
        fields = '__all__'

        filter_fields = {
            'leave_type': ['exact', 'icontains'],
            'reason': ['exact', 'icontains'],
            'from_date': ['exact', 'gte', 'lte'],
            'to_date': ['exact', 'gte', 'lte'],
            'is_approved': ['exact'],
            'approved_by': ['exact'],
            'user': ['exact'],
            'organization': ['exact']
        }

        interfaces = (relay.Node,)