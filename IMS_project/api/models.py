from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

# superuser dan@gmail.com   1234

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extrafields):
        if not email:
            raise ValueError(_("the Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extrafields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))
        return self.create_user(email, password, **extra_fields)


 
class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)


class CustomUser(AbstractUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=25, null=True)
    last_name = models.CharField(max_length=25, null=True)
    username = None           # removing user field
    email = models.EmailField(_("email address"), unique=True)  #setting it as username 
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)  

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email    
    
class Department(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)

class Designation(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    dep_id = models.ForeignKey(Department,on_delete=models.CASCADE)    

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    designation_id = models.ForeignKey(Designation, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=30)
    phone_no = models.CharField(max_length=10)
    user  = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Department_poc(models.Model):
    id = models.AutoField(primary_key=True)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)

class Stake_holder(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
class Incident_type(models.Model):
    id = models.AutoField(primary_key=True)
    name  =models.CharField(max_length=40)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)

class Contributing_factor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class Incident_Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    report_type = models.ForeignKey(Incident_type, on_delete=models.CASCADE)
    occurence_date = models.DateTimeField()
    location = models.CharField(max_length=100)
    risk_level = models.CharField(max_length=20,null=True)
    assigned_POC = models.ForeignKey(Department_poc, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    evidence = models.FileField(null=True)
    requestor_id = models.ForeignKey(Employee, on_delete=models.CASCADE)


class Incident_factor(models.Model):
    factor_id = models.ForeignKey(Contributing_factor, on_delete=models.CASCADE)
    incident_id = models.ForeignKey(Incident_Ticket, on_delete=models.CASCADE)