import os
import shutil
import sys
from pathlib import Path

# Intentar importar Django de forma segura
try:
    import django # type: ignore
except ImportError:
    pass

BASE_DIR = Path.cwd()
WALLET_DIR = BASE_DIR / 'wallet'
TEMPLATE_DIR = WALLET_DIR / 'templates' / 'wallet'

print("⏳ INICIANDO RESTAURACIÓN AL ESTADO DE AYER...")

# ---------------------------------------------------------
# 1. RESTAURAR EL DISEÑO ANTIGUO (home.html)
# ---------------------------------------------------------
print("🎨 Restaurando diseño visual (Tarjeta Visa + Menú Vertical)...")

home_html_content = """{% extends 'wallet/base.html' %}
{% load static %}

{% block content %}
<style>
    .credit-card {
        background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
        color: white;
        border-radius: 15px;
        padding: 25px;
        width: 100%;
        max-width: 400px;
        height: 240px;
        position: relative;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        margin: 0 auto;
        font-family: 'Courier New', Courier, monospace;
    }
    .card-logo {
        position: absolute;
        top: 20px;
        right: 25px;
        height: 50px;
        font-style: italic;
        font-weight: bold;
        font-size: 24px;
    }
    .card-chip {
        width: 50px;
        height: 40px;
        background: linear-gradient(135deg, #ffd700 0%, #b8860b 100%);
        border-radius: 8px;
        margin-top: 30px;
        margin-bottom: 20px;
    }
    .card-number {
        font-size: 1.6em;
        letter-spacing: 3px;
        margin-bottom: 25px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    .card-label {
        font-size: 0.7em;
        text-transform: uppercase;
        opacity: 0.8;
        display: block;
        margin-bottom: 2px;
    }
    .card-info {
        font-size: 1em;
        text-transform: uppercase;
    }
</style>

<div class="container mt-5">
    <div class="row">
        <!-- Sección Izquierda: Tarjeta y Saldos -->
        <div class="col-md-6 mb-4">
            <div class="credit-card">
                <div class="card-logo">VISA</div>
                <div class="card-chip"></div>
                
                <div class="card-number">
                    **** **** **** {{ card.number|slice:"-4:" }}
                </div>
                
                <div class="d-flex justify-content-between">
                    <div>
                        <span class="card-label">Titular</span>
                        <span class="card-info">{{ user.first_name }} {{ user.last_name }}</span>
                    </div>
                    <div>
                        <span class="card-label">Expira</span>
                        <span class="card-info">{{ card.expiry }}</span>
                    </div>
                </div>
            </div>
            
            <div class="mt-4 text-center">
                <div class="row">
                    <div class="col-6">
                        <small class="text-muted">Cupo Nacional</small>
                        <h4 class="text-success">${{ card.national_available }}</h4>
                    </div>
                    <div class="col-6">
                        <small class="text-muted">Cupo Internacional</small>
                        <h4 class="text-primary">${{ card.international_available }} USD</h4>
                    </div>
                </div>
            </div>
        </div>

        <!-- Cuenta Corriente -->
        <div class="col-md-6">
            <h3 class="mb-3">Cuenta Corriente</h3>
            <div class="card shadow-sm">
                <div class="card-body p-4">
                    <div class="text-center mb-4">
                        <small class="text-muted">Saldo Disponible</small>
                        <h1 class="display-4 fw-bold">${{ account.balance }}</h1>
                    </div>
                    
                    <ul class="list-group list-group-flush mb-4">
                        <li class="list-group-item d-flex justify-content-between">
                            <span>Número de Cuenta</span>
                            <strong>{{ account.account_number }}</strong>
                        </li>
                        <li class="list-group-item d-flex justify-content-between">
                            <span>Línea de Crédito</span>
                            <strong>${{ account.credit_line_available }}</strong>
                        </li>
                    </ul>
                    
                    <!-- Menú Vertical Restaurado -->
                    <div class="d-grid gap-2">
                        <a href="{% url 'transfer' %}" class="btn btn-primary btn-lg">Transferir</a>
                        <a href="{% url 'deposit' %}" class="btn btn-success btn-lg">Depositar</a>
                        <a href="{% url 'pay_service' %}" class="btn btn-warning btn-lg text-dark">Pagar Servicios</a>
                        <a href="{% url 'pay_card' %}" class="btn btn-info btn-lg text-white">Pagar Tarjeta</a>
                        <a href="{% url 'movements' %}" class="btn btn-secondary btn-lg">Ver Movimientos</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

# Asegurar que la carpeta existe y escribir el archivo
TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
with open(TEMPLATE_DIR / 'home.html', 'w', encoding='utf-8') as f:
    f.write(home_html_content)

# ---------------------------------------------------------
# 2. EJECUTAR LIMPIEZA Y REINSTALACIÓN (Usando finish_install.py)
# ---------------------------------------------------------
print("⚙️ Ejecutando script de reinstalación para aplicar cambios...")
if (BASE_DIR / 'finish_install.py').exists():
    os.system('python finish_install.py')
else:
    print("❌ No se encontró finish_install.py. Asegúrate de tenerlo en la carpeta.")

print("\n✅ ¡RESTAURACIÓN COMPLETA! El diseño debería ser el de ayer.")
print("👉 Ejecuta: python manage.py runserver")
