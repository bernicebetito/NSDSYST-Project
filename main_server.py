import socket, json, re, threading, select

tic_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hang_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Function to convert a json object into a python object
def to_python(jsonObj):
    data = json.loads(jsonObj)
    return data


# Function to convert a python object into a json object
def to_json(pythonObj):
    data = json.dumps(pythonObj)
    return data


# JSON commands
tic_game_state = '{"command": "game_state", "board": "", "continue": "", "turn": "", "winner": "", "icon": ""}'
hang_game_state = '{"command": "game_state", "word": "", "guess_word": "", "continue": "", "winner": "", "turn": "", "lives": ""}'
success = '{"command": "retcode", "code": "SUCCESS"}'
error = '{"command": "retcode", "code": "ERROR"}'


class MainServer(object):

    def __init__(self, tic_host, tic_port, hang_host, hang_port):
        global tic_sock, hang_sock

        tic_sock.bind((tic_host, tic_port))
        hang_sock.bind((hang_host, hang_port))
        print("Main server online")

    def tic_accept_lobby(self):
        global tic_sock

        # Wait for lobby to register
        self.data = tic_sock.recvfrom(1024)
        self.request = to_python(self.data[0])
        lobby_addr = self.data[1]

        # Process request
        if self.request["command"] == "register":
            if self.request["game"] == "tictactoe":
                print("Tic-tac-toe Lobby has connected")
                self.tic_lobby_addr = lobby_addr
                self.success = to_python(success)
                self.success = to_json(self.success)
                tic_sock.sendto(bytes(self.success, "utf-8"), self.tic_lobby_addr)
                return 1
            else:
                print("Unknown Lobby connecting")
                print("This is from the tic thread")
                self.error = to_python(error)
                self.error = to_json(self.error)
                tic_sock.sendto(bytes(self.error, "utf-8"), lobby_addr)
                return 0
        elif self.request["command"] == "ready":
            if self.request["game"] == "hangman":
                return 0
        else:
            # Ready return code and send
            self.error = to_python(error)
            self.error = to_json(self.error)
            tic_sock.sendto(bytes(self.error, "utf-8"), lobby_addr)
            return 0

    def hang_accept_lobby(self):
        global hang_sock

        # Wait for lobby to register
        self.data = hang_sock.recvfrom(1024)
        self.request = to_python(self.data[0])
        lobby_addr = self.data[1]

        # Process request
        if self.request["command"] == "register":
            if self.request["game"] == "hangman":
                print("Hangman Lobby has connected")
                self.hang_lobby_addr = lobby_addr
                self.success = to_python(success)
                self.success = to_json(self.success)
                hang_sock.sendto(bytes(self.success, "utf-8"), self.hang_lobby_addr)
                return 1
            else:
                print("Unknown Lobby connecting")
                print("This is from the hang thread")
                self.error = to_python(error)
                self.error = to_json(self.error)
                hang_sock.sendto(bytes(self.error, "utf-8"), lobby_addr)
                return 0
        elif self.request["command"] == "ready":
            if self.request["game"] == "tictactoe":
                return 0
        else:
            # Ready return code and send
            self.error = to_python(error)
            self.error = to_json(self.error)
            hang_sock.sendto(bytes(self.error, "utf-8"), lobby_addr)
            return 0

    def tic_accept_players(self):
        global tic_sock

        # Wait for lobby to send players
        self.data = tic_sock.recvfrom(1024)
        self.request = to_python(self.data[0])
        lobby_addr = self.data[1]

        # Process request
        if self.request["command"] == "ready":
            if self.request["game"] == "tictactoe":
                self.tic_lobby_addr = lobby_addr
                self.tic_player_one = self.request["player_one"]
                self.tic_player_two = self.request["player_two"]
                print(f"Players {self.tic_player_one} and {self.tic_player_two} have joined the Tic Tac Toe lobby")
                tic_lobby_ready = 1

                # Ready return code and send
                self.success = to_python(success)
                self.success = to_json(self.success)
                tic_sock.sendto(bytes(self.success, "utf-8"), self.tic_lobby_addr)
                return tic_lobby_ready, "tictactoe"
            else:
                player_one = self.request["player_one"]
                player_two = self.request["player_two"]
                print(f"Players {player_one} and {player_two} have joined a Different lobby")
                # Ready return code and send
                self.error = to_python(error)
                self.error = to_json(self.error)
                tic_sock.sendto(bytes(self.error, "utf-8"), lobby_addr)
        elif self.request["command"] == "register":
            if self.request["game"] == "hangman":
                pass
        else:
            # Ready return code and send
            self.error = to_python(error)
            self.error = to_json(self.error)
            tic_sock.sendto(bytes(self.error, "utf-8"), self.lobby_addr)

    def hang_accept_players(self):
        global hang_sock

        # Wait for lobby to send players
        print("waiting on players")
        self.data = hang_sock.recvfrom(1024)
        self.request = to_python(self.data[0])
        lobby_addr = self.data[1]

        # Process request
        if self.request["command"] == "ready":
            if self.request["game"] == "hangman":
                self.hang_lobby_addr = lobby_addr
                self.hang_player_one = self.request["player_one"]
                self.hang_player_two = self.request["player_two"]
                print(f"Players {self.hang_player_one} and {self.hang_player_two} have joined the Hangman lobby")
                hang_lobby_ready = 1

                # Ready return code and send
                self.success = to_python(success)
                self.success = to_json(self.success)
                hang_sock.sendto(bytes(self.success, "utf-8"), self.hang_lobby_addr)
                return hang_lobby_ready
            else:
                player_one = self.request["player_one"]
                player_two = self.request["player_two"]
                print(f"Players {player_one} and {player_two} have joined a Different lobby")
                # Ready return code and send
                self.error = to_python(error)
                self.error = to_json(self.error)
                hang_sock.sendto(bytes(self.error, "utf-8"), lobby_addr)
        elif self.request["command"] == "register":
            if self.request["game"] == "tictactoe":
                pass
        else:
            # Ready return code and send
            self.error = to_python(error)
            self.error = to_json(self.error)
            hang_sock.sendto(bytes(self.error, "utf-8"), self.lobby_addr)


