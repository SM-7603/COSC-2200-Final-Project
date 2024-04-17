import logging  # Importing logging module for logging game events

import random  # Importing random module for random selection

from deck import Deck  # Importing Deck class from deck module
from player import AIPlayer, Player  # Importing AIPlayer and Player classes from player module



# Configure logging to write to a file
logging.basicConfig(filename='game_logs.txt', level=logging.INFO, format='%(message)s')



class Game:
    def __init__(self):
        # Initialize game attributes
        self.deck = Deck()  # Creating a Deck object
        self.player = Player("Human")  # Creating a Player object for human player
        self.ai_player = AIPlayer()  # Creating an AIPlayer object
        self.trump_suit = None  # Trump suit for the game
        self.table_cards = []  # List to hold cards on the table
        self.winning_player = None  # Player who wins the round
        self.losing_player = None  # Player who loses the round
        self.attacking_player = None  # Player who is currently attacking
        self.defending_player = None  # Player who is currently defending



    def setup_game(self):
        # Shuffle the deck and deal 6 cards to each player
        self.deck.shuffle()  # Shuffle the deck
        for _ in range(6):
            self.player.draw_card(self.deck)  # Human player draws a card
            self.ai_player.draw_card(self.deck)  # AI player draws a card

        # Determine the trump suit by taking the suit of the last card in the deck
        self.trump_suit = self.deck.cards[-1].suit
        print(f"The trump suit is {self.trump_suit}")  # Print the trump suit
        logging.info(f"The trump suit is {self.trump_suit}")  # Log the trump suit
        print(f"Number of cards left in the deck: {len(self.deck.cards)}")  # Print remaining cards in the deck
        logging.info(f"Number of cards left in the deck: {len(self.deck.cards)}")  # Log remaining cards
        
        # printing the rules for the human player to understand the game
        print("===========================================================")
        print("                        GAME RULES:")
        print("===========================================================")
        print("1. Total number of cards is 36.")
        print("2. We'll distribute 12 cards between players: 6 each.")
        print("   The remaining 24 cards are used when a player can't play.")
        print("3. The game declares trump suits after distributing cards.")
        print("4. Randomly, one player attacks and the other defends for")
        print("   the first round.")
        print("5. In the first round, the attacker plays a card. The")
        print("   defender defends until out of valid cards. The defender")
        print("   then takes all cards on the table.")
        print("6. If the attacker can't play, they take all cards on the")
        print("   table. The defender draws from the deck to replenish")
        print("   their hand.")
        print("7. The player who took cards from the table attacks next,")
        print("   using a card from their hand. The previous attacker")
        print("   defends.")
        print("8. This process continues until one player runs out of cards.")
        print("9. A player without cards wins. The other player loses.")
        print("===========================================================")

    def start_game_loop(self):
        # Start the main game loop
        self.attacking_player = random.choice([self.player, self.ai_player])  # Randomly select attacking player
        print("\nNew round!")  # Print new round
        logging.info("\nNew round!")  # Log new round

        while self.player.hand and self.ai_player.hand:
            # Continue game loop until one of the players runs out of cards

            # Attacking phase
            print(f"\n{self.attacking_player.name} is attacking.")
            logging.info(f"\n{self.attacking_player.name} is attacking.")

            if isinstance(self.attacking_player, AIPlayer):
                self.ai_attack(self.attacking_player)  # AI attacks
            else:
                self.attack(self.attacking_player)  # Human player attacks

            defending_player = self.ai_player if self.attacking_player == self.player else self.player

            # Defending phase
            if isinstance(defending_player, AIPlayer):
                self.ai_defend(defending_player)  # AI defends
            else:
                self.defend(defending_player)  # Human player defends

            # Handle scenarios where players are unsuccessful in attacking or defending

            # Handle scenario when human player is unsuccessful in attacking
            if (self.attacking_player == self.player and not self.player.has_valid_card(self)):
                print("Human player does not have valid card to play. AI will now attack.")
                logging.info("Human player does not have valid card to play. AI will now attack.")
                self.player.hand.extend(self.table_cards)
                self.table_cards.clear()
                self.attacking_player = self.ai_player
                self.winning_player = self.ai_player
                self.losing_player = self.player
                self.redistribute_cards(self.losing_player, self.winning_player)

            elif (self.attacking_player == self.player and len(self.table_cards) !=0 and not self.table_cards[-1] in [card for card in self.player.hand if self.player.is_valid_card(card, self)] and self.table_cards[-1] in self.player.hand):
                print("Human player was unsuccessful in attacking because it does not have valid cards to play. AI will now attack.")
                logging.info("Human player was unsuccessful in attacking because it does not have valid cards to play. AI will now attack.")
                self.player.hand.extend(self.table_cards)
                self.table_cards.clear()
                self.attacking_player = self.ai_player
                self.winning_player = self.ai_player
                self.losing_player = self.player
                self.redistribute_cards(self.losing_player, self.winning_player)


            if self.attacking_player == self.ai_player and not self.ai_player.has_valid_card(self):
                print("AI was unsuccessful in attacking. Human player will now attack.")
                logging.info("AI was unsuccessful in attacking. Human player will now attack.")
                self.ai_player.hand.extend(self.table_cards)
                self.table_cards.clear()
                self.attacking_player = self.player
                self.winning_player = self.player
                self.losing_player = self.ai_player
                self.redistribute_cards(self.losing_player, self.winning_player)
                while len(self.player.hand) < 6 and self.deck.cards:
                    self.player.hand.append(self.deck.deal())

            elif (self.attacking_player == self.ai_player and len(self.table_cards) !=0 and not self.table_cards[-1] in [card for card in self.ai_player.hand if self.ai_player.is_valid_card(card, self)] and self.table_cards[-1] in self.ai_player.hand):
                print("AI player was unsuccessful in attacking because it does not have valid cards to play. Human will now attack.")
                logging.info("AI player was unsuccessful in attacking because it does not have valid cards to play. Human will now attack.")
                self.player.hand.extend(self.table_cards)
                self.table_cards.clear()
                self.attacking_player = self.ai_player
                self.winning_player = self.ai_player
                self.losing_player = self.player
                self.redistribute_cards(self.losing_player, self.winning_player)

            
            if self.defending_player == self.player and not self.player.has_valid_card(self):
                print("Human player was unsuccessful in defending. AI will now attack.")
                logging.info("Human player was unsuccessful in defending. AI will now attack.")
                self.player.hand.extend(self.table_cards)
                self.table_cards.clear()
                self.attacking_player = self.ai_player
                self.winning_player = self.ai_player
                self.losing_player = self.player
                while len(self.winning_player.hand) < 6 and self.deck.cards:
                    self.winning_player.hand.append(self.deck.deal())

            elif (self.defending_player == self.player and len(self.table_cards) !=0 and not self.table_cards[-1] in [card for card in self.player.hand if self.player.is_valid_card(card, self)] and self.table_cards[-1] in self.player.hand):
                print("Human player was unsuccessful in defending because it does not have valid cards to play. AI will continue now attack.")
                logging.info("Human player was unsuccessful in defending because it does not have valid cards to play. AI will continue now attack.")

                self.player.hand.extend(self.table_cards)
                self.table_cards.clear()
                self.attacking_player = self.ai_player
                self.winning_player = self.ai_player
                self.losing_player = self.player
                self.redistribute_cards(self.losing_player, self.winning_player)

            
            elif self.defending_player == self.ai_player and not self.ai_player.has_valid_card(self):
                print("AI was unsuccessful in defending. Human player will now attack.")
                logging.info("AI was unsuccessful in defending. Human player will now attack.")
                self.player.hand.extend(self.table_cards)
                self.table_cards.clear()
                self.attacking_player = self.player
                self.winning_player = self.player
                self.losing_player = self.ai_player
                while len(self.winning_player.hand) < 6 and self.deck.cards:
                    self.winning_player.hand.append(self.deck.deal())

        if len(self.player.hand) == 0:
            print(f"\nCongratulations! {self.player.name} wins!")  # Declare human player as winner
            logging.info(f"\nCongratulations! {self.player.name} wins!")  # Log winning player
            print(f"{self.ai_player.name} ran out of cards. {self.ai_player.name} is DURAK!")  # Declare AI player as loser
            logging.info(f"{self.ai_player.name} ran out of cards. {self.ai_player.name} is DURAK!")  # Log losing player
        if len(self.ai_player.hand) == 0:
            print(f"\nCongratulations! {self.ai_player.name} wins!")  # Declare AI player as winner
            logging.info(f"\nCongratulations! {self.ai_player.name} wins!")  # Log winning player
            print(f"{self.player.name} ran out of cards. {self.player.name} is DURAK!")  # Declare human player as loser
            logging.info(f"{self.player.name} ran out of cards. {self.player.name} is DURAK!")  # Log losing player
            
        print("\nGame Over!")  # Print game over message
        logging.info("\nGame Over!")  # Log game over



    def attack(self, player):
        # Human player attacks
        self.attacking_player = self.player
        print(f"\nYour hand: {', '.join(map(str, self.player.hand))}")  # Print human player's hand
        logging.info(f"\nYour hand: {', '.join(map(str, self.player.hand))}")  # Log human player's hand
        logging.info(f" AI hand: {', '.join(map(str, self.ai_player.hand))}")  # Log AI player's hand

        while True:
            try:
                card_index = int(input("Enter the index of the card you wish to play (0-based): "))  # Prompt for card index
                if card_index >= len(self.player.hand):
                    print("Invalid card index. Try again.")  # Invalid index message
                    continue
            except ValueError:
                print("Invalid input. Please enter a valid number.")  # Handle invalid input
                continue

            # Player plays the selected card
            played_card = player.play_card(card_index)

            # Check if the attack was successful
            if(len(self.table_cards) != 0):
                defending_rank = played_card.get_rank_index()
                attacking_rank = self.table_cards[-1].get_rank_index()

                if ((played_card.suit == self.table_cards[-1].suit and defending_rank > attacking_rank) \
                        or (played_card.suit == self.trump_suit and self.table_cards[-1].suit != self.trump_suit) or (played_card.suit == self.trump_suit and self.table_cards[-1].suit == self.trump_suit and defending_rank > attacking_rank)) :
                    # Attack successful
                    print(f"{player.name} played: {played_card}")  # Print played card
                    logging.info(f"{player.name} played: {played_card}")  # Log played card
                    self.table_cards.append(played_card)  # Add card to table
                    logging.info(f"Number of cards on the table: {len(self.table_cards)}")  # Log number of cards on table
                    print(f"Number of cards left in the deck: {len(self.deck.cards)}")  # Print remaining cards in deck
                    logging.info(f"Number of cards left in the deck: {len(self.deck.cards)}")  # Log remaining cards
                    break
                else:
                    self.table_cards.append(played_card)  # Add card to table
                    break
            else:
                print(f"{player.name} played: {played_card}")  # Print played card
                logging.info(f"{player.name} played: {played_card}")  # Log played card
                self.table_cards.append(played_card)  # Add card to table
                logging.info(f"Number of cards on the table: {len(self.table_cards)}")  # Log number of cards on table
                print(f"Number of cards left in the deck: {len(self.deck.cards)}")  # Print remaining cards in deck
                logging.info(f"Number of cards left in the deck: {len(self.deck.cards)}")  # Log remaining cards
                break



    def ai_attack(self, player):
        # AI attacks
        self.attacking_player = self.ai_player
        played_card = player.play_card(self)
        if played_card:
            print(f"{player.name} played: {played_card}")  # Print played card
            logging.info(f"{player.name} played: {played_card}")  # Log played card
            self.table_cards.append(played_card)  # Add card to table
            logging.info(f"Number of cards on the table: {len(self.table_cards)}")  # Log number of cards on table
        else:
            played_card = random(self.ai_player.hand)  # Randomly select card if AI couldn't play
            self.table_cards.append(played_card)



    def defend(self, player):
        # Human player defends
        print(f"\n{player.name} is defending.")  # Print defending player
        logging.info(f"\n{player.name} is defending.")  # Log defending player
        while True:
            if player == self.player:
                print(f"Your hand: {', '.join(map(str, self.player.hand))}")  # Print human player's hand
                logging.info(f"Your hand: {', '.join(map(str, self.player.hand))}")  # Log human player's hand
                try:
                    card_index = int(input("Enter the index of the card you wish to play (0-based): "))  # Prompt for card index
                    if card_index >= len(self.player.hand):
                        print("Invalid card index. Try again.")  # Invalid index message
                        continue
                except ValueError:
                    print("Invalid input. Please enter a valid number.")  # Handle invalid input
                    continue
                played_card = player.play_card(card_index)  # Player plays selected card
                print(f"{player.name} played: {played_card}")  # Print played card
                logging.info(f"{player.name} played: {played_card}")  # Log played card
            else:
                played_card = player.play_card(self)  # AI plays card
                print(f"{player.name} played: {played_card}")  # Print played card
                logging.info(f"{player.name} played: {played_card}")  # Log played card

            if played_card is not None:
                defending_rank = played_card.get_rank_index()
                attacking_rank = self.table_cards[-1].get_rank_index()

                # Check if defending card successfully defends
                if (played_card.suit == self.table_cards[-1].suit and defending_rank > attacking_rank) \
                        or (played_card.suit == self.trump_suit and self.table_cards[-1].suit != self.trump_suit) or (played_card.suit == self.trump_suit and self.table_cards[-1].suit == self.trump_suit and defending_rank > attacking_rank):
                    logging.info(f" {player.name} successfully defends with {played_card}.")
                    self.table_cards.append(played_card)  # Add card to table
                    logging.info(f"Number of cards on the table: {len(self.table_cards)}")  # Log number of cards on table
                    break
                else:
                    self.table_cards.append(played_card)
                    print(f"{player.name} could not defend with {played_card}. Round Over.")
                    logging.info(f"{player.name} could not defend with {played_card}. Round Over.")
                    player.hand.extend(self.table_cards)
                    self.table_cards.clear()
                    logging.info(f"Number of cards in {player.name}'s hand after taking cards: {len(player.hand)}")
                    self.winning_player = self.ai_player
                    self.losing_player = self.player
                    self.redistribute_cards(self.losing_player, self.winning_player)
                    self.attacking_player = self.ai_player
                    print(f"{player.name} was unable to defend successfully so the roles will be be same but the human will take cards from table")
                    logging.info(f"{player.name} was unable to defend successfully so the roles will be be same but the human will take cards from table")
                    break
            else:
                print(f"{player.name} has no valid cards to play. Round Over")
                logging.info(f"{player.name} has no valid cards to play. Round Over")
                logging.info(f"Number of cards on the table before taking: {len(self.table_cards)}")
                player.hand.extend(self.table_cards)
                self.table_cards.clear()
                logging.info(f"Number of cards in {player.name}'s hand after taking cards: {len(player.hand)}")
                self.winning_player = self.ai_player
                self.losing_player = self.player
                self.redistribute_cards(self.losing_player, self.winning_player)
                break



    def ai_defend(self, player):
        # AI defends
        print(f"\nAI is defending.")  # Print AI is defending
        logging.info(f"\nAI is defending.")  # Log AI is defending
        ai_played_card = player.play_card(self)  # AI plays card
        if ai_played_card is not None:
            print(f"{player.name} played: {ai_played_card}")  # Print played card
            logging.info(f"{player.name} played: {ai_played_card}")  # Log played card
            defending_rank = ai_played_card.get_rank_index()
            attacking_rank = self.table_cards[-1].get_rank_index()

            # Check if defending card successfully defends
            if (ai_played_card.suit == self.table_cards[-1].suit and defending_rank > attacking_rank) \
                    or (ai_played_card.suit == self.trump_suit and self.table_cards[-1].suit != self.trump_suit):
                logging.info(f" {player.name} successfully defends with {ai_played_card}.")
                self.table_cards.append(ai_played_card)  # Add card to table
                logging.info(f"Number of cards on the table: {len(self.table_cards)}")  # Log number of cards on table
            else:
                print(f" {player.name} could not defend with {ai_played_card}. Round Over")
                logging.info(f" {player.name} could not defend with {ai_played_card}. Round Over")
                print(f"Number of cards on the table before taking: {len(self.table_cards)}")
                logging.info(f"Number of cards on the table before taking: {len(self.table_cards)}")
                player.hand.extend(self.table_cards)
                self.table_cards.clear()
                logging.info(f"Number of cards in {player.name}'s hand after taking cards: {len(player.hand)}")
                self.winning_player = self.player
                self.losing_player = self.ai_player
                self.redistribute_cards(self.losing_player, self.winning_player)

        else:
            print(f" {player.name} has no valid cards to play. Round Over")
            logging.info(f" {player.name} has no valid cards to play. Round Over")
            logging.info(f"Number of cards on the table before taking: {len(self.table_cards)}")
            player.hand.extend(self.table_cards)
            self.table_cards.clear()
            logging.info(f"Number of cards in {player.name}'s hand after taking cards: {len(player.hand)}")
            self.winning_player = self.player
            self.losing_player = self.ai_player
            self.redistribute_cards(self.losing_player, self.winning_player)



    def redistribute_cards(self, losing_player, winning_player):
        # Redistribute cards after round ends
        while len(winning_player.hand) < 6 and self.deck.cards:
            winning_player.hand.append(self.deck.deal())

        logging.info(f" After redistribution, {winning_player.name} has {len(winning_player.hand)} cards.")
        logging.info(f"After redistribution, {losing_player.name} has {len(losing_player.hand)} cards.")
        print(f"Number of cards left in the deck: {len(self.deck.cards)}")
        logging.info(f"Number of cards left in the deck: {len(self.deck.cards)}")



if __name__ == "__main__":
    # Create a game object and start the game
    game = Game()  # Create Game object
    game.setup_game()  # Setup game
    game.start_game_loop()  # Start game loop
