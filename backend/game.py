# game.py
from tkinter import messagebox
from .deck import Deck
from .player import AIPlayer, Player

class Game:
    def __init__(self, update_gui_callback):
        self.deck = Deck()
        self.player = Player("Human")
        self.ai_player = AIPlayer()
        self.trump_suit = None
        self.table_cards = []
        # This function updates the GUI
        self.update_gui = update_gui_callback  

    def setup_game(self):
        self.deck.shuffle()
        # Deal 6 cards to each player
        for _ in range(6):
            self.player.draw_card(self.deck)
            self.ai_player.draw_card(self.deck)
        # Determine the trump suit
        self.trump_suit = self.deck.cards[-1].suit
        self.current_attacker = self.player  # Assuming the human player always starts
        self.current_defender = self.ai_player
        # Initially update GUI based on game setup
        self.update_gui(message="Game setup complete.", update_cards=True)
        print(f"The trump suit is {self.trump_suit}")
        # Print the number of cards left in the deck
        print(f"Number of cards left in the deck: {len(self.deck.cards)}")
        # GUI update to display trump suit would go here
        if self.update_gui:
            # Call the callback function with the new trump suit
            self.update_gui(f"Trump Suit: {self.trump_suit}")

    
    # New method to handle a card being played
    def handle_card_played(self, card):
        # This method will be called by the GUI when the player plays a card
        # Implement logic to handle the played card here
        
        # Dummy implementation, replace with actual game logic
        if card.suit == self.trump_suit:
            messagebox.showinfo("Info", "You played a trump card!")
        
        # After handling the card play, update the GUI
        if self.update_gui:
            self.update_gui()

    def player_attack(self, card_index):
        # Player initiates an attack
        if card_index < len(self.player.hand):
            played_card = self.player.play_card(card_index)
            self.table_cards.append(played_card)
            self.ai_defend()  # Trigger AI defense after player attack
        else:
            self.update_gui(message="Invalid card index.", update_cards=True)

    def ai_attack(self):
        # AI decides which card to play
        played_card = self.ai_player.decide_card(self)
        self.table_cards.append(played_card)
        self.update_gui(message="AI has attacked.", update_cards=True)
        # Now, wait for player's defense action, which will be triggered by another GUI event

    def player_defend(self, card_index):
        # Player defends against AI's attack
        if self.is_valid_defense(self.player.hand[card_index]):
            played_card = self.player.play_card(card_index)
            self.table_cards.append(played_card)
            self.end_round(successful_defense=True)
        else:
            self.end_round(successful_defense=False)

    def ai_defend(self):
        # AI attempts to defend against player's attack
        for card in self.ai_player.hand:
            if self.is_valid_defense(card):
                self.ai_player.hand.remove(card)
                self.table_cards.append(card)
                self.update_gui(message="AI defended successfully.", update_cards=True)
                self.end_round(successful_defense=True)
                return
        self.end_round(successful_defense=False)

    def is_valid_defense(self, defending_card):
        attacking_card = self.table_cards[-1]
        return (defending_card.suit == attacking_card.suit and defending_card.rank > attacking_card.rank) or \
               (defending_card.suit == self.trump_suit and attacking_card.suit != self.trump_suit)
    
    def start_round(self):
        # Logic to start a new round.
        if self.current_attacker == self.player:
            # Player's turn to attack
            self.update_gui("Human's turn to attack.")
        else:
            # AI's turn to attack
            self.ai_attack()
            self.update_gui("AI's turn, please defend.")

    def is_round_over(self):
        # Check if the round is over, typically when no more moves can be made
        # For example, if the deck is empty and one of the players has no cards left
        return not self.deck.cards and (not self.player.hand or not self.ai_player.hand)
    

    def play_card_from_hand(self, card):
        if self.is_players_turn and self.is_card_playable(card):
            # Remove card from player's hand
            self.player.hand.remove(card)
            # Add card to table cards
            self.table_cards.append(card)
            # Logic to handle the progression of the game, like attacking or defending
            # ...

            # Switch to AI turn
            self.is_players_turn = False
            self.ai_turn()  # You would need to implement this method

    def is_card_playable(self, card):
        # Assuming self.current_attacker and self.current_defender are defined elsewhere in your class
        # And self.table_cards holds the cards currently played in the round
        
        if self.current_attacker == self.player:
            # If the player is attacking, any card can be played
            return True
        elif self.current_defender == self.player:
            # If the player is defending, they must beat the attacking card
            attacking_card = self.table_cards[-1]
            if card.suit == attacking_card.suit and card.get_rank_index() > attacking_card.get_rank_index():
                # The card is of the same suit and has a higher rank, so it's playable
                return True
            elif card.suit == self.trump_suit and attacking_card.suit != self.trump_suit:
                # The card is a trump card and beats any non-trump card
                return True
        
        # If neither condition is met, the card is not playable
        return False
    
    def take_cards_from_table(self):
        # The current defender takes all cards from the table
        self.current_defender.hand.extend(self.table_cards)
        self.table_cards.clear()

    def draw_cards_to_hand(self):
        # Draw cards from the deck until each player has 6 cards or the deck is empty
        while len(self.player.hand) < 6 and self.deck.cards:
            self.player.draw_card(self.deck)
        while len(self.ai_player.hand) < 6 and self.deck.cards:
            self.ai_player.draw_card(self.deck)

    def player_play_card(self, card_index):
        # Simplified logic for playing a card
        if 0 <= card_index < len(self.player.hand):
            card = self.player.hand.pop(card_index)
            # Process the card (e.g., adding it to the table, checking for a win)
            self.table_cards.append(card)
            if self.update_gui:
                self.update_gui(message=f"Played {card}.", update_cards=True)
            # Add logic for AI to respond, etc.

    def process_player_card(self, card):
        pass
        # Example of processing a played card
        # Add card to table, check for win conditions, etc.

    def update_game_state(self):
        pass
        # This could be where you check game state, who's turn it is, win conditions etc.
        # And call `update_gui_callback` with relevant messages or state information

    def end_round(self, successful_defense):
        if not successful_defense:
            # Defender takes all cards from the table if defense fails
            self.defending_player.hand.extend(self.table_cards)
        self.table_cards.clear()
        self.redistribute_cards()
        self.switch_roles()  # Decide who attacks next
        self.update_gui(message="Round ended.", update_cards=True)

    def redistribute_cards(self):
        # Ensure both players have 6 cards if possible
        while len(self.player.hand) < 6 and self.deck.cards:
            self.player.draw_card(self.deck)
        while len(self.ai_player.hand) < 6 and self.deck.cards:
            self.ai_player.draw_card(self.deck)
        self.update_gui(message="Cards redistributed.", update_cards=True)

    def switch_roles(self):
        # Switch roles between player and AI
        self.player, self.ai_player = self.ai_player, self.player
        self.update_gui(message="Roles switched.", update_cards=False)# This function could be triggered by an "end of round" event


if __name__ == "__main__":
    game = Game()
    game.setup_game()
    game.start_game_loop()