class tictactoeGame():
    def __init__(self, lobby_addr, playerOne, playerTwo):
        self.lobby_addr = lobby_addr
        self.tic_player_one = playerOne
        self.tic_player_two = playerTwo

    def init_tictactoe(self):
        self.grid_content = [["     " for _ in range(3)] for _ in range(3)]
        self.winner = "draw"
        self.turn = self.tic_player_one
        self.do_continue = "true"
        self.moves = dict()
        self.icon = "X"

        count = 1
        for row in range(len(self.grid_content)):
            for col in range(len(self.grid_content[row])):
                self.moves[count] = (row, col)
                count += 1

    def gameContinue(self):
        for row in range(3):
            if list(self.grid_content[row][col] for col in range(3)) == [self.grid_content[row][0] for _ in range(3)] and "     " not in self.grid_content[row]:
                self.winner = self.grid_content[row][0]
                if self.winner == "  X  ":
                    self.winner = self.tic_player_one
                else:
                    self.winner = self.tic_player_two
                return "false"

        for col in range(3):
            if list(self.grid_content[row][col] for row in range(3)) == [self.grid_content[0][col] for _ in range(3)] and self.grid_content[0][col] != "     ":
                self.winner = self.grid_content[0][col]
                if self.winner == "  X  ":
                    self.winner = self.tic_player_one
                else:
                    self.winner = self.tic_player_two
                return "false"

        if self.grid_content[0][0] == self.grid_content[1][1] == self.grid_content[2][2] and self.grid_content[0][
            0] != "     ":
            self.winner = self.grid_content[0][0]
            if self.winner == "  X  ":
                self.winner = self.tic_player_one
            else:
                self.winner = self.tic_player_two
            return "false"

        if self.grid_content[0][2] == self.grid_content[1][1] == self.grid_content[2][0] and self.grid_content[0][
            2] != "     ":
            self.winner = self.grid_content[0][0]
            if self.winner == "  X  ":
                self.winner = self.tic_player_one
            else:
                self.winner = self.tic_player_two
            return "false"

        return str(any("     " in content for content in self.grid_content)).lower()

    def playerTurn(self, player, move):
        if player == self.tic_player_one:
            piece = "  X  "
        else:
            piece = "  O  "

        if move in self.moves:
            if self.grid_content[self.moves[move][0]][self.moves[move][1]] == "     ":
                self.grid_content[self.moves[move][0]][self.moves[move][1]] = piece

    def handle_tictactoe(self):
        global tic_sock
        while self.do_continue == "true":
            # Ready game state
            self.game_state = to_python(tic_game_state)
            self.game_state["board"] = self.grid_content
            self.game_state["winner"] = self.winner
            self.game_state["turn"] = self.turn
            self.game_state["continue"] = self.do_continue
            self.game_state["icon"] = self.icon
            self.game_state = to_json(self.game_state)

            # Forward game state
            tic_sock.sendto(bytes(self.game_state, "utf-8"), self.lobby_addr)
            print("Game state forwarded to tictactoe game server")

            # Wait for player action
            self.data = tic_sock.recvfrom(1024)
            self.action = to_python(self.data[0])

            # Process player action
            if self.action["command"] == "action":
                print("Player action received from tictactoe game server")
                self.player_move = int(self.action["action"])
                self.player_name = self.action["name"]
                self.playerTurn(self.player_name, int(self.player_move))
                self.do_continue = self.gameContinue()
                if self.turn == self.tic_player_one:
                    self.turn = self.tic_player_two
                    self.icon = "O"
                else:
                    self.turn = self.tic_player_one
                    self.icon = "X"

        # Forward final game state
        self.game_state = to_python(tic_game_state)
        self.game_state["board"] = self.grid_content
        self.game_state["winner"] = self.winner
        self.game_state["turn"] = self.turn
        self.game_state["continue"] = self.do_continue
        self.game_state = to_json(self.game_state)

        # Forward game state
        tic_sock.sendto(bytes(self.game_state, "utf-8"), self.lobby_addr)


