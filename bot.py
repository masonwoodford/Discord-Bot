import os
import discord

from discord.ext import commands

#client = discord.Client()
guild_token = os.environ['GUILD_TOKEN']
#id = client.get_guild(guild_token)
TOKEN = os.environ['DISCORD_TOKEN']

bot = commands.Bot(command_prefix='!')

#@client.event
#async def on_ready():
#    print(f'{client.user.name} has successfully connected to the server')

@bot.event
async def on_ready():
    global gameStarted
    gameStarted = False
    global board
    board = ""
    global playerChosen
    playerChosen = False
    global userTeam
    userTeam = {}
    print(f'{bot.user.name} has successfully connected to the server')

#@bot.event
#async def on_message(message):
#    print(message.content)

@bot.event
async def on_member_join(member):
    print("hello")
    await member.create_dm()
    await member.dm_channel.send(
        f'Welcome {member.name} to this Discord server!'
    )

@bot.command(name='error', help='Sends error message')
async def generateText(ctx):
    await ctx.send("Stack Overflow :(")

@bot.command(name='tictac', help="Plays tic tac toe")
async def generateText(ctx):
    global gameStarted
    global board
    if (gameStarted == False):
        gameStarted = True
        board = "----------\n" \
                "|    |    |    |\n" \
                "----------\n" \
                "|    |    |    |\n" \
                "----------\n" \
                "|    |    |    |\n" \
                "----------\n"
        prompt = "Tic-tac-toe game started! Use !circle or !x to choose your player"
        await ctx.send(board+prompt)
    else:
        await ctx.send("Game already in progress")

@bot.command(name = 'circle')
async def generateText(ctx):
    global playerChosen
    global userTeam
    if playerChosen == False:
        userTeam = {ctx.author:'CIRCLE'}
        playerChosen = True

@bot.command(name = 'test')
async def printTest(ctx):
    global userTeam
    print(userTeam[ctx.author])


#client.run(TOKEN)
bot.run(TOKEN)