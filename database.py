import aiosqlite

DB_PATH = "tareas.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                telegram_id INTEGER UNIQUE,
                nombre TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                titulo TEXT,
                estado TEXT DEFAULT 'pendiente',
                prioridad TEXT DEFAULT 'media',
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)
        await db.commit()