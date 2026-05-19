import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

from database import init_db
from handlers.start import start, ayuda
from handlers.tareas import (
    nueva_tarea, lista_tareas, completar_tarea,
    progreso_tarea, eliminar_tarea, cambiar_prioridad
)

load_dotenv()

async def post_init(application):
    await init_db()

def main():
    try:
        token = os.getenv("BOT_TOKEN")
        if not token:
            print("ERROR: No se encontró el token en el archivo .env")
            input("Pulsa Enter para cerrar...")
            return
            
        print("Conectando con Telegram...")
        app = ApplicationBuilder().token(token).post_init(post_init).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("ayuda", ayuda))
        app.add_handler(CommandHandler("nueva", nueva_tarea))
        app.add_handler(CommandHandler("lista", lista_tareas))
        app.add_handler(CommandHandler("completar", completar_tarea))
        app.add_handler(CommandHandler("progreso", progreso_tarea))
        app.add_handler(CommandHandler("eliminar", eliminar_tarea))
        app.add_handler(CommandHandler("prioridad", cambiar_prioridad))

        print("🤖 Bot iniciado correctamente...")
        app.run_polling()

    except Exception as e:
        print(f"ERROR: {e}")
        input("Pulsa Enter para cerrar...")

if __name__ == "__main__":
    main()