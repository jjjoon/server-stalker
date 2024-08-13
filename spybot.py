import discord
from discord.ext import commands
import datetime
import requests

# Replace with your accounts token
TOKEN = 'abcdefghijklmnopqrstuvwxyz'

# The server and channel IDs to monitor
SERVER_ID = 921598000302800947 # Replace with the actual server ID
CHANNEL_ID = 1270902020785700914  # Replace with the actual channel ID
WEBHOOK_URL = 'https://discord.com/api/webhooks/12345678910/abcdefghijklmnopqrstuvwxyz'  # Replace with your actual webhook URL

client = commands.Bot(command_prefix=".")

@client.event
async def on_message_delete(message):
    if message.author.bot or not message.guild:
        return

    log_message = (
        f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message.author} ({message.author.id})\n"
        f"Deleted Message: {message.content}\n"
        f"Channel: {message.channel.name}\n"
        f"Message ID: {message.id}\n\n"
    )

    with open("deleted_messages.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_message)

    webhook_message = (
        f"**Message Deleted**\n"
        f"Author: {message.author} ({message.author.id})\n"
        f"Channel: {message.channel.name}\n"
        f"Message: {message.content}\n"
        f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    requests.post(WEBHOOK_URL, json={"content": webhook_message})

    print(f"Logged and sent deleted message by {message.author} in channel {message.channel}")

@client.event
async def on_message_edit(before, after):
    if before.author.bot or not before.guild:
        return

    log_message = (
        f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {before.author} ({before.author.id})\n"
        f"Original Message: {before.content}\n"
        f"Edited Message: {after.content}\n"
        f"Channel: {before.channel.name}\n"
        f"Message ID: {before.id}\n\n"
    )

    with open("edited_messages.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_message)

    webhook_message = (
        f"**Message Edited**\n"
        f"Author: {before.author} ({before.author.id})\n"
        f"Channel: {before.channel.name}\n"
        f"Before: {before.content}\n"
        f"After: {after.content}\n"
        f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    requests.post(WEBHOOK_URL, json={"content": webhook_message})

    print(f"Logged and sent edited message by {before.author} in channel {before.channel}")
    
@client.event
async def on_message(message):
    if message.author.bot:
        return

    log_message = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message.author} ({message.author.id}): {message.content}\n"
    
    with open("chatlogs.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_message)
    
    webhook_message = (
        f"**New Message**\n"
        f"Author: {message.author} ({message.author.id})\n"
        f"Channel: {message.channel.name}\n"
        f"Message: {message.content}\n"
        f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    requests.post(WEBHOOK_URL, json={"content": webhook_message})

    print(f"Logged and sent message by {message.author} in channel {message.channel}")

    await client.process_commands(message)

client.run(TOKEN)
