from django import forms
from .models import Service, Contact, BANK_CHOICES, ACCOUNT_TYPE_CHOICES
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DepositForm(forms.Form):
    ORIGIN_CHOICES = [
        ('CAJERO', 'Cajero Automático'),
        ('SUCURSAL', 'Sucursal'),
        ('TRANSFERENCIA', 'Transferencia de otro banco'),
    ]
    amount = forms.IntegerField(label="Monto a depositar", min_value=1)
    origin = forms.ChoiceField(choices=ORIGIN_CHOICES, label="Origen de fondos")

class TransferForm(forms.Form):
    account_number = forms.CharField(label="Número de Cuenta Destino")
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE_CHOICES, label="Tipo de Cuenta")
    bank = forms.ChoiceField(choices=BANK_CHOICES, label="Banco Destino")
    email = forms.EmailField(label="Correo Destinatario")
    amount = forms.IntegerField(label="Monto a transferir", min_value=1)

class PayServiceForm(forms.Form):
    SERVICE_TYPE_CHOICES = [
        ('LUZ', 'Luz'),
        ('AGUA', 'Agua'),
        ('INTERNET', 'Internet Hogar'),
        ('MOVIL', 'Telefonía Móvil'),
        ('GAS', 'Gas'),
        ('AUTOPISTA', 'Autopista / TAG'),
    ]
    PAYMENT_METHODS = [
        ('ACCOUNT', 'Cuenta Corriente / Línea Crédito'),
        ('CREDIT_CARD', 'Tarjeta de Crédito (Cuotas)'),
    ]
    service = forms.ModelChoiceField(queryset=Service.objects.all(), label="Empresa")
    service_type = forms.ChoiceField(choices=SERVICE_TYPE_CHOICES, label="Tipo de Servicio")
    client_number = forms.CharField(label="Número de Cliente")
    amount = forms.IntegerField(label="Monto a pagar", min_value=1)
    payment_method = forms.ChoiceField(choices=PAYMENT_METHODS, label="Medio de Pago")
    installments = forms.IntegerField(label="Cuotas (Solo Tarjeta)", min_value=1, max_value=24, required=False, initial=1)

class PayCardForm(forms.Form):
    TYPE_CHOICES = [
        ('NATIONAL', 'Deuda Nacional (CLP)'),
        ('INTERNATIONAL', 'Deuda Internacional (USD)'),
    ]
    payment_type = forms.ChoiceField(choices=TYPE_CHOICES, label="Tipo de Deuda a Pagar")
    amount = forms.DecimalField(label="Monto a pagar", min_value=1)

class PinForm(forms.Form):
    pin = forms.CharField(widget=forms.PasswordInput, label="Ingrese PIN (1234)", max_length=4)

    def clean_pin(self):
        pin = self.cleaned_data.get('pin')
        if pin != '1234':
            raise forms.ValidationError("PIN incorrecto.")
        return pin

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'account_number', 'account_type', 'bank', 'email']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo Electrónico")
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']