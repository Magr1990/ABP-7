from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.conf import settings
from .models import Account, CreditCard, Transaction, Service, Contact
from .forms import DepositForm, TransferForm, PayServiceForm, PayCardForm, PinForm, ContactForm, CustomUserCreationForm
from django.core.exceptions import ValidationError

@login_required
def home(request):
    account = request.user.account
    card = request.user.credit_card
    
    context = {
        'account': account,
        'card': card,
        'exchange_rate': settings.EXCHANGE_RATE
    }
    return render(request, 'wallet/home.html', context)

@login_required
def deposit(request):
    account = request.user.account
    card = request.user.credit_card
    
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            origin = form.cleaned_data['origin']
            
            # Lógica: Pagar deuda línea crédito primero, el resto a la cuenta
            account.deposit(amount)
            
            Transaction.objects.create(
                user=request.user,
                amount=amount,
                transaction_type='DEPOSIT',
                description=f"Depósito desde {origin}"
            )
            messages.success(request, "Depósito realizado con éxito.")
            return redirect('home')
    else:
        form = DepositForm()

    return render(request, 'wallet/deposit.html', {
        'form': form, 
        'account': account,
        'card': card
    })

@login_required
def transfer(request):
    account = request.user.account
    contacts = request.user.contacts.all()
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            dest_email = form.cleaned_data['email']
            # Nota: bank y account_type están en cleaned_data pero no los usamos 
            # para la lógica de descuento, solo para validar el formulario.
            
            try:
                success, warning = account.withdraw_funds(amount)
                if warning:
                    messages.warning(request, warning)
                
                Transaction.objects.create(
                    user=request.user,
                    amount=amount,
                    transaction_type='TRANSFER',
                    description=f"Transferencia a {dest_email}"
                )
                messages.success(request, "Transferencia realizada.")
                return redirect('home')
            except ValidationError as e:
                messages.error(request, e.message)
    else:
        form = TransferForm()
    
    return render(request, 'wallet/transfer.html', {'form': form, 'contacts': contacts})

@login_required
def pay_service(request):
    account = request.user.account
    card = request.user.credit_card
    
    if request.method == 'POST':
        form = PayServiceForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            method = form.cleaned_data['payment_method']
            service = form.cleaned_data['service']
            service_type = form.cleaned_data['service_type']
            
            try:
                if method == 'ACCOUNT':
                    success, warning = account.withdraw_funds(amount)
                    if warning:
                        messages.warning(request, warning)
                else: # CREDIT_CARD
                    # Lógica tarjeta de crédito: aumenta la deuda nacional
                    if card.national_available >= amount:
                        card.national_balance += amount
                        card.save()
                    else:
                        messages.error(request, "Cupo insuficiente en tarjeta de crédito.")
                        return redirect('pay_service')

                Transaction.objects.create(
                    user=request.user,
                    amount=amount,
                    transaction_type='PAY_SERVICE',
                    description=f"Pago servicio {service} ({service_type})"
                )
                messages.success(request, f"Pago a {service} realizado.")
                return redirect('home')
            except ValidationError as e:
                messages.error(request, e.message)
    else:
        form = PayServiceForm()
        
    return render(request, 'wallet/pay_service.html', {'form': form})

@login_required
def pay_card(request):
    account = request.user.account
    card = request.user.credit_card
    
    if request.method == 'POST':
        form = PayCardForm(request.POST)
        if form.is_valid():
            payment_type = form.cleaned_data['payment_type']
            amount_to_pay = form.cleaned_data['amount'] # Puede ser USD o CLP
            
            # Calcular cuánto descontar de la cuenta corriente en CLP
            amount_clp_deduct = amount_to_pay
            
            if payment_type == 'INTERNATIONAL':
                # Conversión USD a CLP
                amount_clp_deduct = amount_to_pay * getattr(settings, 'EXCHANGE_RATE', 950)
            
            try:
                # Intentar descontar de la cuenta (o línea de crédito)
                success, warning = account.withdraw_funds(amount_clp_deduct)
                if warning:
                    messages.warning(request, warning)
                
                # Si pasó, actualizamos la deuda de la tarjeta
                if payment_type == 'NATIONAL':
                    card.national_balance -= amount_to_pay
                else:
                    card.international_balance -= amount_to_pay
                
                card.save()
                
                Transaction.objects.create(
                    user=request.user,
                    amount=amount_clp_deduct,
                    transaction_type='PAY_CARD',
                    description=f"Pago Tarjeta ({payment_type})"
                )
                messages.success(request, "Pago de tarjeta realizado.")
                return redirect('home')
                
            except ValidationError as e:
                messages.error(request, e.message)
    else:
        form = PayCardForm()

    return render(request, 'wallet/pay_card.html', {'form': form, 'card': card})

@login_required
def card_detail(request):
    card = request.user.credit_card
    show_details = False
    
    if request.method == 'POST':
        form = PinForm(request.POST)
        # La validación del PIN (1234) se hace en el form
        if form.is_valid():
            show_details = True
    else:
        form = PinForm()
        
    return render(request, 'wallet/card_detail.html', {
        'card': card, 
        'form': form, 
        'show_details': show_details
    })

@login_required
def movements(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'wallet/movements.html', {'transactions': transactions})

@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.success(request, "Contacto agregado exitosamente.")
            return redirect('transfer')
    else:
        form = ContactForm()
    return render(request, 'wallet/add_contact.html', {'form': form})

@login_required
def edit_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, user=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, "Contacto actualizado exitosamente.")
            return redirect('transfer')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'wallet/edit_contact.html', {'form': form, 'contact': contact})

@login_required
def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, user=request.user)
    if request.method == 'POST':
        contact_name = contact.name
        contact.delete()
        messages.success(request, f"Contacto '{contact_name}' eliminado.")
    return redirect('transfer')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def credit_line(request):
    return render(request, 'wallet/credit_line.html', {'account': request.user.account})