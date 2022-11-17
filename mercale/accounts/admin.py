from django.contrib import admin
from .models import loginRegister
from django.contrib.auth.models import User   

##Cria a database que registra todos os logins
@admin.register(loginRegister)
class loginRegister(admin.ModelAdmin):
    #modelagem dos itens que aparecem na tabela, filtros e campo de pesquisa
    list_display =('userId', 'userIp', 'userLoginTime')
    list_filter = ('userId',)
    search_fields = ['userId__username', 'userIp', 'userLoginTime'] 
    list_per_page = 10
    list_display_links = None
    #change_list_template = "admin/change_list_filter_sidebar.html"
    
    class Media:
        css = {
             "all": ("css/admin/adminTable.css",)
        }
    
    #funções que desabilitam edição, inserção e deletação dos registros
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    
    def change_view(self, request,object_id,form_url='', obj=None):
        from django.urls import reverse
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(reverse('admin:accounts_loginregister_changelist'))
    

class userAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'last_login', 'is_active', 'is_superuser')
    list_filter = ('is_active','is_superuser')
    search_fields = ['username', 'first_name','email']
    list_per_page = 10
    #change_list_template = "admin/change_list_filter_sidebar.html"
    
    @staticmethod
    def autocomplete_search_fields():
        return ( "username")

    class Media:
        css = {
            "all": ("css/admin/adminTable.css",)
        }
    def has_add_permission(self, request):
        return False

admin.site.unregister(User)
admin.site.register(User, userAdmin)