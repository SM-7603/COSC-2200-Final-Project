from deck import Deck
from player import AIPlayer, Player

class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player("Human")
        self.ai_player = AIPlayer()
        self.trump_suit = None
        self.table_cards = []

    def setup_game(self):
        self.deck.shuffle()
        # Deal 6 cards to each player
        for _ in range(6):
            self.player.draw_card(self.deck)
            self.ai_player.draw_card(self.deck)
        # Determine the trump suit
        self.trump_suit = self.deck.cards[-1].suit
        print(f"The trump suit is {self.trump_suit}")
            # Print the number of cards left in the deck
        print(f"Number of cards left in the deck: {len(self.deck.cards)}")

    def start_game_loop(self):
        attacking_player = self.player

        while self.player.hand and self.ai_player.hand:
            print("\nNew round!")
            # self.table_cards.clear() # clearing this, now fixed the issue with the cards on the table not 

            # Attacking phase
            print(f"\n{attacking_player.name} is attacking.")
            self.attack(attacking_player)
            defending_player = self.ai_player if attacking_player == self.player else self.player

            # Defending phase
            self.defend(defending_player)

            if not defending_player.hand:
                print(f"{defending_player.name} couldn't defend. Taking cards...")
                defending_player.hand.extend(self.table_cards)
                self.table_cards.clear()
                if defending_player == self.player:
                    print("AI wins this round!")
                else:
                    print("You win this round!")
                attacking_player = self.ai_player if defending_player == self.player else self.player
                self.redistribute_cards(attacking_player)

        print("\nGame over!")

    def attack(self, player):
        print(f"\nYour hand: {', '.join(map(str, self.player.hand))}")
        print(f"AI hand: {', '.join(map(str, self.ai_player.hand))}")
        while True:
            card_index = int(input("Enter the index of the card you wish to play (0-based), or 'q' to quit: "))
            if card_index == 'q':
                print("You chose to quit. AI wins this round!")
                # transfer the table cards to the player's hands
                self.player.hand.extend(self.table_cards)
                self.table_cards.clear() # it should clear the table, once the cards are gone to the loser
                attacking_player = self.ai_player
                self.redistribute_cards(attacking_player)
                break
            if card_index >= len(player.hand):
                print("Invalid card index. Try again.")
                continue
            played_card = player.play_card(card_index)
            print(f"{player.name} played: {played_card}")
            self.table_cards.append(played_card)
            # Print the number of cards on the table and in the deck after a card is played
            print(f"Number of cards on the table: {len(self.table_cards)}")
            print(f"Number of cards left in the deck: {len(self.deck.cards)}")
            break

    def defend(self, player):
        print(f"\n{player.name} is defending.")
        ai_played_card = player.play_card(self)
        if ai_played_card is not None:
            print(f"{player.name} played: {ai_played_card}")
            # Use get_rank_index for comparison
            defending_rank = ai_played_card.get_rank_index()
            attacking_rank = self.table_cards[-1].get_rank_index()

            # Check if defending card successfully defends
            if (ai_played_card.suit == self.table_cards[-1].suit and defending_rank > attacking_rank) \
                    or (ai_played_card.suit == self.trump_suit and self.table_cards[-1].suit != self.trump_suit):
                print(f"{player.name} successfully defends with {ai_played_card}.")
                # Print the number of cards on the table
                print(f"Number of cards on the table: {len(self.table_cards)}")
                self.table_cards.append(ai_played_card) # append the ai played card to the table card list
                # self.table_cards.clear()  # Clearing table cards after successful defense
                # print(f"Number of cards on the table after clearing: {len(self.table_cards)}")  # Should be 0
                return True
            # This should be appended, when the player loses
            # i.e. all the cards on the table should go to the player that lost
            # I don't think this block is even being used ¯\_(ツ)_/¯
            else:
                print(f"{player.name} could not defend with {ai_played_card}. Taking cards...")
                print(f"Number of cards on the table before taking: {len(self.table_cards)}")
                player.hand.extend(self.table_cards)
                self.table_cards.clear()
                print(f"Number of cards on the table after taking: {len(self.table_cards)}")
                print(f"Number of cards in {player.name}'s hand after taking cards: {len(player.hand)}")
                return False
        else:
            print(f"{player.name} has no valid cards to play. Taking cards...")
            print(f"Number of cards on the table before taking: {len(self.table_cards)}")
            player.hand.extend(self.table_cards)
            self.table_cards.clear()
            print(f"Number of cards on the table after taking: {len(self.table_cards)}")
            print(f"Number of cards in {player.name}'s hand after taking cards: {len(player.hand)}")
            return False

    def redistribute_cards(self):
        # Determine the order for drawing cards based on the game rules
        if self.table_cards:  # Check if there are cards on the table indicating a defense failure
            # The defending player failed to defend and has already taken the table cards
            drawing_order = [self.defending_player, self.attacking_player]
        else:
            # Defense was successful, no cards to take from the table
            drawing_order = [self.attacking_player, self.defending_player]

        for player in drawing_order:
            while len(player.hand) < 6 and len(self.deck.cards) > 0:
                player.hand.append(self.deck.deal())

        print(f"After redistribution, {self.attacking_player.name} has {len(self.attacking_player.hand)} cards.")
        print(f"After redistribution, {self.defending_player.name} has {len(self.defending_player.hand)} cards.")

if __name__ == "__main__":
    game = Game()
    game.setup_game()
    game.start_game_loop()
