import tkinter as tk
from tkinter import messagebox
from tkintergame import Game

class DurakApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Durak")
        self.game = None  # Game object will be initialized when starting the game
        
        self.create_widgets()

    def create_widgets(self):
        self.welcome_label = tk.Label(self.root, text="Welcome to Durak!", font=("Helvetica", 16))
        self.welcome_label.pack()

        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_button.pack()

        self.deck_label = tk.Label(self.root, text="Deck: ")
        self.deck_label.pack()

        self.display_deck = tk.Text(self.root, height=2, width=30)
        self.display_deck.pack()

        self.print_output = tk.Text(self.root, height=10, width=60)
        self.print_output.pack()

    def start_game(self):
        self.game = Game(self.root)
        self.game.setup_game()
        self.display_game()

    def display_game(self):
        self.clear_widgets()

        # Display player's hand
        player_hand_label = tk.Label(self.root, text=f"Your Hand: {', '.join(map(str, self.game.player.hand))}")
        player_hand_label.pack()

        # Display AI player's hand (hidden)
        ai_hand_label = tk.Label(self.root, text="AI's Hand: [Hidden]")
        ai_hand_label.pack()

        # Display table cards
        table_cards_label = tk.Label(self.root, text=f"Table Cards: {', '.join(map(str, self.game.table_cards))}")
        table_cards_label.pack()

        # Display button for player action
        action_button_text = "Play Card"
        action_button_command = self.play_card
        action_button = tk.Button(self.root, text=action_button_text, command=action_button_command)
        action_button.pack()

        # Update the deck display
        remaining_cards_count = len(self.game.deck.cards)
        self.display_deck.delete('1.0', tk.END)
        self.display_deck.insert(tk.END, f"Number of cards left in the deck: {remaining_cards_count}")

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            if widget != self.deck_label and widget != self.display_deck and widget != self.print_output:
                widget.destroy()

    def play_card(self):
        # If it's the player's turn to attack, the play_card method will perform the attack
            if self.game.player == self.game.attacking_player:
                card_index_str = self.game.show_card_selection_dialog(self.game.player)
                if card_index_str is None:
                    self.append_output("You chose to quit. AI wins this round!")
                    self.game.table_cards.clear()
                    attacking_player = self.game.ai_player
                    self.game.redistribute_cards(attacking_player)
                    self.display_game()
                    return

                card_index = int(card_index_str)
                # Convert index from string to integer
                played_card = self.game.player.play_card(card_index)
                self.append_output(f"You played: {played_card}")
                self.game.table_cards.append(played_card)
                self.display_game()

                # AI's turn
                ai_played_card = self.game.ai_player.play_card(self.game)
                if ai_played_card:
                    self.append_output(f"AI played: {ai_played_card}")
                    self.game.table_cards.append(ai_played_card)
                    self.display_game()

            # If it's the player's turn to defend, the play_card method will perform the defense
            else:
                defending_card_index_str = self.game.show_card_selection_dialog(self.game.ai_player)
                if defending_card_index_str is None:
                    self.append_output("AI chose to quit. You win this round!")
                    self.game.table_cards.clear()
                    attacking_player = self.game.player
                    self.game.redistribute_cards(attacking_player)
                    self.display_game()
                    return

                defending_card_index = int(defending_card_index_str)  # Convert index from string to integer
                defending_card = self.game.ai_player.hand[defending_card_index]
                last_card_played = self.game.table_cards[-1]

                if self.game.is_defense_successful(last_card_played, defending_card):
                    self.game.table_cards.append(defending_card)
                    self.append_output(f"You successfully defended with: {defending_card}")
                else:
                    self.game.table_cards.append(defending_card)
                    self.append_output(f"You failed to defend. AI played: {defending_card}")

                # Check if the game is over
                if not self.game.player.hand:
                    self.append_output("You couldn't defend. GAME OVER.")
                    self.display_game()
                    return

                # AI's turn to attack again
                self.append_output("AI is attacking again.")
                ai_played_card = self.game.ai_player.play_card(self.game)
                if ai_played_card:
                    self.append_output(f"AI played: {ai_played_card}")
                    self.game.table_cards.append(ai_played_card)
                    self.display_game()

    def append_output(self, text):
        self.print_output.insert(tk.END, text + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = DurakApp(root)
    root.mainloop()
