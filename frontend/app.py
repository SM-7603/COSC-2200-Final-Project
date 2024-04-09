# frontend/app.py
import tkinter as tk
from tkinter import messagebox
from backend.game import Game

class DurakApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Durak Card Game")
        self.geometry("800x600")  # Set the window size

        # Initialize the game with a callback to update the GUI
        self.game = Game(update_gui_callback=self.update_game_status)
        self.game.setup_game()

        # Create GUI components
        self.create_gui_elements()

    def create_gui_elements(self):
        # Display the trump suit (will be updated after game setup)
        self.trump_label = tk.Label(self, text=f"Trump Suit: {self.game.trump_suit}")
        self.trump_label.pack(pady=10)

        # Start round button
        self.start_button = tk.Button(self, text="Start Round", command=self.start_round)
        self.start_button.pack(pady=20)

        # Status label for displaying game messages
        self.status_label = tk.Label(self, text="Click 'Start Round' to begin!")
        self.status_label.pack(pady=10)

        # Frame for displaying player's hand
        self.player_hand_frame = tk.Frame(self)
        self.player_hand_frame.pack(pady=20)

        # Initially draw the player's hand
        self.draw_player_hand()

    def start_round(self):
        # Hide the start button to prevent multiple round starts
        self.start_button.pack_forget()

        # Start the game logic for a new round
        self.game.start_new_round()

    def draw_player_hand(self):
        # Clear out the old hand
        for widget in self.player_hand_frame.winfo_children():
            widget.destroy()

        # Draw buttons for each card in the player's hand
        for i, card in enumerate(self.game.player.hand):
            card_button = tk.Button(self.player_hand_frame, text=str(card),
                                    command=lambda c=i: self.play_card(c))
            card_button.pack(side="left", padx=5)

    def play_card(self, card_index):
        # The player plays a card
        played_card = self.game.player_play_card(card_index)
        if played_card:
            # Update GUI accordingly
            self.update_game_status(f"Played {played_card}.")
        else:
            # The card couldn't be played, show an error message
            messagebox.showerror("Error", "Invalid move")

    def update_game_status(self, message, update_cards=False):
        # Update the status label
        self.status_label.config(text=message)

        if update_cards:
            # Redraw the player's hand if update_cards is True
            self.draw_player_hand()
        # Optionally, show AI's cards or any other debug information
        # This can be done similarly to player's hand or in a separate method

def run_gui():
    app = DurakApp()
    app.mainloop()

if __name__ == "__main__":
    run_gui()
