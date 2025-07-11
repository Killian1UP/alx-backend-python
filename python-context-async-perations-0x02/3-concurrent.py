import asyncio
import aiosqlite

async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users
        
async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            users = await cursor.fetchall()
            print("All users older than 40:")
            return users
        
async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
    print("All Users:")
    for user in all_users:
        print(user)
        
    print("Users Older Than 40:")
    for user in older_users:
        print(user)
        
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
