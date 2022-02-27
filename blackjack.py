from time import sleep
from os import system
from random import shuffle

clear = lambda : system("clear") # system("cls")

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

game_over = False
replaying = False


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

        if amount.lower() in ['q', 'quit', 'exit']:
                quit()

        if amount.isdigit():
            amount = int(amount)
        else:
            clear()
            print("Invalid Value!")
            return False

        if self.bal < amount:
            clear
            print(f"Your bet can't exceed {self.bal}")
            return False
        else:
            self.bal -= amount
            return True

    def add_card(self, card):
        global game_over

        self.cards.append(card)
        self.value += card.value
        if card.rank == 'Ace' or card.value == 11:
            self.aces += 1
        if self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

        if self.value == 21:
            game_over = True
            player_win()
        if self.value > 21:
            clear()
            print("You went over 21 and busted!")
            sleep(0.5)
            game_over = True
            dealer_win()



    def __str__(self):
        global game_over

        all_cards = ''
        for card in self.cards:
            all_cards = all_cards + card.__str__() + ', '
        all_cards = all_cards[ : len(all_cards) - 2]

        if game_over == True:
            return f'\n\nPlayer:\n  Balance: {self.bal}\n  Cards: {all_cards}\n  Total: {self.value}'

        elif game_over == False: 
            return f'\nPlayer:\n  Cards: {all_cards}\n  Total: {self.value}'

class Dealer:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0


    def add_card(self, card):
        global game_over

        self.cards.append(card)
        self.value += card.value
        if card.rank == 'Ace' or card.value == 11:
            self.aces += 1
        if self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

        if self.value == 21:
            game_over = True
            dealer_win()
        if self.value > 21:
            clear()
            print("The dealer went over 21 and busted!")
            sleep(0.5)
            game_over = True
            player_win()

    def __str__(self):
        global game_over

        if game_over == False:
            return f'\n\nDealer:\n  Cards: {self.cards[0]}, ?\n  Total: ?'

        elif game_over == True:
            all_cards = ''
            for card in self.cards:
                all_cards = all_cards + card.__str__() + ', '
            all_cards = all_cards[ : len(all_cards) - 2]
            return f'\n\nDealer:\n  Cards: {all_cards}\n  Total: {self.value}'


def place_bet():
    global bet

    while True:
        print(f'Balance: {player.bal}')
        bet = input("Place your bet: ")
        choice = player.withdraw(bet)

        while not choice:
            sleep(0.6)
            clear()
            print(f'Balance: {player.bal}')
            bet = input("Place your bet: ")
            choice = player.withdraw(bet)
        break

def player_win():
    clear()
    global game_over
    game_over = True
    clear()
    print("You won!")
    player.deposit(int(bet)*2)
    sleep(0.5)
    print(player)
    print(dealer)

    replay()

def dealer_win():
    clear()
    global game_over
    game_over = True
    print("The dealer won!")
    sleep(0.5)

    print(player)
    print(dealer)
    replay()

def tie():
    clear()
    global game_over
    game_over = True
    print("Tie!")
    sleep(0.5)

    print(player)
    print(dealer)
    replay()


def replay():
    global replaying

    choice = input("\nPlayer again (Y or N): ")
    while choice.lower() not in ['y', 'yes', 'n', 'no', 'q', 'quit', 'exit']:
        clear()
        choice = input("\nPlayer again (Y or N): ")

    if choice.lower() in ['y', 'yes']:
        replaying = True
        game()
            
    elif choice.lower() in ['n', 'no', 'q', 'quit', 'exit']:
        quit()




def game():
    global game_over
    global replaying
    global deck
    global player
    global dealer


    if replaying:
        clear() 
        print("Welcome to Black Jack!")
        print("\nEnter 'q' to quit the game.")
        sleep(1)
        clear()
        
        deck = Deck()
        deck.shuffle()
        player = Player(bal=player.bal)
        dealer = Dealer()

        game_over = False
        stay = False
        deck = Deck()
        deck.shuffle()
        dealer = Dealer()
    
    else:
        game_over = False
        stay = False

    
    place_bet()

    player.add_card(deck.deal())
    player.add_card(deck.deal())
    dealer.add_card(deck.deal())
    dealer.add_card(deck.deal())

    while not game_over:
        while True:
            clear()
            print(player)
            print(dealer)
            choice = input("\nHit or Stay: ")
            if choice.lower() in ['h', 'hit', 'deal']:
                player.add_card(deck.deal())
                break
            elif choice.lower() in ['s', 'stop', 'stay']:
                stay = True
                break
            elif choice.lower() in ['q', 'quit', 'exit']:
                quit()

        if stay:
            while dealer.value < 17:
                dealer.add_card(deck.deal())

            if dealer.value > player.value:
                dealer_win()          
            elif player.value > dealer.value:
                player_win()
            elif dealer.value == player.value:
                tie()




if __name__ == "__main__":
    clear() 
    print("Welcome to Black Jack!")
    print("\nEnter 'q' to quit the game.")
    sleep(1)
    clear()

    player = Player(bal=100)
    deck = Deck()
    deck.shuffle()
    dealer = Dealer()
    game()
