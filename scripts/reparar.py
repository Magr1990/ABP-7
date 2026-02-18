import os
from pathlib import Path

# Verificar que estamos en la carpeta correcta
if not os.path.exists('manage.py'):
    print("❌ ERROR: Debes ejecutar este script en la misma carpeta que manage.py")
    exit()

print("🔧 Iniciando reparación y actualización de plantillas HTML...")

base_dir = Path.cwd()

# Diccionario con los archivos y su contenido LIMPIO (sin caracteres ocultos)
files = {
    "wallet/templates/wallet/base.html": """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wallet Chile</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .card-custom { border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .navbar-brand { font-weight: bold; color: #0d6efd !important; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">🇨🇱 Wallet Chile</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    {% if user.is_authenticated %}
                        <li class="nav-item"><a class="nav-link" href="{% url 'home' %}">Inicio</a></li>
                        <li class="nav-item"><a class="nav-link" href="{% url 'movements' %}">Movimientos</a></li>
                        <li class="nav-item">
                            <form action="{% url 'logout' %}" method="post" class="d-inline">
                                {% csrf_token %}
                                <button type="submit" class="btn btn-link nav-link" style="text-decoration: none;">Cerrar Sesión</button>
                            </form>
                        </li>
                    {% else %}
                        <li class="nav-item"><a class="nav-link" href="{% url 'login' %}">Iniciar Sesión</a></li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <div class="container">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            {% endfor %}
        {% endif %}

        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>""",

    "wallet/templates/registration/login.html": """{% extends 'wallet/base.html' %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 col-lg-4">
        <div class="card card-custom p-4">
            <h3 class="text-center mb-4">Bienvenido</h3>
            <form method="post">
                {% csrf_token %}
                {% if form.errors %}
                    <div class="alert alert-danger text-center" role="alert">
                        Credenciales inválidas. Intente nuevamente.
                    </div>
                {% endif %}
                <div class="form-floating mb-3">
                    <input type="text" name="username" class="form-control" id="id_username" placeholder="Nombre de Usuario" required autofocus>
                    <label for="id_username">Nombre de Usuario</label>
                </div>
                <div class="form-floating mb-3">
                    <input type="password" name="password" class="form-control" id="id_password" placeholder="Contraseña" required>
                    <label for="id_password">Contraseña</label>
                </div>
                <div class="d-grid">
                    <button type="submit" class="btn btn-primary">Iniciar Sesión</button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}""",

    "wallet/templates/wallet/home.html": """{% extends 'wallet/base.html' %}

{% block content %}
<div class="row">
    <div class="col-md-12 mb-4">
        <div class="card card-custom bg-primary text-white p-4">
            <h2>Saldo Cuenta Corriente</h2>
            <h1 class="display-4 fw-bold">${{ account.balance }} CLP</h1>
            <p class="mb-0">N° Cuenta: {{ account.account_number }}</p>
        </div>
    </div>

    <div class="col-md-4 mb-3">
        <div class="card card-custom p-3">
            <h6 class="text-muted">Línea de Crédito</h6>
            <h4>Disp: ${{ account.credit_line_available }}</h4>
            <small class="text-danger">Uso: ${{ account.credit_line_usage }}</small>
        </div>
    </div>
    <div class="col-md-4 mb-3">
        <div class="card card-custom p-3">
            <h6 class="text-muted">Tarjeta Crédito (CLP)</h6>
            <h4>Disp: ${{ card.national_available }}</h4>
            <small class="text-danger">Deuda: ${{ card.national_balance }}</small>
        </div>
    </div>
    <div class="col-md-4 mb-3">
        <div class="card card-custom p-3">
            <h6 class="text-muted">Tarjeta Crédito (USD)</h6>
            <h4>Disp: ${{ card.international_available }}</h4>
            <small class="text-danger">Deuda: ${{ card.international_balance }}</small>
        </div>
    </div>

    <div class="col-12 mt-4">
        <h4 class="mb-3">Operaciones</h4>
        <div class="row g-3">
            <div class="col-6 col-md-2">
                <a href="{% url 'deposit' %}" class="btn btn-outline-primary w-100 h-100 py-3">📥<br>Depositar</a>
            </div>
            <div class="col-6 col-md-2">
                <a href="{% url 'transfer' %}" class="btn btn-outline-primary w-100 h-100 py-3">💸<br>Transferir</a>
            </div>
            <div class="col-6 col-md-2">
                <a href="{% url 'movements' %}" class="btn btn-outline-primary w-100 h-100 py-3">📋<br>Movimientos</a>
            </div>
            <div class="col-6 col-md-2">
                <a href="{% url 'credit_line' %}" class="btn btn-outline-primary w-100 h-100 py-3">🏦<br>Línea Crédito</a>
            </div>
            <div class="col-6 col-md-2">
                <a href="{% url 'pay_service' %}" class="btn btn-outline-primary w-100 h-100 py-3">💡<br>Servicios</a>
            </div>
            <div class="col-6 col-md-2">
                <a href="{% url 'card_detail' %}" class="btn btn-outline-primary w-100 h-100 py-3">💳<br>Tarjeta</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}""",

    "wallet/templates/wallet/deposit.html": """{% extends 'wallet/base.html' %}
{% block content %}
<div class="card card-custom p-4 mx-auto" style="max-width: 600px;">
    <h3 class="mb-3">Depositar Fondos</h3>
    <div class="alert alert-info">
        <div class="row">
            <div class="col-md-6">
                <strong>Saldo Cta. Corriente:</strong> ${{ account.balance }}<br>
                <strong>Deuda Línea Crédito:</strong> ${{ account.credit_line_usage }}
            </div>
            <div class="col-md-6">
                <strong>Cupo Tarjeta Nacional:</strong> ${{ card.national_available }}<br>
                <strong>Cupo Tarjeta Intl. (USD):</strong> ${{ card.international_available }}
            </div>
        </div>
    </div>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <div class="d-flex justify-content-between mt-4">
            <a href="{% url 'home' %}" class="btn btn-secondary">Volver</a>
            <button type="submit" class="btn btn-success">Depositar</button>
        </div>
    </form>
</div>
{% endblock %}""",

    "wallet/templates/wallet/transfer.html": """{% extends 'wallet/base.html' %}
{% block content %}
<div class="card card-custom p-4 mx-auto" style="max-width: 600px;">
    <h3 class="mb-3">Transferir a Terceros</h3>
    <p class="text-muted">Se descontará de su Cuenta Corriente o Línea de Crédito.</p>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <div class="d-flex justify-content-between mt-4">
            <a href="{% url 'home' %}" class="btn btn-secondary">Volver</a>
            <button type="submit" class="btn btn-primary">Transferir</button>
        </div>
    </form>
</div>
{% endblock %}""",

    "wallet/templates/wallet/pay_service.html": """{% extends 'wallet/base.html' %}
{% block content %}
<div class="card card-custom p-4 mx-auto" style="max-width: 600px;">
    <h3 class="mb-3">Pago de Servicios</h3>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <div class="d-flex justify-content-between mt-4">
            <a href="{% url 'home' %}" class="btn btn-secondary">Volver</a>
            <button type="submit" class="btn btn-primary">Pagar Cuenta</button>
        </div>
    </form>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const paymentMethodSelect = document.getElementById('id_payment_method');
    const installmentsInput = document.getElementById('id_installments');
    
    // El form.as_p de Django envuelve los campos en etiquetas <p>. Buscamos la etiqueta padre para ocultarla/mostrarla.
    const installmentsWrapper = installmentsInput.closest('p'); 

    function toggleInstallments() {
        if (paymentMethodSelect.value === 'CREDIT_CARD') {
            // Habilitar cuotas para Tarjeta de Crédito
            if (installmentsWrapper) installmentsWrapper.style.display = 'block';
            installmentsInput.disabled = false;
        } else {
            // Bloquear cuotas para Cuenta Corriente
            if (installmentsWrapper) installmentsWrapper.style.display = 'none';
            installmentsInput.disabled = true;
        }
    }

    // Ejecutar la función al cargar la página para establecer el estado inicial correcto.
    toggleInstallments();

    // Añadir un detector de eventos para cuando el usuario cambie el método de pago.
    paymentMethodSelect.addEventListener('change', toggleInstallments);
});
</script>
{% endblock %}""",

    "wallet/templates/wallet/pay_card.html": """{% extends 'wallet/base.html' %}
{% block content %}
<div class="card card-custom p-4 mx-auto" style="max-width: 600px;">
    <h3 class="mb-3">Pagar Tarjeta de Crédito</h3>
    <div class="alert alert-warning">
        <strong>Deuda Nacional:</strong> ${{ card.national_balance }} CLP<br>
        <strong>Deuda Internacional:</strong> ${{ card.international_balance }} USD
    </div>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <div class="d-flex justify-content-between mt-4">
            <a href="{% url 'card_detail' %}" class="btn btn-secondary">Volver</a>
            <button type="submit" class="btn btn-success">Pagar Deuda</button>
        </div>
    </form>
</div>
{% endblock %}""",

    "wallet/templates/wallet/card_detail.html": """{% extends 'wallet/base.html' %}
{% block content %}
<style>
    .credit-card-visual {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        border-radius: 15px;
        color: white;
        padding: 20px;
        height: 220px;
        position: relative;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        margin-bottom: 20px;
    }
    .card-chip {
        width: 50px;
        height: 35px;
        background: #ffd700;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    .card-number-text {
        font-family: 'Courier New', Courier, monospace;
        font-size: 1.5rem;
        letter-spacing: 2px;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px black;
    }
</style>

<div class="row">
    <div class="col-md-6 mx-auto">
        <div class="card card-custom p-4 mb-4">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h3>Mi Tarjeta</h3>
                <img src="https://www.freepnglogos.com/uploads/visa-logo-png-20.png" alt="Visa" height="25">
            </div>
            {% if show_details %}
                <!-- Tarjeta Visual Desbloqueada -->
                <div class="credit-card-visual">
                    <div class="d-flex justify-content-between">
                        <div class="card-chip"></div>
                        <img src="https://www.freepnglogos.com/uploads/visa-logo-white-png-11.png" alt="Visa" height="25">
                    </div>
                    <div class="text-center" style="margin-bottom: 20px;">
                        <div class="d-inline-flex align-items-center">
                            <span id="cardNumber" class="card-number-text" style="margin-bottom: 0;">{{ card.number }}</span>
                            <button id="copyBtn" class="btn btn-sm p-1 ms-2" title="Copiar número" style="background: none; border: none; color: white;">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clipboard" viewBox="0 0 16 16"><path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"/><path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z"/></svg>
                            </button>
                        </div>
                    </div>
                    <div class="d-flex justify-content-between mt-4">
                        <div>
                            <small style="font-size: 0.7rem;">TITULAR</small><br>
                            {{ user.username|upper }}
                        </div>
                        <div class="text-end">
                            <small style="font-size: 0.7rem;">VENCE / CVV</small><br>
                            {{ card.expiry }} / {{ card.cvv }}
                        </div>
                    </div>
                </div>
            {% else %}
                <!-- Tarjeta Visual Bloqueada -->
                <div class="credit-card-visual" style="filter: grayscale(80%);">
                    <div class="d-flex justify-content-between">
                        <div class="card-chip" style="background: #ccc;"></div>
                        <img src="https://www.freepnglogos.com/uploads/visa-logo-white-png-11.png" alt="Visa" height="25">
                    </div>
                    <div class="card-number-text text-center">**** **** **** {{ card.number|slice:"-4:" }}</div>
                    <div class="d-flex justify-content-between mt-4">
                        <div>
                            <small style="font-size: 0.7rem;">TITULAR</small><br>
                            {{ user.username|upper }}
                        </div>
                        <div class="text-end">
                            <small style="font-size: 0.7rem;">VENCE</small><br>
                            **/**
                        </div>
                    </div>
                </div>
                
                <form method="post" class="mt-3">
                    {% csrf_token %}
                    <div class="input-group">
                        {{ form.pin }}
                        <button class="btn btn-warning" type="submit">👁️ Ver Datos</button>
                    </div>
                    <small class="text-muted">PIN por defecto: 1234</small>
                </form>
            {% endif %}
            <hr>
            <div class="row">
                <div class="col-6">
                    <h5>Nacional (CLP)</h5>
                    <p>Utilizado: ${{ card.national_balance }}</p>
                    <p>Disponible: ${{ card.national_available }}</p>
                </div>
                <div class="col-6 border-start">
                    <h5>Internacional (USD)</h5>
                    <p>Utilizado: ${{ card.international_balance }}</p>
                    <p>Disponible: ${{ card.international_available }}</p>
                </div>
            </div>
            <div class="d-grid gap-2 mt-4">
                <a href="{% url 'pay_card' %}" class="btn btn-success">Pagar Tarjeta</a>
                <div class="d-flex gap-2">
                    <a href="{% url 'movements' %}" class="btn btn-outline-primary flex-grow-1">Movimientos</a>
                    <button class="btn btn-outline-secondary flex-grow-1">Configuración</button>
                </div>
            </div>
        </div>
        <div class="text-center">
            <a href="{% url 'home' %}" class="btn btn-secondary">Volver al Inicio</a>
        </div>
    </div>
</div>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const copyBtn = document.getElementById('copyBtn');
        if (copyBtn) {
            copyBtn.addEventListener('click', function() {
                const cardNumber = document.getElementById('cardNumber').innerText;
                navigator.clipboard.writeText(cardNumber.replace(/\s/g, '')).then(function() {
                    const originalTitle = copyBtn.title;
                    copyBtn.title = '¡Copiado!';
                    setTimeout(() => {
                        copyBtn.title = originalTitle;
                    }, 2000);
                }, function(err) {
                    console.error('No se pudo copiar el texto: ', err);
                });
            });
        }
    });
</script>
{% endblock %}""",

    "wallet/templates/wallet/movements.html": """{% extends 'wallet/base.html' %}
{% block content %}
<div class="card card-custom p-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h3>Historial de Movimientos</h3>
        <a href="{% url 'home' %}" class="btn btn-secondary">Volver</a>
    </div>
    <div class="table-responsive">
        <table class="table table-hover">
            <thead class="table-light">
                <tr>
                    <th>Fecha</th>
                    <th>Tipo</th>
                    <th>Descripción</th>
                    <th class="text-end">Monto</th>
                </tr>
            </thead>
            <tbody>
                {% for t in transactions %}
                <tr>
                    <td>{{ t.date|date:"d/m/Y H:i" }}</td>
                    <td>
                        {% if t.transaction_type == 'DEPOSIT' %}
                            <span class="badge bg-success">Depósito</span>
                        {% elif t.transaction_type == 'TRANSFER' %}
                            <span class="badge bg-warning text-dark">Transferencia</span>
                        {% else %}
                            <span class="badge bg-info text-dark">Pago</span>
                        {% endif %}
                    </td>
                    <td>{{ t.description }}</td>
                    <td class="text-end fw-bold">${{ t.amount }}</td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="4" class="text-center">No hay movimientos registrados.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}""",

    "wallet/templates/wallet/credit_line.html": """{% extends 'wallet/base.html' %}
{% block content %}
<div class="card card-custom p-4 mx-auto" style="max-width: 600px;">
    <h3 class="mb-3">Estado Línea de Crédito</h3>
    
    <div class="row text-center mb-4">
        <div class="col-4">
            <h5 class="text-muted">Cupo Total</h5>
            <p class="fs-5">${{ account.credit_line_limit }}</p>
        </div>
        <div class="col-4 border-start border-end">
            <h5 class="text-danger">Utilizado</h5>
            <p class="fs-5 fw-bold">${{ account.credit_line_usage }}</p>
        </div>
        <div class="col-4">
            <h5 class="text-success">Disponible</h5>
            <p class="fs-5 fw-bold">${{ account.credit_line_available }}</p>
        </div>
    </div>

    <div class="alert alert-secondary">
        <small>ℹ️ La línea de crédito se utiliza automáticamente cuando realizas transferencias o retiros sin saldo suficiente en tu Cuenta Corriente.</small>
    </div>

    {% if account.credit_line_usage > 0 %}
        <div class="alert alert-warning">
            Tienes una deuda activa. Cualquier depósito que realices se usará primero para pagar esta deuda.
        </div>
        <div class="d-grid gap-2">
            <a href="{% url 'deposit' %}" class="btn btn-success">Pagar Deuda (Depositar)</a>
        </div>
    {% else %}
        <div class="alert alert-success">
            ¡Excelente! No tienes deuda en tu línea de crédito.
        </div>
    {% endif %}

    <div class="text-center mt-3">
        <a href="{% url 'home' %}" class="btn btn-link">Volver al Inicio</a>
    </div>
</div>
{% endblock %}"""
}

