from graphene import ObjectType, Schema
from organization.mutations import OrganizationMutation
from address.mutations import AddressMutation
from address.queries import AddressQuery
from organization.queries import OrganizationQuery
from attendance.mutations import AttendanceMutation
from attendance.queries import AttendanceQuery
from leave.mutations import LeaveMutation
from leave.queries import LeaveQuery
from user.mutations import LoginMutation
from user.queries import UserQuery
from permission.mutations import PermissionMutation
from permission.queries import PermissionQuery
from userrole.mutations import RoleMutation
from userrole.queries import UserRoleQuery
from usertype.mutations import UserTypeMutation
from usertype.queries import UserTypeQuery
from employeeaddress.queries import EmpAddressQuery
from workingdays.mutations import WorkingDaysMutation
from workingdays.queries import WorkingDaysQuery
from message.mutations import MessageMutation
from message.queries import MessageQuery
from message.queries import MessageSubscription

class Query(OrganizationQuery, AddressQuery, AttendanceQuery, LeaveQuery, 
            PermissionQuery, UserRoleQuery, UserTypeQuery, UserQuery,
            EmpAddressQuery, WorkingDaysQuery, MessageQuery, ObjectType):
    pass

class Mutation(OrganizationMutation, AddressMutation, AttendanceMutation, 
               LeaveMutation, LoginMutation, PermissionMutation, 
               RoleMutation, UserTypeMutation, WorkingDaysMutation, MessageMutation,
               ObjectType):
    pass

schema = Schema(query=Query, mutation=Mutation, subscription=MessageSubscription)

