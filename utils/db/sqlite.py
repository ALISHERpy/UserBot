import aiosqlite
from typing import Union


class Database:
    def __init__(self, db_path="data.db"):
        self.db_path = db_path

    async def execute(self, command, *args, fetch=False, fetchval=False, fetchrow=False, execute=False):
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(command, args)
            if fetch:
                result = await cursor.fetchall()
            elif fetchval:
                result = (await cursor.fetchone())[0]
            elif fetchrow:
                result = await cursor.fetchone()
            elif execute:
                await db.commit()
                result = None
            await cursor.close()
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            username TEXT,
            telegram_id INTEGER NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO Users (full_name, username, telegram_id) VALUES (?, ?, ?)"
        return await self.execute(sql, full_name, username, telegram_id, execute=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=? WHERE telegram_id=?"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE 1=1", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE IF EXISTS Users", execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([f"{key}=?" for key in parameters])
        return sql, tuple(parameters.values())
