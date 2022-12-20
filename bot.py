import discord
import random
import json
from datetime import timedelta
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


def getChannel():
    return bot.get_channel(1047531070314250311)


@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='Plebs')
    channel = bot.get_channel(401071542110388257)
    await member.add_roles(role)
    await channel.send(f'> Hey {member.mention}, welcome to **HeHeXD**')


@bot.event
async def on_member_remove(member):
    member_name = str(member).split('#')[0]
    channel = bot.get_channel(401071542110388257)
    await channel.send(f'> **{member_name}** finally pissed off')


def addUserToDict(member):
    with open('UserBalance.txt') as f:
        data = f.read()
    js = json.loads(data)
    js[str(member)] = 0
    f.close()
    with open('UserBalance.txt', 'w') as file:
        file.write(
            json.dumps(js))  # json dumps - replaces single quotes with double quotes
        file.close()
    return


def getUserBalance(member):
    with open('UserBalance.txt') as f:
        data = f.read()
        js = json.loads(data)  # nolasa informaciju to parversot dictionarya
        balance = js[str(member)]
    return balance


def checkDict(member):
    with open(r'UserBalance.txt', 'r+') as file:
        data = file.read()
        res = data.find(str(member))
        file.close()
        return res


def updateBalance(member, balanceChange):
    with open('UserBalance.txt') as f:
        data = f.read()
    js = json.loads(data)  # nolasa informaciju to parversot dictionarya
    with open('UserBalance.txt', 'r') as file:
        data = file.read()
        stringToReplace = f'"{member}": {str(js[str(member)])}'
        newBalance = int(js[str(member)]) + balanceChange
        updatedString = f'"{member}": {str(newBalance)}'
        # data = data.replace(str(js[str(member)]),
        #                     str(int(js[str(member)]) + balanceChange))  # js[member] - user vecais balance
        data = data.replace(stringToReplace,
                            updatedString)  # js[member] - user vecais balance
    with open('UserBalance.txt', 'w') as file:
        file.write(str(data))


class Card:

    def __init__(self, value, points, suit):
        self.value = value
        self.points = value
        if value in ["J", "Q", "K"]:
            self.points = 10
        elif value == "A":
            self.points = 11
        self.suit = suit

    def get_value(self):
        return self.value

    def get_points(self):
        return self.points

    def change_points(self, point_val):
        self.points = point_val

    def string(self):
        return str(self.value) + self.suit


class Deck:

    def __init__(self):
        self.deck = []
        suits = ["**♥**", "**♠**", "**♦**", "**♣**"]
        cards = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
        for suit in suits:
            for card in cards:
                if card in ["J", "Q", "K"]:
                    points = 10
                elif card == "A":
                    points = 11
                else:
                    points = int(card)
                self.deck.append(Card(card, points, suit))

    def sum_cards(self, list_cards):
        sum = 0
        for card in self.deck:
            sum += card.get_points()
        return sum

    def draw(self, num):
        cards = []
        for i in range(0, num):
            c = random.choice(self.deck)
            cards.append(c)
            self.deck.remove(c)
        return cards


class Hand:

    def __init__(self):
        self.deck = []
        self.not_done = True

    def add_card(self, cards):
        for card in cards:
            self.deck.append(card)

    def sum_cards(self):
        sum = 0
        for card in self.deck:
            sum += card.get_points()
        return sum

    def checkHandAceValue(self):
        for card in self.deck:
            if card.get_points() == 11:
                card.points = 1
        return self.deck

    def sumFirstCard(self):
        return self.deck[0].get_points()

    def dealer_print(self):
        return self.deck[0].string()

    def print_cards(self):
        ret_str = ""
        for card in self.deck:
            ret_str += card.string() + ", "
        return ret_str[0:len(ret_str) - 2]

    def done(self):
        self.not_done = False

    def get_cards(self):
        return self.deck


async def printMessage(text):
    channel = getChannel()
    await channel.send(str(text))


async def print_res(text, player, dealer):
    channel = getChannel()
    if text != '':  # when the game has ended
        await channel.send(text + "\nYour cards are " + player.print_cards() +
                           ' (' + str(player.sum_cards()) + ')' + "\nDealer has " +
                           dealer.print_cards() + ' (' + str(dealer.sum_cards()) +
                           ')' + "\nScores: You: " + str(player.sum_cards()) +
                           " vs. Dealer: " + str(dealer.sum_cards()))
    else:  # for the ongoing game
        await channel.send('Your cards are ' + player.print_cards() + ' (' +
                           str(player.sum_cards()) + ')' + '\nDealer has ' +
                           dealer.dealer_print() + ' (' +
                           str(dealer.sumFirstCard()) + ')' + '\nhit or stay?')


@bot.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
    try:
        if checkDict(ctx.author) == -1:
            addUserToDict(
                ctx.author)  # adds the message author on the user balance.txt file
        await ctx.send('you redeemed 100 credits')
        updateBalance(ctx.author, 100)
    except Exception as e:
        print(e)
    return


