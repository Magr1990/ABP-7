import os
import shutil
from pathlib import Path

# Directorio base (ABP 7)
BASE_DIR = Path.cwd()
print(f"🔧 Analizando estructura en: {BASE_DIR}")

# Buscar settings.py para encontrar la carpeta real del proyecto
settings_files = list(BASE_DIR.rglob("settings.py"))

if not settings_files:
    print("❌ No se encontró settings.py. Asegúrate de estar en la carpeta correcta.")
    exit()

# Tomamos el primer settings.py encontrado
settings_path = settings_files[0]
project_package = settings_path.parent  # Carpeta 'alke_wallet'
project_root = project_package.parent   # Carpeta contenedora (ej: ProyectoWallet)

print(f"📦 Carpeta de configuración encontrada: {project_package}")

# 1. Mover la carpeta de configuración (alke_wallet) a la raíz
target_package = BASE_DIR / project_package.name
if project_package != target_package:
    if not target_package.exists():
        print(f" -> Moviendo {project_package.name} a la raíz...")
        shutil.move(str(project_package), str(target_package))
    else:
        print(f" -> La carpeta {target_package.name} ya existe en la raíz.")

# 2. Buscar y mover la app 'wallet' a la raíz
wallet_dirs = list(BASE_DIR.rglob("wallet"))
real_wallet_app = None

# Identificar cuál es la app real (la que tiene models.py)
for w in wallet_dirs:
    if (w / "models.py").exists() and "templates" not in str(w):
        real_wallet_app = w
        break

if real_wallet_app:
    target_wallet = BASE_DIR / "wallet"
    if real_wallet_app != target_wallet:
        if not target_wallet.exists():
            print(f" -> Moviendo app 'wallet' a la raíz...")
            shutil.move(str(real_wallet_app), str(target_wallet))
        else:
            print(f" -> La carpeta 'wallet' ya existe en la raíz.")

# 3. Limpiar carpetas vacías antiguas
if (BASE_DIR / "ProyectoWallet").exists():
    print(" -> Limpiando carpetas antiguas...")
    shutil.rmtree(BASE_DIR / "ProyectoWallet", ignore_errors=True)

print("\n✅ ¡Estructura reparada! Ahora puedes ejecutar los comandos de Django.")