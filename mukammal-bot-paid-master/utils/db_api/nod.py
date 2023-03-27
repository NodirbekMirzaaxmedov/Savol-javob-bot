from typing import Union
from environs import Env
import asyncpg
from asyncpg import Connection
from asyncpg import Pool
import os

env = Env()
env.read_env()

# from data import config

PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))
DATABASE = str(os.getenv("DATABASE"))
DB_HOST=env.str("DB_HOST")
class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    # async def check_args(args,user_id:int):
    #     if args == "":
    #         args = "0"
    #         return args
    #     elif not args.isnumeric():
    #         args = "0"
    #         return args
    #     elif args.isnumeric():
    #         if int(args) == user_id:
    #             args = "0"
    #             return args
    #         elif await se

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=PGUSER,
            password=PGPASSWORD,
            host=DB_HOST,
            database=DATABASE,
            port = 7122
        )

    async def execute(self, command, *args,
                       fetch: bool=False,
                       fetchval: bool=False,
                       fetchrow: bool=False,
                       execute: bool=False 
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id SERIAL PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            username varchar(255) NULL,
            telegram_id BIGINT NOT NULL UNIQUE,
            telefon_raqami BIGINT NOT NULL UNIQUE,
            balans BIGINT NOT NULL,
            taklif_qilganlari BIGINT,
            corrects  BIGINT,
            savol_olish  BOOLEAN
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod 
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item}=${num}" for num, item in enumerate(parameters.keys(),
                                                        start=1)
        ])
        return sql, tuple(parameters.values())

    
    async def create_table_savollar(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Savollar (
            id SERIAL PRIMARY KEY,
            savol VARCHAR(255) NOT NULL,
            notogri_javob1 varchar(255) NOT NULL,
            notogri_javob2 varchar(255) NOT NULL,
            notogri_javob3 varchar(255) NOT NULL,
            togri_javob varchar(255) NOT NULL,
            topildi BIGINT,
            topganlar_id BIGINT,
            new  BOOLEAN
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod 
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item}=${num}" for num, item in enumerate(parameters.keys(),
                                                        start=1)
        ])
        return sql, tuple(parameters.values())
    
    async def add_user(self, full_name, username, telegram_id,telefon_raqami,balans,taklif_qilganlari,corrects,savol_olish):
        sql = "INSERT INTO Users (full_name, username, telegram_id,telefon_raqami,balans,taklif_qilganlari,corrects,savol_olish) VALUES($1,$2,$3,$4,$5,$6,$7,$8) returning *"
        return await self.execute(sql,full_name,username,telegram_id,telefon_raqami,balans,taklif_qilganlari,corrects,savol_olish, fetchrow=True)

    async def add_savol(self,savol,notogri_javob1,notogri_javob2,notogri_javob3,togri_javob,topildi,topganlar_id,new):
        sql = "INSERT INTO Savollar (savol,notogri_javob1,notogri_javob2,notogri_javob3,togri_javob,topildi,topganlar_id,new) VALUES($1,$2,$3,$4,$5,$6,$7,$8) returning *"
        return await self.execute(sql,savol,notogri_javob1,notogri_javob2,notogri_javob3,togri_javob,topildi,topganlar_id,new, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_one_user(self,tg_id):
        sql = f"SELECT * FROM Users Where telegram_id={tg_id}"
        return await self.execute(sql,fetchrow=True)
    
    async def select_all_savollar(self,savol_id):
        sql = f"SELECT * FROM Savollar Where id={savol_id}"
        return await self.execute(sql, fetchrow=True)

    async def select_filer_savollar(self,tg_id):
        sql = f"SELECT * FROM Savollar Where topganlar_id<>{tg_id}"
        return await self.execute(sql, fetchrow=True)

    
    async def get_balans(self,tg_id,**kwargs):
        sql = f"SELECT * from Users Where telegram_id={tg_id}"
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql,*parameters,fetchrow=True)
    async def update_balans(self,tg_id,summa):
        sql = f"UPDATE Users SET balans = balans + {summa} WHERE telegram_id={tg_id}"
        return await self.execute(sql, execute=True)
    async def update_balans_minus(self,tg_id,summa):
        sql = f"UPDATE Users SET balans = balans - {summa} WHERE telegram_id={tg_id}"
        return await self.execute(sql, execute=True)
    async def update_taklif(self,tg_id):
        sql = f"UPDATE Users SET taklif_qilganlari = taklif_qilganlari + 1 WHERE telegram_id={tg_id}"
        return await self.execute(sql, execute=True)
    async def update_savol(self,tg_id,savol):
        sql = f"UPDATE Savollar SET topganlar_id = {tg_id} WHERE savol='{savol}'"
        return await self.execute(sql, execute=True)
    
    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_savol_olish(self,tg_id):
        sql = f"UPDATE Users SET savol_olish = FALSE WHERE telegram_id={tg_id}"
        return await self.execute(sql, execute=True)

    async def update_users_savol_olish_true(self,):
        sql = f"UPDATE Users SET savol_olish = TRUE"
        return await self.execute(sql, execute=True)
    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

    async def drop_savollar(self):
        await self.execute("DROP TABLE Savollar", execute=True)

    