@bot.command()
async def timeout(ctx, member: discord.Member, *, minutes):
    if (int(minutes) <= 0):
        return
    userCredits = getUserBalance(ctx.author)
    timeoutPrice = int(minutes) * 100
    if member.id == ctx.author.id:
        await ctx.send("You can't timeout yourself!")
        return
    if int(userCredits) >= int(timeoutPrice):

        duration = timedelta(minutes=int(minutes))
        await member.timeout(duration)
        await ctx.send(
            f"<@{member.id}> has been timed out for {minutes} minutes by <@{ctx.author.id}>."
        )
        updateBalance(ctx.author, -timeoutPrice)
    elif int(userCredits) < int(timeoutPrice):
        await ctx.send(
            f"you have {userCredits} credits but you need {timeoutPrice}")
    # elif member.id == 898900187966218252:  # bot id
    #   await ctx.send(f'XD? <@{ctx.author.id}>')
    #   duration = timedelta(minutes=int(60))
    #   await ctx.author.timeout(duration)
    else:
        await ctx.send(f"type it like **!timeout @someone time_in_minutes**")


@bot.command()
async def info(ctx):
    await ctx.send(
        '> **!daily** to claim 100 daily credits\n > **!bal** to check your credits\n > **!blackjack '
        'credits** to play blackjack with a credit bet\n > **!timeout @user minutes** to timeout someone - '
        '100 credits for 1 minute')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        hours = int(error.retry_after) / 3600
        minutes = (error.retry_after / 60) - (int(hours) * 60)

        await ctx.send(
            f'This command is on a {int(hours)} hour and {int(minutes)} minute cooldown'
        )
    raise error


@bot.command()
async def bal(ctx):
    await balance.invoke(ctx)


@bot.command()
async def balance(ctx):
    userCredits = getUserBalance(ctx.author)
    if checkDict(ctx.author) == -1:
        addUserToDict(ctx.author)  # ads the message author on the user balance.txt filed
    await ctx.send('you have ' + str(getUserBalance(ctx.author)) + ' credits')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "!blackjack" in message.content.lower():
        global userBet
        if checkDict(message.author) == -1:
            addUserToDict(
                message.author)  # adds the message author on the user balance.txt file
        splitMsg = message.content.split(' ')

        try:
            userBet = int(splitMsg[1])
        except:
            await printMessage('specify an amount ex. !blackjack 50')
            return

        userBalance = getUserBalance(message.author)
        if userBet > userBalance:
            await printMessage('you too broke for that fella, you only have ' +
                               str(userBalance) + ' credits')
            return
        elif userBet <= 0:
            await printMessage('only positive bets')
            return
        else:
            updateBalance(message.author, -userBet)

        # cwd = os.getcwd()  # Get the current working directory (cwd)
        # files = os.listdir(cwd)  # Get all the files in that directory
        # print("Files in %r: %s" % (cwd, files))

        if checkDict(message.author) == -1:
            addUserToDict(
                message.author)  # adds the message author on the user balance.txt file

        global deck, dealer_cards, players, player_cards, gamestate
        deck = Deck()
        dealer_cards = Hand()
        dealer_cards.add_card(deck.draw(2))
        players = [dealer_cards]
        player_cards = Hand()
        player_cards.add_card(deck.draw(2))
        players.append(player_cards)
        gamestate = True
        # DEALER CODE
        while players[0].not_done:
            sum = players[0].sum_cards()
            if sum >= 17:
                players[0].done()
            else:
                players[0].add_card(deck.draw(1))
        if player_cards.sum_cards() == 21 and len(player_cards.get_cards()) == 2:
            player_sum = players[1].sum_cards()
            dealer_sum = players[0].sum_cards()
            if player_sum != dealer_sum or len(players[1].get_cards()) != len(
                    players[1].get_cards()):
                gamestate = False
                userBet = userBet * 2.5
                updateBalance(message.author, int(userBet))
                await print_res("**BLACKJACK!**", players[1], players[0])
            else:
                gamestate = False  #
                updateBalance(message.author, userBet)
                await print_res("**You tied!**", players[1], players[0])

        else:
            await print_res('', players[1], players[0])

    elif message.content.lower() == "stay" and gamestate == True:
        gamestate = False
        player_sum = players[1].sum_cards()
        dealer_sum = players[0].sum_cards()
        if dealer_sum > 21 or player_sum > dealer_sum:
            userBet = userBet * 2
            updateBalance(message.author, userBet)
            await print_res(f"**You Won!**", players[1], players[0])
        elif player_sum == dealer_sum:
            updateBalance(message.author, userBet)
            await print_res("**Tie!**", players[1], players[0])
        elif dealer_sum > player_sum:
            await print_res("**You Lose!**", players[1], players[0])
        else:
            await print_res("**this shouldn't happen**", players[1], players[0])

    elif message.content.lower() == "hit" and gamestate:
        players[1].add_card(deck.draw(1))
        sum = players[1].sum_cards()
        if sum > 21:
            players[1].checkHandAceValue(
            )  # checks the hand for an ace and changes the ace's value from 11 -> 1
            sum = players[1].sum_cards()
        if sum > 21:
            players[1].done()
            gamestate = False
            await print_res("**🚫 Bust!**", players[1], players[0])
        elif sum == 21:  # and len(players[1].get_cards()) == 2
            gamestate = False
            userBet = userBet * 2
            updateBalance(message.author, userBet)
            await print_res("**You Win!**", players[1], players[0])
            players[1].done()
        elif sum < 21:
            await print_res('', players[1], players[0])
    await bot.process_commands(message)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


bot.run('ODk4OTAwMTg3OTY2MjE4MjUy.Gt4uHK.uXvJ5X5JGMILiSZXgCzxCkF2dYEzh4e7z0NGO0')
