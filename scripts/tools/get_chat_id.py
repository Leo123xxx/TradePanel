import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv

async def get_chat_id():
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN not found in .env")
        return

    bot = Bot(token=token)
    print(f"Connecting to bot...")
    
    try:
        me = await bot.get_me()
        print(f"Bot Name: @{me.username}")
        print("Please send a message to your bot now...")
        
        last_update_id = 0
        while True:
            updates = await bot.get_updates(offset=last_update_id + 1, timeout=10)
            for update in updates:
                if update.message:
                    chat_id = update.message.chat_id
                    print(f"\nSUCCESS!")
                    print(f"Your Chat ID is: {chat_id}")
                    print(f"Update your .env file with: TELEGRAM_CHAT_ID={chat_id}")
                    return
                last_update_id = update.update_id
            await asyncio.sleep(1)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(get_chat_id())
