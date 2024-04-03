# main.py
from game import Game

def main():
    print("Welcome to Durak!")
    game = Game()
    game.setup_game()
    game.start_game_loop()

if __name__ == "__main__":
    main()

