class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw_card(self, deck):
        # Draw a card from the deck and add it to the player's hand
        card = deck.deal()
        if card:
            self.hand.append(card)
            
    def get_valid_card_choices(self):
        # Return a list of strings representing valid card choices
        return [str(card) for card in self.hand]

    def play_card_by_choice(self, card_choice):
        # Adapted play_card method to accept a card choice directly
        for card in self.hand:
            if str(card) == card_choice:
                self.hand.remove(card)
                return card
        return None


    def play_card(self, card):
        # Debugging: print out the hand before attempting to play the card
        print(f"Attempting to play {card}. Current hand: {[str(c) for c in self.hand]}")
        if card in self.hand:
            self.hand.remove(card)
            # Debugging: print out the hand after attempting to play the card
            print(f"Played {card}. New hand: {[str(c) for c in self.hand]}")
            return card
        else:
            print(f"Cannot play {card} as it is not in the hand.")
            return None
    
    def has_valid_card(self, game_state):
        # Check if the player has any valid cards to play
        if game_state.table_cards:
            attacking_card = game_state.table_cards[-1]
            for card in self.hand:
                if self.is_valid_card(card, game_state, attacking_card):
                    return True
            return False
        else:
            return True

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
        reason = ""  # Initialize the reason for card selection

        # Check if there are cards on the table to respond to
        if game_state.table_cards:
            # The card AI needs to beat or respond to
            attacking_card = game_state.table_cards[-1]
            print(f"Card to beat: {attacking_card}")  # Debugging

            # Attempt to play a non-trump card first
            selected_card = self.play_non_trump_card(valid_cards, attacking_card, game_state)
            if selected_card:
                reason = "playing a higher-ranking non-trump card"
            else:
                print("No same suit cards available. AI considering trump cards...")
                # Attempt to play a trump card if a non-trump card is not available
                selected_card = self.play_trump_card(valid_cards, game_state)
                reason = "responding with a trump card" if selected_card else "no valid response available"

        else:
            # It's the AI's turn to attack, choose the best card based on availability and trump suit
            # Check if there are multiple trump cards
            trump_cards = [card for card in valid_cards if card.suit == game_state.trump_suit]
            if trump_cards:
                # If multiple trump cards are available, play the highest one
                selected_card = max(trump_cards, key=lambda card: card.get_rank_index())
                reason = "first turn, playing highest trump card"
            else:
                # If no trump cards are available, play the highest-ranked card
                selected_card = max(valid_cards, key=lambda card: card.get_rank_index())
                reason = "first turn, playing highest card"


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
        attacking_card = game_state.table_cards[-1] if game_state.table_cards else None
        print(f"Attacking card to beat: {attacking_card}")

        trump_cards = [card for card in cards if card.suit == game_state.trump_suit]
        print(f"Available trump cards: {trump_cards}")

        if trump_cards:
            valid_trumps = [card for card in trump_cards if attacking_card and card.get_rank_index() > attacking_card.get_rank_index()]
            selected_card = min(valid_trumps, key=lambda card: card.get_rank_index()) if valid_trumps else min(trump_cards, key=lambda card: card.get_rank_index())

            print(f"Selected trump card: {selected_card} to play against {attacking_card}")
            return selected_card
        else:
            print("No trump cards available to play.")
            return None

    def play_non_trump_card(self, cards, attacking_card, game_state):
        print(f"AI deciding on non-trump card to play against {attacking_card}")
        same_suit_cards = [card for card in cards if card.suit == attacking_card.suit]
        print(f"Available same suit cards: {same_suit_cards}")

        if same_suit_cards:
            valid_cards = [card for card in same_suit_cards if card.get_rank_index() > attacking_card.get_rank_index()]
            selected_card = min(valid_cards, key=lambda card: card.get_rank_index()) if valid_cards else None

            if selected_card:
                print(f"Selected same suit card: {selected_card} to play against {attacking_card}")
                return selected_card
            else:
                print("No higher same suit cards available. AI may need to play a trump card or take the attacking card.")
                return None
        else:
            print("No same suit cards available. AI may need to resort to trump cards.")
            return None

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
        if game_state.table_cards:
            attacking_card = game_state.table_cards[-1]

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