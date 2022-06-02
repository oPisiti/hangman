import os
import random

clearConsole = lambda: os.system('cls')
pathToParts = "hangmanParts.txt"
pathToWords = "possibleWords.txt"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    UPONELINE = '\033[F'

class Hangman():
    def __init__(self) -> None:        
        with open(pathToParts, mode="r") as p:
            self.hangmanParts = p.read().split("\n\n")
        
        with open(pathToWords, mode="r") as w:
            words = w.read().split("\n")

            self.chosenWord = words[random.randint(0, len(words)-1)]
            self.correctGuesses = "_"*len(self.chosenWord)

        self.score = {
            "current":0,
            "errors":0,
            "max":len(self.chosenWord)
        }

        self.previousGuesses = set()
    
    # Main game loop
    def start(self):
        while True:            
            self.render()

            # Getting valid input
            userGuess = input().lower()
            if len(userGuess) > 1 or not userGuess.isalpha(): continue

            self.checkInput(userGuess)

            # End of game
            if self.score["current"] >= self.score["max"]:
                self.endGame(won=True)
            if self.score["errors"] >= len(self.hangmanParts)-1:
                self.endGame(won=False)

    def checkInput(self, guess):
        foundGuess = False
        if guess in self.previousGuesses: return

        for i, letter in enumerate(self.chosenWord):
            if letter == guess:
                self.correctGuesses = self.correctGuesses[:i] + letter + self.correctGuesses[i+1:]
                self.score["current"] += 1
                foundGuess = True

        if not foundGuess:  self.score["errors"] += 1

        self.previousGuesses.add(guess)

    def render(self):
        clearConsole()
        print(self.hangmanParts[self.score["errors"]])
        print()
        print("   " + self.correctGuesses + "\n")
        print(f"Word size: {len(self.chosenWord)}")
        print("Previous guesses: " + (f"{self.previousGuesses}" if len(self.previousGuesses)>0 else ""))
        print("Current guess: ", end="")

    # Renders the game one last time with result and terminates the program
    def endGame(self, won:bool):
        self.render()
        print("\nYou " + ((bcolors.OKGREEN + "WON") if won else (bcolors.FAIL + "LOST")) + bcolors.ENDC + "!")
        if not won: print(f"The word was: {self.chosenWord}")
        input()
        quit()

if __name__ == "__main__":
    myGame = Hangman()
    myGame.start()