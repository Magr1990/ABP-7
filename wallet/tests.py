from django.test import TestCase
from django.contrib.auth.models import User
from .models import Account
from decimal import Decimal
from django.core.exceptions import ValidationError

class AccountModelTest(TestCase):

    def setUp(self):
        """Crea un usuario y su cuenta asociada para cada prueba."""
        self.user = User.objects.create_user(username='testuser', password='password123')
        # La cuenta se crea automáticamente por la señal, pero la obtenemos aquí.
        self.account = self.user.account
        self.account.balance = Decimal('100000')
        self.account.credit_line_limit = Decimal('50000')
        self.account.credit_line_usage = Decimal('0')
        self.account.save()

    def test_withdraw_sufficient_funds(self):
        """Prueba retirar fondos cuando hay saldo suficiente en la cuenta corriente."""
        success, warning = self.account.withdraw_funds(Decimal('50000'))
        self.account.refresh_from_db()

        self.assertTrue(success)
        self.assertIsNone(warning) # No debería haber advertencia
        self.assertEqual(self.account.balance, Decimal('50000'))
        self.assertEqual(self.account.credit_line_usage, Decimal('0'))

    def test_withdraw_using_credit_line(self):
        """Prueba retirar fondos usando la línea de crédito cuando el saldo es insuficiente."""
        # Retirar 120,000 (100,000 de saldo + 20,000 de línea de crédito)
        success, warning = self.account.withdraw_funds(Decimal('120000'))
        self.account.refresh_from_db()
        
        self.assertTrue(success)
        self.assertIsNotNone(warning) # Debería haber una advertencia
        self.assertEqual(self.account.balance, Decimal('0'))
        self.assertEqual(self.account.credit_line_usage, Decimal('20000'))

    def test_withdraw_insufficient_funds_total(self):
        """Prueba retirar fondos cuando ni el saldo ni la línea de crédito son suficientes."""
        # Saldo total disponible = 100,000 (balance) + 50,000 (línea) = 150,000
        # Intentar retirar 160,000
        with self.assertRaises(ValidationError):
            self.account.withdraw_funds(Decimal('160000'))

    def test_deposit_pays_credit_line_first(self):
        """Prueba que un depósito pague primero la deuda de la línea de crédito."""
        self.account.credit_line_usage = Decimal('30000')
        self.account.save()

        self.account.deposit(Decimal('50000'))
        self.account.refresh_from_db()

        self.assertEqual(self.account.credit_line_usage, Decimal('0'))
        self.assertEqual(self.account.balance, Decimal('120000')) # 100,000 iniciales + 20,000 sobrantes