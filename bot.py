import os
import discord
import asyncio
import random

from discord.ext import commands

#client = discord.Client()
guild_token = os.environ['GUILD_TOKEN']
#id = client.get_guild(guild_token)
TOKEN = os.environ['DISCORD_TOKEN']

bot = commands.Bot(command_prefix='!')

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
    global possiblePositions
    possiblePositions = [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(f'{bot.user.name} has successfully connected to the server')

async def updateAndSendBoard(ctx):
    global board
    dashString = '---------'
    wall = '|'
    board = f'{dashString.center(21, "-")}\n' \
            f'|{boardPositions[1].center(8, " ")}|{boardPositions[2].center(8, " ")}|{boardPositions[3].center(8, " ")}|\n' \
            f'{dashString.center(21, "-")}\n' \
            f'|{boardPositions[4].center(8, " ")}|{boardPositions[5].center(8, " ")}|{boardPositions[6].center(8, " ")}|\n' \
            f'{dashString.center(21, "-")}\n' \
            f'|{boardPositions[7].center(8, " ")}|{boardPositions[8].center(8, " ")}|{boardPositions[9].center(8, " ")}|\n' \
            f'{dashString.center(21, "-")}\n'

    await ctx.send(board)

async def checkRows():
    row = []
    for i in range(1,4):
        row.append(boardPositions[i])
    if len(set(row)) == 1:
        if boardPositions[1] == 'O':
            return True
        elif boardPositions[1] == 'X':
            return True
    row.clear()
    for i in range(4,7):
        row.append(boardPositions[i])
    if len(set(row)) == 1:
        if boardPositions[4] == 'O':
            return True
        elif boardPositions[4] == 'X':
            return True
    row.clear()
    for i in range(7,10):
        row.append(boardPositions[i])
    if len(set(row)) == 1:
        if boardPositions[7] == 'O':
            return True
        elif boardPositions[7] == 'X':
            return True
    row.clear()
    return False

async def checkCols():
    col = []
    for i in range(1,8,3):
        col.append(boardPositions[i])
    if len(set(col)) == 1:
        if boardPositions[1] == 'O':
            return True
        elif boardPositions[1] == 'X':
            return True
    col.clear()
    for i in range(2, 9, 3):
        col.append(boardPositions[i])
    if len(set(col)) == 1:
        if boardPositions[2] == 'O':
            return True
        elif boardPositions[2] == 'X':
            return True
    col.clear()
    for i in range(3, 10, 3):
        col.append(boardPositions[i])
    if len(set(col)) == 1:
        if boardPositions[3] == 'O':
            return True
        elif boardPositions[3] == 'X':
            return True
    col.clear()
    return False

async def checkDiags():
    diag = []
    diag.append(boardPositions[1])
    diag.append(boardPositions[5])
    diag.append(boardPositions[9])
    if len(set(diag)) == 1:
        if boardPositions[1] == '0':
            return True
        elif boardPositions[1] == 'X':
            return True
    diag.clear()
    diag.append(boardPositions[3])
    diag.append(boardPositions[5])
    diag.append(boardPositions[7])
    if len(set(diag)) == 1:
        if boardPositions[3] == '0':
            return True
        elif boardPositions[3] == 'X':
            return True
    diag.clear()
    return False

async def AI(ctx):
    global userTeam
    global possiblePositions
    global boardPositions
    if len(possiblePositions) == 1:
        await tieGame(ctx)
        return
    await ctx.send("Thinking...")
    await asyncio.sleep(1.5)
    choice = random.choice(possiblePositions[1:])
    possiblePositions.remove(choice)
    if userTeam[ctx.author] == 'X':
        boardPositions[choice] = 'O'
    elif userTeam[ctx.author] == 'O':
        boardPositions[choice] = 'X'
    await updateAndSendBoard(ctx)
    await hasWon(ctx)

async def resetGame():
    global gameStarted
    gameStarted = False
    global board
    board = ""
    global userTeam
    userTeam = {}
    global boardPositions
    boardPositions = {1: '', 2: '', 3: '', 4: '',
                      5: '', 6: '', 7: '', 8: '', 9: ''}
    global possiblePositions
    possiblePositions = [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    return

async def tieGame(ctx):
    await resetGame()
    await ctx.send("Cat's Game!")

async def hasWon(ctx):
    if await checkCols() == True or await checkRows() == True or await checkDiags() == True:
        await resetGame()
        await ctx.send("Game over!")
        return True


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Welcome {member.name} to this Discord server!'
    )

@bot.command(name='error', help='Sends error message')
async def generateText(ctx):
    await ctx.send("Stack Overflow :(")

@bot.command(name='tictac', help="Plays tic tac toe")
async def generateText(ctx, arg = None):
    global gameStarted
    global board
    global playerChosen
    global userTeam
    if (gameStarted == True):
        await ctx.send("Error: game already in progress")
        return
    if arg == None:
        await ctx.send("You need to specify your team")
        return
    await updateAndSendBoard(ctx)
    if (gameStarted == False and (arg == "o" or arg == "O")):
        gameStarted = True
        prompt = "Tic-tac-toe game started! O chosen!"
        userTeam = {ctx.author:'O'}
        await ctx.send(prompt)
    elif gameStarted == False and (arg == "x" or arg == "X"):
        gameStarted = True
        prompt = "Tic-tac-toe game started! X chosen!"
        userTeam = {ctx.author:'X'}
        await ctx.send(prompt)
    else:
        await ctx.send("Error starting game, check the command")

@bot.command(name = 'place')
async def generateText(ctx, arg = None):
    global gameStarted
    global userTeam
    global boardPositions
    global board
    global possiblePositions
    global hasP1Won
    if (gameStarted == False):
        await ctx.send("Game has not started yet")
        return
    if arg == None:
        await ctx.send("Need placement position")
        return
    position = ord(arg)
    if position < 49 or position > 57:
        await ctx.send("Invalid position")
        return
    arg = int(arg)
    if (gameStarted and userTeam[ctx.author] == 'O'):
        if (boardPositions[arg] == ''):
            boardPositions[arg] = 'O'
            possiblePositions.remove(arg)
            await updateAndSendBoard(ctx)
            if await hasWon(ctx) == True:
                return
            if len(possiblePositions) == 1:
                await tieGame(ctx)
                return
            await AI(ctx)
        else:
            await ctx.send("Space already taken")
    elif gameStarted and userTeam[ctx.author] == 'X':
        if (boardPositions[arg] == ''):
            boardPositions[arg] = 'X'
            possiblePositions.remove(arg)
            await updateAndSendBoard(ctx)
            if await hasWon(ctx) == True:
                return
            if len(possiblePositions) == 1:
                await tieGame(ctx)
                return
            await AI(ctx)

        else:
            await ctx.send("Space already taken")
    else:
        await ctx.send("Error, report bug please")

@bot.command(name = "stop")
async def generateText(ctx):
    await resetGame()
    await ctx.send("Game was ended")

@bot.command(name = 'test')
async def printTest(ctx):
    global userTeam
    print(userTeam[ctx.author])

bot.run(TOKEN)