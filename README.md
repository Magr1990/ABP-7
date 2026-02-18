# 🇨🇱 Alke Wallet Chile

Alke Wallet Chile es una aplicación web desarrollada con Django que simula una billetera digital para el mercado chileno. Permite a los usuarios gestionar sus finanzas, incluyendo una cuenta corriente, línea de crédito y tarjetas de crédito en pesos chilenos (CLP) y dólares (USD).

## ✨ Características Principales

- **Gestión de Cuentas:** Visualización de saldos de cuenta corriente, línea de crédito y tarjetas.
- **Operaciones Bancarias:**
  - **Depósitos:** Con lógica de pago automático de deudas en la línea de crédito.
  - **Transferencias a Terceros:** Descuento desde la cuenta corriente con uso automático de la línea de crédito como sobregiro.
  - **Pago de Servicios:** Permite pagar cuentas de servicios básicos (luz, agua, gas, etc.) usando la cuenta corriente o la tarjeta de crédito (con opción de cuotas).
  - **Pago de Tarjeta de Crédito:** Soporta el pago de deudas nacionales (CLP) e internacionales (USD), con conversión de moneda automática.
- **Gestión de Contactos:** Funcionalidad CRUD completa (Crear, Leer, Actualizar, Eliminar) para una agenda de contactos de transferencia.
- **Seguridad de Tarjeta:** Visualización de datos sensibles de la tarjeta de crédito (número, CVV, fecha) protegida por un PIN.
- **Historial de Movimientos:** Registro detallado de todas las transacciones realizadas por el usuario.

## 🛠️ Tecnologías Utilizadas

- **Backend:** Python, Django
- **Base de Datos:** SQLite (por defecto en Django)
- **Frontend:** HTML, CSS, Bootstrap 5
- **JavaScript:** Para funcionalidades interactivas en el frontend.

## 🚀 Instalación y Puesta en Marcha

Sigue estos pasos para ejecutar el proyecto en tu máquina local.

### Prerrequisitos

- Tener Python 3.x instalado.
- Tener `pip` (el gestor de paquetes de Python) instalado.

### Pasos

1.  **Clona el repositorio (o descarga el ZIP):**
    ```bash
    git clone <URL-del-repositorio>
    cd ABP-7 # O el nombre de la carpeta del proyecto
    ```

2.  **Crea y activa un entorno virtual:**
    Esto aísla las dependencias del proyecto.
    ```bash
    # Crear el entorno
    python -m venv venv

    # Activar en Windows
    .\venv\Scripts\activate

    # Activar en macOS/Linux
    source venv/bin/activate
    ```

3.  **Instala las dependencias:**
    El archivo `requirements.txt` contiene las librerías necesarias.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura la base de datos y crea un superusuario:**
    El proyecto incluye un script para automatizar este proceso.
    ```bash
    python finish_install.py
    ```
    Esto creará la base de datos, aplicará las migraciones y creará un usuario administrador con las credenciales:
    - **Usuario:** `admin`
    - **Contraseña:** `admin`

5.  **Inicia el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```

6.  **¡Listo!** Abre tu navegador y ve a `http://127.0.0.1:8000/` para usar la aplicación. Inicia sesión con el usuario `admin`.