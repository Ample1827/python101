# Rock, Paper, Scissors Game

import random

def get_choices():
    
    player_choice = input("Enter your choice (rock, paper, scissors): ")
    options = ["rock", "paper", "scissors"]
    computer_choice = random.choice(options)
    choices = {"player": player_choice, "computer": computer_choice}
    
    return choices

   
def check_win(player, computer):
    print(f" You chose {player}, and the computer chose {computer}.")
    if player == computer:
        return "Its a tie!"
    # elif player == "rock"
    elif player == "rock":
        if computer == "scissors":
         return " Rock beats Scissors, You win!"
        else:
         return "Paper beats Rock, You lose :("
    # elif player == "paper"
    elif player == "paper":
        if computer == "rock":
         return "Paper beats Rock, You win!"
        else:
         return "Scissores beats Paper, You lose :("
    # elif player == "scissors"
    elif player == "scissors":
        if computer == "paper":
         return "Scissores beats Paper, You win!"
        else:
         return "Scissores beat Paper, You lose :("
   
choices = get_choices()
result = check_win(choices["player"], choices["computer"])
print(result)