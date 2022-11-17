"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'mercale.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Dashboard customizado
    """
    class Media:
        css = {
             "all": ("css/admin/adminIndex.css",)
        }
        
    def init_with_context(self, context):
 
        # Funcionalidades da Administração do Portal
        self.children.append(modules.ModelList(
            _(u'Administração'),
            column=1,
            collapsible=True,
            models=('django.contrib.*',),
        ))
 
        # Funcionalidade de Formas de Pagamento
        self.children.append(modules.ModelList(
            _(u'Registro de login'),
            column=1,
            collapsible=True,
            models=('accounts.*',),
        ))
 
        self.children.append(modules.ModelList(
            _(u'Criação e liberação de relatórios'),
            column=1,
            collapsible=True,
            models=('visions.*',),
        ))
        
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _(u'Outras Opções'),
            column=2,
            children=[
                {
                    'title': _(u'Voltar para o sistema'),
                    'url': '/',
                },
                {
                    'title': _(u'Alterar Senha'),
                    'url': '/admin/password_change',
                },
                {
                    'title': _(u'Sair do Acesso Administrativo'),
                    'url': '/admin/logout/',
                },
            ]
        ))
 
        # Ações Recentes
        self.children.append(modules.RecentActions(
            _(u'Ações Recentes'),
            limit=10,
            collapsible=True,
            column=3,
        ))