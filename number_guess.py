import random

class NumberGuess:
    def __init__(self):
        self.number_to_guess = random.randint(1, 100)


class Game:
    def __init__(self):
        self.number_guess = NumberGuess()

    def play(self):
        n = self.number_guess.number_to_guess
        while True:
            try:
                guess = int(input("Guess a number between 1 and 100: "))
                if guess < 1 or guess > 100:
                    print("Invalid input. Please enter a number between 1 and 100.")
                    continue
                if guess == n:
                    print("Congratulations! You've guessed the number!")
                    break
                elif guess < n:
                    print("Too low! Try again.")
                else:
                    print("Too high! Try again.")
            except ValueError:
                print("Please enter a valid integer.")

g = Game()
g.play()
