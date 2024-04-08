# frontend/app.py
import tkinter as tk
from backend.game import Game


class DurakApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Durak Card Game")
        self.geometry("800x600")  # Increase the window size
        
        self.game = Game()
        self.game.setup_game()
        
        # Display the trump suit
        self.trump_label = tk.Label(self, text=f"Trump Suit: {self.game.trump_suit}")
        self.trump_label.pack()

        # Add GUI elements (buttons, labels, etc.) that interact with game logic
        self.start_button = tk.Button(self, text="Start Round", command=self.start_round)
        self.start_button.pack(pady=10)

        # A label to show the current status
        self.status_label = tk.Label(self, text="Click 'Start Round' to begin!", wraplength=500)
        self.status_label.pack(pady=10)

        # Create an area to show player's hand
        self.player_hand_frame = tk.Frame(self)
        self.player_hand_frame.pack(pady=20)

        # Draw the player's hand
        self.draw_player_hand()

    def start_round(self):
        # Logic to start a new round
        # This is just placeholder text; we'll need to call methods to handle the round start
        self.status_label.config(text="Round started. Make your move!")
        
        # Hide the start button to prevent starting multiple rounds simultaneously
        self.start_button.pack_forget()

    def draw_player_hand(self):
        # Clear the previous hand
        for widget in self.player_hand_frame.winfo_children():
            widget.destroy()
        
        # Display each card as a button
        for i, card in enumerate(self.game.player.hand):
            card_button = tk.Button(self.player_hand_frame, text=str(card),
                                    command=lambda c=card: self.play_card(c))
            card_button.pack(side="left", padx=10)

    def play_card(self, card):
        # Logic to play a card
        print(f"You played: {card}")
        # Here, we would integrate with the backend logic to play a card and update game state
        # For example:
        # self.game.player.play_card(card)
        
        # Then, we would refresh the GUI to reflect the new state
        self.update_game_status()

    def update_game_status(self):
        # This method will update the GUI to reflect the current game state
        # We'll need to add more comprehensive updates based on game status
        self.status_label.config(text="Your move was registered. Waiting for AI...")
        self.draw_player_hand()

def run_gui():
    app = DurakApp()
    app.mainloop()

if __name__ == "__main__":
    run_gui()