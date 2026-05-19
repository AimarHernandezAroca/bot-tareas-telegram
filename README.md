# 🤖 Bot de Telegram - Gestor de Tareas

Bot de Telegram para gestionar tareas personales directamente desde el chat. Desarrollado en Python con base de datos SQLite y desplegado en Railway.

## ✨ Funcionalidades

- 👤 Registro automático de usuarios via Telegram
- 📋 Crear, listar y eliminar tareas
- 🔄 Cambiar el estado de las tareas (pendiente, en progreso, completada)
- 🔺 Asignar prioridades (alta, media, baja)
- ☁️ Activo 24/7 en la nube

## 🛠️ Tecnologías

- **Python 3.11**
- **python-telegram-bot 20.7**
- **SQLite** con aiosqlite
- **Railway** para el despliegue

## 📋 Comandos disponibles

| Comando | Descripción |
|--------|-------------|
| `/start` | Registrarse e ver los comandos |
| `/nueva <título>` | Crear una nueva tarea |
| `/lista` | Ver todas tus tareas |
| `/completar <id>` | Marcar tarea como completada |
| `/progreso <id>` | Marcar tarea como en progreso |
| `/eliminar <id>` | Eliminar una tarea |
| `/prioridad <id> <alta/media/baja>` | Cambiar la prioridad |

## 🚀 Instalación local

1. Clona el repositorio
```bash
git clone https://github.com/AimarHernandezAroca/bot-tareas-telegram.git
cd bot-tareas-telegram
```

2. Crea el entorno virtual e instala dependencias
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Crea un archivo `.env` con tu token
```
BOT_TOKEN=tu_token_aqui
```

4. Ejecuta el bot
```bash
python main.py
```

## 📁 Estructura del proyecto

```
bot-tareas/
├── handlers/
│   ├── start.py       # Comandos de inicio y ayuda
│   └── tareas.py      # Lógica de gestión de tareas
├── main.py            # Punto de entrada
├── database.py        # Inicialización de la base de datos
├── requirements.txt
└── Procfile           # Configuración para Railway
```

## 👨‍💻 Autor

**Aimar Hernandez** — [@AimarHernandezAroca](https://github.com/AimarHernandezAroca)