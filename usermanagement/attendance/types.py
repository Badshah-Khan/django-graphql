from graphene_django import DjangoObjectType
from .models import Attendance
from organization.types import OrganizationType
from user.types import UserType
from graphene import InputObjectType, Int, ObjectType, Field, String

class AttendanceType(DjangoObjectType):
    class Meta:
        model = Attendance
        fields = '__all__'

class AttendanceInput(InputObjectType):
    date = String(required = True)
    current_time = String(required = True)
    organization = Int(required = True)

class AttendanceUpdateInput(InputObjectType):
    date = String(required = True)
    in_time = String()
    out_time = String()
    user = Int(required = True)
    organization = Int(required = True)

class AttendanceUserType(ObjectType):
    attendance = Field(AttendanceType)
    organization = Field(OrganizationType)
    user = Field(UserType)

class UserAttendanceType(ObjectType):
    first_name = String()
    last_name = String()
    user_id = Int()
    present = Int()
    absent = Int()
    working_days = Int()