from deck import Deck
from player import AIPlayer, Player

class Game:
    def __init__(self):
        # Initialize the game with a deck, human player, AI player, trump suit, and table cards
        self.deck = Deck()                   # Create a new deck
        self.player = Player("Human")        # Create a human player object
        self.ai_player = AIPlayer()          # Create an AI player object
        self.trump_suit = None               # Initialize trump suit to None
        self.table_cards = []                # Initialize an empty list to hold cards on the table

    def setup_game(self):
        # Shuffle the deck and deal 6 cards to each player
        self.deck.shuffle()
        for _ in range(6):
            self.player.draw_card(self.deck)        # Human player draws a card
            self.ai_player.draw_card(self.deck)     # AI player draws a card
        
        # Determine the trump suit by taking the suit of the last card in the deck
        self.trump_suit = self.deck.cards[-1].suit
        print(f"The trump suit is {self.trump_suit}")

    def start_game_loop(self):
        # Start the game loop until either the human player or the AI player runs out of cards
        attacking_player = self.player

        while self.player.hand and self.ai_player.hand:
            print("\nNew round!")
            self.table_cards.clear()

            # Attacking phase: Player attacks first
            print(f"\n{attacking_player.name} is attacking.")
            self.attack(attacking_player)

            # Defending phase: Opponent defends
            defending_player = self.ai_player if attacking_player == self.player else self.player
            self.defend(defending_player)

            # Check if the defending player couldn't defend and take cards from the table
            if not defending_player.hand:
                print(f"{defending_player.name} couldn't defend. Taking cards...")
                defending_player.hand.extend(self.table_cards)
                self.table_cards.clear()
                if defending_player == self.player:
                    print("AI wins this round!")
                else:
                    print("You win this round!")
                
                # Switch attacking player for the next round
                attacking_player = self.ai_player if defending_player == self.player else self.player
                self.redistribute_cards(attacking_player)

        print("\nGame over!")

    def attack(self, player):
        # Display hands and let the player choose a card to attack with
        print(f"\nYour hand: {', '.join(map(str, self.player.hand))}")
        print(f"AI hand: {', '.join(map(str, self.ai_player.hand))}")
        
        while True:
            card_index = int(input("Enter the index of the card you wish to play (0-based), or 'q' to quit: "))
            if card_index == 'q':
                # If the player chooses to quit, AI wins this round
                print("You chose to quit. AI wins this round!")
                self.table_cards.clear()
                attacking_player = self.ai_player
                self.redistribute_cards(attacking_player)
                break
            if card_index >= len(player.hand):
                print("Invalid card index. Try again.")
                continue
            
            # Player plays the selected card
            played_card = player.play_card(card_index)
            print(f"{player.name} played: {played_card}")
            self.table_cards.append(played_card)
            break

    def defend(self, player):
        # Display the defending player and let them play a card to defend
        print(f"\n{player.name} is defending.")
        ai_played_card = player.play_card(self)
        
        if ai_played_card is not None:
            print(f"{player.name} played: {ai_played_card}")
            # Check if the defending card beats the card played by the attacker
            if ai_played_card.suit == self.table_cards[-1].suit:
                if ai_played_card.rank > self.table_cards[-1].rank:
                    print(f"{player.name} wins this round.")
                    return
            elif ai_played_card.suit == self.trump_suit:
                print(f"{player.name} played trump card.")
                return
        
        # If the defending player couldn't defend, take cards from the table
        print(f"{player.name} couldn't defend. Taking cards...")
        player.hand.extend(self.table_cards)
        self.table_cards.clear()

    def redistribute_cards(self, winning_player):
        # Redistribute cards from the table to the winning player and draw new cards if necessary
        losing_player = self.player if winning_player == self.ai_player else self.ai_player
        losing_player.hand.extend(self.table_cards)  # Add cards from the table to the losing player's hand
        self.table_cards.clear()

        # Draw cards until the winning player has 6 cards or the deck is empty
        while len(winning_player.hand) < 6 and self.deck.cards:
            winning_player.draw_card(self.deck)

if __name__ == "__main__":
    # Create a game object and start the game
    game = Game()
    game.setup_game()
    game.start_game_loop()