class tictactoeThread(threading.Thread):
    def __init__(self, main):
        threading.Thread.__init__(self)
        self.main = main

    def run(self):
        # Wait for lobby to connect
        tic_lobby_online = 0
        while tic_lobby_online == 0:
            tic_lobby_online = main.tic_accept_lobby()

        # Wait for lobby to be ready
        tic_lobby_ready = 0
        while tic_lobby_ready == 0:
            tic_lobby_ready = self.main.tic_accept_players()

        # Handle player actions and game states
        game = tictactoeGame(self.main.tic_lobby_addr, self.main.tic_player_one, self.main.tic_player_two)
        game.init_tictactoe()
        game.handle_tictactoe()


class hangmanGame():
    def __init__(self, lobby_addr, playerOne, playerTwo):
        self.lobby_addr = lobby_addr
        self.hang_player_one = playerOne
        self.hang_player_two = playerTwo
        self.lives = 6
        self.winner = self.hang_player_two
        self.turn = self.hang_player_two
        self.do_continue = "true"
        self.word_entered = False

    def init_hangman(self, word):
        self.word = []
        self.word[:0] = word.upper()
        self.guess_word = ["_" for _ in range(len(self.word))]
        self.letters = [chr(65 + x) for x in range(26)]
        self.word_entered = True

    def gameContinue(self):
        if self.guess_word == self.word:
            self.winner = self.hang_player_one
            return "false"
        elif self.lives == 0:
            self.guess_word = self.word
            self.winner = self.hang_player_two
            return "false"
        return "true"

    def findLetter(self, letter):
        if letter.upper() in self.word:
            indexes = [a for a, x in enumerate(self.word) if x == letter.upper()]
            self.guess_word = [letter.upper() if x in indexes else self.guess_word[x] for x in
                               range(len(self.guess_word))]
        else:
            self.lives -= 1

    def guessWord(self, word):
        guess = []
        guess[:0] = word.upper()
        if guess != self.word:
            self.lives -= 1
        else:
            self.winner = self.hang_player_one
            self.guess_word = guess

    def handle_hangman(self):
        global hang_sock
        while not self.word_entered:
            # Ready game state
            self.game_state = to_python(hang_game_state)
            self.game_state["continue"] = self.do_continue
            self.game_state["winner"] = self.winner
            self.game_state["turn"] = self.turn
            self.game_state = to_json(self.game_state)

            # Forward game state
            hang_sock.sendto(bytes(self.game_state, "utf-8"), self.lobby_addr)
            print("Game state forwarded to hangman game server")

            # Wait for player action
            self.data = hang_sock.recvfrom(1024)
            self.action = to_python(self.data[0])

            # Process player action
            if self.action["command"] == "action":
                print("Player action received from hangman game server")
                self.init_hangman(self.action["action"])
                self.turn = self.hang_player_one

        while self.do_continue == "true":
            # Ready game state
            self.game_state = to_python(hang_game_state)
            self.game_state["word"] = self.word
            self.game_state["guess_word"] = self.guess_word
            self.game_state["continue"] = self.do_continue
            self.game_state["winner"] = self.winner
            self.game_state["turn"] = self.turn
            self.game_state["lives"] = self.lives
            self.game_state = to_json(self.game_state)

            # Forward game state
            hang_sock.sendto(bytes(self.game_state, "utf-8"), self.lobby_addr)
            print("Game state forwarded to hangman game server")

            # Wait for player action
            self.data = hang_sock.recvfrom(1024)
            self.action = to_python(self.data[0])

            # Process player action
            if self.action["command"] == "action":
                print("Player action received from hangman game server")
                self.player_move = self.action["action"]
                if len(self.player_move) == 1:
                    self.findLetter(self.player_move)
                else:
                    self.guessWord(self.player_move)
                self.do_continue = self.gameContinue()

        # Forward final game state
        self.game_state = to_python(hang_game_state)
        self.game_state["word"] = self.word
        self.game_state["guess_word"] = self.guess_word
        self.game_state["continue"] = self.do_continue
        self.game_state["winner"] = self.winner
        self.game_state["turn"] = self.turn
        self.game_state["lives"] = self.lives
        self.game_state = to_json(self.game_state)

        # Forward game state
        hang_sock.sendto(bytes(self.game_state, "utf-8"), self.lobby_addr)


