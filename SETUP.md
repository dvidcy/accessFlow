# AccessFlow — Guía de Instalación y Ejecución

Sistema de asistencia escolar con notificaciones por email a tutores.

---

## Requisitos previos

| Herramienta | Versión mínima | Descarga |
|---|---|---|
| Node.js | 18+ | https://nodejs.org |
| XAMPP | Cualquier versión reciente | https://www.apachefriends.org |
| Git | Cualquier versión | https://git-scm.com |

Verifica que Node.js esté instalado:
```bash
node --version
npm --version
```

---

## 1. Levantar MySQL con XAMPP

1. Abre el panel de control de XAMPP
2. Haz clic en **Start** junto a **MySQL**
3. Verifica que el indicador esté en verde

> Apache es opcional — el proyecto no lo necesita.

---

## 2. Crear la base de datos

1. Abre tu navegador y entra a `http://localhost/phpmyadmin`
2. En el panel izquierdo haz clic en **Nueva**
3. Escribe el nombre: `accessflow_db`
4. Selecciona cotejamiento: `utf8mb4_general_ci`
5. Haz clic en **Crear**

---

## 3. Configurar variables de entorno

Edita el archivo `server/.env` con tus credenciales:

```env
# Base de datos
DB_HOST=localhost
DB_PORT=3306
DB_NAME=accessflow_db
DB_USER=root
DB_PASSWORD=          ← dejar vacío si XAMPP no tiene contraseña

# Email Gmail
SMTP_EMAIL=tu_correo@gmail.com
SMTP_PASSWORD=tu_app_password_aqui

# JWT (puedes dejar el valor por defecto)
JWT_SECRET=accessflow_secret_key_2024
PORT=3001
```

### Configurar App Password de Gmail (para notificaciones por email)

1. Ve a tu cuenta Google → **Seguridad**
2. Activa la **Verificación en dos pasos**
3. Busca **Contraseñas de aplicación**
4. Genera una para "Correo" → copia los 16 caracteres
5. Pégala en `SMTP_PASSWORD`

> Si no configuras el email, el sistema funciona con normalidad pero no enviará notificaciones.

---

## 4. Instalar dependencias e inicializar la base de datos

Abre una terminal en la raíz del proyecto y ejecuta:

```bash
# Instalar dependencias del servidor
cd server
npm install

# Crear tablas e insertar datos de prueba (ejecutar solo una vez)
node src/db/seed.js
```

El seed crea automáticamente:

| Dato | Detalle |
|---|---|
| 1 Administrador | `admin@accessflow.com` / `admin123` |
| 2 Grupos | 1A matutino, 2B vespertino |
| 5 Alumnos | Distribuidos entre los grupos |
| 3 Tutores | Vinculados a los alumnos |

> Si ya ejecutaste el seed anteriormente, el script lo detecta y no hace nada.

---

## 5. Instalar dependencias del frontend

Abre **otra terminal** en la raíz del proyecto:

```bash
cd client
npm install
```

---

## 6. Ejecutar la aplicación

Necesitas **dos terminales abiertas al mismo tiempo**.

**Terminal 1 — API (backend):**
```bash
cd server
node src/index.js
```
Deberías ver:
```
AccessFlow API → http://localhost:3001
```

**Terminal 2 — Frontend:**
```bash
cd client
npm run dev
```
Deberías ver:
```
VITE ready → http://localhost:5173
```

Abre tu navegador en **http://localhost:5173** e inicia sesión con:

```
Correo:     admin@accessflow.com
Contraseña: admin123
```

---

## Estructura del proyecto

```
accessFlow/
├── server/                   # API Node.js (Express)
│   ├── .env                  # Credenciales (NO subir a git)
│   ├── package.json
│   └── src/
│       ├── index.js          # Punto de entrada del servidor
│       ├── db/
│       │   ├── connection.js # Conexión Sequelize
│       │   ├── models/       # Modelos ORM (tablas)
│       │   └── seed.js       # Datos de prueba
│       ├── middleware/
│       │   └── auth.js       # Verificación JWT
│       ├── routes/           # auth, asistencia, alumnos, grupos, tutores, mensajes
│       └── services/
│           ├── attendance.js # Lógica de entrada/salida
│           └── email.js      # Envío de correos
└── client/                   # Frontend React (Vite)
    ├── package.json
    └── src/
        ├── App.jsx           # Rutas + protección de páginas
        ├── api/index.js      # Axios con token de autenticación
        ├── context/          # Estado de sesión (AuthContext)
        ├── components/       # Layout y Sidebar
        └── pages/            # Login, Asistencia, Alumnos, Grupos, Tutores, Mensajes
```

---

## Resumen de comandos

```bash
# Terminal 1 — Servidor
cd server && node src/index.js

# Terminal 2 — Frontend
cd client && npm run dev

# Seed (solo la primera vez)
cd server && node src/db/seed.js
```

---

## Solución de problemas comunes

### "Cannot connect to MySQL"
MySQL no está iniciado. Abre XAMPP y haz clic en **Start** junto a **MySQL**.

### "Access denied for user 'root'"
La contraseña en `server/.env` no coincide. En XAMPP, por defecto `DB_PASSWORD` va vacío.

### "Unknown database 'accessflow_db'"
La base de datos no fue creada. Sigue el paso 2 de esta guía.

### El email no llega
- Verifica que `SMTP_EMAIL` y `SMTP_PASSWORD` en `server/.env` sean correctos
- Usa un **App Password** de Google, no tu contraseña normal
- Revisa la carpeta de spam del destinatario

### Puerto 3001 en uso
Cambia `PORT=3002` en `server/.env` y actualiza `vite.config.js`:
```js
proxy: { '/api': 'http://localhost:3002' }
```
