import random

class Game:
    def __init__(self):
        self.number_to_guess = random.randint(1, 100)
       
    def play(self):
        while True:
            try:
                guess = int(input("Guess a number between 1 and 100: "))
                if guess == self.number_to_guess:
                    print("Congratulations! You've guessed the number!")
                    break
                elif guess < self.number_to_guess:
                    print("Too low! Try again.")
                else:
                    print("Too high! Try again.")
            except ValueError:
                print("Please enter a valid Number.")

g = Game()
g.play()

