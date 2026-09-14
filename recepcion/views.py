from django.shortcuts import render, redirect, get_object_or_404
from solucion import decidir # ¡Corregido! Importamos decidir
from .models import Paciente
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from functools import wraps

# --- SISTEMA DE SEGURIDAD Y ROLES ---

def tiene_rol(user, *roles):
    return user.groups.filter(name__in=roles).exists() or user.is_superuser

def requiere_rol(*roles):
    def decorador(view_func):
        @wraps(view_func)
        @login_required(login_url="login")
        def wrapper(request, *args, **kwargs):
            if tiene_rol(request.user, *roles):
                return view_func(request, *args, **kwargs)
            messages.error(request, "No tienes permiso para esta acción.")
            return redirect("lista")
        return wrapper
    return decorador

# --- VISTAS DE AUTENTICACIÓN ---

def vista_login(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username", "").strip(),
            password=request.POST.get("password", "")
        )
        if user:
            login(request, user)
            return redirect("lista")
        messages.error(request, "Usuario o contraseña incorrectos.")
    
    return render(request, "login.html")

def vista_logout(request):
    logout(request)
    return redirect("login")

# 1. READ (Leer la sala de espera)
@login_required(login_url="login")
def lista(request):
    pacientes = Paciente.objects.filter(eliminado=False) 
    return render(request, "lista.html", {"pacientes": pacientes})

# 2. CREATE (Crear paciente)
@requiere_rol("admin", "normal")
def crear(request):
    error = None
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        respiracion = request.POST.get("dificultad_respiracion", "").strip()
        
        try:
            dolor = int(request.POST.get("dolor", ""))
        except ValueError:
            error = "El dolor debe ser un número entero."
        else:
            # ¡Corregido! Usamos decidir()
            resultado = decidir(respiracion, dolor)
            Paciente.objects.create(
                nombre=nombre, 
                dificultad_respiracion=respiracion,
                dolor=dolor, 
                gravedad=resultado
            )
            return redirect("lista")
            
    return render(request, "form.html", {"accion": "Crear", "error": error})

# 3. UPDATE (Editar paciente)
@requiere_rol("admin")
def editar(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk, eliminado=False)
    error = None
    
    if request.method == "POST":
        paciente.nombre = request.POST.get("nombre", "").strip()
        paciente.dificultad_respiracion = request.POST.get("dificultad_respiracion", "").strip()
        
        try:
            paciente.dolor = int(request.POST.get("dolor", ""))
        except ValueError:
            error = "El dolor debe ser un número entero."
        else:
            # ¡Corregido! Usamos decidir()
            paciente.gravedad = decidir(paciente.dificultad_respiracion, paciente.dolor)
            paciente.save()
            return redirect("lista")
            
    return render(request, "form.html", {"accion": "Editar", "registro": paciente, "error": error})

# 4. DELETE (Eliminar paciente)
@requiere_rol("admin")
def eliminar(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk, eliminado=False)
    
    if request.method == "POST":
        paciente.soft_delete()
        return redirect("lista")
        
    return render(request, "confirmar.html", {"registro": paciente})