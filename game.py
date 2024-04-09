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

    def setup_game(self):
        self.deck.shuffle()
        for _ in range(6):
            self.player.draw_card(self.deck)
            self.ai_player.draw_card(self.deck)
        
        self.trump_suit = self.deck.cards[-1].suit
        print(f"The trump suit is {self.trump_suit}")
        print(f"Number of cards left in the deck: {len(self.deck.cards)}")

    def start_game_loop(self):
        while self.player.hand and self.ai_player.hand:
            self.attacking_player = random.choice([self.player, self.ai_player])
            print(f"\n{self.attacking_player.name} is attacking.")
            self.execute_turn(self.attacking_player)

            if not self.player.hand or not self.ai_player.hand:
                break  # End game if any player runs out of cards

            self.switch_players()
        
        print("\nGame Over!")

    def execute_turn(self, attacking_player):
        if isinstance(attacking_player, AIPlayer):
            self.perform_ai_attack()
        else:
            self.perform_player_attack()

        self.defending_player = self.ai_player if attacking_player == self.player else self.player
        if isinstance(self.defending_player, AIPlayer):
            self.perform_ai_defend()
        else:
            self.perform_player_defend()

    def perform_ai_attack(self):
        card = self.ai_player.play_card(self)
        self.process_card_played(card, self.ai_player)

    def perform_player_attack(self):
        card = self.prompt_player_card(self.player)
        self.process_card_played(card, self.player)

    def perform_ai_defend(self):
        card = self.ai_player.play_card(self)
        self.process_card_played(card, self.ai_player)

    def perform_player_defend(self):
        card = self.prompt_player_card(self.player)
        self.process_card_played(card, self.player)

    def prompt_player_card(self, player):
        while True:
            print(f"Your hand: {', '.join(map(str, player.hand))}")
            try:
                card_index = int(input("Choose a card to play (0-based index): "))
                if 0 <= card_index < len(player.hand):
                    return player.play_card(card_index)
            except ValueError:
                pass
            print("Invalid selection. Try again.")

    def process_card_played(self, card, player):
        if card:
            print(f"{player.name} played: {card}")
            self.table_cards.append(card)
            print(f"Number of cards on the table: {len(self.table_cards)}")
        else:
            print(f"{player.name} couldn't play a valid card. Round Over.")
            self.handle_round_completion()

    def handle_round_completion(self):
        loser = self.defending_player if self.table_cards else self.attacking_player
        winner = self.player if loser == self.ai_player else self.ai_player
        loser.hand.extend(self.table_cards)
        self.table_cards.clear()
        self.redistribute_cards(loser, winner)
        self.attacking_player = winner  # Winner attacks next

    def redistribute_cards(self, losing_player, winning_player):
        while len(winning_player.hand) < 6 and self.deck.cards:
            winning_player.hand.append(self.deck.deal())
        print(f"After redistribution, {winning_player.name} has {len(winning_player.hand)} cards.")
        print(f"After redistribution, {losing_player.name} has {len(losing_player.hand)} cards.")
        print(f"Number of cards left in the deck: {len(self.deck.cards)}")

    def switch_players(self):
        self.attacking_player, self.defending_player = self.defending_player, self.attacking_player

if __name__ == "__main__":
    game = Game()
    game.setup_game()
    game.start_game_loop()
