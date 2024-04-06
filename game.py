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
        self.attacking_player = None
        self.defending_player = None

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
        self.attacking_player = random.choice([self.player, self.ai_player])
        self.defending_player = self.ai_player if self.attacking_player == self.player else self.player
        print(f"{self.attacking_player.name} will start as the attacker.")

    def start_game_loop(self):
        while self.player.hand and self.ai_player.hand:
            print("\nNew round!")
            print(f"{self.attacking_player.name} is attacking.")
            print(f"{self.defending_player.name} is defending.")

            # Attacking phase
            if isinstance(self.attacking_player, AIPlayer):
                self.ai_attack()
            else:
                self.human_attack()

            # Defending phase
            if isinstance(self.defending_player, AIPlayer):
                defense_successful = self.ai_defend()
            else:
                defense_successful = self.human_defend()

            # Handle the outcome of the defense
            if defense_successful:
                print(f"Defense was successful. {self.defending_player.name} takes no cards.")
                self.table_cards.clear()
                self.switch_roles()
            else:
                print(f"Defense failed. {self.defending_player.name} takes the table cards.")
                self.defending_player.hand.extend(self.table_cards)
                self.table_cards.clear()
            
            # Redistribute cards after the round to ensure both players have 6 cards if possible
            self.redistribute_cards()

            print(f"After the round, {self.attacking_player.name} has {len(self.attacking_player.hand)} cards.")
            print(f"After the round, {self.defending_player.name} has {len(self.defending_player.hand)} cards.")

        print("\nGame over!")



    def human_attack(self):
        # Additional debug statement to show current player's hand
        print(f"\n{self.attacking_player.name}'s hand: {', '.join(map(str, self.attacking_player.hand))}")
        print(f"\n{self.defending_player.name}'s hand: {', '.join(map(str, self.defending_player.hand))}")
        card_index = int(input("Enter the index of the card you wish to play (0-based): "))
        played_card = self.attacking_player.play_card(card_index)
        print(f"{self.attacking_player.name} played: {played_card}")
        self.table_cards.append(played_card)
        print(f"Number of cards on the table: {len(self.table_cards)}")
        print(f"Number of cards left in the deck: {len(self.deck.cards)}")

    def ai_attack(self):
        played_card = self.attacking_player.play_card(self)
        print(f"{self.attacking_player.name} played: {played_card}")
        self.table_cards.append(played_card)
        print(f"Number of cards on the table: {len(self.table_cards)}")

    def human_defend(self):
        print(f"\n{self.defending_player.name}'s hand: {', '.join(map(str, self.defending_player.hand))}")
        print(f"\n{self.attacking_player.name}'s hand: {', '.join(map(str, self.attacking_player.hand))}")
        card_index = int(input("Enter the index of the card you wish to play (0-based): "))
        played_card = self.defending_player.play_card(card_index)
        print(f"{self.defending_player.name} played: {played_card}")

        if self.is_valid_defense(played_card):
            print(f"{self.defending_player.name} successfully defends with {played_card}.")
            self.table_cards.append(played_card)
            return True
        else:
            print(f"{self.defending_player.name} could not defend with {played_card}.")
            self.defending_player.hand.extend(self.table_cards)
            self.table_cards.clear()
            print(f"{self.defending_player.name} is taking the cards from the table.")
            self.redistribute_cards()
            return False

    def ai_defend(self):
        played_card = self.defending_player.play_card(self)
        print(f"{self.defending_player.name} played: {played_card}")

        if self.is_valid_defense(played_card):
            print(f"{self.defending_player.name} successfully defends with {played_card}.")
            self.table_cards.append(played_card)
            return True
        else:
            self.defending_player.hand.extend(self.table_cards)
            self.table_cards.clear()
            return False

    def is_valid_defense(self, defending_card):
        attacking_card = self.table_cards[-1]
        defending_rank = defending_card.get_rank_index()
        attacking_rank = attacking_card.get_rank_index()
        if defending_card.suit == attacking_card.suit and defending_rank > attacking_rank:
            return True
        elif defending_card.suit == self.trump_suit and attacking_card.suit != self.trump_suit:
            return True
        else:
            return False

    def redistribute_cards(self):
        print("Redistributing cards.")
        # Both players draw cards from the deck until they have 6 cards or the deck is empty
        for player in [self.attacking_player, self.defending_player]:
            while len(player.hand) < 6 and self.deck.cards:
                player.draw_card(self.deck)
            print(f"After redistribution, {player.name} has {len(player.hand)} cards.")

    def switch_roles(self):
        self.attacking_player, self.defending_player = self.defending_player, self.attacking_player
        print(f"Roles have switched! {self.attacking_player.name} is now attacking.")
        print(f"{self.defending_player.name} is now defending.")

if __name__ == "__main__":
    game = Game()
    game.setup_game()
    game.start_game_loop()
