
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
join = '{"command": "join", "username": ""}'
action = '{"command": "action", "action": "", "name": ""}'

class Player(object):
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
        self.joinRequest = to_json(self.joinRequest)

        # Send join request
        sock.sendto(bytes(self.joinRequest, "utf-8"), (self.server_host, self.server_port))

        # Process return code
        self.data = sock.recvfrom(1024)
        self.return_code = to_python(self.data[0])

        if self.return_code["code"] == "SUCCESS":
            print("You have joined the lobby.")
            global joined
            joined = 1

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
                            player_move = input("\nEnter Location of " + self.game_state["icon"] + " :")

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

if __name__ == "__main__":
    print("Welcome to multiplayer Tic-Tac-Toe!")

    regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    while True:
    # Set variables for server address and destination port
        server_host = "192.168.64.1"
        server_port = 5555

        result = bool(re.match(regex, server_host))
        if (result):
            break

        else:
            print("Invalid IP Address, please try again.\n")

    # Initialize player
    player = Player(server_host, server_port)

    # Connect to lobby
    joined = 0

    while joined == 0:
        player.connect_to_server()

    while joined == 1:
        player.gameplay()

    print("Thank you for playing!")



            






