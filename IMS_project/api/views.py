# from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
import random

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
    

@api_view(["GET","POST","PATCH","DELETE"])  
def DepartmentPOCView(request): 
    if request.method == "GET":
        obj = Department_poc.objects.all()
        serializer = Department_pocSerializer(obj, many=True)
        return Response(serializer.data)
    
    if request.method == "POST":
        data = request.data
        serializer = Department_pocSerializer(data = data)

        if serializer.is_valid():
            department_id = Department.objects.get(id = data["department_id"]) 
            employee_id = Employee.objects.get(id = data["employee_id"])
            department_poc = Department_poc.objects.create(department_id = department_id,
                                                           employee_id = employee_id
                                                        )
            department_poc.save()
            return Response(Department_pocSerializer(department_poc).data ,status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    
    if request.method == "PATCH":
        data = request.data
        obj = Department_poc.objects.get(id = data["id"])
        serializer = Department_pocSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    if request.method == "DELETE":
        obj_id = request.data.get('id')
        
        if not obj_id:
            return Response({'message': 'ID is required for deletion'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Department_poc.objects.get(id=obj_id).delete()
            return Response({'message': 'Department_poc deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Department_poc.DoesNotExist:
            return Response({'message': 'Department_poc not found'}, status=status.HTTP_404_NOT_FOUND)

            


@api_view(["GET","POST","PATCH","DELETE"])  
def Incident_typeView(request):
    if request.method == "GET":
        obj = Incident_type.objects.all()
        serializer = Incident_typeSerializer(obj, many=True)
        return Response(serializer.data)
    
    if request.method == "POST":
        data = request.data
        serializer = Incident_typeSerializer(data=data)

        if serializer.is_valid():
            department_id = Department.objects.get(id = data["department_id"])

            incident_type = Incident_type.objects.create(name = data["name"],
                                                         department_id= department_id)
            incident_type.save()
            return Response(Incident_typeSerializer(incident_type).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    
    if request.method == "PATCH":
        data = request.data
        obj = Incident_type.objects.get(id = data["id"])
        serializer = Incident_typeSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    if request.method == "DELETE":
        obj_id = request.data.get('id')
        
        if not obj_id:
            return Response({'message': 'ID is required for deletion'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Incident_type.objects.get(id=obj_id).delete()
            return Response({'message': 'Incident_type deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Incident_type.DoesNotExist:
            return Response({'message': 'Incident_type not found'}, status=status.HTTP_404_NOT_FOUND)
        


@api_view(["GET","POST","PATCH","DELETE"])  
def Contributing_factorsView(request):
    if request.method == "GET":
        obj = Contributing_factor.objects.all()
        serializer = Contributing_factorsSerializer(obj, many=True)
        return Response(serializer.data)  

    if request.method == "POST":
        data = request.data
        serializer = Contributing_factorsSerializer(data=data)  
        if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors) 

    if request.method == "PATCH":
        data = request.data
        obj = Contributing_factor.objects.get(id = data["id"])
        serializer = Contributing_factor(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)  

    if request.method == "DELETE":
        obj_id = request.data.get('id')
        
        if not obj_id:
            return Response({'message': 'ID is required for deletion'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Contributing_factor.objects.get(id=obj_id).delete()
            return Response({'message': 'Contributing_factor deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Contributing_factor.DoesNotExist:
            return Response({'message': 'Contributing_factor not found'}, status=status.HTTP_404_NOT_FOUND) 
        


@api_view(["GET","POST","PATCH","DELETE"])
def Incident_ticketView(request):
    if request.method == "GET":
        obj = Incident_Ticket.objects.all()
        serializer = Incident_ticketSerilizer(obj, many=True)
        return Response(serializer.data)
    
    if request.method == "POST":
        data = request.data
        serializer = Incident_ticketSerilizer(data = data)

        if serializer.is_valid():
            report_type = Incident_type.objects.get(id = data["incident_type"])
            assigned_poc = Department_poc.objects.get(id = data["assigned_poc"])
            department = Department.objects.get(id = data["department"])
            requester_id = Employee.objects.get(id = data["requester_id"])

            incident_ticket = Incident_Ticket.objects.create(report_type = report_type,
                                                             occurence_date = data["occurence_date"],
                                                             loction = data["location"],
                                                             assigned_poc = assigned_poc,
                                                             department = department,
                                                             evidence= data["evidence"],
                                                             requester_id = requester_id)
            return Response(Incident_ticketSerilizer(incident_ticket).data)
        return Response(serializer.errors)
    
    if request.method == "PATCH":
        data = request.data
        obj = Incident_Ticket.objects.get(id = data["id"])
        serializer = Incident_ticketSerilizer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    if request.method == "DELETE":
        obj_id = request.data.get('id')
        
        if not obj_id:
            return Response({'message': 'ID is required for deletion'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Incident_Ticket.objects.get(id=obj_id).delete()
            return Response({'message': 'Incident_Ticket deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Incident_Ticket.DoesNotExist:
            return Response({'message': 'Incident_Ticket not found'}, status=status.HTTP_404_NOT_FOUND) 
        
    # payload for the response
# {"report_type":"",
# "occurence_data":"",
# "location": "",
# "assigned_poc" : "",
# "department" : "",
# "evidence": " " ,
# "requestor_id":  ""
# }




@api_view(["POST"])
def send_test_email(request):
    email = request.data.get("email")

    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    subject = "Test Email from DRF"
    message = "This is a test email sent using @api_view."
    from_email = "workwithdaniyall@gmail.com"  

    try:
        send_mail(subject, message, from_email, [email], fail_silently=False)
        return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

from django.core.cache import cache  

@api_view(["POST"])
def email_otp(request):
    email = request.data.get("email")

    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)    

    otp = str(random.randint(100000,999999))
    cache.set(email, otp, timeout=300)

    send_mail(
        subject="Your OTP code",
        message=f"Your OTP code is {otp}.",
        from_email="workwithdaniyall@gmail.com",
        recipient_list=[email],
        fail_silently=False
    )

    return Response({"message": "OTP send to email successfully"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def verify_otp(request):
    email = request.data.get("email")
    otp_input = request.data.get("otp")

    if not email or not otp_input:
        return Response({"error": "email and otp are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    otp_stored = cache.get(email)

    if otp_stored == otp_input:
        cache.delete(email)
        return Response({"message" : "OTP verified successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"error" : "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)
    


#***********************************************************************************************************************    
#                                                FORGET PASSWORD VERIFICATION
@api_view(["POST"])
def request_reset_password(request):
    email = request.data.get("email")

    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    otp = str(random.randint(100000,999999))

    cache.set(f"reset_otp_{email}",otp, timeout=300)

    send_mail(
        subject="Password reset OTP",
        message=f"Your OTP for Password reset is: {otp}.",
        from_email= "workwithdaniyall@gmail.com",
        recipient_list=[email],
        fail_silently=False
    )
     
    return Response({"message": "OTP sent to your email for password reset"}, status=status.HTTP_200_OK)

@api_view(["POST"])
def otp_verification(request):
    email = request.data.get("email")
    otp_input = request.data.get("otp")

    if not email or not  otp_input:
        return Response({"error": "email and otp are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    otp_stored = cache.get(f"reset_otp_{email}")

    if otp_stored == otp_input:
        cache.set(f"otp_verified_email", True, timeout=600)
        return Response({"message":"OTP verified. You may now reset your password"})
    else:
        return Response({"error":"Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)




#***********************************************************************************************************************