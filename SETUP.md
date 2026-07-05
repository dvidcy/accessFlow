# AccessFlow — Guía de Instalación y Ejecución

Sistema de asistencia escolar de secundaria con notificaciones por email a tutores.

---

## Requisitos previos

Asegúrate de tener instalado lo siguiente antes de comenzar:

| Herramienta | Versión mínima | Descarga |
|---|---|---|
| Python | 3.9+ | https://www.python.org/downloads/ |
| XAMPP | Cualquier versión reciente | https://www.apachefriends.org/ |
| Git | Cualquier versión | https://git-scm.com/ |

> **Nota:** En macOS Python generalmente ya viene instalado. Verifica con `python3 --version` en la terminal.

---

## 1. Clonar el repositorio

```bash
git clone <URL-del-repositorio>
cd accessFlow
```

---

## 2. Levantar MySQL con XAMPP

1. Abre el panel de control de XAMPP
2. Haz clic en **Start** junto a **MySQL** (Apache es opcional)
3. Verifica que MySQL esté corriendo (indicador verde)

---

## 3. Crear la base de datos

1. Abre tu navegador y entra a: `http://localhost/phpmyadmin`
2. En el panel izquierdo haz clic en **Nueva**
3. Escribe el nombre: `accessflow_db`
4. Selecciona cotejamiento: `utf8mb4_general_ci`
5. Haz clic en **Crear**

> La base de datos debe llamarse exactamente `accessflow_db`.

---

## 4. Crear el entorno virtual

En la raíz del proyecto ejecuta:

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

Sabrás que el entorno está activo cuando veas `(venv)` al inicio de tu línea de comandos.

---

## 5. Instalar dependencias

Con el entorno virtual activo:

```bash
pip install -r requirements.txt
```

Esto instalará: `customtkinter`, `sqlalchemy`, `pymysql`, `bcrypt`, `yagmail`, `python-dotenv` y sus dependencias.

---

## 6. Configurar el archivo `.env`

El archivo `.env` contiene las credenciales del sistema. Ya existe en el proyecto con valores de ejemplo. Ábrelo y edítalo:

```
# Base de datos MySQL (XAMPP)
DB_HOST=localhost
DB_PORT=3306
DB_NAME=accessflow_db
DB_USER=root
DB_PASSWORD=          ← dejar vacío si XAMPP no tiene contraseña (por defecto)

# SMTP Email (Gmail)
SMTP_EMAIL=tu_correo@gmail.com
SMTP_PASSWORD=tu_app_password_aqui
```

### Configurar email (Gmail) — opcional por ahora

Para que las notificaciones por email funcionen necesitas un **App Password** de Google:

1. Ve a tu cuenta de Google → **Seguridad**
2. Activa la **Verificación en dos pasos** (requerido)
3. Busca **Contraseñas de aplicación**
4. Genera una contraseña para "Correo" en "Otro dispositivo"
5. Copia esa contraseña de 16 caracteres y pégala en `SMTP_PASSWORD`

> Si no configuras el email, la app funciona con normalidad pero no enviará notificaciones.

---

## 7. Crear tablas e insertar datos de prueba

Ejecuta el script de seed **una sola vez**:

```bash
python db/seed.py
```

Esto creará automáticamente todas las tablas en MySQL e insertará:

| Dato | Detalle |
|---|---|
| 1 Administrador | `admin@accessflow.com` / `admin123` |
| 2 Grupos | 1A matutino, 2B vespertino |
| 5 Alumnos | Distribuidos entre los grupos |
| 3 Tutores | Vinculados a los alumnos |

> **Importante:** Solo ejecutar una vez. Si se ejecuta de nuevo con datos existentes, el script lo detecta y no hace nada.

---

## 8. Ejecutar la aplicación

```bash
python main.py
```

Se abrirá la ventana de login. Usa las credenciales del administrador de prueba:

```
Correo:     admin@accessflow.com
Contraseña: admin123
```

---

## Estructura del proyecto

```
accessFlow/
├── .env                  # Credenciales (NO subir a git)
├── .gitignore
├── main.py               # Punto de entrada
├── config.py             # Carga variables del .env
├── requirements.txt      # Dependencias Python
├── PLAN.md               # Plan de desarrollo con progreso
├── SETUP.md              # Este archivo
├── db/
│   ├── database.py       # Conexión SQLAlchemy
│   ├── models.py         # Modelos ORM (tablas)
│   └── seed.py           # Datos de prueba
├── services/
│   ├── auth.py           # Login y contraseñas
│   ├── attendance.py     # Lógica de asistencia
│   ├── email_service.py  # Envío de emails
│   └── messaging.py      # Mensajes a tutores
├── ui/
│   ├── app.py            # Ventana principal
│   ├── login.py          # Pantalla de login
│   ├── dashboard.py      # Panel con menú lateral
│   ├── attendance.py     # Registro de asistencia
│   ├── students.py       # CRUD alumnos
│   ├── groups.py         # CRUD grupos
│   ├── tutors.py         # CRUD tutores
│   └── messaging.py      # Mensajes individuales y grupales
└── assets/               # Recursos gráficos (logo, íconos)
```

---

## Resumen de comandos

```bash
# 1. Activar entorno virtual
source venv/bin/activate          # macOS / Linux
venv\Scripts\activate             # Windows

# 2. Instalar dependencias (solo la primera vez)
pip install -r requirements.txt

# 3. Crear tablas y datos de prueba (solo la primera vez)
python db/seed.py

# 4. Correr la aplicación
python main.py
```

---

## Solución de problemas comunes

### "No module named 'pymysql'"
El entorno virtual no está activo. Ejecuta `source venv/bin/activate` primero.

### "Access denied for user 'root'"
XAMPP no está corriendo o la contraseña de MySQL no coincide. Revisa que MySQL esté activo en el panel de XAMPP y que `DB_PASSWORD` en `.env` sea correcto (vacío por defecto en XAMPP).

### "Can't connect to MySQL server"
MySQL no está iniciado. Abre XAMPP y haz clic en **Start** junto a **MySQL**.

### "Unknown database 'accessflow_db'"
La base de datos no fue creada. Sigue el paso 3 de esta guía.

### La ventana no abre / error de display (Linux)
Instala las dependencias gráficas de Tkinter:
```bash
sudo apt-get install python3-tk
```

### El email no llega
- Verifica que `SMTP_EMAIL` y `SMTP_PASSWORD` en `.env` sean correctos
- Asegúrate de usar un **App Password** de Google, no tu contraseña normal
- Revisa la carpeta de spam del tutor destinatario
