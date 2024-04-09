
# deck.py
import random
from .card import Card

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Card.suits for rank in Card.ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if self.cards:
            return self.cards.pop()
        else:
            return None