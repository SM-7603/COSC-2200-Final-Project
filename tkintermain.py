import tkinter as tk
from tkinter import messagebox
from game import Game

class DurakApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Durak")
        
        self.game = Game(self.root)

        self.welcome_label = tk.Label(root, text="Welcome to Durak!", font=("Helvetica", 16))
        self.welcome_label.pack()

        self.trump_label = tk.Label(root, text="Trump Suit:", font=("Helvetica", 12))
        self.trump_label.place(x=10, y=10)

        self.trump_textbox = tk.Text(root, height=1, width=10)
        self.trump_textbox.place(x=100, y=10)
        self.trump_textbox.insert(tk.END, self.game.trump_suit)  # Show initial trump suit

        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_button.pack()

    def start_game(self):
        self.game.setup_game()
        self.display_game()

    def display_game(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Display player's hand
        player_hand_label = tk.Label(self.root, text=f"Your Hand: {', '.join(map(str, self.game.player.hand))}")
        player_hand_label.pack()

        # Display AI player's hand (hidden)
        ai_hand_label = tk.Label(self.root, text="AI's Hand: [Hidden]")
        ai_hand_label.pack()

        # Display table cards
        table_cards_label = tk.Label(self.root, text="Table Cards: None")
        table_cards_label.pack()

        # Display buttons for player actions
        attack_button = tk.Button(self.root, text="Attack", command=self.attack)
        attack_button.pack()

        defend_button = tk.Button(self.root, text="Defend", command=self.defend)
        defend_button.pack()

    def attack(self):
        card_index = self.game.show_card_selection_dialog(self.game.player)
        if card_index is None:
            messagebox.showinfo("Round Result", "You chose to quit. AI wins this round!")
            self.game.table_cards.clear()
            attacking_player = self.game.ai_player
            self.game.redistribute_cards(attacking_player)
            self.display_game()
            return
        played_card = self.game.player.play_card(card_index)
        messagebox.showinfo("Card Played", f"You played: {played_card}")
        self.game.table_cards.append(played_card)
        self.display_game()

    def defend(self):
        messagebox.showinfo("Defend", "You are defending!")
        # Implement defend logic here

if __name__ == "__main__":
    root = tk.Tk()
    app = DurakApp(root)
    root.mainloop()
