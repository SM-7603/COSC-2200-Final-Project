class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw_card(self, deck):
        card = deck.deal()
        if card:
            self.hand.append(card)

    def play_card(self, index):
        return self.hand.pop(index) if index < len(self.hand) else None

    def has_valid_card(self, game_state):
        return any(self.is_valid_card(card, game_state) for card in self.hand)

    def is_valid_card(self, card, game_state, attacking_card=None):
        if not game_state.table_cards:
            return True
        attacking_card = game_state.table_cards[-1]
        is_higher_rank = card.suit == attacking_card.suit and card.rank > attacking_card.rank
        is_trump = card.suit == game_state.trump_suit and attacking_card.suit != game_state.trump_suit
        return is_higher_rank or is_trump

class AIPlayer(Player):
    def __init__(self):
        super().__init__("AI")
        self.played_cards = set()

    def play_card(self, game_state):
        valid_cards = self.get_valid_cards(game_state)
        if not valid_cards:
            return None
        selected_card = self.select_card_to_play(valid_cards, game_state)
        if selected_card:
            self.hand.remove(selected_card)
            self.played_cards.add(selected_card)
        return selected_card

    def select_card_to_play(self, valid_cards, game_state):
        if game_state.table_cards:
            attacking_card = game_state.table_cards[-1]
            selected_card = self.choose_defensive_card(valid_cards, attacking_card, game_state)
        else:
            selected_card = max(valid_cards, key=lambda card: (card.suit == game_state.trump_suit, card.rank))
        return selected_card

    def choose_defensive_card(self, valid_cards, attacking_card, game_state):
        non_trump_cards = [card for card in valid_cards if card.suit == attacking_card.suit and card.rank > attacking_card.rank]
        if non_trump_cards:
            return min(non_trump_cards, key=lambda card: card.rank)
        trump_cards = [card for card in valid_cards if card.suit == game_state.trump_suit and (not attacking_card or card.rank > attacking_card.rank)]
        return min(trump_cards, key=lambda card: card.rank) if trump_cards else None

    def get_valid_cards(self, game_state):
        if game_state.table_cards:
            attacking_card = game_state.table_cards[-1]
            return [card for card in self.hand if self.is_valid_card(card, game_state, attacking_card)]
        return self.hand[:]
