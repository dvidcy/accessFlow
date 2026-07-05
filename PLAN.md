# AccessFlow — Plan de Proyecto

Sistema de asistencia escolar de secundaria con notificaciones por email a tutores.

---

## Stack Tecnológico

| Capa | Tecnología |
|---|---|
| UI Desktop | `CustomTkinter` |
| ORM / BD | `SQLAlchemy` + `PyMySQL` |
| Base de datos | MySQL vía XAMPP |
| Email | `yagmail` / `smtplib` + Gmail SMTP |
| Contraseñas | `bcrypt` |
| Config | `python-dotenv` |

---

## Modelo de Base de Datos

```
Grupo ──< Alumno >──< AlumnoTutor >── Tutor
                         ↓
                     Asistencia

Admin ──< Mensaje >── MensajeDestinatario >── Tutor
```

### Tablas

| Tabla | Campos clave |
|---|---|
| `Grupo` | id, nombre, grado, turno |
| `Alumno` | id, nombre, rfid_uid, grupo_id |
| `Tutor` | id, nombre, email, telefono |
| `AlumnoTutor` | alumno_id, tutor_id, parentesco |
| `Admin` | id, nombre, email, password_hash |
| `Asistencia` | id, alumno_id, fecha_entrada, fecha_salida |
| `Mensaje` | id, admin_id, asunto, cuerpo, tipo, enviado_en |
| `MensajeDestinatario` | mensaje_id, tutor_id |

---

## Estructura del Proyecto

```
accessFlow/
├── .env                        # Credenciales (SMTP, DB) — no subir a git
├── main.py                     # Punto de entrada
├── config.py                   # Carga de variables de entorno
├── db/
│   ├── __init__.py
│   ├── database.py             # Conexión SQLAlchemy
│   └── models.py               # Todos los modelos ORM
├── services/
│   ├── __init__.py
│   ├── auth.py                 # Login, hashing de contraseñas
│   ├── attendance.py           # Lógica de entrada/salida
│   ├── email_service.py        # Envío de correos a tutores
│   └── messaging.py            # Mensajes individuales y grupales
├── ui/
│   ├── __init__.py
│   ├── app.py                  # Ventana principal / navegación
│   ├── login.py                # Pantalla de login
│   ├── dashboard.py            # Panel principal del admin
│   ├── students.py             # CRUD alumnos
│   ├── groups.py               # CRUD grupos
│   ├── tutors.py               # CRUD tutores
│   ├── attendance.py           # Pantalla de registro de asistencia
│   └── messaging.py            # Pantalla de mensajes
└── assets/
    └── logo.png                # (opcional)
```

---

## Fases de Desarrollo

---

### FASE 1 — Configuración e Infraestructura

- [x] **1.1** Crear entorno virtual Python (`venv`)
- [x] **1.2** Instalar dependencias: `customtkinter`, `sqlalchemy`, `pymysql`, `bcrypt`, `yagmail`, `python-dotenv`
- [x] **1.3** Crear archivo `requirements.txt`
- [x] **1.4** Crear archivo `.env` con credenciales de BD y SMTP
- [x] **1.5** Crear `config.py` que lea variables del `.env`
- [ ] **1.6** Crear base de datos `accessflow_db` en MySQL (XAMPP) ← pendiente manual

---

### FASE 2 — Base de Datos y Modelos

- [x] **2.1** Crear `db/database.py` — conexión SQLAlchemy + engine + sesión
- [x] **2.2** Crear `db/models.py` con los modelos:
  - [x] `Grupo`
  - [x] `Alumno`
  - [x] `Tutor`
  - [x] `AlumnoTutor` (tabla intermedia)
  - [x] `Admin`
  - [x] `Asistencia`
  - [x] `Mensaje`
  - [x] `MensajeDestinatario`
- [x] **2.3** Generar tablas con `Base.metadata.create_all()`
- [x] **2.4** Insertar datos de prueba (1 admin, 2 grupos, 5 alumnos, 3 tutores)

---

### FASE 3 — Servicios (Lógica de Negocio)

- [ ] **3.1** `services/auth.py`
  - [ ] Función `login(email, password)` → valida contra BD
  - [ ] Función `hash_password(plain)` y `verify_password(plain, hash)`

- [ ] **3.2** `services/attendance.py`
  - [ ] Función `registrar_asistencia(alumno_id)` → detecta si es entrada o salida
  - [ ] Función `buscar_alumno_por_rfid(rfid_uid)`
  - [ ] Función `buscar_alumno_por_id(id)`
  - [ ] Función `get_asistencias_hoy()`

- [ ] **3.3** `services/email_service.py`
  - [ ] Función `enviar_notificacion_entrada(tutor_email, alumno_nombre, hora)`
  - [ ] Función `enviar_notificacion_salida(tutor_email, alumno_nombre, hora)`
  - [ ] Función `enviar_mensaje_personalizado(tutor_email, asunto, cuerpo)`

