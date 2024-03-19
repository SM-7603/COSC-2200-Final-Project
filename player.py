
# player.py
from card import Card
from deck import Deck

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

class AIPlayer(Player):
    def __init__(self):
        super().__init__("AI")

    def play_card(self, game_state):
        # Simple AI logic to play the first available card
        return self.hand.pop(0) if self.hand else None
