import random


class Card:

    def __init__(self, value, points, suit):
        self.value = value
        self.points = value
        if value in ["J", "Q", "K"]:
            self.points = 10
        elif value == "A":
            self.points = 11
        self.suit = suit

    def getCardValue(self):
        return self.value

    def getCardPoints(self):
        return self.points

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

    def addCard(self, cards):
        for card in cards:
            self.deck.append(card)

    def sumCards(self):
        sum = 0
        for card in self.deck:
            sum += card.getCardPoints()
        return sum

    def dealerCheckHandAceValue(self, dealer):
        for card in self.deck:
            if card.getCardPoints() == 11:
                card.points = 1
                return self.deck, dealer.notDone(
                )  # so multiple aces dont get turned into 1 pt value
        return self.deck

    def checkHandAceValue(self):
        for card in self.deck:
            if card.getCardPoints() == 11:
                card.points = 1
        return self.deck

    def sumFirstCard(self):
        return self.deck[0].getCardPoints()

    def dealerPrint(self):
        return self.deck[0].string()

    def printCards(self):
        ret_str = ""
        for card in self.deck:
            ret_str += card.string() + ", "
        return ret_str[0:len(ret_str) - 2]

    def done(self):
        self.not_done = False

    def notDone(self):
        self.not_done = True

    def getCards(self):
        return self.deck


async def printResult(text, player, dealer, channel):
    if text != '':  # when the game has ended
        await channel.send(text + "\n> Your cards are " + player.printCards() +
                           ' (' + str(player.sumCards()) + ')' + "\n> Dealer has " +
                           dealer.printCards() + ' (' + str(dealer.sumCards()) +
                           ')' + "\n> Scores: You: " + str(player.sumCards()) +
                           " vs. Dealer: " + str(dealer.sumCards()))
    else:  # for the ongoing game
        message = await channel.send('Your cards are ' + player.printCards() + ' (' +
                           str(player.sumCards()) + ')' + '\nDealer has ' +
                           dealer.dealerPrint() + ' (' +
                           str(dealer.sumFirstCard()) + ')' + '\nhit or stay?') #f'\n> <:approvedmoment:1116670205763010671> to hit or ⛔ stay?')

        reactions = ['<:approvedmoment:1116670205763010671>', '⛔']
        for reaction in reactions:
            await message.add_reaction(reaction)
