import os
import django

# Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alke_wallet.settings')
django.setup()

from wallet.models import Service

def populate():
    services = [
        ('ENEL', 'enel_logo.png'),
        ('AGUAS_ANDINAS', 'aguas_logo.png'),
        ('METROGAS', 'metrogas_logo.png'),
        ('VTR', 'vtr_logo.png'),
    ]

    print("🔄 Creando servicios...")
    for name_key, logo in services:
        obj, created = Service.objects.get_or_create(name=name_key, defaults={'logo': logo})
        print(f"   {'✅ Creado' if created else 'ℹ️ Ya existe'}: {name_key}")

if __name__ == '__main__':
    populate()