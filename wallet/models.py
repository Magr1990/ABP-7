from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
import random
import string

def generate_account_number():
    """Genera un número de cuenta de 9 dígitos."""
    return ''.join(random.choices(string.digits, k=9))

BANK_CHOICES = [
    ('BANCO_ESTADO', 'Banco Estado'),
    ('BANCO_CHILE', 'Banco de Chile'),
    ('SANTANDER', 'Banco Santander'),
    ('BCI', 'BCI'),
    ('SCOTIABANK', 'Scotiabank'),
    ('ITAU', 'Itaú'),
    ('FALABELLA', 'Banco Falabella'),
    ('RIPLEY', 'Banco Ripley'),
    ('SECURITY', 'Banco Security'),
    ('CONSORCIO', 'Banco Consorcio'),
]

ACCOUNT_TYPE_CHOICES = [
    ('CORRIENTE', 'Cuenta Corriente'),
    ('VISTA', 'Cuenta Vista / RUT'),
    ('AHORRO', 'Cuenta de Ahorro'),
]

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    balance = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Saldo Cuenta Corriente")
    
    # Línea de Crédito
    credit_line_limit = models.DecimalField(max_digits=12, decimal_places=0, default=1000000, verbose_name="Cupo Línea Crédito")
    credit_line_usage = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Uso Línea Crédito")
    account_number = models.CharField(max_length=20, unique=True, default=generate_account_number, verbose_name="Número de Cuenta")

    def __str__(self):
        return f"Cuenta {self.account_number} - Saldo: ${self.balance}"

    @property
    def credit_line_available(self):
        return self.credit_line_limit - self.credit_line_usage

    def deposit(self, amount):
        """
        Lógica: Si se deposita se debe pagar primero la deuda de la linea de crédito 
        y lo restante ira a la cuenta principal.
        """
        amount = Decimal(amount)
        if self.credit_line_usage > 0:
            if amount >= self.credit_line_usage:
                remainder = amount - self.credit_line_usage
                self.credit_line_usage = 0
                self.balance += remainder
            else:
                self.credit_line_usage -= amount
        else:
            self.balance += amount
        self.save()

    def withdraw_funds(self, amount):
        """
        Lógica: Descuenta de cuenta corriente. Si no hay saldo, usa línea de crédito.
        Retorna (bool, str): (Exito, Mensaje de advertencia si aplica)
        """
        amount = Decimal(amount)
        warning_msg = None

        if self.balance >= amount:
            self.balance -= amount
        else:
            # Lógica de sobregiro
            deficit = amount - self.balance
            if self.credit_line_available >= deficit:
                self.balance = 0
                self.credit_line_usage += deficit
                warning_msg = "Alerta: Se ha utilizado saldo de la Línea de Crédito para completar la operación."
            else:
                raise ValidationError("Saldo insuficiente (incluso con línea de crédito).")
        
        self.save()
        return True, warning_msg

class CreditCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='credit_card')
    number = models.CharField(max_length=16, default="4000123456789010")
    cvv = models.CharField(max_length=3, default="123")
    expiry = models.CharField(max_length=5, default="12/28")
    issuer_image = models.CharField(max_length=100, default="visa_logo.png") # Ruta estática simulada
    
    # Cupos independientes
    national_limit = models.DecimalField(max_digits=12, decimal_places=0, default=500000)
    national_balance = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Deuda Nacional")
    
    international_limit = models.DecimalField(max_digits=12, decimal_places=2, default=1000.00) # En USD
    international_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Deuda Internacional USD")

    @property
    def national_available(self):
        return self.national_limit - self.national_balance

    @property
    def international_available(self):
        return self.international_limit - self.international_balance

class Service(models.Model):
    NAME_CHOICES = [
        ('ENEL', 'Enel (Luz)'),
        ('AGUAS_ANDINAS', 'Aguas Andinas (Agua)'),
        ('METROGAS', 'Metrogas (Gas)'),
        ('VTR', 'VTR (Internet/TV/Teléfono)'),
        ('MOVISTAR', 'Movistar (Internet/TV/Teléfono)'),
        ('CLARO', 'Claro (Internet/TV/Teléfono)'),
        ('MUNDO', 'Mundo (Internet/TV/Teléfono)'),
        ('AUTOPISTA_CENTRAL', 'Autopista Central (TAG)'),
        ('COSTANERA_NORTE', 'Costanera Norte (TAG)'),
    ]
    name = models.CharField(max_length=50, choices=NAME_CHOICES)
    logo = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.get_name_display()

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Depósito'),
        ('TRANSFER', 'Transferencia'),
        ('PAY_SERVICE', 'Pago Servicio'),
        ('PAY_CARD', 'Pago Tarjeta'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.transaction_type} - ${self.amount}"

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100, verbose_name="Nombre")
    account_number = models.CharField(max_length=20, verbose_name="Número de Cuenta")
    email = models.EmailField(verbose_name="Correo Destinatario")
    bank = models.CharField(max_length=50, choices=BANK_CHOICES, default='BANCO_ESTADO', verbose_name="Banco")
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, default='VISTA', verbose_name="Tipo de Cuenta")

    def __str__(self):
        return self.name

# Señal para crear cuenta y tarjeta automáticamente al crear usuario
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_products(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
        CreditCard.objects.create(user=instance)