import discord
from discord.ext import commands
import datetime
import requests

# Replace with your account's token
TOKEN = 'usertokenhere'

# The server and channel IDs to monitor
SERVER_ID = 1234567890  # Replace with the actual server ID
CHANNEL_ID = 1234567890  # Replace with the actual channel ID
WEBHOOK_URL = 'webhookgoeshere'  # Replace with your actual webhook URL

client = commands.Bot(command_prefix=".")

def contains_link(message):
    return any(word.startswith('http') or word.startswith('www') for word in message.split())

def create_message_link(guild_id, channel_id, message_id):
    return f"https://discord.com/channels/{guild_id}/{channel_id}/{message_id}"

@client.event
async def on_message_delete(message):
    if message.guild.id != SERVER_ID:
        return

    log_message = (
        f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message.author} ({message.author.id})\n"
        f"Deleted Message: {message.content}\n"
        f"Channel: {message.channel.name}\n"
        f"Message ID: {message.id}\n"
        f"Message Link: {create_message_link(message.guild.id, message.channel.id, message.id)}\n"
        f"Server: {message.guild.name}\n"
        f"Contains Link: {contains_link(message.content)}\n\n"
    )

    with open("deleted_messages.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_message)

    webhook_message = (
        f"**Message Deleted**\n"
        f"Author: <@{message.author.id}> ({message.author.id})\n"
        f"Channel: {message.channel.name}\n"
        f"Message: {message.content}\n"
        f"Server: {message.guild.name}\n"
        f"Contains Link: {contains_link(message.content)}\n"
        f"Message Link: {create_message_link(message.guild.id, message.channel.id, message.id)}\n"
        f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    requests.post(WEBHOOK_URL, json={"content": webhook_message})

    print(f"Logged and sent deleted message by {message.author} in channel {message.channel}")

@client.event
async def on_message_edit(before, after):
    if before.guild.id != SERVER_ID:
        return

    log_message = (
        f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {before.author} ({before.author.id})\n"
        f"Original Message: {before.content}\n"
        f"Edited Message: {after.content}\n"
        f"Channel: {before.channel.name}\n"
        f"Message ID: {before.id}\n"
        f"Message Link: {create_message_link(before.guild.id, before.channel.id, before.id)}\n"
        f"Server: {before.guild.name}\n"
        f"Contains Link: {contains_link(after.content)}\n\n"
    )

    with open("edited_messages.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_message)

    webhook_message = (
        f"**Message Edited**\n"
        f"Author: <@{before.author.id}> ({before.author.id})\n"
        f"Channel: {before.channel.name}\n"
        f"Before: {before.content}\n"
        f"After: {after.content}\n"
        f"Server: {before.guild.name}\n"
        f"Contains Link: {contains_link(after.content)}\n"
        f"Message Link: {create_message_link(before.guild.id, before.channel.id, before.id)}\n"
        f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    requests.post(WEBHOOK_URL, json={"content": webhook_message})

    print(f"Logged and sent edited message by {before.author} in channel {before.channel}")

@client.event
async def on_message(message):
    if message.guild.id != SERVER_ID:
        return

    log_message = (
        f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message.author} ({message.author.id}): {message.content}\n"
        f"Server: {message.guild.name}\n"
        f"Channel: {message.channel.name}\n"
        f"Message Link: {create_message_link(message.guild.id, message.channel.id, message.id)}\n"
        f"Contains Link: {contains_link(message.content)}\n\n"
    )

    with open("chatlogs.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_message)
    
    webhook_message = (
        f"**New Message**\n"
        f"Author: <@{message.author.id}> ({message.author.id})\n"
        f"Channel: {message.channel.name}\n"
        f"Message: {message.content}\n"
        f"Server: {message.guild.name}\n"
        f"Contains Link: {contains_link(message.content)}\n"
        f"Message Link: {create_message_link(message.guild.id, message.channel.id, message.id)}\n"
        f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    requests.post(WEBHOOK_URL, json={"content": webhook_message})

    print(f"Logged and sent message by {message.author} in channel {message.channel}")

    await client.process_commands(message)

client.run(TOKEN)
