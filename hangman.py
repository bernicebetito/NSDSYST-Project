import os


class Hangman:
    def __init__(self, word):
        self.word = []
        self.word[:0] = word.upper()
        self.guess_word = ["_" for _ in range(len(self.word))]
        self.letters = [chr(65 + x) for x in range(26)]
        self.lives = 6
        self.winner = "Player One"

    def gameContinue(self):
        if self.guess_word == self.word:
            self.winner = "Player Two"
            return False
        elif self.lives == 0:
            self.guess_word = self.word
            return False
        return True

    def findLetter(self, letter):
        if letter.upper() in self.letters and letter.upper() in self.word and letter.upper() not in self.guess_word:
            indexes = [a for a, x in enumerate(self.word) if x == letter.upper()]
            self.guess_word = [letter.upper() if x in indexes else self.guess_word[x] for x in range(len(self.guess_word))]
            self.letters[self.letters.index(letter.upper())] = " "
            return True
        elif letter.upper() in self.guess_word or not letter.upper() in self.letters:
            return False
        self.letters[self.letters.index(letter.upper())] = " "
        self.lives -= 1
        return True

    def guessWord(self, word):
        guess = []
        guess[:0] = word.upper()
        if guess != self.word:
            self.lives -= 1
        else:
            self.guess_word = guess
        return True

    def printWord(self):
        space = " "
        space_letters = space * int(abs(len(self.word) - (len(f"{len(self.word)} Letters") / 4)))
        space_drawing = space * int(abs(len(self.word) - (len("=============") / 4)))
        space_lives = space * int(abs(len(self.word) - (len(f"LIVES REMAINING: {self.lives}") / 4)))

        drawing = ["-", "-", "\\", "/", "|", "O"]
        drawing = [" " if x + 1 <= self.lives else drawing[x] for x in range(len(drawing))]
        print(f"\n\t{space_drawing}=============")
        print(f"\t{space_drawing}||        |")
        print(f"\t{space_drawing}||        {drawing[5]}")
        print(f"\t{space_drawing}||       {drawing[1]}{drawing[4]}{drawing[0]}")
        print(f"\t{space_drawing}||       {drawing[3]} {drawing[2]}")
        print(f"\t{space_drawing}||\n\n")
        print(f"\t{space_lives}LIVES REMAINING: {self.lives}")

        print(f"\n\t{space_letters}{len(self.word)} Letters\n", end="\n\t")
        for letter in self.guess_word:
            print(letter, end=" ")

        space_avail = space * int((len(self.word) - (13 / 4)) - (len("AVAILABLE LETTERS") / 4))
        space_alpha = space * int(len(self.word) - (13 / 4))
        print(f"\n\n\n\t{space_avail}AVAILABLE LETTERS\n", end=f"\n{space_alpha}")
        for letter in range(len(self.letters)):
            print(self.letters[letter], end=" ")
            if letter == 12:
                print(end=f"\n{space_alpha}")


if __name__ == "__main__":
    try:
        word = "0"
        while not word.isalpha() or len(word) <= 1:
            word = input("PLAYER ONE\nEnter a Word for Player Two to guess:\t")
            if not word.isalpha() or len(word) <= 1:
                print("Invalid Word! Please enter a valid word.\n")
        hangman = Hangman(word)

        while hangman.gameContinue():
            os.system("cls" if os.name == "nt" else "clear")
            hangman.printWord()
            print("\n\n")

            playerTurn = False
            playerGuess = False
            print("\nPLAYER TWO\nTo guess the word, enter [GUESS]")
            while not playerTurn and not playerGuess:
                player_guess = input("Enter a letter:\t")
                if player_guess.isalpha():
                    if player_guess.upper() == "GUESS":
                        playerGuess = True
                    elif len(player_guess) == 1:
                        playerTurn = hangman.findLetter(player_guess)
                        if not playerTurn:
                            print("Letter already guessed!\n")
                    else:
                        print("Invalid letter!\n")
                else:
                    print("Invalid letter!\n")

            while playerGuess and not playerTurn:
                guess_word = input("\nEnter your guess:\t")
                if all(x.isalpha() or x.isspace() for x in guess_word) or len(guess_word) <= 1:
                    playerTurn = hangman.guessWord(guess_word)
                else:
                    print("Invalid Word! Please enter a valid word.\n")

        os.system("cls" if os.name == "nt" else "clear")
        hangman.printWord()

        print(f"\n\nGame Over! {hangman.winner} wins!")
    except KeyboardInterrupt:
        print("\nThank you for playing!")