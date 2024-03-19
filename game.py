# game.py
from deck import Deck
from player import Player, AIPlayer

class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player("Human")
        self.ai_player = AIPlayer()
        self.trump_suit = None

    def setup_game(self):
        self.deck.shuffle()
        self.trump_suit = self.deck.cards[-1].suit  # Determine the trump suit
        print(f"The trump suit is {self.trump_suit}")
        
        # Deal 6 cards to each player
        for _ in range(6):
            self.player.draw_card(self.deck)
            self.ai_player.draw_card(self.deck)

    def start_game_loop(self):
        # The main game loop
        while self.player.hand and self.ai_player.hand:
            print(f"\nYour hand: {', '.join(map(str, self.player.hand))}")
            print(f"Cards left in deck: {len(self.deck.cards)}")
            card_index = int(input("Enter the index of the card you wish to play (0-based): "))
            played_card = self.player.play_card(card_index)
            print(f"You played: {played_card}")
            
            ai_played_card = self.ai_player.play_card(self)
            print(f"AI played: {ai_played_card}")
            
            # Simple bout win logic, assuming higher rank wins and trump suit beats other suits
            if played_card.suit == ai_played_card.suit:
                bout_winner = "You" if played_card.rank > ai_played_card.rank else "AI"
            elif played_card.suit == self.trump_suit:
                bout_winner = "You"
            elif ai_played_card.suit == self.trump_suit:
                bout_winner = "AI"
            else:
                bout_winner = "You"  # If neither card is a trump, the player wins by default in this simplified logic
            print(f"{bout_winner} wins this round.")
            
            # Draw cards until each player has 6 cards or the deck is empty
            while len(self.player.hand) < 6 and self.deck.cards:
                self.player.draw_card(self.deck)
                self.ai_player.draw_card(self.deck)
            
            # Check if someone has won
            if not self.player.hand and not self.ai_player.hand:
                print("It's a draw! No cards left.")
                break
            elif not self.player.hand:
                print("You win!")
                break
            elif not self.ai_player.hand:
                print("AI wins!")
                break

        print("\nGame over!")
