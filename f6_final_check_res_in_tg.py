from telethon.sync import TelegramClient
from telethon.tl.functions.channels import CreateChannelRequest, UpdateUsernameRequest
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.errors.rpcerrorlist import UsernameInvalidError, UsernameOccupiedError
from config import api_id, api_hash
import asyncio
import pandas as pd



MAX_CHANNELS = 1


df = pd.read_csv('after_gpt.txt', names=['username', 'score'])
df = df.sort_values(by='score', ascending=False).reset_index(drop=True)

created_count = 0

async def is_username_taken(client, username):
    try:
        await client(ResolveUsernameRequest(username))
        return True  # Занят
    except (UsernameInvalidError, UsernameOccupiedError):
        return True  # Занят
    except Exception:
        return False  # Свободен

async def create_channel_if_possible(client, username):
    global created_count
    try:
        result = await client(CreateChannelRequest(
            title=username,
            about="Главный канал",
            megagroup=False
        ))
        channel = result.chats[0]
        await client(UpdateUsernameRequest(
            channel=channel,
            username=username
        ))
        print(f'Канал создан и username установлен: {username}')
        created_count += 1
    except Exception as e:
        print(f'Ошибка при создании/переименовании канала {username}: {e}')

async def main():
    global created_count
    async with TelegramClient('session_name', api_id=api_id, api_hash=api_hash) as client:
        await client.start()
        print('Сессия готова')

        for _, row in df.iterrows():
            if created_count >= MAX_CHANNELS:
                break

            username = row['username'].strip()
            if not username:
                continue

            print(f'🔍 Проверка ника: {username}')
            taken = await is_username_taken(client, username)
            if not taken:
                await create_channel_if_possible(client, username)
            else:
                print(f'Ник {username} уже занят.')

asyncio.run(main())