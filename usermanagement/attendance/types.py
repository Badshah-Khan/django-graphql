from graphene_django import DjangoObjectType
from .models import Attendance
from graphene import relay

class AttendanceType(DjangoObjectType):
    class Meta:
        model = Attendance
        fields = '__all__'

        filter_fields = {
            'date': ['exact', 'gte', 'lte'],
            'in_time': ['exact', 'gte', 'lte'],
            'out_time': ['exact', 'gte', 'lte'],
            'user': ['exact'],
            'organization': ['exact']
        }

        interfaces = (relay.Node,)