from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .models import Cliente, User
from .forms import EmpleadoSignUpForm, ClienteSignUpForm, ProveedorSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from apihostal.views import contarVisita 

def index(request):
    try:
        print(contarVisita(request))
        return render(request,'index.html')
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

def register(request):
    try:
        return render(request, 'register.html')
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

class empleado_register(CreateView):
    try:
        model = User
        form_class = EmpleadoSignUpForm
        template_name = 'empleado_register.html'

        def form_valid(self, form):
            user = form.save()
            login(self.request, user)
            return redirect('/')
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )

class proveedor_register(CreateView):
    try:
        model = User
        form_class = ProveedorSignUpForm
        template_name = 'proveedor_register.html'

        def form_valid(self, form):
            user = form.save()
            login(self.request, user)
            return redirect('/')
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )

class cliente_register(CreateView):
    try:
        model = User
        form_class = ClienteSignUpForm
        template_name = 'cliente_register.html'
        # Redireccion a la pagina principal(index.html)
        def form_valid(self, form):
            user = form.save()
            login(self.request, user)
            return redirect('/')
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )

def login_request(request):
    try:
        if request.method=='POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None :
                    if user.is_cliente == True:
                        login(request,user)
                        return redirect('portadacliente')
                    elif user.is_empleado == True:
                        login(request,user)
                        return redirect('empleado')
                    elif user.is_proveedor == True:
                        login(request,user)
                        return redirect('proveedor')
                    else:
                        login(request,user)
                        return redirect('portadaadmin')

                else:
                    messages.error(request,"Usuario o contraseña incorrecta")
            else:
                messages.error(request,"Usuario o contraseña incorrecta")
        return render(request, 'login.html',
        context={'form':AuthenticationForm()})
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')

def logout_view(request):
    try:
        logout(request)
        return redirect('index')
    except Exception as infoErrorm:
        print("ERROR " + str(infoErrorm) )
        return redirect('paginaerror')


