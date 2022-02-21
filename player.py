import socket, json, re, os

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Function to convert a json object into a python object
def to_python(jsonObj):
    data = json.loads(jsonObj)
    return data


# Function to convert a python object into a json object
def to_json(pythonObj):
    data = json.dumps(pythonObj)
    return data


# JSON commands
join = '{"command": "join", "username": "", "game": ""}'
action = '{"command": "action", "action": "", "name": ""}'


class TicTacToePlayer(object):
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.grid_content = [["     " for _ in range(3)] for _ in range(3)]
        self.moves = dict()
        self.winner = "Draw"

        count = 1
        for row in range(len(self.grid_content)):
            for col in range(len(self.grid_content[row])):
                self.moves[count] = (row, col)
                count += 1

    def print_board(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("-" * 30)
        for row in self.grid_content:
            print("         |" * 3, end="\n")
            for column in row:
                print(" ", column, end="  |")
            print("\n         |", end="")
            print("         |" * 2, end="\n")
            print("-" * 30, end="\n")

    def connect_to_server(self):
        global sock
        self.username = input("Ready to connect to lobby. Please enter your username: ")
        print("Connecting to lobby...")

        # Ready join request
        self.joinRequest = to_python(join)
        self.joinRequest["username"] = self.username
        self.joinRequest["game"] = "tictactoe"
        self.joinRequest = to_json(self.joinRequest)

        # Send join request
        sock.sendto(bytes(self.joinRequest, "utf-8"), (self.server_host, self.server_port))

        # Process return code
        self.data = sock.recvfrom(1024)
        self.return_code = to_python(self.data[0])

        if self.return_code["code"] == "SUCCESS":
            print("You have joined the lobby.")
            return 1

        elif self.return_code["code"] == "ERROR":
            print("An error has occurred")

        else:
            print("Something went wrong")

    def playerTurn(self, move):
        if move in self.moves:
            if self.grid_content[self.moves[move][0]][self.moves[move][1]] == "     ":
                return True
        return False

    def getMoves(self):
        print("      Possible Locations\n")

        loc_count = 1
        for row in range(len(self.grid_content)):
            print(end="  ")
            for col in range(len(self.grid_content[row])):
                if self.grid_content[row][col] == "     ":
                    if col == 0:
                        edge = "   "
                    else:
                        edge = "|  "
                    print(f"{edge}[{loc_count}]", end="  ")
                else:
                    if col == 0:
                        print(end="        ")
                    else:
                        print(end="|       ")
                loc_count += 1
            print("\n", end="  ")
            if row < len(self.grid_content) - 1:
                print("-" * 25)

    def gameplay(self):
        global sock
        global joined
        while joined == 1:

            # Receive game state
            self.data = sock.recvfrom(1024)
            self.game_state = to_python(self.data[0])
            print(self.data[1])
            print(self.game_state)

            if self.game_state["command"] == "game_state":
                if self.game_state["continue"] == "true":

                    # Print game board
                    self.grid_content = self.game_state["board"]
                    self.print_board()

                    # Check if it is player's turn
                    turn = self.game_state["turn"]

                    if self.username == turn:
                        self.getMoves()
                        valid_move = False
                        while not valid_move:
                            player_move = input("\nEnter Location of " + self.game_state["icon"] + " : ")

                            if player_move.isdigit():
                                if 0 < int(player_move) < 10:
                                    playerTurn = self.playerTurn(int(player_move))

                                    if not playerTurn:
                                        print("Tile already occupied!\n")
                                        continue
                                    valid_move = True

                                else:
                                    print("Invalid location!\n")

                            else:
                                print("Invalid location!\n")

                        # Ready action
                        self.action = to_python(action)
                        self.action["action"] = player_move
                        self.action["name"] = self.username
                        self.action = to_json(self.action)

                        # Send action
                        sock.sendto(bytes(self.action, "utf-8"), (self.server_host, self.server_port))

                    else:
                        print(f"It is currently {turn}'s turn")

                else:
                    self.print_board()
                    if self.game_state["winner"] == "draw":
                        print(f"\nGame Over! Draw between X and O!")

                    elif self.game_state["winner"] != "draw":
                        winner = self.game_state["winner"]
                        print(f"\nGame Over! {winner} wins!")

                    joined = 0


class HangmanPlayer(object):
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.word = []
        self.letters = [chr(65 + x) for x in range(26)]
        self.lives = 6
        self.winner = "Player One"

    def connect_to_server(self):
        global sock
        self.username = input("Ready to connect to lobby. Please enter your username: ")
        print("Connecting to lobby...")

        # Ready join request
        self.joinRequest = to_python(join)
        self.joinRequest["username"] = self.username
        self.joinRequest["game"] = "hangman"
        self.joinRequest = to_json(self.joinRequest)

        # Send join request
        sock.sendto(bytes(self.joinRequest, "utf-8"), (self.server_host, self.server_port))

        # Process return code
        self.data = sock.recvfrom(1024)
        self.return_code = to_python(self.data[0])

        if self.return_code["code"] == "SUCCESS":
            print("You have joined the lobby.")
            return 1

        elif self.return_code["code"] == "ERROR":
            print("An error has occurred")

        else:
            print("Something went wrong")

    def initWord(self, word, guess_word):
        self.word[:0] = word
        self.guess_word = guess_word

    def findLetter(self, letter):
        if letter.upper() in self.letters and letter.upper() in self.word and letter.upper() not in self.guess_word:
            self.letters[self.letters.index(letter.upper())] = " "
            return True
        elif letter.upper() in self.guess_word or not letter.upper() in self.letters:
            return False
        self.letters[self.letters.index(letter.upper())] = " "
        return True

    def printWord(self):
        os.system("cls" if os.name == "nt" else "clear")
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

    def gameplay(self):
        global sock
        global joined
        while joined == 1:

            # Receive game state
            self.data = sock.recvfrom(1024)
            self.game_state = to_python(self.data[0])

            if self.game_state["command"] == "game_state":
                if self.game_state["continue"] == "true":
                    # Check if it is player's turn
                    turn = self.game_state["turn"]

                    if self.username == turn:
                        if len(self.game_state["word"]) == 0:
                            word = "0"
                            while not word.isalpha() or len(word) <= 1:
                                word = input("Enter a Word for the other player to guess:\t")
                                if not word.isalpha() or len(word) <= 1:
                                    print("Invalid Word! Please enter a valid word.\n")
                            self.initWord(word, ["_" for _ in range(len(self.word))])

                            # Ready action
                            self.action = to_python(action)
                            self.action["action"] = word
                            self.action["name"] = self.username
                            self.action = to_json(self.action)
                        else:
                            self.action = to_python(action)
                            if len(self.word) == 0:
                                self.initWord(self.game_state["word"], self.game_state["guess_word"])
                            self.guess_word = self.game_state["guess_word"]
                            self.lives = self.game_state["lives"]
                            self.printWord()
                            print("\n\n")

                            playerTurn = False
                            playerGuess = False
                            print("\nTo guess the word, enter [GUESS]")
                            while not playerTurn and not playerGuess:
                                player_guess = input("Enter a letter:\t")
                                if player_guess.isalpha():
                                    if player_guess.upper() == "GUESS":
                                        playerGuess = True
                                    elif len(player_guess) == 1:
                                        playerTurn = self.findLetter(player_guess)
                                        self.action["action"] = player_guess
                                        if not playerTurn:
                                            print("Letter already guessed!\n")
                                    else:
                                        print("Invalid letter!\n")
                                else:
                                    print("Invalid letter!\n")

                            while playerGuess and not playerTurn:
                                guess_word = input("\nEnter your guess:\t")
                                if all(x.isalpha() or x.isspace() for x in guess_word) or len(guess_word) <= 1:
                                    playerTurn = True
                                    self.action["action"] = guess_word
                                else:
                                    print("Invalid Word! Please enter a valid word.\n")

                            # Ready action
                            self.action["name"] = self.username
                            self.action = to_json(self.action)

                        # Send action
                        sock.sendto(bytes(self.action, "utf-8"), (self.server_host, self.server_port))
                    else:
                        if len(self.game_state["word"]) == 0:
                            print(f"{turn} is still entering a word...")
                        else:
                            self.guess_word = self.game_state["guess_word"]
                            self.lives = self.game_state["lives"]
                            self.printWord()
                            print("\n\n")
                            print(f"{turn} is currently guessing...")

                else:
                    self.printWord()
                    winner = self.game_state["winner"]
                    print(f"\n\nGame Over! {winner} wins!")

                    joined = 0


if __name__ == "__main__":
    print("Welcome to multiplayer games!")
    game = 0
    while game != 1 and game != 2:
        game = input("Which lobby do you want to join?\n[1] - Tic-Tac-Toe\n[2] - Hangman\n")
        game = int(game)
        if game != 1 and game != 2:
            print("Invalid input!\n\n")

    regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    while True:
        # Set variables for server address and destination port
        server_host = "192.168.1.2"

        if game == 1:
            server_port = 5555
        
        else:
            server_port = 4444

        result = bool(re.match(regex, server_host))
        if (result):
            break
        else:
            print("Invalid IP Address, please try again.\n")

    # Initialize player
    if game == 1:
        player = TicTacToePlayer(server_host, server_port)
    else:
        player = HangmanPlayer(server_host, server_port)

    # Connect to lobby
    joined = 0
    while joined == 0:
        joined = player.connect_to_server()

    while joined == 1:
        player.gameplay()

    print("Thank you for playing!")