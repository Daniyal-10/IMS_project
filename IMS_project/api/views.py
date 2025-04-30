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
    elif request.method == "DELETE":
        data = request.data
        obj = Role.objects.get(id = data["id"])
        obj.delete()
        return Response({'messege' : 'role deleted'})
    
@api_view(["GET","POST","DELETE"]) 
def DepartmentView(request):
    if request.method == "GET":
        obj = Department.objects.all()
        serializer = DepartmentSerializer(obj , many = True)
        return Response(serializer.data)
    elif request.method == "POST":
        data = request.data
        serializer = DepartmentSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == "DELETE":
        data = request.data
        obj = Department.objects.get(id = data["id"])
        obj.delete()
        return Response({'messege' : 'Department deleted'})
    

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



@api_view(["GET", "POST", "DELETE"])
def CustomUserView(request):
    if request.method == "GET":
        obj = CustomUser.objects.all()
        serializer = CustomUserSerializer(obj, many=True)
        return Response(serializer.data)
    # elif request.method =="POST":

