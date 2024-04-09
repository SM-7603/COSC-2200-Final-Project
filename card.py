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
    
    def __eq__(self, other):
        if isinstance(other, Card):
            return (self.rank == other.rank) and (self.suit == other.suit)
        elif isinstance(other, str):
            return str(self) == other
        return NotImplemented


    # In your DurakApp when you populate the dropdown
    def update_card_options(self):
        self.card_options.set('')  # Reset current card selection
        menu = self.card_dropdown["menu"]
        menu.delete(0, "end")  # Clear current options

        for card in self.game.player.hand:
            menu.add_command(label=str(card), command=lambda value=str(card): self.card_options.set(value))

        # If you have a label or text widget displaying the player's hand, you could update it here too
        self.player_hand_display['text'] = ', '.join(str(card) for card in self.game.player.hand)