class hangmanThread(threading.Thread):
    def __init__(self, main):
        threading.Thread.__init__(self)
        self.main = main

    def run(self):
        # Wait for lobby to connect
        hang_lobby_online = 0
        while hang_lobby_online == 0:
            hang_lobby_online = main.hang_accept_lobby()

        # Wait for lobby to be ready
        hang_lobby_ready = 0
        while hang_lobby_ready == 0:
            hang_lobby_ready = self.main.hang_accept_players()

        # Handle player actions and game states
        game = hangmanGame(self.main.hang_lobby_addr, self.main.hang_player_one, self.main.hang_player_two)
        game.handle_hangman()


if __name__ == "__main__":
    regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    while True:
        # Set variables for server address and destination port
        tic_server_host = "192.168.1.2"
        tic_server_port = 12345
        hang_server_host = tic_server_host
        hang_server_port = 54321

        result = bool(re.match(regex, tic_server_host))
        if (result):
            break

        else:
            print("Invalid IP Address, please try again.\n")

    # Initialize main server
    main = MainServer(tic_server_host, tic_server_port, hang_server_host, hang_server_port)

    tic_thread = tictactoeThread(main)
    hang_thread = hangmanThread(main)

    tic_thread.start()
    hang_thread.start()

    tic_thread.join()
    hang_thread.join()