from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('depositar/', views.deposit, name='deposit'),
    path('transferir/', views.transfer, name='transfer'),
    path('servicios/', views.pay_service, name='pay_service'),
    path('pagar-tarjeta/', views.pay_card, name='pay_card'),
    path('tarjeta/', views.card_detail, name='card_detail'),
    path('movimientos/', views.movements, name='movements'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('contactos/nuevo/', views.add_contact, name='add_contact'),
    path('contactos/editar/<int:contact_id>/', views.edit_contact, name='edit_contact'),
    path('contactos/eliminar/<int:contact_id>/', views.delete_contact, name='delete_contact'),
    path('registro/', views.register, name='register'),
    path('linea-credito/', views.credit_line, name='credit_line'),
    path('recuperar-clave/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('recuperar-clave/listo/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('recuperar-clave/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('recuperar-clave/completado/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]