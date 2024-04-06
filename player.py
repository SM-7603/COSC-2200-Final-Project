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

        if not valid_cards:
            return None  # If no valid cards, return None

        # Filter out cards that have already been played
        valid_cards = [card for card in valid_cards if card not in self.played_cards]

        if not valid_cards:
            return None  # If all valid cards have been played, return None

        selected_card = None  # Default to None in case no card is selected
        if not game_state.player.hand:
            # It's the AI's first turn, choose the best card based on availability and trump suit
            selected_card = max(valid_cards, key=lambda card: (card.suit == game_state.trump_suit, -card.get_rank_index()))
        else:
            # AI is playing after the human
            human_card = game_state.player.hand[0]  # Assuming the first card is the one to beat
            if human_card.suit == game_state.trump_suit:
                # If human played a trump card
                selected_card = self.play_trump_card(valid_cards, game_state)
            else:
                # If human played a non-trump card
                selected_card = self.play_non_trump_card(valid_cards, human_card, game_state)
        
        if selected_card:
            # Remove the selected card from the AI player's hand and mark it as played
            self.hand.remove(selected_card)
            self.played_cards.add(selected_card)

        return selected_card

    def play_trump_card(self, cards, game_state):
        trump_cards = [card for card in cards if card.suit == game_state.trump_suit]
        
        if trump_cards:
            # Use get_rank_index() for comparison
            bigger_trump = max(trump_cards, key=lambda card: card.get_rank_index())
            smaller_trump = min(trump_cards, key=lambda card: card.get_rank_index())
            
            # Assuming game_state.player.hand[0] is the card to beat
            if bigger_trump.get_rank_index() > game_state.player.hand[0].get_rank_index():
                return bigger_trump
            else:
                return smaller_trump
        else:
            # No trump cards; play the card with the lowest rank
            return min(cards, key=lambda card: card.get_rank_index())

    def play_non_trump_card(self, cards, human_card, game_state):
        same_suit_cards = [card for card in cards if card.suit == human_card.suit]
        
        if same_suit_cards:
            # If AI has cards of the same suit as the human player
            bigger_card = max(same_suit_cards, key=lambda card: card.get_rank_index())
            if bigger_card.get_rank_index() > human_card.get_rank_index():
                return bigger_card
            else:
                return min(same_suit_cards, key=lambda card: card.get_rank_index())
        else:
            # If AI doesn't have cards of the same suit as the human player, play the smallest trump card if available
            trump_cards = [card for card in cards if card.suit == game_state.trump_suit]
            if trump_cards:
                return min(trump_cards, key=lambda card: card.get_rank_index())
            else:
                return min(cards, key=lambda card: card.get_rank_index())

    def get_valid_cards(self, game_state):
        # Distinguish between attacking and defending scenarios
        if game_state.table_cards:  
            # Defending scenario: AI needs to respond to an attack
            attacking_card = game_state.table_cards[-1]  
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
