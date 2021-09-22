from django.contrib import admin
from django.urls import path, include
import account.views
from apihostal import views
from rest_framework import routers, serializers, viewsets

import apihostal

# Enrutador del REST FRAMEWORK
router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet, basename='users')
# router.register(r'groups', views.GroupViewSet)
router.register(r'platos', views.PlatoViewSet,  basename='platos')
router.register(r'comedores', views.ComedorViewSet, basename='comedores')

urlpatterns = [
    path('',account.views.index, name='index'),
    path('account/', include('account.urls')),
    path('admin-hostal/', include('administrador.urls')),
    path('cliente/', include('cliente.urls')),
    path('empleado/', include('empleado.urls')),
    path('proveedor/', include('proveedor.urls')),
    path('admin/', admin.site.urls),
    path('logout/', account.views.logout_view, name="logout"),
    
    path('apiclarita/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("paginaerror/", views.paginaerror, name='paginaerror'),
    path("abouthostalclarita/", views.abouthostalclarita, name='abouthostalclarita'),
    path("politicaprivacidad/", views.politicaprivacidad, name='politicaprivacidad'),
]
