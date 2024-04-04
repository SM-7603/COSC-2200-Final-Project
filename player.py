class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw_card(self, deck):
        # Draw a card from the deck and add it to the player's hand
        card = deck.deal()
        if card:
            self.hand.append(card)

    def play_card(self, index):
        # Play a card from the player's hand at the specified index
        return self.hand.pop(index) if index < len(self.hand) else None

class AIPlayer(Player):
    def __init__(self):
        super().__init__("AI")
        self.played_cards = set()  # Keep track of cards played by the AI player

    def play_card(self, game_state):
        # Get a list of valid cards the AI player can play
        valid_cards = self.get_valid_cards(game_state)
        print(f"AI Valid cards before filtering: {valid_cards}")  # Debugging

        if not valid_cards:
            print("No valid cards to play.")
            return None  # If no valid cards, return None

        # Filter out cards that have already been played
        valid_cards = [card for card in valid_cards if card not in self.played_cards]
        print(f"AI Valid cards after filtering played ones: {valid_cards}")  # Debugging

        if not valid_cards:
            print("All valid cards have already been played.")
            return None  # If all valid cards have been played, return None

        selected_card = None  # Default to None in case no card is selected
        if not game_state.player.hand:
            # It's the AI's first turn, choose the best card based on availability and trump suit
            selected_card = max(valid_cards, key=lambda card: (card.suit == game_state.trump_suit, -card.get_rank_index()))
            reason = "first turn, playing highest card based on trump suitability"
        else:
            # AI is playing after the human
            human_card = game_state.player.hand[0]  # Assuming the first card is the one to beat
            print(f"Human played: {human_card}")  # Debugging
            if human_card.suit == game_state.trump_suit:
                # If human played a trump card
                selected_card = self.play_trump_card(valid_cards, game_state)
                reason = "responding to a trump card"
            else:
                # If human played a non-trump card
                selected_card = self.play_non_trump_card(valid_cards, human_card, game_state)
                reason = "responding to a non-trump card"
        
        if selected_card:
            print(f"AI selects {selected_card} because it's the {reason}.")  # Debugging
            # Remove the selected card from the AI player's hand and mark it as played
            self.hand.remove(selected_card)
            self.played_cards.add(selected_card)
        else:
            print("AI could not select a card based on the logic provided.")

        return selected_card

    def play_trump_card(self, cards, game_state):
        print(f"AI deciding on trump card to play...")
        trump_cards = [card for card in cards if card.suit == game_state.trump_suit]
        print(f"Available trump cards: {trump_cards}")
        
        if trump_cards:
            # Use get_rank_index() for comparison
            bigger_trump = max(trump_cards, key=lambda card: card.get_rank_index())
            smaller_trump = min(trump_cards, key=lambda card: card.get_rank_index())
            print(f"Bigger trump: {bigger_trump}, Smaller trump: {smaller_trump}")
            
            # Assuming game_state.player.hand[0] is the card to beat
            if bigger_trump.get_rank_index() > game_state.player.hand[0].get_rank_index():
                print(f"AI chooses bigger trump {bigger_trump} over player's card {game_state.player.hand[0]}")
                return bigger_trump
            else:
                print(f"No bigger trump available, choosing smaller trump {smaller_trump}")
                return smaller_trump
        else:
            # No trump cards; play the card with the lowest rank
            lowest_card = min(cards, key=lambda card: card.get_rank_index())
            print(f"No trump cards available, choosing lowest card {lowest_card}")
            return lowest_card

    def play_non_trump_card(self, cards, human_card, game_state):
        print(f"AI deciding on non-trump card to play against {human_card}")
        same_suit_cards = [card for card in cards if card.suit == human_card.suit]
        print(f"Available same suit cards: {same_suit_cards}")
        
        if same_suit_cards:
            # If AI has cards of the same suit as the human player
            bigger_card = max(same_suit_cards, key=lambda card: card.get_rank_index())
            if bigger_card.get_rank_index() > human_card.get_rank_index():
                print(f"AI chooses bigger same suit card {bigger_card} over player's card {human_card}")
                return bigger_card
            else:
                smallest_card = min(same_suit_cards, key=lambda card: card.get_rank_index())
                print(f"No bigger same suit card available, choosing smallest {smallest_card}")
                return smallest_card
        else:
            # If AI doesn't have cards of the same suit as the human player, play the smallest trump card if available
            trump_cards = [card for card in cards if card.suit == game_state.trump_suit]
            print(f"AI has no same suit cards, checking for trump cards...")
            if trump_cards:
                smallest_trump = min(trump_cards, key=lambda card: card.get_rank_index())
                print(f"Choosing smallest trump card {smallest_trump}")
                return smallest_trump
            else:
                lowest_card = min(cards, key=lambda card: card.get_rank_index())
                print(f"No trump cards available, choosing lowest card {lowest_card}")
                return lowest_card

    def get_valid_cards(self, game_state):
        # Distinguish between attacking and defending scenarios
        if game_state.table_cards:  # Assuming this list is populated with cards in play for the round
            # Defending scenario: AI needs to respond to an attack
            attacking_card = game_state.table_cards[-1]  # The card AI needs to defend against
            valid_cards = [card for card in self.hand if self.is_valid_card(card, game_state, attacking_card)]
        else:
            # Attacking scenario: All cards are valid since AI is initiating
            valid_cards = self.hand[:]
        return valid_cards

    def is_valid_card(self, card, game_state, attacking_card=None):
        # For defending: Check if the card can legally beat the attacking card
        if attacking_card:
            if card.suit == attacking_card.suit and card.ranks.index(card.rank) > card.ranks.index(attacking_card.rank):
                # The card is of the same suit and has a higher rank
                return True
            elif card.suit == game_state.trump_suit and attacking_card.suit != game_state.trump_suit:
                # The card is a trump card, and the attacking card is not
                return True
            else:
                return False
        else:
            # Attacking scenario or no specific card to compare against: All cards are valid
            return True

