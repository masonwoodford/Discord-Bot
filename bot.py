import os
import discord

client = discord.Client()
guild_token = os.environ['GUILD_TOKEN']
id = client.get_guild(guild_token)
TOKEN = os.environ['DISCORD_TOKEN']

@client.event
async def on_message(message):
    print(message.content)


client.run(TOKEN)