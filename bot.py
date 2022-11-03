import discord
import random
#import os

TOKEN = '' #token here

intents = discord.Intents.all()
intents.members = True

client = discord.Client(command_prefix="$", intents=intents)


@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='Plebs')
    channel = client.get_channel(401071542110388257)  # channela id
    await member.add_roles(role)
    await channel.send(f'> Hey {member.mention}, welcome to **HeHeXD**')


@client.event
async def on_member_remove(member):
    member_name = str(member).split('#')[0]
    channel = client.get_channel(401071542110388257)  # channela id
    await channel.send(f'> **{member_name}** finally pissed off')


def append(member):
    with open("UserBalance.txt", 'r+') as f:
        old = f.read()  # read everything in the file
        f.seek(0)  # rewind
        f.write(f'{member} : 0\n' + old)  # write the new line before
        f.close()


def checkDict(member):
    with open(r'UserBalance.txt', 'r+') as file:
        data = file.read()
        res = data.find(str(member))
        file.close()
        return res



@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    channel = str(message.channel.name)
    content = str(message.content)

    print(f'{username}: {content} ({channel})')

    if message.author == client.user:
        return

    s = random.randint(0, 500)
    if s > 499:
        await message.channel.send(f'yes but who asked?')
        return


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

    def print_card(self):
        return str(self.value) + self.suit + " with " + str(self.points) + " points"


class Deck:
    def __init__(self):
        self.deck = []
        # suits = ["Hearts", "Spades", "Diamonds", "Clubs"]
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

    def sumFirstCard(self):
        return self.deck[0].get_points()

    def dealer_print(self):
        return self.deck[0].string()

    def print_cards(self):
        ret_str = ""
        for card in self.deck:
            ret_str += card.string() + ", "
        return ret_str[0:len(ret_str) - 2]

    def ask_A(self):
        channel_general = client.get_channel(898900471618621453)  # channela id
        num_A = []
        for c in range(0, len(self.deck)):
            if self.deck[c].get_value() == "A" and self.deck[c].get_points() == 11:
                num_A.append(c)
        for i in num_A:
            # print("Your cards are " + str(self.print_cards()) + ", Total is " + str(self.sum_cards()) + "\n")
            channel_general.send(
                "Your cards are " + str(self.print_cards()) + ", Total is " + str(self.sum_cards()) + "\n")
            val = str("Change an A from 11 points to 1 point? (Y or N): ")
            if val != "Y" and val != "N":
                print("Please answer with Y or N")
            elif val == "Y":
                self.deck[i].change_points(1)

            # print(f"Your cards are (" + str(self.sum_cards()) + ") " + str(self.print_cards()) + "\n")
            channel_general.send(f"Your crds are (" + str(self.sum_cards()) + ") " + str(self.print_cards()) + "\n")

    def done(self):
        self.not_done = False

    def get_done(self):
        return self.not_done

    def get_cards(self):
        return self.deck


async def print_res(text, player, dealer):
    channel = client.get_channel(898900471618621453)
    if text != '':  # when the game has ended
        await channel.send(text +
                           "\nYour cards are " + player.print_cards() + ' (' + str(player.sum_cards()) + ')' +
                           "\nDealer has " + dealer.print_cards() + ' (' + str(dealer.sum_cards()) + ')' +
                           "\nScores: You: " + str(player.sum_cards()) + " vs. Dealer: " + str(dealer.sum_cards()))
    else:  # for the ongoing game
        await channel.send('Your cards are ' + player.print_cards() + ' (' + str(player.sum_cards()) + ')' +
                           '\nDealer has ' + dealer.dealer_print() + ' (' + str(dealer.sumFirstCard()) + ')' +
                           '\nhit or stay?')


@client.event
async def on_message(message):

    #print(message.author)

    if message.author == client.user:
        return

    if message.content.lower() == "!blackjack":

        # cwd = os.getcwd()  # Get the current working directory (cwd)
        # files = os.listdir(cwd)  # Get all the files in that directory
        # print("Files in %r: %s" % (cwd, files))

        if checkDict(message.author) == -1:
            append(message.author) # adds the message author on the user balance.txt file

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
            if player_sum != dealer_sum or len(players[1].get_cards()) != len(players[1].get_cards()):
                gamestate = False
                await print_res("**BLACKJACK!**", players[1], players[0])
            else:
                gamestate = False
                await print_res("**You tied!**", players[1], players[0])

        else:
            await print_res('', players[1], players[0])

    elif message.content.lower() == "stay" and gamestate == True:
        gamestate = False
        player_sum = players[1].sum_cards()
        dealer_sum = players[0].sum_cards()
        if dealer_sum > 21 or player_sum > dealer_sum:
            await print_res("**You Won!**", players[1], players[0])
        elif player_sum == dealer_sum:
            await print_res("**Tie!**", players[1], players[0])
        elif dealer_sum > player_sum:
            await print_res("**You Lose!**", players[1], players[0])
        else:
            await print_res("**this shouldn't happen**", players[1], players[0])

    elif message.content.lower() == "hit" and gamestate:
        players[1].add_card(deck.draw(1))
        sum = players[1].sum_cards()
        if sum > 21:
            gamestate = False
            players[1].ask_A()
            sum = players[1].sum_cards()
            if sum > 21:
                players[1].done()
                await print_res("**🚫 Bust!**", players[1], players[0])
        elif sum == 21 and len(players[1].get_cards()) == 2:
            gamestate = False
            await print_res("**BLACKJACK!**", players[1], players[0])
            players[1].done()
        elif sum < 21:
            await print_res('', players[1], players[0])


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


client.run(TOKEN)
