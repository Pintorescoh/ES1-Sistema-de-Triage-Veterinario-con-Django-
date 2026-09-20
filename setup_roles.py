import os
import django

# Conectamos este script con la configuración de tu proyecto Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinica.settings')
django.setup()

from django.contrib.auth.models import Group, User

print("Iniciando la creación de grupos y usuarios...")

# Lista de los roles que necesita tu sistema
roles = ["admin", "normal", "viewer"]

for rol in roles:
    # 1. Creamos el grupo si no existe
    grupo, created = Group.objects.get_or_create(name=rol)
    
    # 2. Creamos un usuario de prueba para ese grupo
    user, u_created = User.objects.get_or_create(username=f"usuario_{rol}")
    
    if u_created:
        user.set_password("Inacap2026!") # Le ponemos una contraseña por defecto
        user.save()
    
    # 3. Metemos al usuario dentro de su grupo correspondiente
    user.groups.add(grupo)
    print(f"✅ Grupo '{rol}' y 'usuario_{rol}' configurados correctamente.")

print("¡Proceso terminado con éxito!")