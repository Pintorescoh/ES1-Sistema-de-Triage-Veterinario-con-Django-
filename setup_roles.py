import os
from getpass import getpass
import django

# Conectamos este script con la configuración de tu proyecto Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinica.settings')
django.setup()

password = os.getenv("USERS_PASSWORD")
if not password:
    password = getpass("Contraseña para los usuarios creados: ")
    if not password:
        raise SystemExit("La contraseña no puede estar vacía")

from django.contrib.auth.models import Group, User

print("Iniciando la creación de grupos y usuarios...")

# Lista de los roles que necesita tu sistema
roles = ["admin", "normal", "viewer"]

for rol in roles:
    # 1. Creamos el grupo si no existe
    grupo, created = Group.objects.get_or_create(name=rol)
    
    # 2. Creamos un usuario de prueba para ese grupo
    user, u_created = User.objects.get_or_create(username=f"usuario_{rol}")
    
    user.set_password(password)
    user.save(update_fields=["password"])

    if rol == "admin" and not user.is_staff:
        user.is_staff = True
        user.save(update_fields=["is_staff"])
    
    # 3. Metemos al usuario dentro de su grupo correspondiente
    user.groups.add(grupo)
    print(f"✅ Grupo '{rol}' y 'usuario_{rol}' configurados correctamente.")

print("¡Proceso terminado con éxito!")