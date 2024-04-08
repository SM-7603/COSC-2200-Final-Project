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
        attacking_player = random.choice([self.player, self.ai_player])

        while self.player.hand and self.ai_player.hand:
            print("\nNew round!")

            # Attacking phase
            print(f"\n{attacking_player.name} is attacking.")

            if isinstance(attacking_player, AIPlayer):
                self.ai_attack(attacking_player)
            else:
                self.attack(attacking_player)

            defending_player = self.ai_player if attacking_player == self.player else self.player

            # Defending phase
            if isinstance(defending_player, AIPlayer):
                self.ai_defend(defending_player)
            else:
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
                self.redistribute_cards()

        print("\nGame over!")

    def attack(self, player,):
        print(f"\nYour hand: {', '.join(map(str, self.player.hand))}")
        
        # There should not be card showing to 
        print(f"AI hand: {', '.join(map(str, self.ai_player.hand))}")

        while True:
            card_index = int(input("Enter the index of the card you wish to play (0-based): "))
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

    def ai_attack(self, player):
        print(f"\nAI is attacking.")
        played_card = player.play_card(self)
        if played_card:
            print(f"{player.name} played: {played_card}")
            self.table_cards.append(played_card)
            print(f"Number of cards on the table: {len(self.table_cards)}")
        else:
            print("AI couldn't play a card. GAME OVER")
            player.hand.extend(self.table_cards)
            self.table_cards.clear()
            print(f"Number of cards on the table after taking: {len(self.table_cards)}")
            print(f"Number of cards in {player.name}'s hand after taking cards: {len(player.hand)}")
            self.winning_player = self.player
            self.losing_player = self.ai_player
            self.redistribute_cards(self.losing_player, self.winning_player)
            
    def defend(self, player):
        print(f"\n{player.name} is defending.")
        while True:
            if player == self.player:
                print(f"Your hand: {', '.join(map(str, self.player.hand))}")
                card_index = int(input("Enter the index of the card you wish to play (0-based): "))
                if card_index >= len(player.hand):
                    print("Invalid card index. Try again.")
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
                        or (played_card.suit == self.trump_suit and self.table_cards[-1].suit != self.trump_suit and defending_rank > attacking_rank):
                    print(f"{player.name} successfully defends with {played_card}.")
                    self.table_cards.append(played_card) # append the played card to the table card list
                    # Print the number of cards on the table
                    print(f"Number of cards on the table: {len(self.table_cards)}")
                    break
                else:
                    self.table_cards.append(played_card)
                    print(f"{player.name} could not defend with {played_card}. GAME OVER.")
                    print(f"Number of cards on the table before taking: {len(self.table_cards)}")
                    player.hand.extend(self.table_cards)
                    self.table_cards.clear()
                    print(f"Number of cards on the table after taking: {len(self.table_cards)}")
                    print(f"Number of cards in {player.name}'s hand after taking cards: {len(player.hand)}")
                    self.winning_player = self.ai_player
                    self.losing_player = self.player
                    self.redistribute_cards(self.losing_player, self.winning_player)
                    break
            else:
                print(f"{player.name} has no valid cards to play. GAME OVER")
                print(f"Number of cards on the table before taking: {len(self.table_cards)}")
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
                print(f"{player.name} successfully defends with {ai_played_card}.")
                self.table_cards.append(ai_played_card) # append the ai played card to the table card list
                # Print the number of cards on the table
                print(f"Number of cards on the table: {len(self.table_cards)}")
            else:
                print(f"{player.name} could not defend with {ai_played_card}. GAME OVER")
                print(f"Number of cards on the table before taking: {len(self.table_cards)}")
                player.hand.extend(self.table_cards)
                self.table_cards.clear()
                print(f"Number of cards on the table after taking: {len(self.table_cards)}")
                print(f"Number of cards in {player.name}'s hand after taking cards: {len(player.hand)}")
                self.winning_player = self.player
                self.losing_player = self.ai_player
                self.redistribute_cards(self.losing_player, self.winning_player)
        else:
            print(f"{player.name} has no valid cards to play. GAME OVER")
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

        print(f"After redistribution, {winning_player.name} has {len(winning_player.hand)} cards.")
        print(f"After redistribution, {losing_player.name} has {len(losing_player.hand)} cards.")

if __name__ == "__main__":
    game = Game()
    game.setup_game()
    game.start_game_loop()


    