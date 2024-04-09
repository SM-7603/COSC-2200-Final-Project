import random
from deck import Deck
from player import AIPlayer, Player

class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player("Human")
        self.ai_player = AIPlayer()
        self.trump_suit = None
        self.table_cards = []
        self.winning_player = None
        self.losing_player = None
        self.attacking_player = None
        self.defending_player = None

    def setup_game(self):
        # Shuffle the deck and deal 6 cards to each player
        self.deck.shuffle()
        for _ in range(6):
            self.player.draw_card(self.deck)        # Human player draws a card
            self.ai_player.draw_card(self.deck)     # AI player draws a card
        
        # Determine the trump suit by taking the suit of the last card in the deck
        self.trump_suit = self.deck.cards[-1].suit
        print(f"The trump suit is {self.trump_suit}")
        # Print the number of cards left in the deck
        print(f"Number of cards left in the deck: {len(self.deck.cards)}")

    def start_game_loop(self):

        self.attacking_player = random.choice([self.player, self.ai_player])
        print("\nNew round!")
    
        
        while self.player.hand and self.ai_player.hand:


            # Attacking phase
            print(f"\nline 39 {self.attacking_player.name} is attacking.")


            if isinstance(self.attacking_player, AIPlayer):
                self.ai_attack(self.attacking_player)
            else:
                self.attack(self.attacking_player)

            defending_player = self.ai_player if self.attacking_player == self.player else self.player

            # Defending phase
            if isinstance(defending_player, AIPlayer):
                self.ai_defend(defending_player)
            else:
                self.defend(defending_player)



            #this is just a try to make the switching the player work
            # Check if the attacking player is unsuccessful
            if (self.attacking_player == self.player and not self.player.has_valid_card(self)):
                print("line 59 Human player was unsuccessful in attacking. AI will now attack.")
                self.player.hand.extend(self.table_cards)
                self.table_cards.clear()
                self.attacking_player = self.ai_player
                self.winning_player = self.ai_player
                self.losing_player = self.player
                self.redistribute_cards(self.losing_player, self.winning_player)
                # while len(self.ai_player.hand) < 6 and self.deck.cards:
                #     self.ai_player.hand.append(self.deck.deal())
                    # print(f"line 68 worked")
                print(f"line 67 Number of cards left in the deck: {len(self.deck.cards)}")

            elif (self.attacking_player == self.player and len(self.table_cards) !=0 and not self.table_cards[-1] in [card for card in self.player.hand if self.player.is_valid_card(card, self)] and self.table_cards[-1] in self.player.hand):
                print("line 72 Human player was unsuccessful in attacking because it does not have valid cards to play. AI will now attack.")
                self.player.hand.extend(self.table_cards)
                self.table_cards.clear()
                self.attacking_player = self.ai_player
                self.winning_player = self.ai_player
                self.losing_player = self.player
                self.redistribute_cards(self.losing_player, self.winning_player)
                # while len(self.ai_player.hand) < 6 and self.deck.cards:
                #     self.ai_player.hand.append(self.deck.deal())
                    # print(f"line 68 worked")
                print(f"line 67 Number of cards left in the deck: {len(self.deck.cards)}")

            if self.attacking_player == self.ai_player and not self.ai_player.has_valid_card(self):
                print("line 71 AI was unsuccessful in attacking. Human player will now attack.")
                self.ai_player.hand.extend(self.table_cards)
                self.table_cards.clear()
                self.attacking_player = self.player
                self.winning_player = self.player
                self.losing_player = self.ai_player
                self.redistribute_cards(self.losing_player, self.winning_player)
                while len(self.player.hand) < 6 and self.deck.cards:
                    self.player.hand.append(self.deck.deal())
                    print(f"line 81 worked")
                print(f"line 79 Number of cards left in the deck: {len(self.deck.cards)}")

            elif (self.attacking_player == self.ai_player and len(self.table_cards) !=0 and not self.table_cards[-1] in [card for card in self.ai_player.hand if self.ai_player.is_valid_card(card, self)] and self.table_cards[-1] in self.ai_player.hand):
                print("line 72 AI player was unsuccessful in attacking because it does not have valid cards to play. Human will now attack.")
                self.player.hand.extend(self.table_cards)
                self.table_cards.clear()
                self.attacking_player = self.ai_player
                self.winning_player = self.ai_player
                self.losing_player = self.player
                self.redistribute_cards(self.losing_player, self.winning_player)
                # while len(self.ai_player.hand) < 6 and self.deck.cards:
                #     self.ai_player.hand.append(self.deck.deal())
                    # print(f"line 68 worked")
                print(f"line 67 Number of cards left in the deck: {len(self.deck.cards)}")

            
            if self.defending_player == self.player and not self.player.has_valid_card(self):
                print("line 82 Human player was unsuccessful in defending. AI will now attack.")
                self.player.hand.extend(self.table_cards)
                self.table_cards.clear()
                self.attacking_player = self.ai_player
                self.winning_player = self.ai_player
                self.losing_player = self.player
                while len(self.winning_player.hand) < 6 and self.deck.cards:
                    self.winning_player.hand.append(self.deck.deal())
                print(f"line 90 Number of cards left in the deck: {len(self.deck.cards)}")

            elif (self.defending_player == self.player and len(self.table_cards) !=0 and not self.table_cards[-1] in [card for card in self.player.hand if self.player.is_valid_card(card, self)] and self.table_cards[-1] in self.player.hand):
                print("line 72 Human player was unsuccessful in defending because it does not have valid cards to play. AI will continue now attack.")
                self.player.hand.extend(self.table_cards)
                self.table_cards.clear()
                self.attacking_player = self.ai_player
                self.winning_player = self.ai_player
                self.losing_player = self.player
                self.redistribute_cards(self.losing_player, self.winning_player)
                # while len(self.ai_player.hand) < 6 and self.deck.cards:
                #     self.ai_player.hand.append(self.deck.deal())
                    # print(f"line 68 worked")
                print(f"line 67 Number of cards left in the deck: {len(self.deck.cards)}")

            
            elif self.defending_player == self.ai_player and not self.ai_player.has_valid_card(self):
                print("line 94 AI was unsuccessful in defending. Human player will now attack.")
                self.player.hand.extend(self.table_cards)
                self.table_cards.clear()
                self.attacking_player = self.player
                self.winning_player = self.player
                self.losing_player = self.ai_player
                while len(self.winning_player.hand) < 6 and self.deck.cards:
                    self.winning_player.hand.append(self.deck.deal())
                print(f"line 102 Number of cards left in the deck: {len(self.deck.cards)}")

        print("\nGame Over!")

    def attack(self, player,):
        self.attacking_player = self.player
        print(f"\n line 108 Your hand: {', '.join(map(str, self.player.hand))}")
        print(f"line 109 AI hand: {', '.join(map(str, self.ai_player.hand))}")
        while True:
            card_index = int(input("line 111 Enter the index of the card you wish to play (0-based): "))
            if card_index >= len(player.hand):
                print("line 113 Invalid card index. Try again.")
                continue
            
            # Player plays the selected card
            played_card = player.play_card(card_index)
            
            if(len(self.table_cards) != 0):

                #logic to check if the attack was successful or not as the human will be attacking the one card that was used in defense by ai
                defending_rank = played_card.get_rank_index()
                attacking_rank = self.table_cards[-1].get_rank_index()

                if ((played_card.suit == self.table_cards[-1].suit and defending_rank > attacking_rank) \
                        or (played_card.suit == self.trump_suit and self.table_cards[-1].suit != self.trump_suit) or (played_card.suit == self.trump_suit and self.table_cards[-1].suit == self.trump_suit and defending_rank > attacking_rank)) :
                    # Attack successful
                    print(f"{player.name} played: {played_card}")
                    self.table_cards.append(played_card)
                    # Print the number of cards on the table and in the deck after a card is played
                    print(f"line 133 Number of cards on the table: {len(self.table_cards)}")
                    print(f"Number of cards left in the deck: {len(self.deck.cards)}")
                    break
                
                else:
                    self.table_cards.append(played_card)
                    # if (self.attacking_player == self.player and self.table_cards !=0 and not self.table_cards[-1] in self.player.has_valid_card(self)):
                    #     print("line 72 Human player was unsuccessful in attacking. AI will now attack.")
                    #     self.player.hand.extend(self.table_cards)
                    #     self.table_cards.clear()
                    #     self.attacking_player = self.ai_player
                    #     self.winning_player = self.ai_player
                    #     self.losing_player = self.player
                    #     self.redistribute_cards(self.losing_player, self.winning_player)
                    break
                # # Attack unsuccessful
                #     print(f"line 138 {player.name} could not attack successfully. Round Over.")
                #     print(f"Number of cards on the table before taking: {len(self.table_cards)}")
                #     player.hand.append(self.table_cards)
                #     player.hand.extend(self.table_cards)
                #     self.table_cards.clear()
                #     print(f"Number of cards on the table after taking: {len(self.table_cards)}")
                #     print(f"Number of cards in {player.name}'s hand after taking cards: {len(player.hand)}")
                #     self.winning_player = self.ai_player
                #     self.losing_player = self.player
                #     self.redistribute_cards(self.losing_player, self.winning_player)
                #     self.attacking_player = self.ai_player
                #     self.defending_player = self.player
                #     break
                    # Switch roles 
                    # self.attacking_player = self.ai_player
                    # print(f"{player.name} was unable to attack successfully, so the roles are switched. AI will be attacking now.")
                # else:
                #     self.is_valid_card_played is False
            else:
                print(f"{player.name} played: {played_card}")
                self.table_cards.append(played_card)
                # Print the number of cards on the table and in the deck after a card is played
                print(f"line 157Number of cards on the table: {len(self.table_cards)}")
                print(f"Number of cards left in the deck: {len(self.deck.cards)}")
                break            

    def ai_attack(self, player):
        self.attacking_player = self.ai_player
        print(f"\nAI is attacking.")
        played_card = player.play_card(self)
        if played_card:
            print(f"{player.name} played: {played_card}")
            self.table_cards.append(played_card)
            print(f"line 168 Number of cards on the table: {len(self.table_cards)}")

        else:
            # self.table_cards.append(played_card)
            # print("line 171 AI couldn't play a card. Round Over")
            # player.hand.extend(self.table_cards)
            # self.table_cards.clear()
            # print(f"Number of cards on the table after taking: {len(self.table_cards)}")
            # print(f"Number of cards in {player.name}'s hand after taking cards: {len(player.hand)}")
            # self.winning_player = self.player
            # self.losing_player = self.ai_player
            # self.redistribute_cards(self.losing_player, self.winning_player)
            played_card = random(self.ai_player.hand)
            self.table_cards.append(played_card)
    def defend(self, player):
        # Display the defending player and let them play a card to defend
        print(f"\n{player.name} is defending.")
        while True:
            if player == self.player:
                print(f"Your hand: {', '.join(map(str, self.player.hand))}")
                card_index = int(input("line 194 Enter the index of the card you wish to play (0-based): "))
                if card_index >= len(player.hand):
                    print("line 196 Invalid card index. Try again.")
                    continue
                played_card = player.play_card(card_index)
                print(f"{player.name} played: {played_card}")
            else:
                played_card = player.play_card(self)
                print(f"{player.name} played: {played_card}")
            if played_card is not None:
                defending_rank = played_card.get_rank_index()
                attacking_rank = self.table_cards[-1].get_rank_index()

                # Check if defending card successfully defends
                if (played_card.suit == self.table_cards[-1].suit and defending_rank > attacking_rank) \
                        or (played_card.suit == self.trump_suit and self.table_cards[-1].suit != self.trump_suit) or (played_card.suit == self.trump_suit and self.table_cards[-1].suit == self.trump_suit and defending_rank > attacking_rank):
                    print(f"line 210 {player.name} successfully defends with {played_card}.")
                    self.table_cards.append(played_card) # append the played card to the table card list
                    # Print the number of cards on the table
                    print(f"Number of cards on the table: {len(self.table_cards)}")
                    break
                else:
                    self.table_cards.append(played_card)
                    print(f"{player.name} could not defend with {played_card}. Round Over.")
                    print(f"line 218 Number of cards on the table before taking: {len(self.table_cards)}")
                    player.hand.extend(self.table_cards)
                    self.table_cards.clear()
                    print(f"Number of cards on the table after taking: {len(self.table_cards)}")
                    print(f"Number of cards in {player.name}'s hand after taking cards: {len(player.hand)}")
                    self.winning_player = self.ai_player
                    self.losing_player = self.player
                    self.redistribute_cards(self.losing_player, self.winning_player)

                    self.attacking_player = self.ai_player
                    print(f"{player.name} was unable to defend successfully so the roles will be be same but the human will take cards from table")
                    break

            else:
                print(f"{player.name} has no valid cards to play. Round Over")
                print(f"line 233 Number of cards on the table before taking: {len(self.table_cards)}")
                player.hand.extend(self.table_cards)
                self.table_cards.clear()
                print(f"Number of cards on the table after taking: {len(self.table_cards)}")
                print(f"Number of cards in {player.name}'s hand after taking cards: {len(player.hand)}")
                self.winning_player = self.ai_player
                self.losing_player = self.player
                self.redistribute_cards(self.losing_player, self.winning_player)
                break

    def ai_defend(self, player):
        print(f"\nAI is defending.")
        ai_played_card = player.play_card(self)
        
        if ai_played_card is not None:
            print(f"{player.name} played: {ai_played_card}")
            defending_rank = ai_played_card.get_rank_index()
            attacking_rank = self.table_cards[-1].get_rank_index()

            # Check if defending card successfully defends
            if (ai_played_card.suit == self.table_cards[-1].suit and defending_rank > attacking_rank) \
                    or (ai_played_card.suit == self.trump_suit and self.table_cards[-1].suit != self.trump_suit):
                print(f"line 254 {player.name} successfully defends with {ai_played_card}.")
                self.table_cards.append(ai_played_card) # append the ai played card to the table card list
                # Print the number of cards on the table
                print(f"Number of cards on the table: {len(self.table_cards)}")
            else:
                print(f"line 259 {player.name} could not defend with {ai_played_card}. Round Over")
                print(f"Number of cards on the table before taking: {len(self.table_cards)}")
                player.hand.extend(self.table_cards)
                self.table_cards.clear()
                print(f"Number of cards on the table after taking: {len(self.table_cards)}")
                print(f"Number of cards in {player.name}'s hand after taking cards: {len(player.hand)}")
                self.winning_player = self.player
                self.losing_player = self.ai_player
                self.redistribute_cards(self.losing_player, self.winning_player)
            
        else:
            print(f"line 270 {player.name} has no valid cards to play. Round Over")
            print(f"Number of cards on the table before taking: {len(self.table_cards)}")
            player.hand.extend(self.table_cards)
            self.table_cards.clear()
            print(f"Number of cards on the table after taking: {len(self.table_cards)}")
            print(f"Number of cards in {player.name}'s hand after taking cards: {len(player.hand)}")
            self.winning_player = self.player
            self.losing_player = self.ai_player
            self.redistribute_cards(self.losing_player, self.winning_player)
            

    def redistribute_cards(self, losing_player, winning_player):
        # TO DO make winning and losing player redistribution and extends of the table card in this function.


        while len(winning_player.hand) < 6 and self.deck.cards:
            winning_player.hand.append(self.deck.deal())

        print(f"line 288 After redistribution, {winning_player.name} has {len(winning_player.hand)} cards.")
        print(f"After redistribution, {losing_player.name} has {len(losing_player.hand)} cards.")
        print(f"Number of cards left in the deck: {len(self.deck.cards)}")

    # def is_valid_card_played(self, card):
    #     if len(self.table_cards) != 0:
    #         defending_rank = card.get_rank_index()
    #         attacking_rank = self.table_cards[-1].get_rank_index()
    #         if ((card.suit == self.table_cards[-1].suit and defending_rank > attacking_rank) \
    #                 or (card.suit == self.trump_suit and self.table_cards[-1].suit != self.trump_suit) \
    #                 or (card.suit == self.trump_suit and self.table_cards[-1].suit == self.trump_suit and defending_rank > attacking_rank)):
    #             return True
    #         else:
    #             return False
    #     else:
    #         return True
    

   

if __name__ == "__main__":
    # Create a game object and start the game
    game = Game()
    game.setup_game()
    game.start_game_loop()
