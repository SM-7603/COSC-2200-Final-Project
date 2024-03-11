# Durak PROJECT STRUCTURE.

> This is the project structre for the game Durak.

durak_game/
│
├── main.py                  # Entry point of the game, initializes the game and starts the main loop
├── game.py                  # Contains the Game class with the main game logic
├── player.py                # Contains the Player and AIPlayer classes
├── card.py                  # Contains the Card class
├── deck.py                  # Contains the Deck class
├── ui.py                    # Contains the GameWindow class for Pygame UI components
├── data_persistence.py      # Handles saving and loading game data, preferences, etc., using JSON
│
├── assets/                  # Folder for graphical assets like card images
│   ├── card_faces/          # Contains images for each card face
│   └── back.png             # Back of the card image
│
├── data/                    # Folder for data persistence (e.g., JSON files)
│   ├── game_states.json     # Save game states
│   ├── user_preferences.json# User preferences settings
│   └── system_settings.json # System-wide game settings
│
└── requirements.txt         # Python package requirements, mainly Pygame