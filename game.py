import random
from deck import Deck
from player import AIPlayer, Player

class Game:
    def __init__(self, app=None):
        self.deck = Deck()
        self.player = Player("Human")
        self.ai_player = AIPlayer()
        self.trump_suit = None
        self.table_cards = []
        self.current_attacker = None
        self.winning_player = None
        self.losing_player = None
        self.app = app  # Store the DurakApp instance

    def setup_game(self):
        self.deck.shuffle()
        self.current_attacker = self.player  # Let's assume the human player starts as the attacker
        # Deal 6 cards to each player
        for _ in range(6):
            self.player.draw_card(self.deck)
            self.ai_player.draw_card(self.deck)
        # Determine the trump suit
        self.trump_suit = self.deck.cards[-1].suit
        print(f"The trump suit is {self.trump_suit}")
        # Print the number of cards left in the deck
        print(f"Number of cards left in the deck: {len(self.deck.cards)}")

    # This is a placeholder method and should be updated based on actual logic and variables names
    def end_round(self):
        # Determine if the attacker won the round
        attacker_won = self.game.did_attacker_win()

        if attacker_won:
            # Attacker wins the round
            self.append_output("Attacker wins the round!")
            losing_player = self.game.current_defender
            winning_player = self.game.current_attacker
        else:
            # Defender wins the round
            self.append_output("Defender wins the round!")
            losing_player = self.game.current_attacker
            winning_player = self.game.current_defender

        # Call the redistribute method
        self.game.redistribute_cards(losing_player, winning_player)

        # Prepare for new round
        self.prepare_for_new_round()
        
    def prepare_for_new_round(self):
        # Clear table cards and other round-specific state
        self.game.table_cards.clear()

        # Switch roles if defender won
        if self.game.current_defender and not self.game.did_attacker_win():
            self.game.current_attacker, self.game.current_defender = self.game.current_defender, self.game.current_attacker

        # Update the GUI for the new round
        self.update_game_state()

    def update_game_state(self):
        # Update the GUI with the current game state
        self.update_card_options()  # Update the cards displayed to the player
        # Update other elements like who is attacking/defending, etc.
        if self.game.current_attacker == self.game.player:
            self.append_output("You are attacking.")
        else:
            self.append_output("You are defending.")


    def did_attacker_win(self):
        # If there are an odd number of cards, it means the last attack was not defended.
        if len(self.table_cards) % 2 != 0:
            return True  # Attacker wins because the last card was not defended
        
        # Check if all attack cards were beaten by defend cards
        for attack_card, defend_card in self.table_cards:
            if not self.is_defend_successful(attack_card, defend_card):
                return True  # Attacker wins because at least one card was not successfully defended
        
        return False  # Defender won because they beat all attacks

    def is_defend_successful(self, attack_card, defend_card):
        # Assuming Card class has suit and rank attributes
        if defend_card.suit == attack_card.suit and defend_card.rank > attack_card.rank:
            return True  # Same suit and higher rank beats the attack card
        elif defend_card.suit == self.trump_suit and attack_card.suit != self.trump_suit:
            return True  # A trump suit beats any non-trump suit
        return False  # Defense was not successful


    def start_game(self):
        self.game = Game()  # Initialize the game
        self.game.setup_game()  # Set up the game (shuffle, deal cards, determine trump)
        self.display_game()  # Update the GUI based on the initial game state


    def start_game_loop(self):
        attacking_player = random.choice([self.player, self.ai_player])

        while self.player.hand and self.ai_player.hand:
            print("\nNew round!")

            # Attacking phase
            print(f"\n{attacking_player.name} is attacking.")

            if isinstance(attacking_player, AIPlayer):
                self.ai_attack(attacking_player)
            else:
                self.attack(attacking_player)

            defending_player = self.ai_player if attacking_player == self.player else self.player

            # Defending phase
            if isinstance(defending_player, AIPlayer):
                self.ai_defend(defending_player)
            else:
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
                self.redistribute_cards()

        print("\nGame over!")

    def attack(self, player, card):
        if card in player.hand:
            player.hand.remove(card)  # Remove the card from the player's hand
            self.table_cards.append(card)  # Add the card to the table
            print(f"{player.name} played: {card}")
            # Additional game state updates go here, if any
        else:
            print(f"Card {card} is not in {player.name}'s hand.")

    def ai_attack(self):
        played_card = self.ai_player.play_card()
        if played_card:
            self.table_cards.append(played_card)  # Add the card to the table
            print(f"{self.ai_player.name} played: {played_card}")
            # Additional game state updates go here, if any
        else:
            print("AI couldn't play a card. GAME OVER")
            # Handle game over condition here...
            

    def defend(self, defending_player, attacking_card, defending_card):
        if defending_player.can_defend_with(attacking_card, defending_card):
            self.table_cards.append(defending_card)
            defending_player.hand.remove(defending_card)
            # Proceed with game logic after a successful defense
        else:
            # The defense was unsuccessful, handle the case where the player has to take the cards
            defending_player.take_cards(self.table_cards)
            self.table_cards.clear()
            # Update players for the next turn
            self.switch_players()

    def ai_defend(self):
        # AI should select the best card to defend with
        attacking_card = self.table_cards[-1]  # The last played card which AI has to defend against
        defending_card = self.ai_player.select_card_to_defend(attacking_card)

        if defending_card:
            self.table_cards.append(defending_card)
            self.ai_player.hand.remove(defending_card)
            # AI successfully defended, proceed with the game logic
        else:
            # AI couldn't defend and takes the cards
            self.ai_player.take_cards(self.table_cards)
            self.table_cards.clear()
            # Update players for the next turn
            self.switch_players()

    def redistribute_cards(self, winner):
        # Check who the winner is to determine the order of card distribution.
        if winner == self.player:
            order = [self.player, self.ai_player]
        else:
            order = [self.ai_player, self.player]
        
        for player in order:
            while len(player.hand) < 6 and self.deck.cards:
                player.hand.append(self.deck.deal())

        # Make sure to update the GUI if there's a change in the hands
        self.app.update_game_state()

if __name__ == "__main__":
    game = Game()
    game.setup_game()
    game.start_game_loop()


    