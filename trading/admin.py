from django.contrib import admin
from .models import ideas
# Register your models here.

'''

class accAdmin(admin.AdminSite):
    site_header='Admin Area'
    

class AccntAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request,obj=None):
       return False
    
ac_site=accAdmin(name='Administration')
ac_site.register(Account,AccntAdmin)
'''