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

class EmployeeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    
    class Meta: 
        model = Employee
        fields = "__all__"     