# Escribir archivos
for rel_path, content in files.items():
    file_path = base_dir / rel_path
    # Crear carpetas si no existen
    file_path.parent.mkdir(parents=True, exist_ok=True)
    # Escribir archivo con codificación UTF-8 limpia (sin BOM)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Reparado: {rel_path}")

print("\n🎉 ¡Listo! Todas las plantillas han sido reparadas y actualizadas.")
print("👉 Ahora ejecuta: python manage.py runserver")
import os
from pathlib import Path

# Verificar que estamos en la carpeta correcta
if not os.path.exists('manage.py'):
    print("❌ ERROR: Debes ejecutar este script en la misma carpeta que manage.py")
    exit()

print("🔧 Iniciando reparación de archivos...")

base_dir = Path.cwd()

# Diccionario con los archivos y su contenido LIMPIO (sin caracteres ocultos)
files = {
    "wallet/templates/wallet/base.html": """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wallet Chile</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .card-custom { border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .navbar-brand { font-weight: bold; color: #0d6efd !important; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">🇨🇱 Wallet Chile</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    {% if user.is_authenticated %}
                        <li class="nav-item"><a class="nav-link" href="{% url 'home' %}">Inicio</a></li>
                        <li class="nav-item"><a class="nav-link" href="{% url 'movements' %}">Movimientos</a></li>
                        <li class="nav-item">
                            <form action="{% url 'logout' %}" method="post" class="d-inline">
                                {% csrf_token %}
                                <button type="submit" class="btn btn-link nav-link" style="text-decoration: none;">Cerrar Sesión</button>
                            </form>
                        </li>
                    {% else %}
                        <li class="nav-item"><a class="nav-link" href="{% url 'login' %}">Iniciar Sesión</a></li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <div class="container">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            {% endfor %}
        {% endif %}

        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>""",

    "wallet/templates/registration/login.html": """{% extends 'wallet/base.html' %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 col-lg-4">
        <div class="card card-custom p-4">
            <h3 class="text-center mb-4">Bienvenido</h3>
            <form method="post">
                {% csrf_token %}
                {% if form.errors %}
                    <div class="alert alert-danger text-center" role="alert">
                        Credenciales inválidas. Intente nuevamente.
                    </div>
                {% endif %}
                <div class="form-floating mb-3">
                    <input type="text" name="username" class="form-control" id="id_username" placeholder="Nombre de Usuario" required autofocus>
                    <label for="id_username">Nombre de Usuario</label>
                </div>
                <div class="form-floating mb-3">
                    <input type="password" name="password" class="form-control" id="id_password" placeholder="Contraseña" required>
                    <label for="id_password">Contraseña</label>
                </div>
                <div class="d-grid">
                    <button type="submit" class="btn btn-primary">Iniciar Sesión</button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}""",

    "wallet/templates/wallet/home.html": """{% extends 'wallet/base.html' %}

{% block content %}
<div class="row">
    <div class="col-md-12 mb-4">
        <div class="card card-custom bg-primary text-white p-4">
            <h2>Saldo Cuenta Corriente</h2>
            <h1 class="display-4 fw-bold">${{ account.balance }} CLP</h1>
            <p class="mb-0">N° Cuenta: {{ account.account_number }}</p>
        </div>
    </div>

    <div class="col-md-4 mb-3">
        <div class="card card-custom p-3">
            <h6 class="text-muted">Línea de Crédito</h6>
            <h4>Disp: ${{ account.credit_line_available }}</h4>
            <small class="text-danger">Uso: ${{ account.credit_line_usage }}</small>
        </div>
    </div>
    <div class="col-md-4 mb-3">
        <div class="card card-custom p-3">
            <h6 class="text-muted">Tarjeta Crédito (CLP)</h6>
            <h4>Disp: ${{ card.national_available }}</h4>
            <small class="text-danger">Deuda: ${{ card.national_balance }}</small>
        </div>
    </div>
    <div class="col-md-4 mb-3">
        <div class="card card-custom p-3">
            <h6 class="text-muted">Tarjeta Crédito (USD)</h6>
            <h4>Disp: ${{ card.international_available }}</h4>
            <small class="text-danger">Deuda: ${{ card.international_balance }}</small>
        </div>
    </div>

    <div class="col-12 mt-4">
        <h4 class="mb-3">Operaciones</h4>
        <div class="row g-3">
            <div class="col-6 col-md-2">
                <a href="{% url 'deposit' %}" class="btn btn-outline-primary w-100 h-100 py-3">📥<br>Depositar</a>
            </div>
            <div class="col-6 col-md-2">
                <a href="{% url 'transfer' %}" class="btn btn-outline-primary w-100 h-100 py-3">💸<br>Transferir</a>
            </div>
            <div class="col-6 col-md-2">
                <a href="{% url 'movements' %}" class="btn btn-outline-primary w-100 h-100 py-3">📋<br>Movimientos</a>
            </div>
            <div class="col-6 col-md-2">
                <a href="{% url 'credit_line' %}" class="btn btn-outline-primary w-100 h-100 py-3">🏦<br>Línea Crédito</a>
            </div>
            <div class="col-6 col-md-2">
                <a href="{% url 'pay_service' %}" class="btn btn-outline-primary w-100 h-100 py-3">💡<br>Servicios</a>
            </div>
            <div class="col-6 col-md-2">
                <a href="{% url 'card_detail' %}" class="btn btn-outline-primary w-100 h-100 py-3">💳<br>Tarjeta</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}""",

    "wallet/templates/wallet/deposit.html": """{% extends 'wallet/base.html' %}
{% block content %}
<div class="card card-custom p-4 mx-auto" style="max-width: 600px;">
    <h3 class="mb-3">Depositar Fondos</h3>
    <div class="alert alert-info">
        <div class="row">
            <div class="col-md-6">
                <strong>Saldo Cta. Corriente:</strong> ${{ account.balance }}<br>
                <strong>Deuda Línea Crédito:</strong> ${{ account.credit_line_usage }}
            </div>
            <div class="col-md-6">
                <strong>Cupo Tarjeta Nacional:</strong> ${{ card.national_available }}<br>
                <strong>Cupo Tarjeta Intl. (USD):</strong> ${{ card.international_available }}
            </div>
        </div>
    </div>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <div class="d-flex justify-content-between mt-4">
            <a href="{% url 'home' %}" class="btn btn-secondary">Volver</a>
            <button type="submit" class="btn btn-success">Depositar</button>
        </div>
    </form>
</div>
{% endblock %}""",

    "wallet/templates/wallet/transfer.html": """{% extends 'wallet/base.html' %}
{% block content %}
<div class="row">
    <!-- Columna del Formulario de Transferencia -->
    <div class="col-lg-6 mb-4">
        <div class="card card-custom p-4 h-100">
            <h3 class="mb-3">Transferir a Terceros</h3>
            <p class="text-muted">Se descontará de su Cuenta Corriente o Línea de Crédito.</p>
            <form method="post" id="transferForm">
                {% csrf_token %}
                {{ form.as_p }}
                <div class="d-flex justify-content-between mt-4">
                    <a href="{% url 'home' %}" class="btn btn-secondary">Volver</a>
                    <button type="submit" class="btn btn-primary">Transferir</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Columna de la Lista de Contactos -->
    <div class="col-lg-6 mb-4">
        <div class="card card-custom p-4 h-100">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h3>Mis Contactos</h3>
                <a href="{% url 'add_contact' %}" class="btn btn-success">✚ Nuevo Contacto</a>
            </div>
            <div class="list-group">
                {% for contact in contacts %}
                    <div class="list-group-item list-group-item-action">
                        <div class="d-flex w-100 justify-content-between">
                            <h5 class="mb-1">{{ contact.name }}</h5>
                            <small>{{ contact.get_bank_display }}</small>
                        </div>
                        <p class="mb-1 text-muted">{{ contact.account_number }}</p>
                        <small>{{ contact.email }}</small>
                        <hr class="my-2">
                        <div class="text-end">
                            <button class="btn btn-sm btn-info text-white" onclick="useContact('{{ contact.account_number }}', '{{ contact.account_type }}', '{{ contact.bank }}', '{{ contact.email }}')">Usar</button>
                            <a href="{% url 'edit_contact' contact.id %}" class="btn btn-sm btn-warning">Editar</a>
                            <form method="post" action="{% url 'delete_contact' contact.id %}" class="d-inline" onsubmit="return confirm('¿Estás seguro de que quieres eliminar a {{ contact.name }}?');">
                                {% csrf_token %}
                                <button type="submit" class="btn btn-sm btn-danger">Eliminar</button>
                            </form>
                        </div>
                    </div>
                {% empty %}
                    <p class="text-center text-muted mt-3">No tienes contactos guardados.</p>
                {% endfor %}
            </div>
        </div>
    </div>
</div>

<script>
function useContact(accountNumber, accountType, bank, email) {
    document.getElementById('id_account_number').value = accountNumber;
    document.getElementById('id_account_type').value = accountType;
    document.getElementById('id_bank').value = bank;
    document.getElementById('id_email').value = email;
    document.getElementById('transferForm').scrollIntoView({ behavior: 'smooth', block: 'center' });
}
</script>
{% endblock %}""",

    "wallet/templates/wallet/pay_service.html": """{% extends 'wallet/base.html' %}
{% block content %}
<div class="card card-custom p-4 mx-auto" style="max-width: 600px;">
    <h3 class="mb-3">Pago de Servicios</h3>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <div class="d-flex justify-content-between mt-4">
            <a href="{% url 'home' %}" class="btn btn-secondary">Volver</a>
            <button type="submit" class="btn btn-primary">Pagar Cuenta</button>
        </div>
    </form>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const paymentMethodSelect = document.getElementById('id_payment_method');
    const installmentsInput = document.getElementById('id_installments');
    
    // El form.as_p de Django envuelve los campos en etiquetas <p>. Buscamos la etiqueta padre para ocultarla/mostrarla.
    const installmentsWrapper = installmentsInput.closest('p'); 

    function toggleInstallments() {
        if (paymentMethodSelect.value === 'CREDIT_CARD') {
            // Habilitar cuotas para Tarjeta de Crédito
            if (installmentsWrapper) installmentsWrapper.style.display = 'block';
            installmentsInput.disabled = false;
        } else {
            // Bloquear cuotas para Cuenta Corriente
            if (installmentsWrapper) installmentsWrapper.style.display = 'none';
            installmentsInput.disabled = true;
        }
    }

    // Ejecutar la función al cargar la página para establecer el estado inicial correcto.
    toggleInstallments();

    // Añadir un detector de eventos para cuando el usuario cambie el método de pago.
    paymentMethodSelect.addEventListener('change', toggleInstallments);
});
</script>
{% endblock %}""",

    "wallet/templates/wallet/pay_card.html": """{% extends 'wallet/base.html' %}
{% block content %}
<div class="card card-custom p-4 mx-auto" style="max-width: 600px;">
    <h3 class="mb-3">Pagar Tarjeta de Crédito</h3>
    <div class="alert alert-warning">
        <strong>Deuda Nacional:</strong> ${{ card.national_balance }} CLP<br>
        <strong>Deuda Internacional:</strong> ${{ card.international_balance }} USD
    </div>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <div class="d-flex justify-content-between mt-4">
            <a href="{% url 'card_detail' %}" class="btn btn-secondary">Volver</a>
            <button type="submit" class="btn btn-success">Pagar Deuda</button>
        </div>
    </form>
</div>
{% endblock %}""",

    "wallet/templates/wallet/card_detail.html": """{% extends 'wallet/base.html' %}
{% block content %}
<style>
    .credit-card-visual {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        border-radius: 15px;
        color: white;
        padding: 20px;
        height: 220px;
        position: relative;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        margin-bottom: 20px;
    }
    .card-chip {
        width: 50px;
        height: 35px;
        background: #ffd700;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    .card-number-text {
        font-family: 'Courier New', Courier, monospace;
        font-size: 1.5rem;
        letter-spacing: 2px;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px black;
    }
</style>

<div class="row">
    <div class="col-md-6 mx-auto">
        <div class="card card-custom p-4 mb-4">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h3>Mi Tarjeta</h3>
                <img src="https://www.freepnglogos.com/uploads/visa-logo-png-20.png" alt="Visa" height="25">
            </div>
            {% if show_details %}
                <!-- Tarjeta Visual Desbloqueada -->
                <div class="credit-card-visual">
                    <div class="d-flex justify-content-between">
                        <div class="card-chip"></div>
                        <img src="https://www.freepnglogos.com/uploads/visa-logo-white-png-11.png" alt="Visa" height="25">
                    </div>
                    <div class="text-center" style="margin-bottom: 20px;">
                        <div class="d-inline-flex align-items-center">
                            <span id="cardNumber" class="card-number-text" style="margin-bottom: 0;">{{ card.number }}</span>
                            <button id="copyBtn" class="btn btn-sm p-1 ms-2" title="Copiar número" style="background: none; border: none; color: white;">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clipboard" viewBox="0 0 16 16"><path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"/><path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z"/></svg>
                            </button>
                        </div>
                    </div>
                    <div class="d-flex justify-content-between mt-4">
                        <div>
                            <small style="font-size: 0.7rem;">TITULAR</small><br>
                            {{ user.username|upper }}
                        </div>
                        <div class="text-end">
                            <small style="font-size: 0.7rem;">VENCE / CVV</small><br>
                            {{ card.expiry }} / {{ card.cvv }}
                        </div>
                    </div>
                </div>

            {% else %}
                <!-- Tarjeta Visual Bloqueada -->
                <div class="credit-card-visual" style="filter: grayscale(80%);">
                    <div class="d-flex justify-content-between">
                        <div class="card-chip" style="background: #ccc;"></div>
                        <img src="https://www.freepnglogos.com/uploads/visa-logo-white-png-11.png" alt="Visa" height="25">
                    </div>
                    <div class="card-number-text text-center">**** **** **** {{ card.number|slice:"-4:" }}</div>
                    <div class="d-flex justify-content-between mt-4">
                        <div>
                            <small style="font-size: 0.7rem;">TITULAR</small><br>
                            {{ user.username|upper }}
                        </div>
                        <div class="text-end">
                            <small style="font-size: 0.7rem;">VENCE</small><br>
                            **/**
                        </div>
                    </div>
                </div>
                
                <form method="post" class="mt-3">
                    {% csrf_token %}
                    <div class="input-group">
                        {{ form.pin }}
                        <button class="btn btn-warning" type="submit">👁️ Ver Datos</button>
                    </div>
                    <small class="text-muted">PIN por defecto: 1234</small>
                </form>
            {% endif %}
            <hr>
            <div class="row">
                <div class="col-6">
                    <h5>Nacional (CLP)</h5>
                    <p>Utilizado: ${{ card.national_balance }}</p>
                    <p>Disponible: ${{ card.national_available }}</p>
                </div>
                <div class="col-6 border-start">
                    <h5>Internacional (USD)</h5>
                    <p>Utilizado: ${{ card.international_balance }}</p>
                    <p>Disponible: ${{ card.international_available }}</p>
                </div>
            </div>
            <div class="d-grid gap-2 mt-4">
                <a href="{% url 'pay_card' %}" class="btn btn-success">Pagar Tarjeta</a>
                <div class="d-flex gap-2">
                    <a href="{% url 'movements' %}" class="btn btn-outline-primary flex-grow-1">Movimientos</a>
                    <button class="btn btn-outline-secondary flex-grow-1">Configuración</button>
                </div>
            </div>
        </div>
        <div class="text-center">
            <a href="{% url 'home' %}" class="btn btn-secondary">Volver al Inicio</a>
        </div>
    </div>
</div>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const copyBtn = document.getElementById('copyBtn');
        if (copyBtn) {
            copyBtn.addEventListener('click', function() {
                const cardNumber = document.getElementById('cardNumber').innerText;
                navigator.clipboard.writeText(cardNumber.replace(/\s/g, '')).then(function() {
                    const originalTitle = copyBtn.title;
                    copyBtn.title = '¡Copiado!';
                    setTimeout(() => {
                        copyBtn.title = originalTitle;
                    }, 2000);
                }, function(err) {
                    console.error('No se pudo copiar el texto: ', err);
                });
            });
        }
    });
</script>
{% endblock %}""",

    "wallet/templates/wallet/movements.html": """{% extends 'wallet/base.html' %}
{% block content %}
<div class="card card-custom p-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h3>Historial de Movimientos</h3>
        <a href="{% url 'home' %}" class="btn btn-secondary">Volver</a>
    </div>
    <div class="table-responsive">
        <table class="table table-hover">
            <thead class="table-light">
                <tr>
                    <th>Fecha</th>
                    <th>Tipo</th>
                    <th>Descripción</th>
                    <th class="text-end">Monto</th>
                </tr>
            </thead>
            <tbody>
                {% for t in transactions %}
                <tr>
                    <td>{{ t.date|date:"d/m/Y H:i" }}</td>
                    <td>
                        {% if t.transaction_type == 'DEPOSIT' %}
                            <span class="badge bg-success">Depósito</span>
                        {% elif t.transaction_type == 'TRANSFER' %}
                            <span class="badge bg-warning text-dark">Transferencia</span>
                        {% else %}
                            <span class="badge bg-info text-dark">Pago</span>
                        {% endif %}
                    </td>
                    <td>{{ t.description }}</td>
                    <td class="text-end fw-bold">${{ t.amount }}</td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="4" class="text-center">No hay movimientos registrados.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}""",

    "wallet/templates/wallet/credit_line.html": """{% extends 'wallet/base.html' %}
{% block content %}
<div class="card card-custom p-4 mx-auto" style="max-width: 600px;">
    <h3 class="mb-3">Estado Línea de Crédito</h3>
    
    <div class="row text-center mb-4">
        <div class="col-4">
            <h5 class="text-muted">Cupo Total</h5>
            <p class="fs-5">${{ account.credit_line_limit }}</p>
        </div>
        <div class="col-4 border-start border-end">
            <h5 class="text-danger">Utilizado</h5>
            <p class="fs-5 fw-bold">${{ account.credit_line_usage }}</p>
        </div>
        <div class="col-4">
            <h5 class="text-success">Disponible</h5>
            <p class="fs-5 fw-bold">${{ account.credit_line_available }}</p>
        </div>
    </div>

    <div class="alert alert-secondary">
        <small>ℹ️ La línea de crédito se utiliza automáticamente cuando realizas transferencias o retiros sin saldo suficiente en tu Cuenta Corriente.</small>
    </div>

    {% if account.credit_line_usage > 0 %}
        <div class="alert alert-warning">
            Tienes una deuda activa. Cualquier depósito que realices se usará primero para pagar esta deuda.
        </div>
        <div class="d-grid gap-2">
            <a href="{% url 'deposit' %}" class="btn btn-success">Pagar Deuda (Depositar)</a>
        </div>
    {% else %}
        <div class="alert alert-success">
            ¡Excelente! No tienes deuda en tu línea de crédito.
        </div>
    {% endif %}

    <div class="text-center mt-3">
        <a href="{% url 'home' %}" class="btn btn-link">Volver al Inicio</a>
    </div>
</div>
{% endblock %}"""
}

# Escribir archivos
for rel_path, content in files.items():
    file_path = base_dir / rel_path
    # Crear carpetas si no existen
    file_path.parent.mkdir(parents=True, exist_ok=True)
    # Escribir archivo con codificación UTF-8 limpia (sin BOM)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Reparado: {rel_path}")

print("\n🎉 ¡Listo! Todos los archivos HTML han sido reparados.")
print("👉 Ahora ejecuta: python manage.py runserver")
