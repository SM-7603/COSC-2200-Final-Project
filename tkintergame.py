import tkinter as tk
from tkinter import messagebox
from deck import Deck
from player import Player, AIPlayer

class DurakApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Durak")
        self.game = None  # Game object will be initialized when starting the game
        self.selected_card = None
        
        self.create_widgets()

    def create_widgets(self):
        self.welcome_label = tk.Label(self.root, text="Welcome to Durak!", font=("Helvetica", 16))
        self.welcome_label.pack()

        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_button.pack()

        self.card_selection_frame = tk.Frame(self.root)
        self.card_selection_frame.pack()

        self.card_selection_label = tk.Label(self.card_selection_frame, text="Select a card to play:")
        self.card_selection_label.pack(side=tk.LEFT)

        self.card_options = tk.StringVar(self.card_selection_frame)
        self.card_options.set("")  # Default value

        self.card_dropdown = tk.OptionMenu(self.card_selection_frame, self.card_options, "")
        self.card_dropdown.pack(side=tk.LEFT)

        self.play_button = tk.Button(self.root, text="Play Card", command=self.play_selected_card)
        self.play_button.pack()

        self.print_output = tk.Text(self.root, height=15, width=60)
        self.print_output.pack()

    def start_game(self):
        self.game = Game()
        self.game.setup_game()
        self.display_game()

    def display_game(self):
        self.clear_output()
        self.append_output("New game started!\n")
        self.update_card_options()

        while self.game.player.hand and self.game.ai_player.hand:
            self.append_output("\nNew round!\n")
            self.append_output(f"Trump suit: {self.game.trump_suit}\n")

            # Determine attacking and defending players
            attacking_player = self.game.player if self.game.player == self.game.attacking_player else self.game.ai_player
            defending_player = self.game.ai_player if attacking_player == self.game.player else self.game.player

            # Attacking phase
            self.append_output(f"\n{attacking_player.name} is attacking.\n")
            self.play_attack(attacking_player)

            # Defending phase
            self.append_output(f"\n{defending_player.name} is defending.\n")
            self.play_defend(defending_player)

        # Check for winner
        if not defending_player.hand:
            self.append_output(f"{defending_player.name} couldn't defend. Taking cards...\n")
            defending_player.hand.extend(self.game.table_cards)
            self.game.table_cards.clear()
            self.append_output(f"{attacking_player.name} wins this round!\n")
            attacking_player = self.game.ai_player if defending_player == self.game.player else self.game.player
            self.redistribute_cards(attacking_player)

        self.append_output("\nGame over!\n")

    def update_card_options(self):
        menu = self.card_dropdown["menu"]
        menu.delete(0, "end")

        for card in self.game.player.hand:
            menu.add_command(label=str(card), command=tk._setit(self.card_options, str(card)))

    def play_selected_card(self):
        selected_card = self.card_options.get()
        if selected_card:
            if selected_card in self.game.player.hand:
                self.selected_card = selected_card
                self.append_output(f"You played: {selected_card}\n")
                self.game.player.hand.remove(selected_card)  # Remove the played card from the player's hand
                self.game.table_cards.append(selected_card)  # Add the played card to the table
                self.display_game()  # Update the display
            else:
                self.append_output("The selected card is not in your hand. Please select a card from your hand.\n")
        else:
            self.append_output("Please select a card to play.\n")

    def play_attack(self, player):
        self.append_output(f"{player.name}'s hand: {', '.join(map(str, player.hand))}\n")

        if not isinstance(player, AIPlayer):
            self.append_output("Select a card to play.\n")
        else:
            played_card = player.play_card(self.game)
            if played_card:
                self.append_output(f"{player.name} played: {played_card}\n")
                self.game.table_cards.append(played_card)
                self.display_game()
            else:
                self.append_output("AI couldn't play a card. GAME OVER\n")
                self.game.player.hand.extend(self.game.table_cards)
                self.game.table_cards.clear()
                self.game.attacking_player = self.game.player

        def play_defend(self, player):
            self.append_output(f"{player.name}'s hand: {', '.join(map(str, player.hand))}\n")

        if not isinstance(player, AIPlayer):
            self.append_output("Select a card to defend with.\n")
        else:
            ai_played_card = player.play_card(self.game)
            if ai_played_card is not None:
                self.append_output(f"{player.name} played: {ai_played_card}\n")
                if self.game.table_cards:
                    attacking_rank = self.game.table_cards[-1].get_rank_index()
                else:
                    attacking_rank = None
                defending_rank = ai_played_card.get_rank_index()

                if attacking_rank is None or (ai_played_card.suit == self.game.table_cards[-1].suit and defending_rank > attacking_rank) \
                        or (ai_played_card.suit == self.game.trump_suit and self.game.table_cards[-1].suit != self.game.trump_suit):
                    self.append_output(f"{player.name} successfully defends with {ai_played_card}\n")
                    self.game.table_cards.append(ai_played_card)
                else:
                    self.append_output(f"{player.name} could not defend with {ai_played_card}. GAME OVER\n")
                    self.game.player.hand.extend(self.game.table_cards)
                    self.game.table_cards.clear()
                    self.game.attacking_player = self.game.player
            else:
                self.append_output(f"{player.name} has no valid cards to play. GAME OVER\n")
                self.game.player.hand.extend(self.game.table_cards)
                self.game.table_cards.clear()
                self.game.attacking_player = self.game.player


    def redistribute_cards(self, winning_player):
        losing_player = self.game.player if winning_player == self.game.ai_player else self.game.ai_player
        losing_player.hand.extend(self.game.table_cards)
        self.game.table_cards.clear()

        while len(winning_player.hand) < 6 and self.game.deck.cards:
            winning_player.hand.append(self.game.deck.deal())

        self.append_output(f"After redistribution, {winning_player.name} has {len(winning_player.hand)} cards.\n")
        self.append_output(f"After redistribution, {losing_player.name} has {len(losing_player.hand)} cards.\n")

    def clear_output(self):
        self.print_output.delete('1.0', tk.END)

    def append_output(self, text):
        self.print_output.insert(tk.END, text)
        print(text)


class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player("Human")
        self.ai_player = AIPlayer()
        self.trump_suit = None
        self.table_cards = []
        self.attacking_player = None

    def setup_game(self):
        self.deck.shuffle()
        # Deal 6 cards to each player
        for _ in range(6):
            self.player.draw_card(self.deck)
            self.ai_player.draw_card(self.deck)
        # Determine the trump suit
        self.trump_suit = self.deck.cards[-1].suit

        # Set attacking player
        self.attacking_player = self.player if self.player.has_valid_card(self) else self.ai_player

if __name__ == "__main__":
    root = tk.Tk()
    app = DurakApp(root)
    root.mainloop()
