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
    global userTeam
    userTeam = {}
    global boardPositions
    boardPositions = {1: '', 2: '', 3: '', 4: '',
                      5 : '', 6 : '', 7 : '', 8 : '', 9: ''}
    print(f'{bot.user.name} has successfully connected to the server')

async def updateAndSendBoard(ctx):
    global board
    board = f'----------\n' \
            f'| {boardPositions[1]}   | {boardPositions[2]}   |  {boardPositions[3]}  |\n' \
            f'----------\n' \
            f'|  {boardPositions[4]}  |  {boardPositions[5]}  |  {boardPositions[6]}  |\n' \
            f'----------\n' \
            f'| {boardPositions[7]}   | {boardPositions[8]}   | {boardPositions[9]}   |\n' \
            f'----------\n'
    await ctx.send(board)

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
async def generateText(ctx, arg):
    global gameStarted
    global board
    global playerChosen
    global userTeam
    board = f'----------\n' \
            f'| {boardPositions[1]}   | {boardPositions[2]}   |  {boardPositions[3]}  |\n' \
            f'----------\n' \
            f'|  {boardPositions[4]}  |  {boardPositions[5]}  |  {boardPositions[6]}  |\n' \
            f'----------\n' \
            f'| {boardPositions[7]}   | {boardPositions[8]}   | {boardPositions[9]}   |\n' \
            f'----------\n'
    if (gameStarted == False and (arg == "o" or arg == "O")):
        gameStarted = True
        prompt = "Tic-tac-toe game started! O chosen!"
        userTeam = {ctx.author:'CIRCLE'}
        await ctx.send(board+prompt)
    elif gameStarted == False and (arg == "x" or arg == "X"):
        gameStarted = True
        prompt = "Tic-tac-toe game started! X chosen!"
        userTeam = {ctx.author:'X'}
        await ctx.send(board + prompt)
    else:
        await ctx.send("Error starting game, check the command")

@bot.command(name = 'place')
async def generateText(ctx, arg):
    global gameStarted
    global userTeam
    global boardPositions
    global board

    if (gameStarted and userTeam[ctx.author] == 'CIRCLE'):
        if (arg == '1'):
            boardPositions[1] = 'O'
            await updateAndSendBoard(ctx)
        elif (arg == '2'):
            boardPositions[2] = 'O'
            await updateAndSendBoard(ctx)
        elif (arg == '3'):
            boardPositions[3] = 'O'
            await updateAndSendBoard(ctx)
        elif (arg == '4'):
            boardPositions[4] = 'O'
            await updateAndSendBoard(ctx)
        elif (arg == '5'):
            boardPositions[5] = 'O'
            await updateAndSendBoard(ctx)
        elif (arg == '6'):
            boardPositions[6] = 'O'
            await updateAndSendBoard(ctx)
        elif (arg == '7'):
            boardPositions[7] = 'O'
            await updateAndSendBoard(ctx)
        elif (arg == '8'):
            boardPositions[8] = 'O'
            await updateAndSendBoard(ctx)
        elif (arg == '9'):
            boardPositions[9] = 'O'
            await updateAndSendBoard(ctx)
        else:
            await ctx.send("Invalid placement")
    elif gameStarted and userTeam[ctx.author] == 'X':
        if (arg == '1'):
            boardPositions[1] = 'X'
            await updateAndSendBoard(ctx)
        elif (arg == '2'):
            boardPositions[2] = 'X'
            await updateAndSendBoard(ctx)
        elif (arg == '3'):
            boardPositions[3] = 'X'
            await updateAndSendBoard(ctx)
        elif (arg == '4'):
            boardPositions[4] = 'X'
            await updateAndSendBoard(ctx)
        elif (arg == '5'):
            boardPositions[5] = 'X'
            await updateAndSendBoard(ctx)
        elif (arg == '6'):
            boardPositions[6] = 'X'
            await updateAndSendBoard(ctx)
        elif (arg == '7'):
            boardPositions[7] = 'X'
            await updateAndSendBoard(ctx)
        elif (arg == '8'):
            boardPositions[8] = 'X'
            await updateAndSendBoard(ctx)
        elif (arg == '9'):
            boardPositions[9] = 'X'
            await updateAndSendBoard(ctx)
        else:
            await ctx.send("Invalid placement")
    else:
        await ctx.send("Game has not started yet")


@bot.command(name = 'test')
async def printTest(ctx):
    global userTeam
    print(userTeam[ctx.author])


#client.run(TOKEN)
bot.run(TOKEN)