from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import user_passes_test

urlpatterns = [
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('grappelli-docs/', include('grappelli.urls_docs')), # grappelli docs URLS
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('', include('visions.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

handler404 = 'errors.views.handler404'

handler500 = 'errors.views.handler500'

handler403 = 'errors.views.handler403'
