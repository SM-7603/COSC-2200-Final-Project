import logging

# Configure logging to write to a file, setting the level and format of logs
logging.basicConfig(filename='game_logs.txt', level=logging.INFO, format='%(message)s')

class Player:
    def __init__(self, name):
        self.name = name  # Player's name
        self.hand = []  # List to store the player's cards

    def draw_card(self, deck):
        # Draw a card from the deck
        card = deck.deal()
        # If a card is drawn, add it to the player's hand
        if card:
            self.hand.append(card)

    def play_card(self, index):
        # Play a card from the specified index in the player's hand, if valid
        return self.hand.pop(index) if index < len(self.hand) else None

    def has_valid_card(self, game_state):
        # Determine if there's a valid card in hand to play
        if game_state.table_cards:
            # Get the last played card as the attacking card
            attacking_card = game_state.table_cards[-1]
            # Check each card in hand to see if it's valid
            for card in self.hand:
                if self.is_valid_card(card, game_state, attacking_card):
                    return True
            return False
        else:
            # If there are no cards on the table, any card is considered valid
            return True

    def is_valid_card(self, card, game_state, attacking_card=None):
        # Determine if a card can legally beat the attacking card in a defense situation
        if game_state.table_cards:
            # Get the last played card if attacking card is not provided
            attacking_card = game_state.table_cards[-1]
        else:
            # Assume it's the player's turn to attack; select a card
            attacking_card = self.player.play_card(self.player.card_index)

        if attacking_card:
            # Check if the card matches the suit and outranks the attacking card or if it's a valid trump card
            if card.suit == attacking_card.suit and card.ranks.index(card.rank) > card.ranks.index(attacking_card.rank):
                return True  # Card has the same suit and a higher rank
            elif card.suit == game_state.trump_suit and attacking_card.suit != game_state.trump_suit:
                return True  # Card is a trump card, and the attacking card is not a trump
            else:
                return False
        else:
            # If no card is being attacked, all cards are valid
            return True

class AIPlayer(Player):
    def __init__(self):
        super().__init__("AI")  # Initialize with name "AI"
        self.played_cards = set()  # Set to track cards played by the AI

    def play_card(self, game_state):
        # AI selects a card to play based on the game state
        valid_cards = self.get_valid_cards(game_state)
        if game_state.table_cards:
            # The card the AI needs to respond to
            attacking_card = game_state.table_cards[-1]
            logging.info(f"AI needs to respond to: {attacking_card}")
            # Attempt to play a higher-ranking non-trump card
            selected_card = self.play_non_trump_card(valid_cards, attacking_card, game_state)
            if selected_card:
                reason = "playing a higher-ranking non-trump card"
            else:
                # If no non-trump card available, consider trump cards
                logging.info("No same suit cards available. AI considering trump cards...")
                selected_card = self.play_trump_card(valid_cards, game_state)
                reason = "responding with a trump card" if selected_card else "no valid response available"
        else:
            # AI's turn to attack, pick the best card
            trump_cards = [card for card in valid_cards if card.suit == game_state.trump_suit]
            if trump_cards:
                selected_card = max(trump_cards, key=lambda card: card.get_rank_index())
                reason = "first turn, playing highest trump card"
            else:
                selected_card = max(valid_cards, key=lambda card: card.get_rank_index())
                reason = "first turn, playing highest card"

        if selected_card:
            # Log the selected card and reason, remove it from hand and add to played cards
            logging.info(f"AI selects {selected_card} because it's the {reason}.")
            self.hand.remove(selected_card)
            self.played_cards.add(selected_card)
        else:
            logging.info("AI could not select a card based on the logic provided.")
        return selected_card

    def play_trump_card(self, cards, game_state):
        # Decide on the trump card to play
        logging.info("AI deciding on trump card to play...")
        attacking_card = game_state.table_cards[-1] if game_state.table_cards else None
        logging.info(f"Attacking card to beat: {attacking_card}")
        # Filter trump cards and select the lowest one that can beat the attacking card
        trump_cards = [card for card in cards if card.suit == game_state.trump_suit]
        logging.info(f"Available trump cards: {trump_cards}")
        if trump_cards:
            valid_trumps = [card for card in trump_cards if attacking_card and card.get_rank_index() > attacking_card.get_rank_index()]
            selected_card = min(valid_trumps, key=lambda card: card.get_rank_index()) if valid_trumps else min(trump_cards, key=lambda card: card.get_rank_index())
            logging.info(f"Selected trump card: {selected_card} to play against {attacking_card}")
            return selected_card
        else:
            logging.info("No trump cards available to play.")
            return None

    def play_non_trump_card(self, cards, attacking_card, game_state):
        # Decide on a non-trump card to play against the attacking card
        logging.info(f"AI deciding on non-trump card to play against {attacking_card}")
        same_suit_cards = [card for card in cards if card.suit == attacking_card.suit]
        logging.info(f"Available same suit cards: {same_suit_cards}")
        if same_suit_cards:
            valid_cards = [card for card in same_suit_cards if card.get_rank_index() > attacking_card.get_rank_index()]
            selected_card = min(valid_cards, key=lambda card: card.get_rank_index()) if valid_cards else None
            if selected_card:
                logging.info(f"Selected same suit card: {selected_card} to play against {attacking_card}")
                return selected_card
            else:
                logging.info("No higher same suit cards available. AI may need to play a trump card or take the attacking card.")
                return None
        else:
            logging.info("No same suit cards available. AI may need to resort to trump cards.")
            return None

    def get_valid_cards(self, game_state):
        # Get a list of valid cards for AI based on the current game state
        if game_state.table_cards:  # Defending scenario
            attacking_card = game_state.table_cards[-1]
            valid_cards = [card for card in self.hand if self.is_valid_card(card, game_state, attacking_card)]
        else:
            # Attacking scenario: all cards are valid
            valid_cards = self.hand[:]
        return valid_cards

    def is_valid_card(self, card, game_state, attacking_card=None):
        # Check if a card can legally beat the attacking card
        if game_state.table_cards:
            attacking_card = game_state.table_cards[-1]
        if attacking_card:
            if card.suit == attacking_card.suit and card.ranks.index(card.rank) > card.ranks.index(attacking_card.rank):
                return True  # Card is of the same suit and has a higher rank
            elif card.suit == game_state.trump_suit and attacking_card.suit != game_state.trump_suit:
                return True  # Card is a trump and the attacking card is not
            else:
                return False
        else:
            # No specific card to compare against: all cards are valid
            return True