- [ ] **3.4** `services/messaging.py`
  - [ ] Función `enviar_mensaje_individual(tutor_id, asunto, cuerpo, admin_id)`
  - [ ] Función `enviar_mensaje_grupal(grupo_id, asunto, cuerpo, admin_id)` → obtiene todos los tutores del grupo y envía
  - [ ] Guardar registro en tablas `Mensaje` y `MensajeDestinatario`

---

### FASE 4 — Interfaz de Usuario

- [ ] **4.1** `ui/app.py` — ventana raíz CustomTkinter, navegación entre pantallas

- [ ] **4.2** `ui/login.py`
  - [ ] Campos email y contraseña
  - [ ] Botón iniciar sesión
  - [ ] Manejo de credenciales incorrectas

- [ ] **4.3** `ui/dashboard.py`
  - [ ] Menú lateral con acceso a módulos
  - [ ] Tarjetas con resumen: alumnos hoy, asistencias registradas

- [ ] **4.4** `ui/attendance.py` — Registro de asistencia
  - [ ] Campo de input activo que recibe ID manual o lectura RFID
  - [ ] Muestra nombre del alumno, grupo, turno al registrar
  - [ ] Muestra si fue entrada o salida
  - [ ] Lista de registros del día en pantalla

- [ ] **4.5** `ui/students.py` — CRUD Alumnos
  - [ ] Tabla con lista de alumnos
  - [ ] Formulario: agregar alumno (nombre, grupo, rfid_uid opcional)
  - [ ] Editar alumno
  - [ ] Eliminar alumno (con confirmación)
  - [ ] Búsqueda/filtro por grupo

- [ ] **4.6** `ui/groups.py` — CRUD Grupos
  - [ ] Tabla con grupos existentes
  - [ ] Formulario: agregar grupo (nombre, grado, turno)
  - [ ] Editar y eliminar grupo

- [ ] **4.7** `ui/tutors.py` — CRUD Tutores
  - [ ] Tabla de tutores
  - [ ] Formulario: agregar tutor (nombre, email, teléfono, parentesco, alumno vinculado)
  - [ ] Un tutor puede vincularse a múltiples alumnos
  - [ ] Editar y eliminar tutor

- [ ] **4.8** `ui/messaging.py` — Mensajería
  - [ ] Selector: individual o grupal
  - [ ] Individual: buscar tutor por nombre o email
  - [ ] Grupal: selector de grupo destino
  - [ ] Campos asunto y cuerpo del mensaje
  - [ ] Botón enviar → llama al servicio y guarda en BD

---

### FASE 5 — Integración y Pruebas

- [ ] **5.1** Conectar UI de login con `services/auth.py`
- [ ] **5.2** Conectar pantalla de asistencia con `services/attendance.py` + `services/email_service.py`
- [ ] **5.3** Conectar CRUD de alumnos con BD
- [ ] **5.4** Conectar CRUD de grupos con BD
- [ ] **5.5** Conectar CRUD de tutores con BD
- [ ] **5.6** Conectar mensajería con `services/messaging.py`
- [ ] **5.7** Probar flujo completo: login → registrar asistencia → email llega al tutor
- [ ] **5.8** Probar envío de mensaje grupal a tutores de un grupo

---

### FASE 6 — Pulido Final

- [ ] **6.1** Manejo de errores visible en UI (BD caída, email fallido, alumno no encontrado)
- [ ] **6.2** Validaciones en formularios (campos vacíos, email con formato correcto)
- [ ] **6.3** Protección de rutas: solo admin autenticado accede al sistema
- [ ] **6.4** Crear script `setup.sql` con estructura de BD para entrega

---

### FASE 7 — Opcional / Post-entrega

- [ ] **7.1** Soporte multi-PC: mover BD a servidor compartido en red local
- [ ] **7.2** Integración real con lector RFID USB
- [ ] **7.3** Agregar notificaciones WhatsApp (Twilio o Baileys)
- [ ] **7.4** Módulo de reportes de asistencia (Excel con `openpyxl`)

---

## Progreso General

| Fase | Estado |
|---|---|
| 1 — Configuración | ✅ Completo |
| 2 — Base de Datos | ✅ Completo |
| 3 — Servicios | ⬜ Pendiente |
| 4 — UI | ⬜ Pendiente |
| 5 — Integración | ⬜ Pendiente |
| 6 — Pulido | ⬜ Pendiente |
| 7 — Opcional | ⬜ Pendiente |

---

> Actualiza este archivo marcando `[x]` en cada tarea completada y cambiando el estado en la tabla de progreso a `✅ Completo` o `🔄 En progreso`.
