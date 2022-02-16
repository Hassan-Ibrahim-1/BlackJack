from time import sleep
from os import system
from random import shuffle

clear = lambda : system("clear") # system("cls")

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

game_over = False


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[self.rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:

    def __init__(self):
        self.cards = []

        for suit in suits:
            for rank in ranks:
                card = Card(suit, rank)
                self.cards.append(card)

    def __str__(self):
        all_cards = ''
        for card in self.cards:
            all_cards = all_cards + card.__str__() + '\n'
        return all_cards

    def shuffle(self):
        shuffle(self.cards)

    def deal(self):
        card = self.cards.pop()
        return card


class Player:

    def __init__(self, bal):
        self.bal = bal
        self.cards = []
        self.value = 0
        self.aces = 0

    def deposit(self, amount):
        self.bal += amount

    def withdraw(self, amount):

        if amount.isdigit():
            amount = int(amount)
        else:
            clear()
            print("Invalid Value!")
            return False

        if self.bal < amount:
            clear
            print("Your bet can't exceed", self.bal)
            return False
        else:
            self.bal -= amount
            return True

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == 'Ace' or card.value == 11:
            self.aces += 1
        if self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1


    def __str__(self):
        all_cards = ''
        for card in self.cards:
            all_cards = all_cards + card.__str__() + ', '
        all_cards = all_cards[ : len(all_cards) - 2]

        if game_over == True:
            return f'\n\nPlayer:\n  Balance: {self.bal}\n  Cards: {all_cards}\n  Total: {self.value}'

        else: 
            return f'\n\nPlayer:\n  Cards: {all_cards}\n  Total: {self.value}'

class Dealer:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0


    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == 'Ace' or card.value == 11:
            self.aces += 1
        if self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1


    def __str__(self):
        if game_over == False:
            return f'\n\nDealer:\n  Cards: {self.cards[0]}, ?\n  Total: ?'

        else:
            all_cards = ''
            for card in self.cards:
                all_cards = all_cards + card.__str__() + ', '
            all_cards = all_cards[ : len(all_cards) - 2]
            return f'\n\nDealer:\n  Cards: {all_cards}\n  Total: {self.value}'



def place_bet():
    while True:
        print(f'Balance: {player.bal}')
        bet = input("Place your bet: ")
        check = player.withdraw(bet)

        while not check:
            sleep(0.6)
            clear()
            print(f'Balance: {player.bal}')
            bet = input("Place your bet: ")
            check = player.withdraw(bet)
        break

def game():
    global game_over

    player.add_card(deck.deal())
    player.add_card(deck.deal())
    dealer.add_card(deck.deal())
    dealer.add_card(deck.deal())

    while not game_over:
        pass


if __name__ == "__main__":    
    player = Player(bal=100)
    deck = Deck()
    deck.shuffle()
    dealer = Dealer()
    place_bet()