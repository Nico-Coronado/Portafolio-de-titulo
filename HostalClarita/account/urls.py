from django.urls import path
from .import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/empleado/',views.empleado_register.as_view(), name = "empleado_register" ),
    path('register/cliente/',views.cliente_register.as_view(), name = "cliente_register" ),
    path('register/proveedor/',views.proveedor_register.as_view(), name = "proveedor_register" ),
    path('login/', views.login_request, name = "login"),
]