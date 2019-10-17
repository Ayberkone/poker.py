import random


class Card(object):
    def __init__(self, name, value, suit, symbol):
        self.value = value
        self.suit = suit
        self.name = name
        self.showing = False
        self.symbol = symbol

    def __repr__(self):
        if self.showing:
            return self.symbol
        else:
            return "Card"


class Deck(object):
    def shuffle(self, times=1):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop(0)


class StandardDeck(Deck):
    def __init__(self):
        self.cards = []
        suits = {"Hearts": "♥", "Spades": "♠", "Diamonds": "♦", "Clubs": "♣"}
        values = {
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5,
            "Six": 6,
            "Seven": 7,
            "Eight": 8,
            "Nine": 9,
            "Ten": 10,
            "Jack": 11,
            "Queen": 12,
            "King": 13,
            "Ace": 14
        }
        for name in values:
            for suit in suits:
                symbolIcon = suits[suit]
                if values[name] < 11:
                    symbol = str(values[name]) + suits[suit]
                else:
                    symbol = name[0] + symbolIcon
                self.cards.append(Card(name, values[name], suit, symbol))

    def __repr__(self):
        return "Standard deck of cards\n{0} cards remaining".format(len(self.cards))


class Player(object):
    def __init__(self):
        self.cards = []

    def cardCount(self):
        return len(self.cards)

    def addCard(self, card):
        self.cards.append(card)


class PokerScorer(object):
    def __init__(self, cards):
        # Number of Cards
        self.cards = cards

    def suits(self):
        suits = [card.suit for card in self.cards]
        return list(set(suits))

    def flush(self):
        suits = [card.suit for card in self.cards]
        if len(set(suits)) == 1:
            return True
        return False

    def straight(self):
        values = [card.value for card in self.cards]
        values.sort()

        if not len(set(values)) == 5:
            return False

        if values[4] == 14 and values[3] == 5 and values[2] == 4 and values[1] == 3 and values[0] == 2:
            return 5
        else:
            for i in range(4):
                if not values[i] + 1 == values[i+1]:
                    return False
        return values[4]

    def highCard(self):
        values = [card.value for card in self.cards]
        highCard = None

        for card in self.cards:
            if highCard is None:
                highCard = card
            elif highCard.value < card.value:
                highCard = card

        return highCard

    def highestCount(self):
        count = 0
        values = [card.value for card in self.cards]
        for value in values:
            if values.count(value) > count:
                count = values.count(value)
        return count

    def pairs(self):
        pairs = []
        values = [card.value for card in self.cards]
        for value in values:
            if values.count(value) == 2 and value not in pairs:
                pairs.append(value)

        return pairs

    def fourKind(self):
        values = [card.value for card in self.cards]
        for value in values:
            if values.count(value) == 4:
                return True

    def fullHouse(self):
        two = False
        three = False
        values = [card.value for card in self.cards]

        if values.count(values) == 3:
            three = True
        elif values.count(values) == 2:
            two = True

        if two and three:
            return True

        return False


def Play():
    player = Player()

    # Inital Amount
    points = 100

    # Cost per hand
    handCost = 5

    end = False
    while not end:
        print('----------------------')
        print('You have {0} points'.format(points))
        print('----------------------')

        print()

        points -= handCost

        # Hand Loop
        discard = []
        deck = StandardDeck()
        deck.shuffle()

        # Deal Out
        for i in range(5):
            player.addCard(deck.deal())
        for card in player.cards:
            card.showing = True
        # Hold/Pass

        for card in player.cards:
            card.showing = True
        print(player.cards)
        print('______________________')

        validInput = None
        while not validInput:
            print('Which cards u wanna hold?')
            print('* Hit return to hold all')

            inputStr = input()
            try:
                inputList = [int(inp.strip())
                             for inp in inputStr.split(",") if inp]

                for inp in inputList:
                    if inp > 6:
                        continue
                    if inp < 1:
                        continue

                for inp in inputList:
                    player.cards[inp-1] = deck.deal()
                    player.cards[inp-1].showing = True

                validInput = True
            except:
                print("Input Error: use commas")

        print()
        print(player.cards)

        # Score
        score = PokerScorer(player.cards)
        straight = score.straight()
        flush = score.flush()
        highCount = score.highestCount()
        pairs = score.pairs()
        
        # Royal Flush
        if straight and flush == 14:
            print('Royal Flush !!!')
            points += 2000
            print('+2000')

        # Straight Flush
        elif straight and flush:
            print('Straight Flush !!!')
            points += 250
            print('+250')

        # 4 of a Kind
        elif score.fourKind():
            print('Four of a Kind !!!')
            points += 125
            print('+125')

        # Full House
        elif score.fullHouse():
            print('Full House !!!')
            points += 40
            print('+40')

        # Flush
        elif score.flush():
            print('Flush !!!')
            points += 25
            print('+25')

        # Straight
        elif score.straight():
            print('Straight !!!')
            points += 20
            print('+20')

        # 3 of a Kind
        elif highCount == 3:
            print('Three of a Kind !!!')
            points += 20
            print('+20')

        # 2 Pairs
        elif len(pairs) == 2:
            print('2 Pairs !!!')
            points += 10
            print('+10')

        # High Card
        elif pairs and pairs[0] > 10:
            print('High Card !!!')
            points += 5
            print('+5')

        player.cards = []

        print()
        print()
