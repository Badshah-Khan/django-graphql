from graphene import ObjectType

from graphene_django.filter import DjangoFilterConnectionField
from .models import Leave
from .types import LeaveType


class LeaveQuery(ObjectType):
    leaves = DjangoFilterConnectionField(LeaveType)

    def resolve_leaves(self, info, **kwargs):
        return Leave.objects.all()
