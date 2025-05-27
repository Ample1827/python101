import random

def game_mode():
    player_mode = input("Enter your game mode (easy, medium, hard): ").lower()
    options = ["easy", "medium", "hard"]
    
    if player_mode not in options:
        print("Invalid mode. Please choose from easy, medium, or hard.")
        return game_mode()
    
    return player_mode

def get_player_choice():
    player_choice = input("Enter your choice (rock, paper, scissors): ").lower()
    options = ["rock", "paper", "scissors"]
    
    if player_choice not in options:
        print("Invalid choice. Please choose from rock, paper, or scissors.")
        return get_player_choice()
    
    return player_choice

def get_computer_choice(mode, player_choice):
    win_map = {
        "rock":"scissors",
        "paper":"rock",
        "scissors":"paper"
    }
    lose_map = {loser: winner for winner, loser in win_map.items()}
    
    if mode == "easy":
        # Computer always loses to the player
        return win_map[player_choice]
    
    elif mode == "medium":
        # 50/50 chance of winning or losing
        return lose_map[player_choice] if random.random() < 0.5 else win_map[player_choice]
    
    elif mode == "hard":
        # 80% chance computer wins
        return lose_map[player_choice] if random.random() < 0.8 else win_map[player_choice]
    
    # Fallback (should not happen)
    return random.choice(["rock", "paper", "scissors"])

def check_win(player, computer):
    print(f"You chose {player}, and the computer chose {computer}.")
    if player == computer:
        return "It's a tie!"
    elif (player == "rock" and computer == "scissors") or \
         (player == "paper" and computer == "rock") or \
         (player == "scissors" and computer == "paper"):
        return "You win!"
    else:
        return "You lose!"

def play_game():
    mode = game_mode()
    player_choice = get_player_choice()
    computer_choice = get_computer_choice(mode, player_choice)
    result = check_win(player_choice, computer_choice)
    print(result)

# Start the game
play_game()
