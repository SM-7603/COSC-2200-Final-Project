import tkinter as tk
from deck import Deck
from game import Game  # Import the Game class from game.py
from player import Player, AIPlayer
# from PIL import Image, ImageTk

class DurakApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Durak")
        self.game = None  # Game object will be initialized when starting the game
        self.selected_card = None
        self.last_action = None  # Initialize last_action attribute
        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack()
        self.trump_label = tk.Label(self.root, text="")
        self.trump_label.pack()
        # Load background image
        # self.background_img = Image.open("background.png")
        # self.background_photo = ImageTk.PhotoImage(self.background_img)
        
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
        self.game = Game(self)
        self.game.setup_game()
        self.display_trump_suit()
        self.update_status(f"{self.game.current_attacker.name} is attacking.")
        self.display_game()

    def update_status(self, message):
        self.status_label.config(text=message)

    def display_trump_suit(self):
        self.trump_label.config(text=f"Trump suit: {self.game.trump_suit}")

    def display_game(self):
        self.clear_output()  # Clear any previous game state display
        self.append_output("Game starts!\n")
        self.append_output(f"Trump suit: {self.game.trump_suit}\n")
        self.append_output("Your hand: " + ", ".join(map(str, self.game.player.hand)) + "\n")
        # Optionally display AI's hand count without revealing the cards
        self.append_output(f"AI has {len(self.game.ai_player.hand)} cards.\n")

        self.update_card_options()  # Update the dropdown with the player's current hand

    def clear_output(self):
        """Clears the game output text field."""
        self.print_output.delete('1.0', tk.END)

    def update_card_options(self):
        current_hand = self.game.player.hand  # This is a list of Card objects
        self.card_options.set('')  # Default value or set it to the first card
        menu = self.card_dropdown["menu"]
        menu.delete(0, "end")  # Clear current options

        # Populate the dropdown with the player's current hand
        for card in current_hand:
            card_str = str(card)  # Get the string representation of the Card object
            menu.add_command(label=card_str, command=lambda card_str=card_str: self.card_options.set(card_str))

        # Optionally, update the text widget to show the player's current hand as strings
        self.print_output.delete("1.0", tk.END)
        self.print_output.insert(tk.END, "Your hand: " + ", ".join(str(card) for card in current_hand))
                
        
    def update_game_state(self):
        """Update the GUI to reflect the current game state."""
        # Update player's and AI's hands, table cards, etc.
        self.update_card_options()  # Update the player's card selection dropdown
        # Update any other GUI components as needed, e.g., cards on the table, remaining deck count

        # Check for game end conditions
        if self.game.is_over():
            winner = "You" if self.game.player_wins() else "AI"
            self.append_output(f"Game over! {winner} wins.")


    def play_selected_card(self):
        # Debugging: print out the contents of the player's hand
        print("Debug - Player's hand before playing a card:", [str(card) for card in self.game.player.hand])
        print("Debug - Player's actual hand objects:", self.game.player.hand)

        # Get the string of the selected card from the dropdown
        selected_card_str = self.card_options.get()  
        print("Debug - Selected card string:", selected_card_str)  # Additional debug line


        # Find the card object that matches the string
        selected_card_obj = next((card for card in self.game.player.hand if str(card) == selected_card_str), None)

        # Debugging: print out the selected card string and object
        print("Debug - Selected card string:", selected_card_str)
        print("Debug - Selected card object:", selected_card_obj)

        if selected_card_obj:
            # Play the card object
            self.game.player.play_card(selected_card_obj)
            self.append_output(f"You played: {selected_card_str}\n")
            # After the player plays a card, update the game state
            self.update_game_state_after_play()
            # If it's the AI's turn, proceed to that
            self.play_ai_turn()
        else:
            self.append_output("The selected card is not in your hand. Please select a card from your hand.\n")
            
    # Inside the DurakApp class

    def update_hand_display(self, player):
        # Assuming there is a Text widget or similar in your GUI to display the hand
        hand_display = "Your hand: " + ", ".join(str(card) for card in player.hand)
        self.print_output.delete("1.0", tk.END)  # Clear the current display
        self.print_output.insert(tk.END, hand_display)  # Insert the new hand display

        # If you also want to update the AI's hand count (without showing the cards)
        ai_hand_count = f"AI has {len(self.game.ai_player.hand)} cards."
        self.print_output.insert(tk.END, ai_hand_count)

        # Make sure to scroll to the end if there's overflow
        self.print_output.see(tk.END)

            
    def update_game_state_after_play(self):
        # Placeholder for updating the game state, which needs to be implemented
        # For example, it might include clearing the selection, updating the card display,
        # and handling end-of-turn logic
        self.card_options.set('')  # Reset current card selection
        menu = self.card_dropdown["menu"]
        menu.delete(0, "end")  # Clear current options
        
        attacker = self.game.current_attacker.name
        defender = "AI" if attacker == "Player" else "Player"
        self.update_status(f"{attacker} is attacking, {defender} is defending.")


        # Debugging: print out the contents of the player's hand
        print("Debug - Player's hand during update_card_options:", [str(card) for card in self.game.player.hand])

        for card in self.game.player.hand:
            menu.add_command(label=str(card), command=lambda card=card: self.card_options.set(str(card)))
            # Debugging: print the menu command being added
            print("Debug - Adding command to menu:", str(card))

        self.end_round()


    def play_ai_turn(self):
        if not self.game.table_cards:
            # AI is attacking
            ai_card = self.ai_choose_attack_card()
        else:
            # AI is defending
            attacking_card = self.game.table_cards[-1]
            ai_card = self.ai_choose_defend_card(attacking_card)

        if ai_card:
            # AI plays the card
            self.game.ai_player.hand.remove(ai_card)
            self.game.table_cards.append(ai_card)
            self.append_output(f"AI plays: {ai_card}\n")
            self.last_action = 'ai'
        else:
            self.append_output("AI has no valid cards to play.\n")
            # Handle scenario if AI can't play: maybe AI takes all the cards on the table
            self.game.ai_player.hand.extend(self.game.table_cards)
            self.game.table_cards.clear()
            self.last_action = 'player'  # It's the player's turn next

        self.update_game_state_after_play()
                
    def player_turn(self, card):
        # Assuming 'card' is a Card object passed from the event that triggers this method
        if self.game.is_players_turn():  # Assuming you have a method to check if it's the player's turn
            if card in self.game.player.hand:
                self.game.attack(self.game.player, card)  # Perform the player's attack
                self.update_game_state_after_play()  # Update GUI and game state
                self.append_output(f"You played: {card}")
                self.last_action = 'player'  # Set last_action to 'player'
                self.play_ai_turn()  # Now it's AI's turn
            else:
                self.append_output("You can't play that card.")
        else:
            self.append_output("It's not your turn.")

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
            self.root.wait_variable(self.card_options)  # Wait until the player selects a card
            selected_card = self.card_options.get()
            if selected_card:
                if selected_card in player.hand:
                    self.append_output(f"{player.name} played: {selected_card}\n")
                    self.game.table_cards.append(selected_card)
                    self.display_game()  # Update the display
                else:
                    self.append_output("The selected card is not in your hand. Please select a card from your hand.\n")
            else:
                self.append_output("Please select a card to play.\n")
        else:
            if player.hand:  # Check if the player's hand is not empty
                ai_played_card = player.play_card(self.game)
                if ai_played_card is not None:
                    self.append_output(f"{player.name} played: {ai_played_card}\n")
                    if self.game.table_cards:
                        attacking_rank = self.game.table_cards[-1].get_rank_index()
                    else:
                        attacking_rank = None

                    # Filter AI's valid cards based on their ability to defend
                    valid_defending_cards = [card for card in player.hand if
                                            (not self.game.table_cards or card.suit == self.game.table_cards[-1].suit)
                                            and (attacking_rank is None or card.get_rank_index() > attacking_rank)]

                    if valid_defending_cards:
                        best_defending_card = min(valid_defending_cards, key=lambda card: card.get_rank_index())
                        self.append_output(f"{player.name} successfully defends with {best_defending_card}\n")
                        self.game.table_cards.append(best_defending_card)
                    else:
                        lowest_card = min(player.hand, key=lambda card: card.get_rank_index())
                        self.append_output(f"{player.name} couldn't defend. Playing the lowest card: {lowest_card}\n")
                        self.game.table_cards.append(lowest_card)
                else:
                    self.append_output(f"{player.name} has no valid cards to play. GAME OVER\n")
                    self.game.player.hand.extend(self.game.table_cards)
                    self.game.table_cards.clear()
                    self.game.attacking_player = self.game.player
            else:
                self.append_output(f"{player.name}'s hand is empty. GAME OVER\n")
                self.game.attacking_player = self.game.player

    def redistribute_cards(self, winning_player):
        losing_player = self.game.player if winning_player == self.game.ai_player else self.game.ai_player
        losing_player.hand.extend(self.game.table_cards)
        self.game.table_cards.clear()

        while len(winning_player.hand) < 6 and self.game.deck.cards:
            winning_player.hand.append(self.game.deck.deal())

        self.append_output(f"After redistribution, {winning_player.name} has {len(winning_player.hand)} cards.\n")
        self.append_output(f"After redistribution, {losing_player.name} has {len(losing_player.hand)} cards.\n")


    def append_output(self, text):
        """Add text to the GUI output display."""
        self.print_output.insert(tk.END, text + "\n")
        self.print_output.see(tk.END)  # Auto-scroll to the end

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

    
    def player_defend(self):
        defending_card_str = self.card_options.get()  # Get the card string from the dropdown
        defending_card = next((card for card in self.game.player.hand if str(card) == defending_card_str), None)
        attacking_card = self.game.table_cards[-1]  # The last played card which player has to defend against

        if defending_card:
            self.game.defend(self.game.player, attacking_card, defending_card)
            self.append_output(f"You defended with: {defending_card_str}")
            self.update_game_state_after_play()
        else:
            self.append_output("You cannot defend with the selected card. Please select another card.\n")

    def end_round(self):
        # Determine the winning and losing players based on game logic
        winning_player = self.game.winning_player.name
        self.update_status(f"Round ended. {winning_player} won the round.")
        self.prepare_for_new_round()

        # Here's a simple placeholder check:
        if self.last_action == 'player':  # Let's assume the last action can determine the winner/loser
            winning_player = self.game.player
            losing_player = self.game.ai_player
            self.game.redistribute_cards(self.game.player)

        else:
            winning_player = self.game.ai_player
            losing_player = self.game.player
            self.game.redistribute_cards(self.game.ai_player)
            
        self.update_hand_display(self.game.player)  # Update player hand
        self.update_hand_display(self.game.ai_player)  # Update AI hand (if you display AI's hand count)

        # Update the status label with the new attacker and defender
        self.update_status(f"{self.game.current_attacker.name} is attacking, {self.game.current_defender.name} is defending.")



        # Perform redistribution of cards
        # self.game.redistribute_cards(losing_player, winning_player)

        # Now that the cards have been redistributed, you can prepare for the next round
        self.prepare_for_new_round()

    def prepare_for_new_round(self):
        # This method would reset the necessary state for a new round
        # and update the GUI to reflect this
        self.update_game_state_after_play()

    def play_defend(self, player):
        self.append_output(f"{player.name}'s hand: {', '.join(map(str, player.hand))}\n")

        if not isinstance(player, AIPlayer):
            self.append_output("Select a card to defend with.\n")
            self.root.wait_variable(self.card_options)  # Wait until the player selects a card
            selected_card = self.card_options.get()
            if selected_card:
                if selected_card in player.hand:
                    self.append_output(f"{player.name} played: {selected_card}\n")
                    self.game.table_cards.append(selected_card)
                    self.display_game()  # Update the display
                else:
                    self.append_output("The selected card is not in your hand. Please select a card from your hand.\n")
            else:
                self.append_output("Please select a card to play.\n")
        else:
            if player.hand:  # Check if the player's hand is not empty
                ai_played_card = player.play_card(self.game)
                if ai_played_card is not None:
                    self.append_output(f"{player.name} played: {ai_played_card}\n")
                    if self.game.table_cards:
                        attacking_rank = self.game.table_cards[-1].get_rank_index()
                    else:
                        attacking_rank = None

                    # Filter AI's valid cards based on their ability to defend
                    valid_defending_cards = [card for card in player.hand if
                                            (not self.game.table_cards or card.suit == self.game.table_cards[-1].suit)
                                            and (attacking_rank is None or card.get_rank_index() > attacking_rank)]

                    if valid_defending_cards:
                        best_defending_card = min(valid_defending_cards, key=lambda card: card.get_rank_index())
                        self.append_output(f"{player.name} successfully defends with {best_defending_card}\n")
                        self.game.table_cards.append(best_defending_card)
                    else:
                        lowest_card = min(player.hand, key=lambda card: card.get_rank_index())
                        self.append_output(f"{player.name} couldn't defend. Playing the lowest card: {lowest_card}\n")
                        self.game.table_cards.append(lowest_card)
                else:
                    self.append_output(f"{player.name} has no valid cards to play. GAME OVER\n")
                    self.game.player.hand.extend(self.game.table_cards)
                    self.game.table_cards.clear()
                    self.game.attacking_player = self.game.player
            else:
                self.append_output(f"{player.name}'s hand is empty. GAME OVER\n")
                self.game.attacking_player = self.game.player

    def play_selected_card(self):
        # Get the string of the selected card from the dropdown
        selected_card_str = self.card_options.get()  

        # Find the card object that matches the string
        selected_card_obj = next((card for card in self.game.player.hand if str(card) == selected_card_str), None)

        if selected_card_obj:
            # Use the modified play_card method
            played_card = self.game.player.play_card(selected_card_obj)
            if played_card:
                # Now continue with adding the card to the table and updating the game state
                self.game.table_cards.append(played_card)
                self.update_game_state_after_play()
                self.append_output(f"You played: {played_card}")
                # Trigger the AI's turn
                self.play_ai_turn()
            else:
                self.append_output(f"Could not play the card {selected_card_obj}. It's not in your hand.")
        else:
            self.append_output(f"The selected card {selected_card_str} is not recognized.")
            
    # Within the DurakApp class

    def ai_choose_attack_card(self):
        # Sort the AI's hand to get the lowest non-trump cards first
        non_trump_cards = sorted(
            [card for card in self.game.ai_player.hand if card.suit != self.game.trump_suit],
            key=lambda x: (x.rank, x.suit)
        )
        trump_cards = sorted(
            [card for card in self.game.ai_player.hand if card.suit == self.game.trump_suit],
            key=lambda x: (x.rank, x.suit)
        )

        # AI prefers to play the lowest non-trump card first
        if non_trump_cards:
            return non_trump_cards[0]
        elif trump_cards:
            # If only trump cards are left, play the lowest trump card
            return trump_cards[0]
        else:
            # No cards to play
            return None

    def ai_choose_defend_card(self, attacking_card):
        # Sort AI's cards to find the lowest valid defending card
        # Valid cards are of the same suit and higher rank or any trump if the attacking card is not a trump.
        valid_cards = [
            card for card in self.game.ai_player.hand
            if (card.suit == attacking_card.suit and card.get_rank_index() > attacking_card.get_rank_index())
            or (card.suit == self.game.trump_suit and attacking_card.suit != self.game.trump_suit)
        ]
        if valid_cards:
            # Choose the lowest card from the sorted valid cards
            return min(valid_cards, key=lambda card: card.get_rank_index())
        return None  # No card can defend against the attacking card


# Main function to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = DurakApp(root)
    root.mainloop()
