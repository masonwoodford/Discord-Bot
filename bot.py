import os
import discord
import asyncio
import random

from discord.ext import commands

TOKEN = os.environ['DISCORD_TOKEN']
dashString = '---------'
wall = '|'

class Board:
    def __init__(self):
        self.gameStarted = False
        self.boardPositions = {1: '', 2: '', 3: '', 4: '',
                      5 : '', 6 : '', 7 : '', 8 : '', 9: ''}
        self.possiblePositions = [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.board = ""
        self.userTeam = {}

    def reset(self):
        self.gameStarted = False
        self.boardPositions = {1: '', 2: '', 3: '', 4: '',
                      5 : '', 6 : '', 7 : '', 8 : '', 9: ''}
        self.possiblePositions = [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.board = ""
        self.userTeam = {}
    
bot = commands.Bot(command_prefix='!')
board = Board()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has successfully connected to the server')

async def updateAndSendBoard(ctx):
    board.board = f'{dashString.center(21, "-")}\n' \
            f'|{board.boardPositions[1].center(8, " ")}|{board.boardPositions[2].center(8, " ")}|{board.boardPositions[3].center(8, " ")}|\n' \
            f'{dashString.center(21, "-")}\n' \
            f'|{board.boardPositions[4].center(8, " ")}|{board.boardPositions[5].center(8, " ")}|{board.boardPositions[6].center(8, " ")}|\n' \
            f'{dashString.center(21, "-")}\n' \
            f'|{board.boardPositions[7].center(8, " ")}|{board.boardPositions[8].center(8, " ")}|{board.boardPositions[9].center(8, " ")}|\n' \
            f'{dashString.center(21, "-")}\n'

    await ctx.send(board.board)

def checkRows():
    row = []
    for i in range(1,4):
        row.append(board.boardPositions[i])
    if len(set(row)) == 1:
        if board.boardPositions[1] == 'O':
            return 'O'
        elif board.boardPositions[1] == 'X':
            return 'X'
    row.clear()
    for i in range(4,7):
        row.append(board.boardPositions[i])
    if len(set(row)) == 1:
        if board.boardPositions[4] == 'O':
            return 'O'
        elif board.boardPositions[4] == 'X':
            return 'X'
    row.clear()
    for i in range(7,10):
        row.append(board.boardPositions[i])
    if len(set(row)) == 1:
        if board.boardPositions[7] == 'O':
            return 'O'
        elif board.boardPositions[7] == 'X':
            return 'X'
    row.clear()
    return False

def checkCols():
    col = []
    for i in range(1,8,3):
        col.append(board.boardPositions[i])
    if len(set(col)) == 1:
        if board.boardPositions[1] == 'O':
            return 'O'
        elif board.boardPositions[1] == 'X':
            return 'X'
    col.clear()
    for i in range(2, 9, 3):
        col.append(board.boardPositions[i])
    if len(set(col)) == 1:
        if board.boardPositions[2] == 'O':
            return 'O'
        elif board.boardPositions[2] == 'X':
            return 'X'
    col.clear()
    for i in range(3, 10, 3):
        col.append(board.boardPositions[i])
    if len(set(col)) == 1:
        if board.boardPositions[3] == 'O':
            return 'O'
        elif board.boardPositions[3] == 'X':
            return 'X'
    col.clear()
    return False

def checkDiags():
    diag = []
    diag.append(board.boardPositions[1])
    diag.append(board.boardPositions[5])
    diag.append(board.boardPositions[9])
    if len(set(diag)) == 1:
        if board.boardPositions[1] == 'O':
            return 'O'
        elif board.boardPositions[1] == 'X':
            return 'X'
    diag.clear()
    diag.append(board.boardPositions[3])
    diag.append(board.boardPositions[5])
    diag.append(board.boardPositions[7])
    if len(set(diag)) == 1:
        if board.boardPositions[3] == 'O':
            return 'O'
        elif board.boardPositions[3] == 'X':
            return 'X'
    diag.clear()
    return False

async def AI(ctx):
    if len(board.possiblePositions) == 1:
        await tieGame(ctx)
        return
    await ctx.send("Thinking...")
    await asyncio.sleep(1.3)
    bestScore = float('-inf')
    choice = -1
    for i in range(1, 10):
        if board.boardPositions[i] == '':
            if board.userTeam[ctx.author] == 'X':
                board.boardPositions[i] = 'O'
            elif board.userTeam[ctx.author] == 'O':
                board.boardPositions[i] = 'X'
            score = miniMax(0, False, ctx)
            board.boardPositions[i] = ''
            if score > bestScore:
                bestScore = score
                choice = i
    board.possiblePositions.remove(choice)
    if board.userTeam[ctx.author] == 'X':
        board.boardPositions[choice] = 'O'
    elif board.userTeam[ctx.author] == 'O':
        board.boardPositions[choice] = 'X'
    await updateAndSendBoard(ctx)
    if (hasWon() != False):
        board.reset()
        await ctx.send("Game Over!")


def miniMax(depth, isMaximizing, ctx):
    outcome = hasWon()
    if (outcome == 'O'):
        score = -10
        return score
    elif (outcome == 'X'):
        score = 10
        return score
    notTie = True
    for value in board.boardPositions.values():
        if value == '':
            notTie = False
    if notTie == True and outcome == False:
        score = 0
        return score
    if isMaximizing:
        bestScore = float('-inf')
        for i in range(1, 10):
            if board.boardPositions[i] == '':
                if board.userTeam[ctx.author] == 'X':
                    board.boardPositions[i] = 'O'
                elif board.userTeam[ctx.author] == 'O':
                    board.boardPositions[i] = 'X'
                score = miniMax(depth+1, False, ctx)
                board.boardPositions[i] = ''
                bestScore = max(score, bestScore)
        return bestScore
    else:
        bestScore = float('inf')
        for i in range(1, 10):
            if board.boardPositions[i] == '':
                if board.userTeam[ctx.author] == 'X':
                    board.boardPositions[i] = 'X'
                elif board.userTeam[ctx.author] == 'O':
                    board.boardPositions[i] = 'O'
                score = miniMax(depth+1, True, ctx)
                board.boardPositions[i] = ''
                bestScore = min(score, bestScore)
        return bestScore

async def tieGame(ctx):
    board.reset()
    await ctx.send("Cat's Game!")

def hasWon():
    if checkCols() == 'O' or checkRows() == 'O' or checkDiags() == 'O':
        return 'O'
    elif checkCols() == 'X' or checkRows() == 'X' or checkDiags() == 'X':
        return 'X'
    else:
        return False


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Welcome {member.name} to this Discord server!'
    )

@bot.command(name='error', help='Sends error message')
async def generateText(ctx):
    await ctx.send("Stack Overflow :(")

@bot.command(name='tictac', help="Use !tictac x or !tictac o to start a game")
async def generateText(ctx, arg = None):
    if (board.gameStarted == True):
        await ctx.send("Error: game already in progress")
        return
    if arg == None:
        await ctx.send("You need to specify your team")
        return
    if (board.gameStarted == False and (arg == "o" or arg == "O")):
        board.gameStarted = True
        await updateAndSendBoard(ctx)
        prompt = "Tic-tac-toe game started! O chosen!"
        board.userTeam = {ctx.author:'O'}
        await ctx.send(prompt)
    elif board.gameStarted == False and (arg == "x" or arg == "X"):
        board.gameStarted = True
        await updateAndSendBoard(ctx)
        prompt = "Tic-tac-toe game started! X chosen!"
        board.userTeam = {ctx.author:'X'}
        await ctx.send(prompt)
    else:
        await ctx.send("Error starting game, check the command")

@bot.command(name = 'place', help='Use !place 1-9 to place a piece')
async def generateText(ctx, arg = None):
    if (board.gameStarted == False):
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
    if (board.gameStarted and board.userTeam[ctx.author] == 'O'):
        if (board.boardPositions[arg] == ''):
            board.boardPositions[arg] = 'O'
            board.possiblePositions.remove(arg)
            await updateAndSendBoard(ctx)
            if hasWon() == 'O':
                board.reset()
                await ctx.send("You win!")
                return
            if len(board.possiblePositions) == 1:
                await tieGame(ctx)
                return
            await AI(ctx)
        else:
            await ctx.send("Space already taken")
    elif board.gameStarted and board.userTeam[ctx.author] == 'X':
        if (board.boardPositions[arg] == ''):
            board.boardPositions[arg] = 'X'
            board.possiblePositions.remove(arg)
            await updateAndSendBoard(ctx)
            if hasWon() == 'X':
                board.reset()
                await ctx.send("You win!")
                return
            if len(board.possiblePositions) == 1:
                await tieGame(ctx)
                return
            await AI(ctx)

        else:
            await ctx.send("Space already taken")
    else:
        await ctx.send("Error, report bug please")

@bot.command(name = "stop", help = "Ends the current game")
async def generateText(ctx):
    board.reset()
    await ctx.send("Game was ended")

bot.run(TOKEN)