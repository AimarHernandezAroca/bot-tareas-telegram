from telegram import Update
from telegram.ext import ContextTypes
import aiosqlite
from database import DB_PATH

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuario = update.effective_user
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR IGNORE INTO usuarios (telegram_id, nombre)
            VALUES (?, ?)
        """, (usuario.id, usuario.first_name))
        await db.commit()

    await update.message.reply_text(
        f"👋 ¡Hola, {usuario.first_name}!\n\n"
        "Soy tu gestor de tareas personal. Estos son mis comandos:\n\n"
        "📋 /nueva — Crear una tarea\n"
        "📄 /lista — Ver tus tareas\n"
        "✅ /completar — Marcar tarea como completada\n"
        "🔄 /progreso — Marcar tarea en progreso\n"
        "🗑️ /eliminar — Eliminar una tarea\n"
        "❓ /ayuda — Ver todos los comandos"
    )

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 *Comandos disponibles:*\n\n"
        "📋 /nueva `<título>` — Crear tarea\n"
        "📄 /lista — Ver todas tus tareas\n"
        "✅ /completar `<id>` — Marcar como completada\n"
        "🔄 /progreso `<id>` — Marcar en progreso\n"
        "🗑️ /eliminar `<id>` — Eliminar tarea\n"
        "🔺 /prioridad `<id>` `<alta/media/baja>` — Cambiar prioridad",
        parse_mode="Markdown"
    )