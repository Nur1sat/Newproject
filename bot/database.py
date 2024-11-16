import asyncio

import aiosqlite

# Database file
DB_PATH = "users.db"


async def init_db():
    """
    Initialize the database and create the necessary table if it doesn't exist.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL UNIQUE,
            name TEXT,
            age INTEGER,
            location TEXT
        )
        """)
        await db.commit()


async def save_user(telegram_id: int, name: str, age: int, location: str):
    """
    Save user data into the database.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        INSERT INTO users (telegram_id, name, age, location)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(telegram_id) DO UPDATE SET
            name=excluded.name,
            age=excluded.age,
            location=excluded.location
        """, (telegram_id, name, age, location))
        await db.commit()


async def delete_user(telegram_id: int):
    """
    Delete a user's data from the database.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM users WHERE telegram_id = ?", (telegram_id,))
        await db.commit()


async def get_user(telegram_id: int) -> dict:
    """
    Retrieve a user's data from the database.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT name, age, location FROM users WHERE telegram_id = ?", (telegram_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {"name": row[0], "age": row[1], "location": row[2]}
            return None

async def get_all_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT name, age, location, telegram_id FROM users ") as cursor:
            row = await cursor.fetchone()
            if row:
                return {"name": row[0], "age": row[1], "location": row[2], "telegram_id": row[3]}
            return None

if __name__ == "__main__":
    asyncio.run(init_db())