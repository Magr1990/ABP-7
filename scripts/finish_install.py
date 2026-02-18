import os
import shutil
import sys
from pathlib import Path

# Intentar importar Django de forma segura para evitar errores visuales en el editor
try:
    import django # type: ignore
except ImportError:
    pass # Se manejará más adelante si es necesario

BASE_DIR = Path.cwd()
WALLET_DIR = BASE_DIR / 'wallet'

print("🚀 Iniciando RESTAURACIÓN DEL SISTEMA...")

# 1. Rescatar archivos completos de la raíz si existen (por si acaso)
files_to_rescue = ['views.py', 'urls.py', 'models.py', 'forms.py', 'admin.py']
for filename in files_to_rescue:
    src = BASE_DIR / filename
    dst = WALLET_DIR / filename
    if src.exists():
        print(f"📦 Moviendo {filename} original a la carpeta 'wallet'...")
        if dst.exists():
            os.remove(dst)
        shutil.move(str(src), str(dst))

# 1.1 Eliminar carpetas antiguas que pueden causar conflictos (ProyectoWallet)
old_project_dir = BASE_DIR / 'ProyectoWallet'
if old_project_dir.exists():
    print("🧹 Eliminando carpeta antigua 'ProyectoWallet' para evitar duplicados...")
    shutil.rmtree(old_project_dir)

# 2. Limpieza profunda para arreglar el error "no such table"
print("🧹 Limpiando base de datos y migraciones corruptas...")

# Eliminar db.sqlite3
db_file = BASE_DIR / 'db.sqlite3'
if db_file.exists():
    try:
        os.remove(db_file)
        print(" -> Base de datos eliminada.")
    except PermissionError:
        print("❌ Error: No se pudo eliminar db.sqlite3. Asegúrate de que el servidor no esté corriendo.")
        sys.exit(1)

# Eliminar migraciones de wallet para regenerarlas
migrations_dir = WALLET_DIR / 'migrations'
if migrations_dir.exists():
    shutil.rmtree(migrations_dir)
    print(" -> Migraciones antiguas eliminadas.")

# Recrear carpeta migrations
migrations_dir.mkdir(exist_ok=True)
(migrations_dir / '__init__.py').touch()

# 3. Ejecutar comandos de Django
def run_command(command):
    print(f"⚙️ Ejecutando: {command}")
    result = os.system(f"python manage.py {command}")
    if result != 0:
        print(f"❌ Error al ejecutar {command}")
        sys.exit(1)

# Crear migraciones específicas para wallet y luego generales
run_command("makemigrations wallet")
run_command("makemigrations")
run_command("migrate")

# 4. Cargar servicios
print("🔄 Cargando servicios...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alke_wallet.settings')
if 'django' in sys.modules:
    django.setup()

try:
    from wallet.models import Service # type: ignore
    services = [
        ('ENEL', 'enel_logo.png'),
        ('AGUAS_ANDINAS', 'aguas_logo.png'),
        ('METROGAS', 'metrogas_logo.png'),
        ('VTR', 'vtr_logo.png'),
    ]
    for name_key, logo in services:
        Service.objects.get_or_create(name=name_key, defaults={'logo': logo})
    print("✅ Servicios cargados correctamente.")
except Exception as e:
    print(f"⚠️ Advertencia cargando servicios: {e}")

# 5. Crear superusuario por defecto
try:
    from django.contrib.auth.models import User # type: ignore
    if not User.objects.filter(username='admin').exists():
        print("👤 Creando usuario administrador (User: admin / Pass: admin)...")
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    else:
        print("👤 El usuario 'admin' ya existe.")
except Exception as e:
    print(f"❌ Error creando usuario: {e}")

print("\n✅ ¡Instalación completada con éxito! Ahora ejecuta: python manage.py runserver")