# from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

@api_view(["GET","POST","DELETE"])
def RoleView(request):
    if request.method == "GET":
        obj = Role.objects.all()
        serializer = RoleSerializer(obj, many = True)
        return Response(serializer.data)
    elif request.method == "POST":
        data = request.data
        serializer = RoleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    if request.method == "DELETE":
        obj_id = request.data.get('id')
        
        if not obj_id:
            return Response({'message': 'ID is required for deletion'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Role.objects.get(id=obj_id).delete()
            return Response({'message': 'Role deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Role.DoesNotExist:
            return Response({'message': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)
        
@api_view(["GET","POST","DELETE"]) 
def DepartmentView(request):
    if request.method == "GET":
        obj = Department.objects.all()
        serializer = DepartmentSerializer(obj , many = True)
        return Response(serializer.data)
    if request.method == "POST":
        data = request.data
        serializer = DepartmentSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    if request.method == "DELETE":
        obj_id = request.data.get('id')
        
        if not obj_id:
            return Response({'message': 'ID is required for deletion'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Department.objects.get(id=obj_id).delete()
            return Response({'message': 'Department deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Department.DoesNotExist:
            return Response({'message': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(["GET","POST","DELETE"]) 
def DesignationView(request):
    if request.method == "GET":
        obj = Designation.objects.all()
        serializer = DesignationSerializer(obj , many = True)
        return Response(serializer.data)
    if request.method == "POST":
        data = request.data
        serializer = DesignationSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    if request.method == "DELETE":
        obj_id = request.data.get('id')
        
        if not obj_id:
            return Response({'message': 'ID is required for deletion'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Designation.objects.get(id=obj_id).delete()
            return Response({'message': 'Designation deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Designation.DoesNotExist:
            return Response({'message': 'Designation not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(["GET", "POST", "PATCH", "DELETE"])
def CustomUserView(request):
    if request.method == "GET":
        obj = CustomUser.objects.all()
        serializer = CustomUserSerializer(obj, many=True)
        return Response(serializer.data)
    

    if request.method =="POST":              #IMP stepss [making single view for user and employee creation]
        data = request.data
        serializer_u = CustomUserSerializer(data = data)

        #User creation to get the user id to pass in the employee
        if serializer_u.is_valid():
            role = Role.objects.get(id=data["role"])
        
            user = CustomUser.objects.create(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                role=role)
            user.set_password(data["password"])
            user.save()

            # Now creating employee as saved user and got the user id
            employee_data = {
                "designation_id": data["designation_id"],
                "job_title": data["job_title"],
                "phone_no": data["phone_no"],
                "user": user.id  # This will map to 'user_id'
            }

            serializer_e = EmployeeSerializer(data = employee_data)
            if serializer_e.is_valid():
                serializer_e.save()
                response_data = {
                        "user":CustomUserSerializer(user).data,
                        "employee":serializer_e.data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
    
            else:
                user.delete()
                return Response({"employee_errors": serializer_e.errors}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({"user_errors": serializer_u.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == "PATCH":
        data = request.data
        obj = CustomUser.objects.get(id = data["id"])
        serializer = CustomUserSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors).render.acceptres
    
    if request.method == "DELETE":
        obj_id = request.data.get('id')
        
        if not obj_id:
            return Response({'message': 'ID is required for deletion'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            CustomUser.objects.get(id=obj_id).delete()
            return Response({'message': 'User deleted'}, status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET", "PATCH"])
def EmployeeView(request):
    if request.method == "GET":
        obj = Employee.objects.all()
        serializer = EmployeeSerializer(obj, many=True)
        return Response(serializer.data)
    
    if request.method == "PATCH":
        data = request.data
        obj = Employee.objects.get(id = data["id"])
        serializer = EmployeeSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)






