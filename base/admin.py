from django.contrib import admin

# Register your models here.
from .models import User, Employee, Department

admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Department)