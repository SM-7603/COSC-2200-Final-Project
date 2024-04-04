from deck import Deck
from player import AIPlayer, Player

class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player("Human")
        self.ai_player = AIPlayer()
        self.trump_suit = None
        self.table_cards = []

    def setup_game(self):
        self.deck.shuffle()
        # Deal 6 cards to each player
        for _ in range(6):
            self.player.draw_card(self.deck)
            self.ai_player.draw_card(self.deck)
        # Determine the trump suit
        self.trump_suit = self.deck.cards[-1].suit
        print(f"The trump suit is {self.trump_suit}")

    def start_game_loop(self):
        attacking_player = self.player

        while self.player.hand and self.ai_player.hand:
            print("\nNew round!")
            self.table_cards.clear()

            # Attacking phase
            print(f"\n{attacking_player.name} is attacking.")
            self.attack(attacking_player)
            defending_player = self.ai_player if attacking_player == self.player else self.player

            # Defending phase
            self.defend(defending_player)

            if not defending_player.hand:
                print(f"{defending_player.name} couldn't defend. Taking cards...")
                defending_player.hand.extend(self.table_cards)
                self.table_cards.clear()
                if defending_player == self.player:
                    print("AI wins this round!")
                else:
                    print("You win this round!")
                attacking_player = self.ai_player if defending_player == self.player else self.player
                self.redistribute_cards(attacking_player)

        print("\nGame over!")

    def attack(self, player):
        print(f"\nYour hand: {', '.join(map(str, self.player.hand))}")
        print(f"AI hand: {', '.join(map(str, self.ai_player.hand))}")
        while True:
            card_index = int(input("Enter the index of the card you wish to play (0-based), or 'q' to quit: "))
            if card_index == 'q':
                print("You chose to quit. AI wins this round!")
                self.table_cards.clear()
                attacking_player = self.ai_player
                self.redistribute_cards(attacking_player)
                break
            if card_index >= len(player.hand):
                print("Invalid card index. Try again.")
                continue
            played_card = player.play_card(card_index)
            print(f"{player.name} played: {played_card}")
            self.table_cards.append(played_card)
            break

    def defend(self, player):
        print(f"\n{player.name} is defending.")
        ai_played_card = player.play_card(self)
        if ai_played_card is not None:
            print(f"{player.name} played: {ai_played_card}")
            if ai_played_card.suit == self.table_cards[-1].suit:
                if ai_played_card.rank > self.table_cards[-1].rank:
                    print(f"{player.name} wins this round.")
                    return
            elif ai_played_card.suit == self.trump_suit:
                print(f"{player.name} played trump card.")
                return
        print(f"{player.name} couldn't defend. Taking cards...")
        player.hand.extend(self.table_cards)
        self.table_cards.clear()

    def redistribute_cards(self, winning_player):
        losing_player = self.player if winning_player == self.ai_player else self.ai_player
        losing_player.hand.extend(self.table_cards)
        self.table_cards.clear()
        while len(winning_player.hand) < 6 and self.deck.cards:
            winning_player.draw_card(self.deck)

if __name__ == "__main__":
    game = Game()
    game.setup_game()
    game.start_game_loop()
