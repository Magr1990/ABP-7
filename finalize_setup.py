import os
import shutil
from pathlib import Path

BASE_DIR = Path.cwd()
WALLET_DIR = BASE_DIR / 'wallet'

# 1. Mover archivos desordenados a la carpeta de la app 'wallet'
files_to_move = ['models.py', 'forms.py', 'admin.py', 'tests.py']

if not WALLET_DIR.exists():
    print(f"⚠️ Creando carpeta {WALLET_DIR}...")
    WALLET_DIR.mkdir()

print("🔍 Verificando archivos desordenados...")
for filename in files_to_move:
    src = BASE_DIR / filename
    dst = WALLET_DIR / filename
    if src.exists():
        print(f" -> Moviendo {filename} a la carpeta 'wallet'...")
        if dst.exists():
            os.remove(dst) # Sobrescribir si ya existe para asegurar la versión correcta
        shutil.move(str(src), str(dst))

# 2. Crear wallet/urls.py
urls_content = """from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='wallet/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('transfer/', views.transfer, name='transfer'),
    path('add_contact/', views.add_contact, name='add_contact'),
    path('pay_service/', views.pay_service, name='pay_service'),
]
"""
with open(WALLET_DIR / 'urls.py', 'w', encoding='utf-8') as f:
    f.write(urls_content)
print("✅ wallet/urls.py creado.")

# 3. Crear wallet/views.py con la lógica necesaria
views_content = """from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction, Contact
from .forms import TransferForm, PayServiceForm, ContactForm, CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Cuenta creada exitosamente. Por favor inicia sesión.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'wallet/register.html', {'form': form})

@login_required
def home(request):
    try:
        account = request.user.account
    except:
        account = None
    return render(request, 'wallet/home.html', {'account': account})

@login_required
def transfer(request):
    account = request.user.account
    contacts = request.user.contacts.all()
    
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            try:
                success, msg = account.withdraw_funds(amount)
                if success:
                    Transaction.objects.create(
                        user=request.user,
                        amount=amount,
                        transaction_type='TRANSFER',
                        description=f"Transferencia a {form.cleaned_data['email']}"
                    )
                    messages.success(request, f"Transferencia de ${amount} realizada con éxito.")
                    if msg:
                        messages.warning(request, msg)
                    return redirect('home')
            except Exception as e:
                messages.error(request, str(e))
    else:
        form = TransferForm()
    
    return render(request, 'wallet/transfer.html', {'form': form, 'contacts': contacts})

@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.success(request, "Contacto agregado correctamente.")
            return redirect('transfer')
    else:
        form = ContactForm()
    return render(request, 'wallet/add_contact.html', {'form': form})

@login_required
def pay_service(request):
    if request.method == 'POST':
        form = PayServiceForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            payment_method = form.cleaned_data['payment_method']
            
            if payment_method == 'ACCOUNT':
                try:
                    success, msg = request.user.account.withdraw_funds(amount)
                    if success:
                        Transaction.objects.create(
                            user=request.user,
                            amount=amount,
                            transaction_type='PAY_SERVICE',
                            description=f"Pago servicio: {form.cleaned_data['service']}"
                        )
                        messages.success(request, "Pago realizado con éxito.")
                        return redirect('home')
                except Exception as e:
                    messages.error(request, str(e))
            else:
                # Lógica tarjeta de crédito
                messages.success(request, "Pago con tarjeta de crédito registrado.")
                return redirect('home')
    else:
        form = PayServiceForm()
    return render(request, 'wallet/pay_service.html', {'form': form})
"""
with open(WALLET_DIR / 'views.py', 'w', encoding='utf-8') as f:
    f.write(views_content)
print("✅ wallet/views.py creado.")

print("\\n🚀 ¡Configuración finalizada! Ahora ejecuta los comandos de Django.")