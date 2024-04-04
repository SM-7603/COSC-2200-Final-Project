class Card:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def get_rank_index(self):
        return Card.ranks.index(self.rank)

    def __repr__(self):
        return f"{self.rank} of {self.suit}"
