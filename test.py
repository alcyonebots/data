import asyncio
import os
from telethon import TelegramClient, events
from colorama import init, Fore

init(autoreset=True)

API_ID = int(input(Fore.CYAN + "Enter your API ID: "))
API_HASH = input(Fore.CYAN + "Enter your API HASH: ")
SESSION_NAME = "user_session"

CHANNEL_LINK = "https://t.me/+FZc60FEWcqxkNzJl"  # Jahan user ids bhejne hain

GROUP_LINKS = [
    "https://t.me/+kLjsw-WqpuFkZjM1",
    "https://t.me/BUZZ_IGCC_CHATS",
    "https://t.me/+F9Pp5_gHDB9jYzQ1",
    "https://t.me/BuzzEscrowe",
    "https://t.me/+mcMK_XK6J4M1NDE1",
    "https://t.me/+3khxeH9j6pViMjU9",

]  # Sirf in groups se uthana hai

SAVED_USERS_FILE = "saved_users.txt"
if not os.path.exists(SAVED_USERS_FILE):
    open(SAVED_USERS_FILE, "w").close()

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

group_ids = []

async def login():
    print(Fore.YELLOW + "Logging into your Telegram account...")
    await client.connect()
    if not await client.is_user_authorized():
        phone = input(Fore.CYAN + "Enter your phone number (with country code): ")
        await client.send_code_request(phone)
        code = input(Fore.CYAN + "Enter the OTP sent to your Telegram: ")
        try:
            await client.sign_in(phone, code)
        except Exception as e:
            print(Fore.RED + f"Login failed: {e}")
            exit()

async def resolve_groups():
    for link in GROUP_LINKS:
        try:
            entity = await client.get_entity(link)
            group_ids.append(entity.id)
            print(Fore.GREEN + f"✅ Resolved group: {link}")
        except Exception as e:
            print(Fore.RED + f"⚠️ Failed to resolve {link}: {e}")

@client.on(events.NewMessage)
async def handler(event):
    if not event.is_group:
        return

    if event.chat_id not in group_ids:
        return

    sender = await event.get_sender()
    if sender.bot or sender.deleted or sender.is_self:
        return

    try:
        user_id = str(sender.id)

        with open(SAVED_USERS_FILE, "r") as f:
            saved = f.read().splitlines()

        if user_id in saved:
            return

        await client.send_message(CHANNEL_LINK, user_id)

        with open(SAVED_USERS_FILE, "a") as f:
            f.write(user_id + "\n")

        print(Fore.GREEN + f"✅ Saved and sent user: {user_id}")

    except Exception as e:
        print(Fore.RED + f"⚠️ Error saving user: {e}")

async def main():
    await login()
    print(Fore.GREEN + "✅ Logged in successfully!")

    await resolve_groups()
    print(Fore.YELLOW + "✅ Watching specified groups...")

    await client.run_until_disconnected()

if __name__ == "__main__":
    client.loop.run_until_complete(main())
