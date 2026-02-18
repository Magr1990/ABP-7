import os

# Verificar que estamos en la carpeta correcta
if not os.path.exists('manage.py'):
    print("❌ ERROR: Debes ejecutar este script en la misma carpeta que manage.py")
    print("Ejecuta: cd ProyectoWallet\\alke_wallet")
    exit()

print("🎨 Aplicando diseño final de tarjeta y coordenadas...")

html_code = """{% extends 'wallet/base.html' %}
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
                <img src="https://upload.wikimedia.org/wikipedia/commons/5/5e/Visa_Inc._logo.svg" alt="Visa" height="30">
            </div>
            {% if show_details %}
                <!-- Tarjeta Visual Desbloqueada -->
                <div class="credit-card-visual">
                    <div class="d-flex justify-content-between">
                        <div class="card-chip"></div>
                        <span class="fs-4 fw-bold fst-italic">VISA</span>
                    </div>
                    <div class="card-number-text text-center">{{ card.number }}</div>
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

                <div class="card border-primary mb-3">
                    <div class="card-header bg-primary text-white text-center">Tarjeta de Coordenadas</div>
                    <table class="table table-bordered table-sm text-center mb-0">
                        <thead class="table-light">
                            <tr><th></th><th>1</th><th>2</th><th>3</th></tr>
                        </thead>
                        <tbody>
                            {% for row, values in card.get_coordinates.items %}
                            <tr>
                                <th class="table-light">{{ row }}</th>
                                {% for val in values %}
                                <td>{{ val }}</td>
                                {% endfor %}
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <!-- Tarjeta Visual Bloqueada -->
                <div class="credit-card-visual" style="filter: grayscale(80%);">
                    <div class="d-flex justify-content-between">
                        <div class="card-chip" style="background: #ccc;"></div>
                        <span class="fs-4 fw-bold fst-italic">VISA</span>
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
{% endblock %}"""

# Asegurar que el directorio existe
os.makedirs('wallet/templates/wallet', exist_ok=True)

with open('wallet/templates/wallet/card_detail.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("✅ Diseño actualizado correctamente en wallet/templates/wallet/card_detail.html")
print("👉 Ahora ejecuta: python manage.py runserver")