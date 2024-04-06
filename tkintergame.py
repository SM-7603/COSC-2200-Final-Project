import tkinter as tk
from tkinter import messagebox
from deck import Deck
from player import AIPlayer, Player
import random

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Durak")

        self.deck = Deck()
        self.player = Player("Human")
        self.ai_player = AIPlayer()
        self.trump_suit = None
        self.table_cards = []
        self.attacking_player = None  # Add attacking_player attribute

        self.setup_game()

    def setup_game(self):
        self.deck.shuffle()
        # Deal 6 cards to each player
        for _ in range(6):
            self.player.draw_card(self.deck)
            self.ai_player.draw_card(self.deck)
        # Determine the trump suit if not chosen yet
        if self.trump_suit is None:
            self.trump_suit = random.choice(self.deck.cards).suit
            messagebox.showinfo("Trump Suit", f"The trump suit is {self.trump_suit}")
        self.attacking_player = self.player  # Set attacking player at the start

    def start_game_loop(self):
        while self.player.hand and self.ai_player.hand:
            messagebox.showinfo("New Round", "New round!")
            self.table_cards.clear()

            # Attacking phase
            messagebox.showinfo("Attacking", f"{self.attacking_player.name} is attacking.")
            self.attack(self.attacking_player)
            defending_player = self.ai_player if self.attacking_player == self.player else self.player

            # Defending phase
            self.defend(defending_player)

            if not defending_player.hand:
                messagebox.showinfo("Round Result", f"{defending_player.name} couldn't defend. Taking cards...")
                defending_player.hand.extend(self.table_cards)
                self.table_cards.clear()
                if defending_player == self.player:
                    messagebox.showinfo("Round Result", "AI wins this round!")
                else:
                    messagebox.showinfo("Round Result", "You win this round!")
                self.attacking_player = self.ai_player if defending_player == self.player else self.player
                self.redistribute_cards(self.attacking_player)

        messagebox.showinfo("Game Over", "Game over!")

    def attack(self, player):
        card_index = self.show_card_selection_dialog(player)
        if card_index is None:
            messagebox.showinfo("Round Result", "You chose to quit. AI wins this round!")
            self.table_cards.clear()
            attacking_player = self.ai_player
            self.redistribute_cards(attacking_player)
            return
        played_card = player.play_card(card_index)
        messagebox.showinfo("Card Played", f"{player.name} played: {played_card}")
        self.table_cards.append(played_card)

    def defend(self, player):
        messagebox.showinfo("Defending", f"{player.name} is defending.")
        ai_played_card = player.play_card(self)
        if ai_played_card is not None:
            messagebox.showinfo("AI Played", f"{player.name} played: {ai_played_card}")
            if ai_played_card.suit == self.table_cards[-1].suit:
                if ai_played_card.rank > self.table_cards[-1].rank:
                    messagebox.showinfo("Round Result", f"{player.name} wins this round.")
                    return
            elif ai_played_card.suit == self.trump_suit:
                messagebox.showinfo("Trump Card", f"{player.name} played trump card.")
                return
        messagebox.showinfo("Round Result", f"{player.name} couldn't defend. Taking cards...")
        player.hand.extend(self.table_cards)
        self.table_cards.clear()

    def redistribute_cards(self, winning_player):
        losing_player = self.player if winning_player == self.ai_player else self.ai_player
        losing_player.hand.extend(self.table_cards)
        self.table_cards.clear()
        while len(winning_player.hand) < 6 and self.deck.cards:
            winning_player.draw_card(self.deck)

    def show_card_selection_dialog(self, player):
        root = tk.Toplevel()
        root.title("Select Card")

        selected_index = tk.StringVar()
        options = [f"{card.rank} of {card.suit}" for card in player.hand]

        label = tk.Label(root, text="Select a card to play:")
        label.pack()

        option_menu = tk.OptionMenu(root, selected_index, *options)
        option_menu.pack()

        def play_card():
            try:
                index = options.index(selected_index.get())
                root.destroy()
                return index
            except ValueError:
                messagebox.showerror("Error", "Invalid card selection!")
                return None

        confirm_button = tk.Button(root, text="Play Card", command=play_card)
        confirm_button.pack()

        root.mainloop()

        return selected_index.get()
