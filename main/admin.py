from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import *

# Define an inline admin descriptor for Profile model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    fk_name = "user"
    can_delete = False
    verbose_name_plural = 'Profile'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_filter = BaseUserAdmin.list_filter + ('profile__is_practitioner',)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class PractitionerAdmin(admin.ModelAdmin):
	list_display = ['is_practitioner',]
	can_delete = False
	def get_queryset(self, request):
		return super(PractitionerAdmin,self).get_queryset(request).filter(is_practitioner=True)

admin.site.register(Practitioner, PractitionerAdmin)

class PatientAdmin(admin.ModelAdmin):
	def get_queryset(self, request):
		return super(PatientAdmin,self).get_queryset(request).filter(is_practitioner=False)

admin.site.register(Patient, PatientAdmin)