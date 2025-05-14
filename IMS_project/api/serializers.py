from .models import *
from rest_framework import serializers

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

class DesignationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Designation
        fields = "__all__"

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id","first_name","last_name","email","password","role"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields="__all__"        

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    
    class Meta: 
        model = Employee
        fields = "__all__"   

# Employee view with the user data also with the specific fields
class EmployeeProfile(serializers.ModelSerializer):
    Firstname = serializers.CharField(source = "user.first_name")
    Lastname = serializers.CharField(source = "user.last_name")
    Email = serializers.CharField(source = "user.email")
    Department = serializers.CharField(source = "designation_id.dep_id.name")

    class Meta:
        model = Employee
        fields = ['job_title','id','designation_id','phone_no','Firstname', 'Lastname', 'Email', 'Department']

class Department_pocSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Department_poc
        fields = "__all__"

class Incident_typeSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Incident_type
        fields = "__all__"

class Contributing_factorsSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Contributing_factor
        fields = "__all__"

class Incident_ticketSerilizer(serializers.ModelSerializer):
    class Meta: 
        model = Incident_Ticket
        fields = "__all__"        