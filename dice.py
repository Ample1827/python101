import random


class Dice:
    def __init__(self):
        self.dice1 = 1
        self.dice2 = 1
        self.rolls = []
        for dice1 in range(1, 7):
            for dice2 in range(1, 7):
                self.rolls.append((dice1, dice2))

    
    def roll(self):
        self.dice1 = random.randint(1, 6)
        self.dice2 = random.randint(1, 6)
        return (self.dice1, self.dice2)
    
    
    
class Game:
    choice = ["yes", "no", "y", "n"]

    def play(self):
        while True:
            try:
                play = input("Roll the dice? (yes/no): ").lower()
                if play in ["yes", "y"]:
                    result = dice.roll()
                    print(f"You rolled: {result}")
                elif play in ["no", "n"]:
                    print("Thanks for playing!")
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
            except ValueError:
                print("Invalid input. Please enter 'yes' or 'no'.")
                continue

dice = Dice()
game = Game()
game.play()

