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

        # Remove cards that have already been played
        valid_cards = [card for card in valid_cards if card not in self.played_cards]

        if not valid_cards:
            return None  # If all valid cards have been played, return None

        # If it's the AI's first turn, play the biggest trump card if available, otherwise play the biggest card of any suit
        if not game_state.player.hand:
            selected_card = max(valid_cards, key=lambda card: (card.suit != game_state.trump_suit, card.ranks.index(card.rank)))
        else:
            # If AI is playing after the human
            human_card = game_state.player.hand[0]
            if human_card.suit == game_state.trump_suit:
                # If human played a trump card
                selected_card = self.play_trump_card(valid_cards, game_state)
                print("trump card method")
            else:
                # If human played a non-trump card
                selected_card = self.play_non_trump_card(valid_cards, human_card)
                print("non trump card method")
        # Remove the selected card from the AI player's hand and mark it as played
        self.hand.remove(selected_card)
        self.played_cards.add(selected_card)

        return selected_card

    def play_trump_card(self, cards, game_state):
        trump_cards = [card for card in cards if card.suit == game_state.trump_suit]
        if trump_cards:
            bigger_trump = max(trump_cards, key=lambda card: card.ranks.index(card.rank))
            smaller_trump = min(trump_cards, key=lambda card: card.ranks.index(card.rank))
            if bigger_trump.rank > game_state.player.hand[0].rank:
                return bigger_trump
            else:
                return smaller_trump
        else:
            # If AI doesn't have any trump cards, play the smallest card from its hand
            return min(cards, key=lambda card: card.ranks.index(card.rank))

    def play_non_trump_card(self, cards, human_card):
        same_suit_cards = [card for card in cards if card.suit == human_card.suit]
        if same_suit_cards:
            # If AI has cards of the same suit as the human player
            bigger_card = max(same_suit_cards, key=lambda card: card.ranks.index(card.rank))
            if bigger_card.rank > human_card.rank:
                return bigger_card
            else:
                return min(same_suit_cards, key=lambda card: card.ranks.index(card.rank))
        else:
            # If AI doesn't have cards of the same suit as the human player, play the smallest trump card if available
            trump_cards = [card for card in cards if card.suit == game_state.trump_suit]
            if trump_cards:
                return min(trump_cards, key=lambda card: card.ranks.index(card.rank))
            else:
                return min(cards, key=lambda card: card.ranks.index(card.rank))

    def get_valid_cards(self, game_state):
        # Get a list of valid cards the AI player can play based on the current game state
        valid_cards = []
        for card in self.hand:
            if self.is_valid_card(card, game_state):
                valid_cards.append(card)
        return valid_cards

    def is_valid_card(self, card, game_state):
        # Check if the card matches the suit of the first card played in the round
        return not game_state.player.hand or card.suit == game_state.player.hand[0].suit
