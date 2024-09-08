import random

def init_game() -> dict:
    """
    Initializes the game data structure.

    Returns:
        dict: A dictionary containing game settings, including the number of rows and columns,
              player scores, the game board, and other necessary game state information.
    """
    rows, columns = 4, 4
    cards = ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E', 'F', 'F', 'G', 'G', 'H', 'H']

    game_data = {
        'rows': rows,
        'columns': columns,
        'score': {'player1': 0, 'player2': 0},
        'turn': 'player1',
        'game_over': False,
        'board': prepare_board(rows, columns, cards),
        'move_history': []  # all of the card flips till now
    }
    return game_data

def prepare_board(rows, columns, cards) -> dict:
    """
    Prepares the game board by shuffling cards and placing them into the board structure.

    Args:
        rows (int): Number of rows in the board.
        columns (int): Number of columns in the board.
        cards (list): List of card values to be placed on the board.

    Returns:
        dict: A dictionary representing the game board, where each key is a tuple (row, col)
              and the value is a dictionary with card information (card value, flipped state, matched state).
    """
    board = {}
    random.shuffle(cards)
    index = 0
    for row in range(rows):
        for col in range(columns):
            board[(row, col)] = {'card': cards[index], 'flipped': False, 'matched': False}
            index += 1
    return board

def play(game_data) -> None:
    """
    Runs the main game loop, handling player turns, guessing, and score updates.

    Args:
        game_data (dict): The game data dictionary containing the board, scores, and other game information.
    """
    while not game_data['game_over']:
        display_board(game_data)
        guess1 = get_valid_card(game_data)
        display_board(game_data)
        guess2 = get_valid_card(game_data)
        display_board(game_data)

        if match(game_data, guess1, guess2):
            update_score(game_data)
            print("Match found!")
        else:
            flip_back_cards(game_data, guess1, guess2)
            print("No match.")

        game_data['move_history'].append((guess1, guess2))
        check_game_over(game_data)

        if not game_data['game_over']:
            game_data['turn'] = 'player1' if game_data['turn'] == 'player2' else 'player2'

    print(f"Game Over! Final scores: Player 1 - {game_data['score']['player1']}, Player 2 - {game_data['score']['player2']}")

def display_board(game_data):
    """
    Displays the current state of the game board to the user.

    Args:
        game_data (dict): The game data dictionary containing the board and other game information.
    """
    rows, columns = game_data['rows'], game_data['columns']
    board = game_data['board']
    print("  " + " ".join(str(i+1) for i in range(columns)))
    for row in range(rows):
        row_display = [board[(row, col)]['card'] if board[(row, col)]['flipped'] else '*' for col in range(columns)]
        print(f"{row+1} " + " ".join(row_display))

def get_valid_card(game_data):
    """
    Prompts the current player to select a card and ensures the selection is valid.

    Args:
        game_data (dict): The game data dictionary containing the board and other game information.

    Returns:
        tuple: The coordinates of the selected card (row, column).
    """
    while True:
        try:
            row = int(input(f"Player {game_data['turn']}, enter the row number (1-{game_data['rows']}): ")) - 1
            col = int(input(f"Player {game_data['turn']}, enter the column number (1-{game_data['columns']}): ")) - 1
            if (0 <= row < game_data['rows']) and (0 <= col < game_data['columns']):
                if not game_data['board'][(row, col)]['flipped']:
                    game_data['board'][(row, col)]['flipped'] = True
                    return (row, col)
                else:
                    print("Card already revealed. Choose another card.")
            else:
                print("Invalid input. Try again.")
        except ValueError:
            print("Invalid input. Please enter integers.")

def match(game_data, guess1, guess2) -> bool:
    """
    Checks if the two selected cards match.

    Args:
        game_data (dict): The game data dictionary containing the board.
        guess1 (tuple): The coordinates of the first card.
        guess2 (tuple): The coordinates of the second card.

    Returns:
        bool: True if the cards match, False otherwise.
    """
    card1 = game_data['board'][guess1]['card']
    card2 = game_data['board'][guess2]['card']

    if card1 == card2:
        game_data['board'][guess1]['matched'] = True
        game_data['board'][guess2]['matched'] = True
        return True
    return False

def update_score(game_data):
    """
    Updates the score of the current player.

    Args:
        game_data (dict): The game data dictionary containing the score and turn information.
    """
    current_player = game_data['turn']
    game_data['score'][current_player] += 1

def flip_back_cards(game_data, guess1, guess2):
    """
    Flips back the two selected cards if they do not match.

    Args:
        game_data (dict): The game data dictionary containing the board.
        guess1 (tuple): The coordinates of the first card.
        guess2 (tuple): The coordinates of the second card.
    """
    game_data['board'][guess1]['flipped'] = False
    game_data['board'][guess2]['flipped'] = False

def check_game_over(game_data):
    """
    Checks if the game is over (all pairs are matched).

    Args:
        game_data (dict): The game data dictionary containing the board.

    Returns:
        bool: True if the game is over, False otherwise.
    """
    for card_info in game_data['board'].values():
        if not card_info['matched']:
            return False
    game_data['game_over'] = True
    return True
