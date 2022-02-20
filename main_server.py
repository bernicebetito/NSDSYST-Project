import socket, json, re
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
game_state = '{"command": "game_state", "board": "", "continue": "", "turn": "", "winner": ""}'
success = '{"command": "retcode", "code": "SUCCESS"}'
error = '{"command": "retcode", "code": "ERROR"}'

class MainServer (object):

    def __init__(self, server_host, server_port):
        global sock

        sock.bind((server_host, server_port))
        print("Main server online")

    def accept_lobby(self):
        global sock

        # Wait for lobby to register
        self.data = sock.recvfrom(1024)
        self.request = to_python(self.data[0])
        lobby_addr = self.data[1]

        # Process request
        if self.request["command"] == "register":
            global lobby_online
            lobby_online = 1
            print("Lobby has connected")

            # Ready return code and send
            self.success = to_python(success)
            self.success = to_json(self.success)
            sock.sendto(bytes(self.success, "utf-8"), lobby_addr)

        else:
            # Ready return code and send
            self.error = to_python(error)
            self.error = to_json(self.error)
            sock.sendto(bytes(self.error, "utf-8"), lobby_addr)

    def accept_players(self):
        global sock

        # Wait for lobby to send players
        self.data = sock.recvfrom(1024)
        self.request = to_python(self.data[0])
        self.lobby_addr = self.data[1]

        # Process request
        if self.request["command"] == "ready":
            self.player_one = self.request["player_one"]
            self.player_two = self.request["player_two"]
            print(f"Players {self.player_one} and {self.player_two} have joined the lobby")
            global lobby_ready
            lobby_ready = 1

            # Ready return code and send
            self.success = to_python(success)
            self.success = to_json(self.success)
            sock.sendto(bytes(self.success, "utf-8"), self.lobby_addr)

        else:
            # Ready return code and send
            self.error = to_python(error)
            self.error = to_json(self.error)
            sock.sendto(bytes(self.error, "utf-8"), self.lobby_addr)

    def init_tictactoe(self):
        self.grid_content = [["     " for _ in range(3)] for _ in range(3)]
        self.winner = "draw"
        self.turn = self.player_one
        self.do_continue = "true"
        self.moves = dict()

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
                    self.winner = self.player_one
                else:
                    self.winner = self.player_two
                return "false"

        for col in range(3):
            if list(self.grid_content[row][col] for row in range(3)) == [self.grid_content[0][col] for _ in range(3)] and self.grid_content[0][col] != "     ":
                self.winner = self.grid_content[0][col]
                if self.winner == "  X  ":
                    self.winner = self.player_one
                else:
                    self.winner = self.player_two
                return "false"

        if self.grid_content[0][0] == self.grid_content[1][1] == self.grid_content[2][2] and self.grid_content[0][0] != "     ":
            self.winner = self.grid_content[0][0]
            if self.winner == "  X  ":
                self.winner = self.player_one
            else:
                self.winner = self.player_two
            return "false"

        if self.grid_content[0][2] == self.grid_content[1][1] == self.grid_content[2][0] and self.grid_content[0][2] != "     ":
            self.winner = self.grid_content[0][0]
            if self.winner == "  X  ":
                self.winner = self.player_one
            else:
                self.winner = self.player_two
            return "false"

        return str(any("     " in content for content in self.grid_content)).lower()

    def playerTurn(self, player, move):
        if player == self.player_one:
            piece = "  X  "
        else:
            piece = "  O  "

        if move in self.moves:
            if self.grid_content[self.moves[move][0]][self.moves[move][1]] == "     ":
                self.grid_content[self.moves[move][0]][self.moves[move][1]] = piece
                

    def handle_tictactoe(self):
        global sock

        while self.do_continue == "true":
            # Ready game state
            self.game_state = to_python(game_state)
            self.game_state["board"] = self.grid_content
            self.game_state["winner"] = self.winner
            self.game_state["turn"] = self.turn
            self.game_state["continue"] = self.do_continue
            self.game_state = to_json(self.game_state)

            # Forward game state
            sock.sendto(bytes(self.game_state, "utf-8"), self.lobby_addr)
            print("Game state forwarded to game server")

            # Wait for player action
            self.data = sock.recvfrom(1024)
            self.action = to_python(self.data.decode("utf-8"))

            # Process player action
            if self.action["command"] == "action":
                print("Player action received from game server")
                self.player_move = int(self.action["action"])
                self.player_name = self.action["name"]
                self.playerTurn(self.player_name, self.player_move)
                self.do_continue = self.gameContinue()
                if self.turn == self.player_one:
                    self.turn == self.player_two
                else:
                    self.turn == self.player_one

        # Forward final game state
        self.game_state = to_python(game_state)
        self.game_state["board"] = self.grid_content
        self.game_state["winner"] = self.winner
        self.game_state["turn"] = self.turn
        self.game_state["continue"] = self.do_continue
        self.game_state = to_json(self.game_state)

        # Forward game state
        sock.sendto(bytes(self.game_state, "utf-8"), self.lobby_addr)

if __name__ == "__main__":
    regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    while True:
    # Set variables for server address and destination port
        server_host = "192.168.64.1"
        server_port = 12345

        result = bool(re.match(regex, server_host))
        if (result):
            break

        else:
            print("Invalid IP Address, please try again.\n")

    # Initialize main server
    main = MainServer(server_host, server_port)

    # Wait for lobby to connect
    lobby_online = 0
    while lobby_online == 0:
        main.accept_lobby()

    # Wait for lobby to be ready
    lobby_ready = 0
    while lobby_ready == 0:
        main.accept_players()

    # Handle player actions and game states
    main.init_tictactoe()
    main.handle_tictactoe()









