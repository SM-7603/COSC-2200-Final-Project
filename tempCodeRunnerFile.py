import tkinter as tk
from game import Game

class DurakApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Durak")
        
        self.game = Game()

        self.welcome_label = tk.Label(root, text="Welcome to Durak!", font=("Helvetica", 16))
        self.welcome_label.pack()

        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_button.pack()

    def start_game(self):
        self.game.setup_game()
        self.game.start_game_loop()

if __name__ == "__main__":
    root = tk.Tk()
    app = DurakApp(root)
    root.mainloop()
