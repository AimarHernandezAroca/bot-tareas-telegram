from telegram import Update
from telegram.ext import ContextTypes
import aiosqlite
from database import DB_PATH

async def get_usuario_id(telegram_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id FROM usuarios WHERE telegram_id = ?", (telegram_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None

async def nueva_tarea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Uso correcto: /nueva <título de la tarea>")
        return

    titulo = " ".join(context.args)
    usuario_id = await get_usuario_id(update.effective_user.id)

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO tareas (usuario_id, titulo) VALUES (?, ?)",
            (usuario_id, titulo)
        )
        await db.commit()

    await update.message.reply_text(f"✅ Tarea creada: *{titulo}*", parse_mode="Markdown")

async def lista_tareas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuario_id = await get_usuario_id(update.effective_user.id)

    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id, titulo, estado, prioridad FROM tareas WHERE usuario_id = ?",
            (usuario_id,)
        ) as cursor:
            tareas = await cursor.fetchall()

    if not tareas:
        await update.message.reply_text("📭 No tienes tareas todavía. Usa /nueva para crear una.")
        return

    emojis_estado = {"pendiente": "⏳", "en progreso": "🔄", "completada": "✅"}
    emojis_prioridad = {"alta": "🔺", "media": "🔸", "baja": "🔻"}

    mensaje = "📋 *Tus tareas:*\n\n"
    for tarea in tareas:
        id_, titulo, estado, prioridad = tarea
        mensaje += (
            f"*ID {id_}* — {titulo}\n"
            f"  {emojis_estado.get(estado, '❓')} {estado} | {emojis_prioridad.get(prioridad, '🔸')} {prioridad}\n\n"
        )

    await update.message.reply_text(mensaje, parse_mode="Markdown")

async def completar_tarea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("⚠️ Uso correcto: /completar <id>\nEjemplo: /completar 1\n\nUsa /lista para ver los IDs de tus tareas.")
        return

    tarea_id = int(context.args[0])
    usuario_id = await get_usuario_id(update.effective_user.id)

    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "UPDATE tareas SET estado = 'completada' WHERE id = ? AND usuario_id = ?",
            (tarea_id, usuario_id)
        )
        await db.commit()

    if cursor.rowcount == 0:
        await update.message.reply_text(f"❌ No se encontró la tarea con ID {tarea_id}. Usa /lista para ver tus tareas.")
    else:
        await update.message.reply_text(f"✅ Tarea {tarea_id} marcada como completada.")

async def progreso_tarea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("⚠️ Uso correcto: /progreso <id>\nEjemplo: /progreso 1\n\nUsa /lista para ver los IDs de tus tareas.")
        return

    tarea_id = int(context.args[0])
    usuario_id = await get_usuario_id(update.effective_user.id)

    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "UPDATE tareas SET estado = 'en progreso' WHERE id = ? AND usuario_id = ?",
            (tarea_id, usuario_id)
        )
        await db.commit()

    if cursor.rowcount == 0:
        await update.message.reply_text(f"❌ No se encontró la tarea con ID {tarea_id}. Usa /lista para ver tus tareas.")
    else:
        await update.message.reply_text(f"🔄 Tarea {tarea_id} marcada como en progreso.")

async def eliminar_tarea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("⚠️ Uso correcto: /eliminar <id>\nEjemplo: /eliminar 1\n\nUsa /lista para ver los IDs de tus tareas.")
        return

    tarea_id = int(context.args[0])
    usuario_id = await get_usuario_id(update.effective_user.id)

    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "DELETE FROM tareas WHERE id = ? AND usuario_id = ?",
            (tarea_id, usuario_id)
        )
        await db.commit()

    if cursor.rowcount == 0:
        await update.message.reply_text(f"❌ No se encontró la tarea con ID {tarea_id}. Usa /lista para ver tus tareas.")
    else:
        await update.message.reply_text(f"🗑️ Tarea {tarea_id} eliminada.")

async def cambiar_prioridad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2 or not context.args[0].isdigit():
        await update.message.reply_text("⚠️ Uso correcto: /prioridad <id> <alta/media/baja>\nEjemplo: /prioridad 1 alta\n\nUsa /lista para ver los IDs de tus tareas.")
        return

    tarea_id = int(context.args[0])
    prioridad = context.args[1].lower()

    if prioridad not in ["alta", "media", "baja"]:
        await update.message.reply_text("⚠️ La prioridad debe ser: alta, media o baja\nEjemplo: /prioridad 1 alta")
        return

    usuario_id = await get_usuario_id(update.effective_user.id)

    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "UPDATE tareas SET prioridad = ? WHERE id = ? AND usuario_id = ?",
            (prioridad, tarea_id, usuario_id)
        )
        await db.commit()

    if cursor.rowcount == 0:
        await update.message.reply_text(f"❌ No se encontró la tarea con ID {tarea_id}. Usa /lista para ver tus tareas.")
    else:
        await update.message.reply_text(f"🔺 Prioridad de tarea {tarea_id} cambiada a *{prioridad}*.", parse_mode="Markdown")