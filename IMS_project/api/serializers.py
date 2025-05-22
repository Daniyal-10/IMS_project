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

class StakeHolderSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Stake_holder
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
        fields = ['id','Firstname', 'Lastname','designation_id','Department','job_title','phone_no', 'Email']

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

class IncidentTikcetSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Incident_Ticket
        fields = "__all__"

class IncidentTicketSerializer1(serializers.ModelSerializer):
    Reporter = serializers.SerializerMethodField()
    Department = DepartmentSerializer(source='department', read_only=True)
    Report_Type = serializers.CharField(source='report_type.name', read_only=True)
    Occurance_date = serializers.DateTimeField(source='occurence_date', read_only=True)
    AssignedPOC = serializers.SerializerMethodField()
    ContributingFactors = serializers.SerializerMethodField()

    class Meta:
        model = Incident_Ticket
        fields = [
            'id',
            'Reporter',
            'Report_Type',
            'Department',
            'Occurance_date',
            'location',
            'AssignedPOC',
            'ContributingFactors'
        ]

    def get_Reporter(self, obj):
        emp = obj.requestor_id
        full_name = f"{emp.user.first_name} {emp.user.last_name}"
        designation = emp.designation_id.name if emp.designation_id else ""
        return {
            "Name": full_name,
            "Designation": designation
        }

    def get_AssignedPOC(self, obj):
        if obj.assigned_POC and obj.assigned_POC.employee_id:
            poc_user = obj.assigned_POC.employee_id.user
            return {
                "Name": f"{poc_user.first_name} {poc_user.last_name}"
            }
        return None

    def get_ContributingFactors(self, obj):
        return [factor.name for factor in obj.contributing_factors.all()]
    

class IncidentSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Incident_Ticket
        # fields = "__all__"
        fields = [
            'id',
            'requestor_id',
            'report_type',
            'department',
            'occurence_date',
            'location',
            'assigned_POC',
            'contributing_factors'
        ]
    def to_representation(self, instance):

        rep =  super().to_representation(instance)   #in this we get the initial data from the model

        rep['Reportor'] = {
            "Name":instance.requestor_id.user.full_name(),
            "Designation": instance.requestor_id.designation_id.name,
        }
        rep['assigned_POC'] = instance.assigned_POC.employee_id.user.full_name()
        rep['report_type'] = instance.report_type.name if instance.report_type else None

        rep['contributing_factors'] = [factor.name for factor in instance.contributing_factors.all()]

        rep['department'] = {
            "id": instance.department.id,
            "name": instance.department.name
        } if instance.department else None

        rep.pop('requestor_id', None)

        return rep
        

       

