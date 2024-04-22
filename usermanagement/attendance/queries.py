from graphene import ObjectType

from graphene_django.filter import DjangoFilterConnectionField
from .models import Attendance
from .types import AttendanceType


class AttendanceQuery(ObjectType):
    attendances = DjangoFilterConnectionField(AttendanceType)

    def resolve_attendances(self, info, **kwargs):
        return Attendance.objects.all()
