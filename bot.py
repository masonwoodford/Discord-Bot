import os
import discord

client = discord.Client()
id = client.get_guild('GUILD_TOKEN')
TOKEN = os.environ['DISCORD_TOKEN']

@client.event
async def on_message(message):
    print(message.content)


client.run(TOKEN)