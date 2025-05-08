from django.contrib import admin
from api.models import *

# Register your models here.

admin.site.register(Role)
admin.site.register(CustomUser)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Employee)
admin.site.register(Department_poc)
admin.site.register(Contributing_factor)
# admin.site.register(Stake_holder)
# admin.site.register(Incident_type)
admin.site.register(Incident_Ticket)
# admin.site.register(Incident_factor)