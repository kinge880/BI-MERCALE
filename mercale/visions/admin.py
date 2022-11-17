from django.contrib import admin
from .models import visions, vision_to_user, vision_request   
from django.contrib import messages
from django.utils.translation import ngettext   
from django.core.exceptions import ValidationError
from datetime import datetime

admin.site.site_header = 'Mercale PowerBI Admin'
admin.site.index_title = 'Gerenciamento de registros'
admin.site.enable_nav_sidebar = True

@admin.register(visions)
class visionsAdmin(admin.ModelAdmin):
    list_display =('nameVision', 'is_active', 'created_at','updated_at')
    list_filter = ('is_active',)
    list_per_page = 10
    search_fields = ['nameVision']
    #change_list_template = "admin/change_list_filter_sidebar.html"
    
    @staticmethod
    def autocomplete_search_fields():
        return ("nameVision")
    
    class Media:
        css = {
             "all": ("css/admin/adminTable.css",)
        }

@admin.register(vision_to_user)
class vision_to_userAdmin(admin.ModelAdmin):
    list_display =('userId', 'visionId', 'created_at','updated_at')
    list_filter = ('visionId','userId')
    raw_id_fields = ('userId', 'visionId',)
    list_per_page = 10
    search_fields = ['userId__username', 'visionId__nameVision']
    description='Relatórios PowerBI'
    #change_list_template = "admin/change_list_filter_sidebar.html"
    
    @staticmethod
    def autocomplete_search_fields():
        return ("userId__username", "visionId__nameVision",)
    
    class Media:
        css = {
             "all": ("css/admin/adminTable.css",)
        }
        
@admin.register(vision_request)
class vision_request(admin.ModelAdmin):
    list_display =('userId', 'visionId', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    raw_id_fields = ('userId', 'visionId',)
    list_per_page = 10
    search_fields = ['userId__username', 'visionId__nameVision']
    change_list_template = "admin/change_list_filter_sidebar.html"
    description='Colicitações de PowerBI'
    
    def autocomplete_search_fields():
        return ("userId__username", "visionId__nameVision",)
    
    class Media:
        css = {
             "all": ("css/admin/adminTable.css",)
        }
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    
    #aceita solicitações e salva no banco de dados
    @admin.action(description='Aceitar solicitação')
    def my_admin_ok(self, request, queryset):
        validator = False
        #verifica cada item marcado e se um não for pendente, breka o loop
        for query in queryset:
            if query.status != "Pendente":
                validator = True
                break
        
        #se validator for verdadeiro lança mensagem de erro   
        if validator:
            self.message_user(request,'Somente solicitações pendentes podem ser Aceitas!', messages.WARNING)
        #se validator for falso, cada item já foi verificado e aprovado, então novamente percorro a lista salvando cada um deles no banco
        else:
            for query in queryset:
                newRequest = vision_to_user(userId = query.userId, visionId = query.visionId)
                #verifico se o item já existe no user, apenas uma garantia para evitar duplicidade em casos extremamente raros
                try:
                    vision_to_user.save_admin_panel(newRequest)
                except ValidationError:
                    validator = True
                    self.message_user(request,'Esse usuário já recebeu acesso ao relatório', messages.WARNING)
            if validator == False:
                updated = queryset.update(status='Aceito', updated_at = datetime.today())
                self.message_user(request, ngettext(
                    '%d Solicitação Aceita com sucesso',
                    '%d Solicitações Aceitas com sucesso.',
                    updated,
                ) % updated, messages.SUCCESS)
    
    #rejeita solicitações
    @admin.action(description='Recusar solicitação')
    def my_admin_no(self, request, queryset):
        validator = False
        #verifica cada item marcado e se um não for pendente, breka o loop
        for query in queryset:
            if query.status != "Pendente":
                validator = True
                break
        
        #se validator for verdadeiro lança mensagem de erro, se for falso muda o status de todos os itens para negado e lança mensagem positiva     
        if validator:
            self.message_user(request,'Somente solicitações pendentes podem ser recusadas!', messages.WARNING)
        else:
            updated = queryset.update(status='Negado', updated_at = datetime.today())
            self.message_user(request, ngettext(
                '%d Solicitação recusada com sucesso',
                '%d Solicitações recusadas com sucesso.',
                updated,
            ) % updated, messages.SUCCESS)
        
    actions = [my_admin_ok, my_admin_no]